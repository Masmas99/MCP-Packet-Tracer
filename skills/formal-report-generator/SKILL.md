---
name: formal-report-generator
description: >-
  Standardized skill to create clean, professional, academic, and technical reports (.docx / .doc)
  with strict typography (Times New Roman), monochrome design discipline, zero-overlap flowcharts,
  and structured evidence capture. Use whenever the user asks for a report, documentation, .doc, or .docx file.
---

# Formal Technical Report Generator Skill

## 1. Purpose & Core Philosophy
This skill governs the autonomous creation of high-grade technical, engineering, and academic laboratory reports (in `.docx` and `.doc` formats). It enforces strict visual discipline, pristine typography, structured scientific analysis, and clean screenshot rendering without visual clutter.

---

## 2. When to Use
- Whenever the user requests a report, lab documentation, or answers in `.doc` or `.docx` format.
- After completing network simulations (e.g. Cisco Packet Tracer), coding tasks, or troubleshooting scenarios that require formal reporting.
- When generating flowcharts, CLI captures, or addressing tables for academic/professional submission.

---

## 3. Mandatory Formatting Standards (Non-Negotiable)

### Rule 1: Strict Typography Uniformity
- **Font Family**: **Times New Roman** exclusively across the entire document.
  - Document Title: **14 pt, Bold, Centered**
  - Section Headings (H1): **13 pt, Bold, Left-Aligned**
  - Sub-Headings (H2): **12 pt, Bold, Left-Aligned**
  - Body Text: **12 pt, Regular, Justified (or Left), 1.15 line spacing**
  - Table Content: **9.5 pt – 10.5 pt, Times New Roman**
  - Figure / Table Captions: **10 pt, Italic, Centered**
- **No mixed fonts**: Never allow Arial, Calibri, or Consolas to leak into paragraph runs or headings.

### Rule 2: Monochrome & Neutral Color Discipline ("Jangan Warna-Warni")
- **Body & Heading Text**: **Pure Black (`#000000`)** only. Zero blue, red, or green text.
- **Table Design**:
  - Header Row: Background `#F2F2F2` (soft light neutral gray), Text `#000000` (Bold).
  - Data Rows: Alternating `#FFFFFF` and `#FAFAFA` (or all `#FFFFFF`).
  - Borders: Clean thin borders (`#CCCCCC` or `#000000`, size 4).
- **Callout Boxes**:
  - Background: `#F5F5F5` (light gray).
  - Left Border: Solid black (`#000000`, size 24), top/bottom/right none.
  - Text inside: Pure black (`#000000`).
- **Flowcharts & Diagrams**:
  - Background: White (`#FFFFFF`).
  - Shapes: Soft gray fill (`#F5F5F5` / `#F0F0F0`) or white (`#FFFFFF`) with solid black outline (`#000000`).
  - Lines & Arrows: Solid black (`#000000`).
  - No colored fills (no pink, green, yellow, or blue boxes).

### Rule 3: Single Topology Image at the Beginning
- Include exactly **ONE** topology diagram at the beginning of the report (Bab I / Topologi Jaringan).
- **Never duplicate** the topology diagram in later chapters or steps. Subsequent images must be specific evidence (CLI outputs, Wireshark captures, or flowcharts).

### Rule 4: Packet Tracer Canvas & Labeling Precision (Mandatory)
Every topology diagram on Packet Tracer canvas MUST have explicit visual annotations (`pt_add_note`) matching this standard:
- **Subnet Notes Along Cable Position ("NETWORK\n<Subnet>/<CIDR>")**:
  - Place network subnet notes strictly along the cable link between devices (at cable midpoint: $x = (x_1 + x_2)/2$, $y = (y_1 + y_2)/2 - 15$).
  - **Exact Format**: 2 lines, uppercase "NETWORK" followed by the subnet/CIDR:
    ```text
    NETWORK
    192.168.10.0/24
    ```
    ```text
    NETWORK
    192.168.20.0/24
    ```
  - Follow the cable path/post directly as shown in reference topologies.
- **Host IP Address Under EVERY Device**:
  - Every single host, PC, Server, and client (`PC-Star1..4`, `PC-Bus1..4`, `Server-Star`, etc.) **MUST** have an IP address annotation placed directly underneath the device icon and name label.
  - **Position**: $x = x_{dev}$, $y = y_{dev} + 68$ (or $70$) px.
  - **Exact Format**: The allocated host IP address:
    ```text
    192.168.10.2
    ```
    or
    ```text
    IP ADDRESS PC
    192.168.10.2
    ```
    (Both static and DHCP-leased hosts must show their IP address directly under the device).
- **Interface / Gateway Note**: Place near router/switch interfaces (e.g., `Gig0/0: .1` or `.1 (G0/0)`).
- **Topology Title**: Place a centered title at top canvas ($y=25..35$), e.g. `TOPOLOGI HYBRID: STAR & BUS DENGAN INTER-ROUTING`.

### Rule 5: Zero-Overlap Flowchart Geometry
When generating diagnostic flowcharts:
- **Spatial Separation**: Parallel branches must have at least **40 px** of clear margin between bounding boxes.
- **Dedicated Columns**: If a decision branches into multiple paths (e.g., "YA" vs "TIDAK"), assign each branch its own non-overlapping horizontal column.
- **Orthogonal Connections**: Draw all arrow paths using 90-degree right-angle turns (horizontal and vertical lines), with sharp arrowheads aligned to target edges.
- **Font in Flowchart**: Use **Times New Roman** (`times.ttf`, `timesbd.ttf`) for all diagram labels.

### Rule 6: Dual-Format Delivery (.doc and .docx)
Always generate and deliver both:
1. Modern Word OpenXML format: `<Filename>.docx`
2. Legacy Word format: `<Filename>.doc` (created via safe binary copy)

---

## 4. Standard Document Structure

Every technical report must follow this 5-part architecture:

1. **Header & Metadata Block**:
   - Document Title & Subtitle.
   - 2-Column Metadata Table (Course/Exam, Scenario, Simulator, Status).
2. **Bab I: Topologi Jaringan & Spesifikasi Pengalamatan**:
   - Single clean cropped topology diagram.
   - Complete IP Addressing & VLAN allocation table.
3. **Bab II: Implementasi Konfigurasi Perangkat**:
   - Step-by-step CLI commands formatted inside clean callout boxes.
4. **Bab III: Metodologi & Flowchart Diagnosis**:
   - Technical rationale for the selected methodology (e.g., Divide-and-Conquer, Compare Configurations).
   - High-resolution, zero-overlap monochrome flowchart image.
   - Detailed step-by-step explanation of each phase.
5. **Bab IV: Hasil Pengujian & Bukti Diagnostik (Evidence)**:
   - High-contrast CLI / Command Prompt screenshots (Ping, Traceroute, `show` commands).
   - Protocol analyzer / Wireshark capture breakdown (Layers 2, 3, and 4).
   - Deep-dive technical explanation of why connections succeed or fail.
6. **Bab V: Kesimpulan & Rekomendasi Solusi**:
   - Key findings summary.
   - Industrial Standard Operating Procedure (SOP) recommendations.

---

## 5. Python Automation Utilities

Use the standardized script template in `scripts/report_helper.py` which provides:
- `set_cell_background(cell, hex_color)`
- `set_cell_margins(cell, top, bottom, left, right)`
- `set_table_borders(table, color, sz)`
- `add_callout(doc, text, title)`
- `render_cmd_window(title, lines, filename, width)`
- `render_flowchart(filename, title, subtitle, nodes, connections, width, height)`

---

## 6. Verification Checklist Before Delivering
- [ ] Document font is 100% Times New Roman throughout all styles and runs.
- [ ] No colorful text or blue headings; monochrome palette enforced.
- [ ] Exactly one topology image placed at the beginning.
- [ ] Flowchart has zero overlapping boxes or clipped text labels.
- [ ] Both `.docx` and `.doc` files exist on disk with matching contents.
- [ ] Clickable markdown links (`file:///...`) provided for the user.
