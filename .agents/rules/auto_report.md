# Automatic Formal Report Generation Rule

## MANDATORY WORKFLOW REQUIREMENT
Whenever an agent completes any task, network scenario, topology construction, diagnosis, or troubleshooting exercise in this workspace (`c:\laragon\www\mcp-to-cisco`), the agent **MUST ALWAYS** generate a formal, neat report in both `.doc` and `.docx` formats before ending its response.

The agent must follow the **`formal-report-generator`** skill located at:
- `c:\laragon\www\mcp-to-cisco\skills\formal-report-generator\SKILL.md`
- `c:\laragon\www\mcp-to-cisco\.agents\skills\formal-report-generator\SKILL.md`

## NON-NEGOTIABLE FORMATTING RULES

1. **Strict Typography (Times New Roman Exclusively)**:
   - All document text MUST be in **Times New Roman**:
     - Document Title: 14pt Bold
     - Headings (H1): 13pt Bold
     - Sub-headings (H2): 12pt Bold
     - Body Text: 12pt Regular, 1.15 line spacing
     - Table Content: 9.5pt – 10.5pt
     - Captions: 10pt Italic
   - Never use Calibri, Arial, or Consolas for paragraph or heading text.

2. **Monochrome Design Discipline ("Jangan Warna-Warni")**:
   - All headings, subheadings, and body paragraphs MUST be **Pure Black (`#000000`)**.
   - No colored text anywhere in the document (no blue headings, no red/green text).
   - Tables: Header row background `#F2F2F2` (neutral light gray), table text `#000000` (Bold), borders solid black/subtle gray (`#CCCCCC` / `#000000`).
   - Callout boxes: `#F5F5F5` background with a thick black left border (`#000000`) and pure black text.

3. **Topology Image Discipline**:
   - Exactly **ONE** topology diagram at the beginning of the report (Bab I).
   - Never duplicate the topology picture in later chapters or steps.

4. **Packet Tracer Canvas & Labeling Standard**:
   - Subnet label on the cable/port (e.g. `192.168.10.0/24`).
   - Full host IP address placed cleanly and directly underneath each PC/Server icon and label (e.g. `192.168.10.2` under `PC-Keuangan`).

5. **Flowchart & Diagram Layout Standard**:
   - **Zero Overlap**: All boxes, decision diamonds, and arrow lines must have disjoint bounding boxes with at least 40px of clear space between parallel branches.
   - Text inside diagrams must use **Times New Roman**.
   - Flowchart palette must be monochrome / grayscale only (white or soft gray boxes with black borders; no yellow, green, or pink fills).

6. **Dual Export Delivery**:
   - Always generate both modern `.docx` and legacy `.doc` files in the workspace root `c:\laragon\www\mcp-to-cisco\`.
   - Always provide direct clickable markdown links (`file:///...`) in the final response to the user.
