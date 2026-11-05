# AGENTS.md

Notes for coding agents working in this repo. Read this before changing anything
under `src/`.

## What this is

An MCP server that automates Cisco Packet Tracer. It plans network topologies,
validates them, generates JavaScript for PT's script engine and IOS CLI config
for the devices, and can push all of it into a running copy of Packet Tracer over
a local HTTP bridge.

## Language

Write everything in the repo in **English**: code, comments, docstrings, tool
descriptions, user-facing messages, tests, docs and commit messages. This keeps
the project usable by anyone, whatever their language. Talk to your user in
**their** preferred language — only what you write into the repo is English.

## Build and test

```bash
pip install -e ".[test]"
python -m pytest          # from the repo root, no PT required
```

There is no linter or formatter configured. Match the surrounding style: type
hints on public functions, `from __future__ import annotations` at the top,
comments in English (see Language above).

## Layout

| Path | What lives there |
| --- | --- |
| `src/packet_tracer_mcp/domain/` | Pydantic models, validation rules, planning services |
| `src/packet_tracer_mcp/application/` | Use cases: rules + generators, dependencies injected |
| `src/packet_tracer_mcp/infrastructure/` | Generators, executors, the HTTP + file bridges, device catalog |
| `src/packet_tracer_mcp/adapters/mcp/` | `tools/<topic>.py` — 81 of the 98 tools, one `register(mcp, ctx)` each, run by `tool_registry.py`; `bridge_context.py` — the shared `BridgeContext`; `device_panel_tools.py` + `desktop_service_tools.py` — the 17 device-panel tools; `prompt_registry.py` / `resource_registry.py` — prompts and resources (`pt://guide`) |
| `src/packet_tracer_mcp/infrastructure/ui/` | UI mode: Win32 + UI Automation presenter that opens/captures device windows (Windows only, `[ui]` extra) |
| `EXTENSION/script-engine/` | Script-engine side of the extension. `main.js` is ours (tracked); the rest are PTBuilder reference copies (gitignored) |
| `EXTENSION/webview/` | The MCP Control Center webview (`index.html` + `interface.js`) |

Start at `CODEMAP.md`: which file owns what, and which file holds each tool.
It is generated — rerun `python -m src.packet_tracer_mcp.devtools.codemap`
after adding a module or tool (a test fails when it is stale).

Tools are closures inside each module's `register()`, so helpers defined
there **cannot be imported by tests**: put a helper worth testing at module
level or in `shared/utils.py`. Tool replies go through `reply_json()`
(compact, drops JS once sent). Tests cap `SERVER_INSTRUCTIONS` at 2,000 chars
(Claude Code cuts at 2,048) and tool descriptions at 1,500; longer notes go
in `settings.GUIDE`, served as `pt://guide`. `tests/fixtures/tool_api.json`
snapshots the tool API — regenerate with `UPDATE_TOOL_API=1` only on purpose.

## Rules that are not negotiable

1. **Never build JavaScript with raw f-strings.** Use `json.dumps` for each
   field. PT runs it through `new Function()`, so an unescaped device name is
   arbitrary code execution. `ptbuilder_generator.py` shows the correct pattern.
2. **Never build a path by concatenation.** Use `safe_name_component()` then
   `resolve_within()` from `shared/utils.py`.
3. **Never add an unauthenticated bridge endpoint.** Everything except `/ping`
   requires the token; see `bridge_token.py` for why loopback alone is not a
   control. (The file-bridge channel needs no token — the mailbox lives under a
   user-ACL'd `%LOCALAPPDATA%` dir a browser page can't reach.)
4. **Don't validate in the models.** Validation belongs in `domain/rules/` and
   returns `ValidationResult`, so the use case decides whether to proceed.
5. **A bug fix needs a test that fails without it.** Write the failing test
   first; if it passes before your change, it isn't testing the bug.
6. **Never guess a PT API signature.** If a method isn't already used somewhere
   in this repo, confirm it against Cisco's reference before writing code on top
   of it — PT answers a wrong call with a bare `Invalid arguments for IPC call
   "X"`, so a guess fails without telling you why.

## Working with the bridge

The bridge only really works with Packet Tracer open, so most verification is
offline. `tests/test_bridge_security.py` drives a real `PTCommandBridge` on an
ephemeral port — follow that pattern rather than mocking HTTP.

Set `PT_MCP_BRIDGE_TOKEN` to avoid touching the user's real token file.

Anything involving PT's webview (CORS behaviour, the `this-sm:` origin, whether
the script engine can reach an API) **cannot be verified from tests**. Say so
explicitly instead of assuming; don't claim a change is verified when only the
offline half was.

## Gotchas

- PT's `executeCode()` **strips newlines** from source that is *pasted* into the
  Builder Code Editor, so any such snippet must be a single line without `//`
  comments. (The compiled `.pts` files — `main.js` etc. — are not pasted and can
  be normal multi-line JS.)
- An uncaught error inside `runCode` opens a modal that freezes the webview and
  kills the polling loop. That is why fire-and-forget commands are wrapped in
  `try{...}catch{}`.
- `%LOCALAPPDATA%`, not `%APPDATA%`, for machine-local secrets — the latter
  roams.

## Automatic Reporting Requirement

Whenever an agent completes any task, network simulation, topology build, or troubleshooting exercise in this repository, the agent **MUST automatically generate a formal, neat report in both `.doc` and `.docx` formats** before concluding.

Follow the **`formal-report-generator`** skill located at `skills/formal-report-generator/SKILL.md` (or `.agents/skills/formal-report-generator/SKILL.md`).

**Mandatory Report Rules**:
1. **Typography**: Strictly **Times New Roman** exclusively across all elements (Title 14pt, H1 13pt, H2 12pt, Body 12pt, Tables 9.5-10.5pt, Captions 10pt).
2. **Colors**: **Pure Black (`#000000`)** text and headings ("jangan warna-warni"). Neutral light gray (`#F2F2F2`) table headers with solid black borders.
3. **Topology Image**: Exactly **ONE** topology diagram at the beginning of the report (Bab I). Never duplicate.
4. **Packet Tracer Canvas**: (a) Subnet notes placed strictly along the cable link path formatted as `NETWORK\n<Subnet>/<CIDR>` (e.g. `NETWORK\n192.168.10.0/24`); (b) Full IP address annotation placed directly underneath EVERY device (PC/Server/Laptop) icon and label (`pt_add_note` at $y_{dev}+68$, e.g. `192.168.10.2` or `IP ADDRESS PC\n192.168.10.2`); (c) Centered topology title at top.
5. **Flowcharts**: Zero overlap, minimum 40px spacing between parallel branches, orthogonal lines, Times New Roman labels, monochrome palette.
6. **Delivery**: Always generate both `.docx` and `.doc` files in `c:\laragon\www\mcp-to-cisco\` and provide direct clickable links (`file:///...`).
