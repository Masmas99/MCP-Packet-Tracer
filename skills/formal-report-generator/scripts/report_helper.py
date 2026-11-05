"""
Standard Helper Utilities for Formal Technical Report Generation
Enforces Times New Roman typography, monochrome palettes, and clean diagram generation.
"""

import os
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont

def set_cell_background(cell, fill_hex: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CCCCCC", sz="4"):
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), sz)
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), color)
        tblBorders.append(border)
    insideV = OxmlElement('w:insideV')
    insideV.set(qn('w:val'), 'none')
    tblBorders.append(insideV)
    tblPr.append(tblBorders)

def add_callout(doc, text: str, title="CATATAN TEKNIS:"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F5F5F5")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '24')
    left.set(qn('w:color'), '000000')
    tcBorders.append(left)
    for side in ['top', 'bottom', 'right']:
        b = OxmlElement(f'w:{side}')
        b.set(qn('w:val'), 'none')
        tcBorders.append(b)
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r_title = p.add_run(f"{title} ")
    r_title.bold = True
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(11)
    r_title.font.color.rgb = RGBColor(0, 0, 0)

    r_text = p.add_run(text)
    r_text.font.name = "Times New Roman"
    r_text.font.size = Pt(10.5)
    r_text.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph()

def get_times_font(size: int, bold=False, italic=False):
    if bold and italic:
        names = ['timesbi.ttf', 'timesbd.ttf', 'times.ttf']
    elif bold:
        names = ['timesbd.ttf', 'times.ttf']
    elif italic:
        names = ['timesi.ttf', 'times.ttf']
    else:
        names = ['times.ttf']
    for f in names:
        try:
            return ImageFont.truetype(f, size)
        except:
            pass
    return ImageFont.load_default()

def render_cmd_window(title: str, lines: list, output_path: str, width=760):
    """
    Renders high-contrast dark command line / console screenshots with window chrome.
    lines format: [(text_string, (r, g, b)), ...]
    """
    try:
        font = ImageFont.truetype('consola.ttf', 15)
        title_font = ImageFont.truetype('consola.ttf', 13)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()

    line_h = 22
    pad_top = 40
    pad_bottom = 20
    pad_left = 20
    height = pad_top + len(lines) * line_h + pad_bottom

    img = Image.new('RGB', (width, height), (12, 12, 12))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, width, 32], fill=(32, 32, 32))
    draw.text((36, 8), title, font=title_font, fill=(220, 220, 220))
    draw.rectangle([14, 10, 26, 22], outline=(150, 150, 150), width=1)
    draw.text((width - 65, 6), '—  □  ✕', font=title_font, fill=(180, 180, 180))

    # Content
    y = pad_top
    for line, color in lines:
        draw.text((pad_left, y), line, font=font, fill=color)
        y += line_h

    draw.rectangle([0, 0, width-1, height-1], outline=(60, 60, 60), width=1)
    img.save(output_path)
