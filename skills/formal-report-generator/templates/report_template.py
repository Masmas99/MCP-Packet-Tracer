"""
Template for Formal Technical Report Generation (.docx / .doc)
Follows 100% Times New Roman, monochrome palette, and single topology image.
"""

import os
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_helper import set_cell_background, set_cell_margins, set_table_borders, add_callout

def create_report(title: str, subtitle: str, metadata: list, output_docx: str, output_doc: str = None):
    doc = Document()

    # Normal 1 inch margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Style defaults
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)
    style.font.color.rgb = RGBColor(0, 0, 0)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(2)
    r_title = p_title.add_run(title)
    r_title.bold = True
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(14)
    r_title.font.color.rgb = RGBColor(0, 0, 0)

    # Subtitle
    if subtitle:
        p_sub = doc.add_paragraph()
        p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sub.paragraph_format.space_after = Pt(12)
        r_sub = p_sub.add_run(subtitle)
        r_sub.italic = True
        r_sub.font.name = 'Times New Roman'
        r_sub.font.size = Pt(11)
        r_sub.font.color.rgb = RGBColor(0, 0, 0)

    # Metadata table
    if metadata:
        meta_tbl = doc.add_table(rows=len(metadata), cols=2)
        meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        meta_tbl.autofit = False
        meta_tbl.columns[0].width = Inches(2.2)
        meta_tbl.columns[1].width = Inches(4.3)
        for i, (k, v) in enumerate(metadata):
            c0, c1 = meta_tbl.cell(i, 0), meta_tbl.cell(i, 1)
            set_cell_background(c0, "F5F5F5")
            set_cell_background(c1, "FFFFFF")
            set_cell_margins(c0, top=60, bottom=60, left=100, right=100)
            set_cell_margins(c1, top=60, bottom=60, left=100, right=100)
            r0 = c0.paragraphs[0].add_run(k)
            r0.bold = True
            r0.font.name = "Times New Roman"
            r0.font.size = Pt(10)
            r0.font.color.rgb = RGBColor(0, 0, 0)
            r1 = c1.paragraphs[0].add_run(v)
            r1.font.name = "Times New Roman"
            r1.font.size = Pt(10)
            r1.font.color.rgb = RGBColor(0, 0, 0)
        set_table_borders(meta_tbl, color="CCCCCC", sz="4")
        doc.add_paragraph()

    doc.save(output_docx)
    if output_doc:
        shutil.copyfile(output_docx, output_doc)
