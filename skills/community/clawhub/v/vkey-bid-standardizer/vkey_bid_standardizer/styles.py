"""vkey-bid-standardizer.styles

样式规范化：页面、Heading 1-5、Normal 样式从 profile 应用。
"""
from docx.document import Document as DocumentClass
from docx.shared import Cm

from .core import set_style_font, apply_paragraph_format


# ═══════════════════════════════════════════
#  页面
# ═══════════════════════════════════════════

def setup_page(doc: DocumentClass, page_cfg: dict) -> None:
    """配置页面边距。page_cfg: {top, bottom, left, right, unit}。"""
    for sec in doc.sections:
        sec.top_margin = Cm(page_cfg['top'])
        sec.bottom_margin = Cm(page_cfg['bottom'])
        sec.left_margin = Cm(page_cfg['left'])
        sec.right_margin = Cm(page_cfg['right'])


# ═══════════════════════════════════════════
#  Heading 1-5
# ═══════════════════════════════════════════

def setup_heading_styles(doc: DocumentClass, profile: dict) -> None:
    """配置 Heading 1-5 样式。"""
    available = {s.name for s in doc.styles}
    for h in profile['headings']:
        name = f"Heading {h['level']}"
        if name not in available:
            continue
        style = doc.styles[name]
        set_style_font(style, h['font_west'], h['font_east'], h['size'], bold=True)
        apply_paragraph_format(style, h)


# ═══════════════════════════════════════════
#  Normal
# ═══════════════════════════════════════════

def setup_normal_style(doc: DocumentClass, profile: dict) -> None:
    """配置 Normal 样式。"""
    body = profile['body']
    normal = doc.styles['Normal']
    set_style_font(normal, body['font_west'], body['font_east'], body['size'], bold=False)
    apply_paragraph_format(normal, body)


# ═══════════════════════════════════════════
#  表格（表头 + 内容）
# ═══════════════════════════════════════════

def setup_table_styles(doc: DocumentClass, profile: dict) -> None:
    """占位：表格样式由 fix_tables() 在段落级 run 上应用，不在 style 层。

    保留此函数以便未来把表格规范化也移到样式层。
    """
    pass


# ═══════════════════════════════════════════
#  一键应用
# ═══════════════════════════════════════════

def apply_all_styles(doc: DocumentClass, profile: dict) -> None:
    """一次性应用页面 + 标题 + 正文样式。"""
    setup_page(doc, profile['page'])
    setup_heading_styles(doc, profile)
    setup_normal_style(doc, profile)
