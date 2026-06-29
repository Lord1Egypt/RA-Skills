"""
WPS Office 全家桶 - MS Office 兼容层（三引擎之二）
当 WPS 不可用时，自动回退到 MS Word/Excel/PPT COM 接口

API 与 WPS 模式完全一致，调用方无感知。
"""
import sys
from pathlib import Path

from wps_common import safe_path, ensure_desktop_path, get_ms_word, release_ms


# ==================== Word ====================

def ms_create_word(title: str, filepath: str) -> dict:
    filepath = ensure_desktop_path(filepath)
    app = get_ms_word()
    doc = app.Documents.Add()
    if title:
        doc.Content.Text = title
        doc.Content.Font.Size = 16
        doc.Content.Font.Bold = True
        doc.Content.ParagraphFormat.Alignment = 1
    doc.SaveAs(str(filepath))
    doc.Close()
    return {"success": True, "path": str(filepath)}


def ms_edit_word(filepath: str, text: str, position: str = "end") -> dict:
    app = get_ms_word()
    doc = app.Documents.Open(filepath)
    if position == "end":
        doc.Content.InsertAfter(Text=text)
    elif position == "start":
        doc.Content.InsertBefore(Text=text)
    doc.Save()
    doc.Close()
    return {"success": True}


def ms_format_word(filepath: str, align: str = "center", font: str = "", size: int = 0, indent: int = 0) -> dict:
    app = get_ms_word()
    doc = app.Documents.Open(filepath)
    for para in doc.Paragraphs:
        if not para.Range.Text.strip():
            continue
        am = {"center": 1, "left": 0, "right": 2}
        if align in am:
            para.Range.ParagraphFormat.Alignment = am[align]
        if font:
            para.Range.Font.Name = font
        if size > 0:
            para.Range.Font.Size = size
        if indent > 0:
            para.Range.ParagraphFormat.FirstLineIndent = indent * 12
    doc.Save()
    doc.Close()
    return {"success": True}


def ms_export_word(filepath: str, fmt: str) -> dict:
    app = get_ms_word()
    doc = app.Documents.Open(filepath)
    fmt_map = {"pdf": 17, "txt": 7, "html": 8}
    if fmt not in fmt_map:
        doc.Close()
        return {"success": False, "error": f"不支持转 {fmt}"}
    out = Path(filepath).with_suffix(f".{fmt}")
    doc.SaveAs(str(out), fmt_map[fmt])
    doc.Close()
    return {"success": True, "path": str(out)}


# ==================== Excel ====================

def ms_create_excel(name: str, sheets=None) -> dict:
    app = get_ms_word()
    wb = app.Workbooks.Add()
    if sheets:
        for i, sn in enumerate(sheets):
            if i < wb.Sheets.Count:
                wb.Sheets(i+1).Name = sn
            else:
                wb.Sheets.Add().Name = sn
    filepath = ensure_desktop_path(f"{name}.xlsx")
    wb.SaveAs(str(filepath))
    wb.Close()
    return {"success": True, "path": str(filepath)}


# ==================== PPT ====================

def ms_create_ppt(title: str) -> dict:
    app = get_ms_word()
    ppt = app.Presentations.Add()
    slide = ppt.Slides.Add(1, 1)
    if slide.Shapes.Count > 0:
        slide.Shapes(1).TextFrame.TextRange.Text = title
    filepath = ensure_desktop_path(f"{title}.pptx")
    ppt.SaveAs(filepath)
    ppt.Close()
    return {"success": True, "path": filepath}
