#!/usr/bin/env python3
"""Export list-of-tables to a Chinese academic-style Word doc (三线表)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor


def _set_run_font(run, name_cn: str = "宋体", name_en: str = "Times New Roman", size_pt: float = 10.5):
    run.font.size = Pt(size_pt)
    run.font.name = name_en
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:ascii"), name_en)
    rFonts.set(qn("w:hAnsi"), name_en)
    rFonts.set(qn("w:eastAsia"), name_cn)


def _set_three_line_borders(table):
    """Classic 三线表: top thick, header bottom thin, bottom thick; no vertical lines."""
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement("w:tblPr")
    # remove existing borders
    for child in list(tblPr):
        if child.tag == qn("w:tblBorders"):
            tblPr.remove(child)

    borders = OxmlElement("w:tblBorders")
    specs = [
        ("top", "single", "12"),      # 顶线加粗
        ("left", "nil", "0"),
        ("bottom", "single", "12"),   # 底线加粗
        ("right", "nil", "0"),
        ("insideH", "nil", "0"),
        ("insideV", "nil", "0"),
    ]
    for edge, val, sz in specs:
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), val)
        el.set(qn("w:sz"), sz)
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")
        borders.append(el)
    tblPr.append(borders)
    if tbl.tblPr is None:
        tbl.insert(0, tblPr)

    # header row bottom border (第二条线)
    if table.rows:
        for cell in table.rows[0].cells:
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcBorders = OxmlElement("w:tcBorders")
            bottom = OxmlElement("w:bottom")
            bottom.set(qn("w:val"), "single")
            bottom.set(qn("w:sz"), "6")
            bottom.set(qn("w:space"), "0")
            bottom.set(qn("w:color"), "000000")
            tcBorders.append(bottom)
            # clear others
            for edge in ("top", "left", "right"):
                e = OxmlElement(f"w:{edge}")
                e.set(qn("w:val"), "nil")
                e.set(qn("w:sz"), "0")
                e.set(qn("w:space"), "0")
                e.set(qn("w:color"), "000000")
                tcBorders.append(e)
            # remove old borders
            for child in list(tcPr):
                if child.tag == qn("w:tcBorders"):
                    tcPr.remove(child)
            tcPr.append(tcBorders)


def _yes_no(flag: bool) -> str:
    return "是" if flag else ""


def export_design_doc(tables: list[dict[str, Any]], out_path: str | Path, title: str = "数据库设计文档") -> Path:
    """
    Generate Word doc matching yanleaf export style:
    - Title centered
    - 表N·table_name (中文注释)
    - 三线表: 字段名 | 类型 | 主键 | 外键 | 说明
    """
    out_path = Path(out_path)
    doc = Document()

    # page margins
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

    # Title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    _set_run_font(run, "黑体", "Arial", 16)
    run.bold = True
    p.paragraph_format.space_after = Pt(18)

    for idx, table in enumerate(tables, start=1):
        name = table.get("name") or f"table_{idx}"
        comment = table.get("comment") or ""
        caption = f"表 {idx}  {name}"
        if comment:
            caption += f"（{comment}）"

        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = cap.add_run(caption)
        _set_run_font(run, "宋体", "Times New Roman", 12)
        run.bold = True
        cap.paragraph_format.space_before = Pt(12)
        cap.paragraph_format.space_after = Pt(6)

        columns = table.get("columns") or []
        # header + rows
        n_rows = 1 + max(len(columns), 1)
        tbl = doc.add_table(rows=n_rows, cols=5)
        tbl.autofit = True

        headers = ["字段名", "类型", "主键", "外键", "说明"]
        for j, h in enumerate(headers):
            cell = tbl.rows[0].cells[j]
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(h)
            _set_run_font(run, "宋体", "Times New Roman", 10.5)
            run.bold = True

        if not columns:
            for j in range(5):
                tbl.rows[1].cells[j].text = ""
        else:
            for i, col in enumerate(columns):
                row = tbl.rows[i + 1]
                values = [
                    str(col.get("name") or ""),
                    str(col.get("data_type") or col.get("type") or ""),
                    _yes_no(bool(col.get("is_primary"))),
                    _yes_no(bool(col.get("is_foreign"))),
                    str(col.get("comment") or ""),
                ]
                # 外键说明补充引用表
                if col.get("is_foreign") and col.get("reference_table"):
                    ref = col["reference_table"]
                    ref_col = col.get("reference_column") or ""
                    extra = f"→ {ref}" + (f".{ref_col}" if ref_col else "")
                    if values[4]:
                        values[4] = f"{values[4]} {extra}"
                    else:
                        values[4] = extra

                for j, val in enumerate(values):
                    cell = row.cells[j]
                    cell.text = ""
                    p = cell.paragraphs[0]
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j in (2, 3) else WD_ALIGN_PARAGRAPH.LEFT
                    run = p.add_run(val)
                    _set_run_font(run, "宋体", "Times New Roman", 10.5)

        _set_three_line_borders(tbl)

        # spacer
        doc.add_paragraph()

    # footer note
    foot = doc.add_paragraph()
    foot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = foot.add_run("由 yanleaf.com SQL→ER 工具生成")
    _set_run_font(run, "宋体", "Times New Roman", 9)
    run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

    doc.save(str(out_path))
    return out_path
