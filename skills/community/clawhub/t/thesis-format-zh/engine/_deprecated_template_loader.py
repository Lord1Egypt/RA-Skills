"""
模板加载模块

从 JSON 文件加载学校模板，转换为 python-docx 可用的配置。
"""

import os
import json
import glob
from docx.shared import Cm


SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(SKILL_DIR, "templates")


def load_templates():
    """从 templates/ 目录加载所有 JSON 模板"""
    tmpls = {}
    if not os.path.isdir(TEMPLATE_DIR):
        return tmpls
    for fp in sorted(glob.glob(os.path.join(TEMPLATE_DIR, "*.json"))):
        name = os.path.splitext(os.path.basename(fp))[0]
        with open(fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
        tmpls[name] = data
    return tmpls


def json_to_cfg(tmpl):
    """将 JSON 模板配置转换为 python-docx 可用单位"""
    p = tmpl["page"]
    cfg = {
        "name": tmpl["name"],
        "page_cfg": {
            "width": Cm(p["width_cm"]),
            "height": Cm(p["height_cm"]),
            "top": Cm(p["top_cm"]),
            "bottom": Cm(p["bottom_cm"]),
            "left": Cm(p["left_cm"]),
            "right": Cm(p["right_cm"]),
            "header": Cm(p["header_cm"]),
            "footer": Cm(p["footer_cm"]),
            "gutter": Cm(p.get("gutter_cm", 0)),
        },
        "header_text": tmpl.get("header_text", ""),
        "header_font": tmpl.get("header_font", "宋体"),
        "header_size": tmpl.get("header_size_pt", 10.5),
        "header_underline": tmpl.get("header_underline", False),
        "heading1": _heading_cfg(tmpl.get("heading1", {})),
        "heading2": _heading_cfg(tmpl.get("heading2", {})),
        "heading3": _heading_cfg(tmpl.get("heading3", {})),
        "heading4": _heading_cfg(tmpl.get("heading4", {})) if "heading4" in tmpl else None,
        "normal": _normal_cfg(tmpl.get("normal", {})),
        "caption": _caption_cfg(tmpl.get("caption", {})) if "caption" in tmpl else None,
        "figure_caption": _caption_cfg(tmpl.get("figure_caption", {})) if "figure_caption" in tmpl else None,
        "table_caption": _caption_cfg(tmpl.get("table_caption", {})) if "table_caption" in tmpl else None,
        "table_cell": tmpl.get("table_cell", None),
        "reference": _ref_cfg(tmpl.get("reference", {})),
        "abstract_title": _heading_cfg(tmpl.get("abstract", {})),
        "abstract_en": tmpl.get("abstract_en", None),
        "page_number": tmpl.get("page_number", None),
        "formula": tmpl.get("formula", None),
        "appendix": tmpl.get("appendix", None),
        "continuation_table": tmpl.get("continuation_table", None),
        "toc_field": tmpl.get("toc_field", None),
        "page_number_align": tmpl.get("page_number_align", None),
        "sections": tmpl.get("sections", []),
    }
    return cfg


def _heading_cfg(h):
    return {
        "font": h.get("font", "黑体"),
        "size": h.get("size_pt", 14),
        "bold": h.get("bold", False),
        "align": h.get("align", "left"),
        "space_before": h.get("space_before_pt", 24),
        "space_after": h.get("space_after_pt", 6),
        "line_spacing": h.get("line_spacing_pt", 20),
    }


def _normal_cfg(n):
    return {
        "font": n.get("font", "宋体"),
        "font_en": n.get("font_en", "Times New Roman"),
        "size": n.get("size_pt", 12),
        "align": n.get("align", "justify"),
        "first_line_indent": n.get("first_line_indent_char", 2) > 0,
        "line_spacing": n.get("line_spacing_pt", 20),
        "space_before": n.get("space_before_pt", 0),
        "space_after": n.get("space_after_pt", 0),
    }


def _caption_cfg(c):
    return {
        "font": c.get("font", "黑体"),
        "size": c.get("size_pt", 11),
        "bold": c.get("bold", False),
        "space_before": c.get("space_before_pt", 6),
        "space_after": c.get("space_after_pt", 6),
    }


def _ref_cfg(r):
    return {
        "font": r.get("font", "宋体"),
        "font_en": r.get("font_en", "Times New Roman"),
        "size": r.get("size_pt", 10.5),
        "line_spacing": r.get("line_spacing_pt", 16),
        "space_before": r.get("space_before_pt", 3),
        "space_after": r.get("space_after_pt", 0),
        "hanging_indent": r.get("hanging_indent", False),
        "first_line_indent_char": r.get("first_line_indent_char", 0),
    }


def create_template_skeleton(tmpl_name):
    """创建新学校模板骨架文件"""
    skeleton = {
        "name": tmpl_name,
        "version": "1.0",
        "page": {
            "width_cm": 21.0, "height_cm": 29.7,
            "top_cm": 2.5, "bottom_cm": 2.0,
            "left_cm": 2.5, "right_cm": 2.0,
            "header_cm": 1.5, "footer_cm": 1.75,
        },
        "header_text": "XX大学本科毕业论文",
        "header_font": "宋体",
        "header_size_pt": 10.5,
        "heading1": {"font": "黑体", "size_pt": 15, "align": "center", "space_before_pt": 40, "space_after_pt": 20},
        "heading2": {"font": "黑体", "size_pt": 14, "align": "left", "space_before_pt": 24, "space_after_pt": 6},
        "heading3": {"font": "黑体", "size_pt": 12, "align": "left", "space_before_pt": 12, "space_after_pt": 6},
        "normal": {"font": "宋体", "size_pt": 12, "align": "justify", "first_line_indent_char": 2, "line_spacing_pt": 20},
        "caption": {"font": "宋体", "size_pt": 11, "align": "center", "bold": True},
        "reference": {"font": "宋体", "size_pt": 10.5, "align": "justify", "line_spacing_pt": 16, "first_line_indent_char": 0},
        "abstract": {"title_font": "黑体", "title_size_pt": 15, "align": "center", "space_before_pt": 40, "space_after_pt": 20},
        "sections": [
            {"name": "封面", "page_range": [0, 0], "header": False, "page_number": False},
            {"name": "摘要目录", "page_range": [1, 2], "header": False, "page_number": "roman"},
            {"name": "正文", "section_idx": 3, "header": True, "page_number": "arabic", "page_start": 1},
        ],
    }
    slug = tmpl_name.replace(' ', '-').replace('（', '(').replace('）', ')')
    outpath = os.path.join(TEMPLATE_DIR, f"{slug}.json")
    os.makedirs(TEMPLATE_DIR, exist_ok=True)
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(skeleton, f, ensure_ascii=False, indent=2)
    return outpath
