from __future__ import annotations

from docx.document import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

TITLE_STYLE = "KB-SDS-Title"
META_STYLE = "KB-SDS-Meta"
SECTION_STYLE = "KB-SDS-Section"
SUBSECTION_STYLE = "KB-SDS-Subsection"
BODY_STYLE = "KB-SDS-Body"
BODY_TIGHT_STYLE = "KB-SDS-Body-Tight"
LABEL_STYLE = "KB-SDS-Label"
TABLE_STYLE = "KB-SDS-Table"
TABLE_HEADER_STYLE = "KB-SDS-TableHeader"
FOOTER_STYLE = "KB-SDS-Footer"

FONT_NAME = "Aptos"
ACCENT_COLOR = "23425B"
RULE_COLOR = "7F8A94"


def _set_font_family(style, font_name: str) -> None:
    style.font.name = font_name
    element = style.element
    rpr = element.get_or_add_rPr()
    rfonts = rpr.rFonts
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for key in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(key), font_name)


def _ensure_paragraph_style(
    document: Document,
    name: str,
    *,
    base: str = "Normal",
    size: float = 10.5,
    bold: bool = False,
    italic: bool = False,
    color: str = "222222",
    alignment: WD_ALIGN_PARAGRAPH | None = None,
    space_before: float = 0,
    space_after: float = 0,
    line_spacing: float = 1.08,
) -> None:
    styles = document.styles
    style = styles[name] if name in styles else styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    if base in styles:
        style.base_style = styles[base]
    _set_font_family(style, FONT_NAME)
    style.font.size = Pt(size)
    style.font.bold = bold
    style.font.italic = italic
    style.font.color.rgb = RGBColor.from_string(color)
    paragraph_format = style.paragraph_format
    paragraph_format.space_before = Pt(space_before)
    paragraph_format.space_after = Pt(space_after)
    paragraph_format.line_spacing = line_spacing
    if alignment is not None:
        paragraph_format.alignment = alignment


def _ensure_table_style(document: Document, name: str) -> None:
    styles = document.styles
    if name in styles:
        return
    style = styles.add_style(name, WD_STYLE_TYPE.TABLE)
    style.base_style = styles["Table Grid"]


def apply_section_rule(paragraph) -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    borders = p_pr.find(qn("w:pBdr"))
    if borders is None:
        borders = OxmlElement("w:pBdr")
        p_pr.append(borders)
    bottom = borders.find(qn("w:bottom"))
    if bottom is None:
        bottom = OxmlElement("w:bottom")
        borders.append(bottom)
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "8")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), RULE_COLOR)


def ensure_styles(document: Document) -> None:
    _ensure_paragraph_style(
        document,
        TITLE_STYLE,
        size=17,
        bold=True,
        color=ACCENT_COLOR,
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=10,
        line_spacing=1.0,
    )
    _ensure_paragraph_style(
        document,
        META_STYLE,
        size=9.5,
        color="3A3A3A",
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=8,
        line_spacing=1.0,
    )
    _ensure_paragraph_style(
        document,
        SECTION_STYLE,
        size=11.5,
        bold=True,
        color=ACCENT_COLOR,
        space_before=10,
        space_after=5,
        line_spacing=1.0,
    )
    _ensure_paragraph_style(
        document,
        SUBSECTION_STYLE,
        size=10.5,
        bold=True,
        color=ACCENT_COLOR,
        space_before=5,
        space_after=2,
        line_spacing=1.0,
    )
    _ensure_paragraph_style(document, BODY_STYLE, size=10.0, space_after=3)
    _ensure_paragraph_style(document, BODY_TIGHT_STYLE, size=9.5, space_after=1, line_spacing=1.0)
    _ensure_paragraph_style(document, LABEL_STYLE, size=10.0, bold=True, color=ACCENT_COLOR, space_after=1)
    _ensure_paragraph_style(
        document,
        FOOTER_STYLE,
        size=8.5,
        color="555555",
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        line_spacing=1.0,
    )
    _ensure_table_style(document, TABLE_STYLE)
    _ensure_table_style(document, TABLE_HEADER_STYLE)
