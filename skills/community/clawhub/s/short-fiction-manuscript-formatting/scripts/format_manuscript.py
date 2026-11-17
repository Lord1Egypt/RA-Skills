#!/usr/bin/env python3
"""Emit one short story in William Shunn's modern short-fiction format.

Not a novel formatter: chapter, part, prologue, and epilogue headings are
rejected. Not Shunn Classic: two spaces after sentences are rejected.

Font is Courier New 12 pt (the writer's preference). Other rules stay modern:
one space between sentences, italics, curly quotes. A dash is two hyphens
with no spaces, because in Courier an em dash is easy to mistake for a hyphen.
The article text is not reproduced. Facts follow
https://format.ms/story (updated 13 July 2026).

The title's vertical position is measured against the text area, not the paper
edge, so the "a third to halfway down" band holds on both Letter and A4.

Standard library only.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import re
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import escape

NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
NS_CT = "http://schemas.openxmlformats.org/package/2006/content-types"
NS_CP = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
NS_DC = "http://purl.org/dc/elements/1.1/"
NS_DCTERMS = "http://purl.org/dc/terms/"
NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
NS_EP = "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"

PAPER = {
    "letter": (12240, 15840),
    "a4": (11906, 16838),
}
MARGIN = 1440  # 1 inch
INDENT = 720  # 0.5 inch
FONT = "Courier New"
# Leading apostrophes that must not become opening quotes.
_APOS_WORD = re.compile(
    r"(?:em|tis|twas|cause|round|bout|n|neath|fore|gainst|\d\ds)\b",
    re.IGNORECASE,
)
_SUFFIXES = {"jr", "jr.", "sr", "sr.", "ii", "iii", "iv", "v", "phd", "ph.d.", "md", "m.d."}
_ARTICLES = {"a", "an", "the", "of", "and", "or", "to", "in", "on", "for"}
_NOVEL_HEADING = re.compile(
    r"(?i)^(?:#{1,6}\s*)?(?:"
    r"chapter\b[^.?!]{0,60}|"
    r"prologue\b[^.?!]{0,60}|"
    r"epilogue\b[^.?!]{0,60}|"
    r"part\s+(?:[ivxlcdm]+|\d+)\b[^.?!]{0,60}|"
    r"book\s+(?:[ivxlcdm]+|\d+)\b[^.?!]{0,60}"
    r")$"
)
_NOVEL_REFUSAL = (
    "This skill formats one short story, not a novel. "
    "A chapter, part, book, prologue, or epilogue heading is novel structure, "
    "and this emitter will not invent it. See https://www.shunn.net/format/novels/ "
    "and use a novel workflow instead."
)


class FormatError(Exception):
    pass


@dataclass
class Run:
    text: str
    italic: bool = False


@dataclass
class Block:
    kind: str  # contact, title, byline, body, scene, end, spacer
    runs: list[Run] = field(default_factory=list)
    before: int = 0
    tab_count: str | None = None

    @property
    def plain(self) -> str:
        return "".join(run.text for run in self.runs)


def round_to(n: int, step: int) -> int:
    """Nearest multiple. Halves round away from zero (1,550 -> 1,600)."""
    if step <= 0:
        raise FormatError("rounding step must be positive")
    return int((n + step // 2) // step * step)


def _strip_controls(text: str) -> str:
    return "".join(ch for ch in text if ch in "\t\n" or ord(ch) >= 32)


def smarten(text: str) -> str:
    """Straight quotes to curly quotes. Leading contractions stay apostrophes."""
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    # Apostrophes inside or at the end of a word: don't, dogs', 90's
    text = re.sub(r"(?<=\w)'(?=\w)", "\u2019", text)
    text = re.sub(r"(?<=\w)'(?=$|[\s,.;:!?\)\]])", "\u2019", text)
    # 'em, 'tis, '90s — including after an em dash or opening quote.
    text = re.sub(
        r"(?<![\w])'(?=" + _APOS_WORD.pattern + ")",
        "\u2019",
        text,
        flags=re.IGNORECASE,
    )

    out: list[str] = []
    for i, ch in enumerate(text):
        if ch == '"':
            out.append("\u201c" if _opens(text, i) else "\u201d")
        elif ch == "'":
            out.append("\u2018" if _opens(text, i) else "\u2019")
        else:
            out.append(ch)
    return "".join(out)


def _opens(text: str, i: int) -> bool:
    if i == 0:
        return True
    return text[i - 1] in " \t\n([{\u2014\u2013-\u201c\u2018/:"


def normalize_inline(text: str) -> tuple[str, dict[str, int]]:
    """Collapse spacing. Keep a dash as two hyphens, which read clearly in Courier."""
    stats = {"double_spaces": 0, "dashes_as_hyphens": 0, "bold_to_italic": 0, "underline_to_italic": 0}
    text = _strip_controls(text).replace("\u00a0", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    stats["double_spaces"] = len(re.findall(r" {2,}", text))
    text = re.sub(r"[ \t]*\n[ \t]*", " ", text)
    text = re.sub(r" {2,}", " ", text).strip()
    text, n_bold = re.subn(r"\*\*([^*\n]+)\*\*", r"*\1*", text)
    stats["bold_to_italic"] = n_bold
    text, n_under = re.subn(r"(?<!\w)__([^_\n]+)__(?!\w)", r"*\1*", text)
    stats["underline_to_italic"] = n_under
    text, n_u = re.subn(r"(?is)<u>(.*?)</u>", r"*\1*", text)
    stats["underline_to_italic"] += n_u
    text = re.sub(r"(?is)<(i|em)>(.*?)</\1>", r"*\2*", text)
    # Em dash, or a spaced en dash, becomes --. A single hyphen in a word stays.
    text, n_dash = re.subn(r"\s*(?:—|--)\s*|\s+–\s+", "--", text)
    stats["dashes_as_hyphens"] = n_dash
    text = smarten(text)
    return text, stats


def split_emphasis(text: str) -> tuple[list[Run], int]:
    """*asterisks* and boundary _underscores_ become italic runs."""
    pattern = re.compile(r"(?<!\w)\*([^*\n]+)\*(?!\w)|(?<!\w)_([^_\n]+)_(?!\w)")
    runs: list[Run] = []
    pos = 0
    unclosed = text.count("*") % 2
    for match in pattern.finditer(text):
        if match.start() > pos:
            runs.append(Run(text[pos : match.start()], False))
        inner = match.group(1) if match.group(1) is not None else match.group(2)
        runs.append(Run(inner, True))
        pos = match.end()
    if pos < len(text):
        runs.append(Run(text[pos:], False))
    return [run for run in runs if run.text], unclosed


def add_stats(total: dict[str, int], extra: dict[str, int]) -> None:
    for key, value in extra.items():
        total[key] = total.get(key, 0) + value


def parse_front_matter(raw: str) -> tuple[dict[str, object], str]:
    text = raw.lstrip("\ufeff")
    if not text.startswith("---"):
        raise FormatError("manuscript.md must start with a --- front-matter block")
    lines = text.splitlines()
    if lines[0].strip() != "---":
        raise FormatError("opening --- must be alone on the first line")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise FormatError("front matter is missing its closing ---") from exc
    data: dict[str, object] = {}
    i = 1
    while i < end:
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        if line.startswith((" ", "\t")):
            raise FormatError(f"unexpected indent in front matter: {line!r}")
        if ":" not in line:
            raise FormatError(f"front matter line needs a key: {line!r}")
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value == "|":
            i += 1
            block: list[str] = []
            while i < end and (lines[i].startswith(" ") or lines[i].startswith("\t") or lines[i].strip() == ""):
                if lines[i].strip() == "":
                    # A blank line ends the block only when the next matter line is a key.
                    nxt = i + 1
                    if nxt < end and lines[nxt] and not lines[nxt].startswith((" ", "\t")):
                        break
                    block.append("")
                else:
                    block.append(lines[i].strip())
                i += 1
            data[key] = "\n".join(block).strip("\n")
            continue
        data[key] = _scalar(value)
        i += 1
    body = "\n".join(lines[end + 1 :]).strip("\n")
    return data, body


def _scalar(value: str) -> object:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    lower = value.lower()
    if lower in {"true", "false"}:
        return lower == "true"
    return value


def _as_str(data: dict[str, object], key: str, default: str = "") -> str:
    value = data.get(key, default)
    if value is None:
        return default
    return str(value).strip()


def _as_bool(data: dict[str, object], key: str) -> bool:
    value = data.get(key, False)
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _lines(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


def surname_from(byline: str) -> str:
    cleaned = re.sub(r"(?i)^by\s+", "", byline).strip()
    parts = cleaned.split()
    while parts and parts[-1].lower().strip(",.") in _SUFFIXES:
        parts.pop()
    if not parts:
        raise FormatError("byline is empty; cannot build the running header")
    return parts[-1].strip(",")


def keyword_from(title: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)?", title)
    significant = [word for word in words if word.lower() not in _ARTICLES]
    chosen = significant or words
    if not chosen:
        raise FormatError("title is empty; cannot build the running header")
    if len(chosen) <= 2:
        return " ".join(chosen)
    return chosen[-1]


def byline_text(byline: str) -> str:
    cleaned = re.sub(r"(?i)^by\s+", "", byline).strip()
    if not cleaned:
        raise FormatError("byline is required")
    return f"by {cleaned}"


def parse_body(body: str, include_end: bool, stats: dict[str, int]) -> list[Block]:
    warnings = stats.setdefault("_warnings", [])  # type: ignore[assignment]
    if re.search(r"\n[ \t]*\n[ \t]*\n", body):
        warnings.append(
            "Collapsed extra blank lines. A blank line is not a scene break; put # alone on its own line."
        )
    chunks = re.split(r"\n\s*\n", body.strip()) if body.strip() else []
    blocks: list[Block] = []
    for chunk in chunks:
        flat = " ".join(line.strip() for line in chunk.splitlines() if line.strip())
        if not flat:
            continue
        if _NOVEL_HEADING.match(flat):
            raise FormatError(_NOVEL_REFUSAL)
        if re.fullmatch(r"#|\*{3}|#\s*#\s*#|(?:\* ?){3}|---+|—{1,3}", flat):
            if flat != "#":
                stats["scene_normalized"] = stats.get("scene_normalized", 0) + 1
            blocks.append(Block("scene", [Run("#")]))
            continue
        if flat == "END":
            blocks.append(Block("end", [Run("END")]))
            continue
        text, inline_stats = normalize_inline(flat)
        add_stats(stats, inline_stats)
        if re.match(r"(?i)^copyright\b", text):
            raise FormatError(
                "a story paragraph begins with 'Copyright'. Shunn says not to put a copyright notice on a submission. Remove it, or do not use this skill for that paragraph."
            )
        runs, unclosed = split_emphasis(text)
        if unclosed:
            warnings.append("An unclosed *emphasis* marker was left as literal text.")
        blocks.append(Block("body", runs or [Run(text)]))
    ends = [i for i, block in enumerate(blocks) if block.kind == "end"]
    if len(ends) > 1:
        warnings.append("More than one END mark; kept a single centered END after the last line.")
        blocks = [block for i, block in enumerate(blocks) if block.kind != "end" or i == ends[-1]]
        ends = [i for i, block in enumerate(blocks) if block.kind == "end"]
    if ends and ends[-1] != len(blocks) - 1:
        warnings.append("Moved END to after the last line.")
        end = blocks.pop(ends[-1])
        blocks.append(end)
    if include_end and not any(block.kind == "end" for block in blocks):
        blocks.append(Block("end", [Run("END")]))
    if not any(block.kind == "body" for block in blocks):
        raise FormatError("the story has no paragraphs")
    return blocks


def word_count(blocks: list[Block]) -> int:
    return sum(len(block.plain.split()) for block in blocks if block.kind == "body")


def build_blocks(data: dict[str, object], body: str) -> tuple[list[Block], dict[str, object]]:
    title_raw = _as_str(data, "title")
    byline_raw = _as_str(data, "byline")
    if not title_raw:
        raise FormatError("front matter needs a title")
    if not byline_raw:
        raise FormatError("front matter needs a byline (the name printed with the story)")
    if _as_bool(data, "novel") or _as_bool(data, "novella") or _as_str(data, "chapters"):
        raise FormatError(_NOVEL_REFUSAL)
    paper = _as_str(data, "paper", "letter").lower() or "letter"
    if paper not in PAPER:
        raise FormatError("paper must be 'letter' or 'a4'")
    include_end = _as_bool(data, "include_end")

    stats: dict[str, int] = {}
    story = parse_body(body, include_end, stats)
    count = word_count(story)
    rounded = round_to(count, 100)
    count_line = f"{rounded:,} words"

    title, title_stats = normalize_inline(title_raw)
    byline, byline_stats = normalize_inline(byline_text(byline_raw))
    add_stats(stats, title_stats)
    add_stats(stats, byline_stats)
    title_runs, _ = split_emphasis(title)
    byline_runs, _ = split_emphasis(byline)

    header_surname = _as_str(data, "header_surname") or surname_from(byline_raw)
    header_keyword = _as_str(data, "header_keyword") or keyword_from(title_raw)
    header_surname, _ = normalize_inline(header_surname)
    header_keyword, _ = normalize_inline(header_keyword)
    for label, value in ("header surname", header_surname), ("header keyword", header_keyword):
        if not value or "/" in value or len(value) > 40:
            raise FormatError(f"{label} must be 1–40 characters and must not contain '/'")

    legal = _as_str(data, "legal_name")
    name_line = legal
    address = _lines(_as_str(data, "address"))
    phone = _as_str(data, "phone")
    email = _as_str(data, "email")
    affiliation = _lines(_as_str(data, "affiliation"))

    contact_lines: list[str] = []
    if name_line:
        contact_lines.append(name_line)
    contact_lines.extend(address)
    if phone:
        contact_lines.append(phone)
    if email:
        contact_lines.append(email)
    if affiliation:
        if contact_lines:
            contact_lines.append("")
        contact_lines.extend(affiliation)

    page_w, page_h = PAPER[paper]
    # Shunn: the title sits "a third to halfway down the first page", centered.
    # Measure from the top of the *text area*, not the paper edge: what matters is
    # how far the editor has to scroll to reach the title, and the paper's top
    # margin is already blank note space. A4 and Letter differ by ~5.6%, so the
    # twip constants keep the same ratio on both sizes.
    text_top = MARGIN
    text_bottom = page_h - MARGIN
    text_h = text_bottom - text_top
    # Single-spaced 12 pt line is 240 twips.
    contact_h = len(contact_lines) * 240
    # Target 40% of the text area, inside the 1/3-1/2 band.
    target = text_top + int(round(0.40 * text_h))
    before = max(target - text_top - contact_h, 0)
    title_from_top = text_top + contact_h + before
    fraction = (title_from_top - text_top) / text_h
    position_note = ""
    if before < 0:
        before = 0
        if fraction < (1 / 3) - 0.005:
            position_note = (
                "title sits above one-third of the page because the contact block is long; "
                "shorten the address rather than shrinking the margins"
            )
    elif not (1 / 3 - 0.01) <= fraction <= 0.50 + 0.005:
        raise FormatError(f"title position {fraction:.2f} is outside a third to halfway down the page")

    blocks: list[Block] = []
    if contact_lines:
        for index, line in enumerate(contact_lines):
            runs = [Run(line)] if line else []
            blocks.append(Block("contact", runs, tab_count=count_line if index == 0 else None))
    else:
        blocks.append(Block("contact", [], tab_count=count_line))
    blocks.append(Block("title", title_runs or [Run(title)], before=before))
    blocks.append(Block("spacer"))
    blocks.append(Block("byline", byline_runs or [Run(byline)]))
    blocks.append(Block("spacer"))
    blocks.append(Block("spacer"))
    blocks.extend(story)

    meta = {
        "title": title,
        "byline": byline,
        "words": count,
        "rounded": rounded,
        "step": 100,
        "word_count_line": count_line,
        "header": f"{header_surname} / {header_keyword} / #",
        "header_surname": header_surname,
        "header_keyword": header_keyword,
        "paper": paper,
        "page_w": page_w,
        "page_h": page_h,
        "title_before": before,
        "title_fraction": round(fraction, 3),
        "position_note": position_note,
        "scenes": sum(1 for block in blocks if block.kind == "scene"),
        "italics": sum(1 for block in blocks for run in block.runs if run.italic),
        "fixes": {key: value for key, value in stats.items() if not key.startswith("_") and value},
        "warnings": list(stats.get("_warnings", [])),
        "contact_lines": len(contact_lines),
    }
    if position_note:
        meta["warnings"].append(position_note)
    return blocks, meta


def _rpr(italic: bool) -> str:
    italic_xml = "<w:i/><w:iCs/>" if italic else ""
    return (
        "<w:rPr>"
        f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}" w:eastAsia="{FONT}"/>'
        f"{italic_xml}"
        '<w:color w:val="000000"/>'
        '<w:sz w:val="24"/><w:szCs w:val="24"/>'
        "</w:rPr>"
    )


def _runs_xml(runs: list[Run]) -> str:
    if not runs:
        return f"<w:r>{_rpr(False)}<w:t></w:t></w:r>"
    parts: list[str] = []
    for run in runs:
        parts.append(
            f"<w:r>{_rpr(run.italic)}"
            f'<w:t xml:space="preserve">{escape(run.text)}</w:t></w:r>'
        )
    return "".join(parts)


def _paragraph(block: Block, content_width: int) -> str:
    kind = block.kind
    if kind == "contact":
        align = "right" if block.plain.startswith("about ") and not block.tab_count else "left"
        tabs = ""
        if block.tab_count:
            tabs = f'<w:tabs><w:tab w:val="right" w:pos="{content_width}"/></w:tabs>'
            align = "left"
        ppr = (
            "<w:pPr>"
            '<w:pStyle w:val="Contact"/>'
            f"{tabs}"
            '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
            '<w:ind w:firstLine="0" w:left="0"/>'
            f'<w:jc w:val="{align}"/>'
            "</w:pPr>"
        )
        runs = _runs_xml(block.runs)
        if block.tab_count:
            runs += (
                f"<w:r>{_rpr(False)}<w:tab/></w:r>"
                f"<w:r>{_rpr(False)}<w:t xml:space=\"preserve\">{escape(block.tab_count)}</w:t></w:r>"
            )
        return f"<w:p>{ppr}{runs}</w:p>"

    if kind == "spacer":
        ppr = (
            "<w:pPr>"
            '<w:pStyle w:val="Spacer"/>'
            '<w:spacing w:before="0" w:after="0" w:line="480" w:lineRule="auto"/>'
            '<w:ind w:firstLine="0" w:left="0"/>'
            '<w:jc w:val="left"/>'
            "</w:pPr>"
        )
        return f"<w:p>{ppr}</w:p>"

    specs = {
        "title": ("Title", "center", 0, 480),
        "byline": ("Byline", "center", 0, 480),
        "body": ("BodyText", "left", INDENT, 480),
        "scene": ("SceneBreak", "center", 0, 480),
        "end": ("EndMark", "center", 0, 480),
    }
    style, align, indent, line = specs[kind]
    ppr = (
        "<w:pPr>"
        f'<w:pStyle w:val="{style}"/>'
        f'<w:spacing w:before="{block.before}" w:after="0" w:line="{line}" w:lineRule="auto"/>'
        f'<w:ind w:firstLine="{indent}" w:left="0"/>'
        f'<w:jc w:val="{align}"/>'
        '<w:widowControl w:val="0"/>'
        "</w:pPr>"
    )
    return f"<w:p>{ppr}{_runs_xml(block.runs)}</w:p>"


def _header(surname: str, keyword: str, *, first: bool) -> str:
    if first:
        body = (
            "<w:p><w:pPr>"
            '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
            '<w:ind w:firstLine="0"/>'
            '<w:jc w:val="right"/>'
            f"</w:pPr><w:r>{_rpr(False)}<w:t></w:t></w:r></w:p>"
        )
    else:
        label = f"{surname} / {keyword} / "
        body = (
            "<w:p><w:pPr>"
            '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
            '<w:ind w:firstLine="0"/>'
            '<w:jc w:val="right"/>'
            "</w:pPr>"
            f"<w:r>{_rpr(False)}<w:t xml:space=\"preserve\">{escape(label)}</w:t></w:r>"
            f"<w:r>{_rpr(False)}<w:fldChar w:fldCharType=\"begin\" w:dirty=\"true\"/></w:r>"
            f"<w:r>{_rpr(False)}<w:instrText xml:space=\"preserve\"> PAGE </w:instrText></w:r>"
            f"<w:r>{_rpr(False)}<w:fldChar w:fldCharType=\"end\"/></w:r>"
            "</w:p>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:hdr xmlns:w="{NS_W}" xmlns:r="{NS_R}">{body}</w:hdr>'
    )


def _styles() -> str:
    def style(style_id: str, name: str) -> str:
        return (
            f'<w:style w:type="paragraph" w:styleId="{style_id}">'
            f"<w:name w:val=\"{name}\"/>"
            '<w:basedOn w:val="Normal"/>'
            "<w:qFormat/>"
            "</w:style>"
        )

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:styles xmlns:w="{NS_W}">'
        "<w:docDefaults><w:rPrDefault><w:rPr>"
        f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}" w:eastAsia="{FONT}"/>'
        '<w:color w:val="000000"/>'
        '<w:sz w:val="24"/><w:szCs w:val="24"/>'
        "</w:rPr></w:rPrDefault>"
        '<w:pPrDefault><w:pPr>'
        '<w:spacing w:before="0" w:after="0" w:line="480" w:lineRule="auto"/>'
        "</w:pPr></w:pPrDefault></w:docDefaults>"
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
        '<w:name w:val="Normal"/>'
        "<w:rPr>"
        f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}" w:eastAsia="{FONT}"/>'
        '<w:sz w:val="24"/><w:szCs w:val="24"/>'
        "</w:rPr></w:style>"
        + style("Contact", "Contact")
        + style("Title", "Title")
        + style("Byline", "Byline")
        + style("BodyText", "Body Text")
        + style("SceneBreak", "Scene Break")
        + style("EndMark", "End Mark")
        + style("Spacer", "Spacer")
        + "</w:styles>"
    )


def _settings() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:settings xmlns:w="{NS_W}">'
        '<w:view w:val="print"/>'
        '<w:updateFields w:val="true"/>'
        '<w:defaultTabStop w:val="720"/>'
        "</w:settings>"
    )


def render_docx(blocks: list[Block], meta: dict[str, object]) -> dict[str, str]:
    page_w = int(meta["page_w"])
    page_h = int(meta["page_h"])
    content_width = page_w - 2 * MARGIN
    body = "".join(_paragraph(block, content_width) for block in blocks)
    sect = (
        "<w:sectPr>"
        '<w:headerReference w:type="default" r:id="rId3"/>'
        '<w:headerReference w:type="first" r:id="rId4"/>'
        f'<w:pgSz w:w="{page_w}" w:h="{page_h}" w:orient="portrait"/>'
        f'<w:pgMar w:top="{MARGIN}" w:right="{MARGIN}" w:bottom="{MARGIN}" '
        f'w:left="{MARGIN}" w:header="720" w:footer="720" w:gutter="0"/>'
        "<w:titlePg/>"
        '<w:pgNumType w:start="1"/>'
        "</w:sectPr>"
    )
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:document xmlns:w="{NS_W}" xmlns:r="{NS_R}">'
        f"<w:body>{body}{sect}</w:body></w:document>"
    )
    surname = str(meta["header_surname"])
    keyword = str(meta["header_keyword"])
    return {
        "[Content_Types].xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<Types xmlns="{NS_CT}">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
            '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
            '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
            '<Override PartName="/word/header2.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
            '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
            '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
            "</Types>"
        ),
        "_rels/.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<Relationships xmlns="{NS_REL}">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
            "</Relationships>"
        ),
        "word/_rels/document.xml.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<Relationships xmlns="{NS_REL}">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>'
            '<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header2.xml"/>'
            "</Relationships>"
        ),
        "word/document.xml": document,
        "word/styles.xml": _styles(),
        "word/settings.xml": _settings(),
        "word/header1.xml": _header(surname, keyword, first=False),
        "word/header2.xml": _header(surname, keyword, first=True),
        "docProps/core.xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<cp:coreProperties xmlns:cp="{NS_CP}" xmlns:dc="{NS_DC}" '
            f'xmlns:dcterms="{NS_DCTERMS}" xmlns:xsi="{NS_XSI}">'
            f"<dc:title>{escape(str(meta['title']))}</dc:title>"
            f"<dc:creator>{escape(str(meta['byline']))}</dc:creator>"
            "<cp:lastModifiedBy>short-fiction-manuscript</cp:lastModifiedBy>"
            "</cp:coreProperties>"
        ),
        "docProps/app.xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<Properties xmlns="{NS_EP}">'
            "<Application>short-fiction-manuscript</Application>"
            "</Properties>"
        ),
    }


def write_docx(path: Path, parts: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for name, xml in parts.items():
            package.writestr(name, xml.encode("utf-8"))


def verify(path: Path, meta: dict[str, object]) -> list[str]:
    problems: list[str] = []
    with zipfile.ZipFile(path) as package:
        files = {name: package.read(name).decode("utf-8") for name in package.namelist()}
    document = files.get("word/document.xml", "")
    header = files.get("word/header1.xml", "")
    first = files.get("word/header2.xml", "")
    styles = files.get("word/styles.xml", "")
    required = [
        "[Content_Types].xml",
        "word/document.xml",
        "word/styles.xml",
        "word/settings.xml",
        "word/header1.xml",
        "word/header2.xml",
    ]
    for name in required:
        if name not in files:
            problems.append(f"missing part {name}")

    if f'w:top="{MARGIN}"' not in document or f'w:left="{MARGIN}"' not in document:
        problems.append("margins are not 1 inch")
    if f'w:w="{meta["page_w"]}"' not in document or f'w:h="{meta["page_h"]}"' not in document:
        problems.append("page size does not match the request")
    if "<w:titlePg/>" not in document:
        problems.append("first page is not a different first page")
    if 'w:header="720"' not in document:
        problems.append("header is not 0.5 inch from the edge")
    if FONT not in styles or FONT not in document:
        problems.append("Courier New is missing")
    for banned in ("Times New Roman", "Calibri", "Arial", "Cambria", "Garamond", "Verdana", "Georgia"):
        if banned in document or banned in header or banned in styles:
            problems.append(f"banned font {banned}")
    if "<w:b/>" in document or "<w:bCs/>" in document or "<w:u " in document:
        problems.append("bold or underline is present")
    if 'w:val="both"' in document:
        problems.append("justified text is present")
    if "<w:sz w:val=\"24\"/>" not in document:
        problems.append("12 pt type is missing")

    texts = re.findall(r"<w:t[^>]*>([^<]*)</w:t>", document)
    joined = "\n".join(texts)
    if "\u2014" in joined:
        problems.append("an em dash remains; Courier New manuscripts use --")
    if '"' in joined or "'" in joined:
        problems.append("straight quotes remain in the story")
    if re.search(r" {2,}", joined):
        problems.append("double spaces remain")
    if re.search(r"\b\d{3}-\d{2}-\d{4}\b", joined):
        problems.append("a Social Security pattern is present")
    if re.search(r"(?im)^copyright\b", joined):
        problems.append("a copyright line is present")
    if str(meta["word_count_line"]) not in joined:
        problems.append("word-count line is missing or does not match the rounded count")
    if str(meta["title"]) not in joined:
        problems.append("title text is missing")
    if str(meta["byline"]) not in joined:
        problems.append("byline is missing")

    def paras(style: str) -> list[str]:
        return re.findall(rf"<w:p>(?:(?!</w:p>).)*?<w:pStyle w:val=\"{style}\"/>.*?</w:p>", document)

    bodies = paras("BodyText")
    if not bodies:
        problems.append("no body paragraphs")
    for para in bodies:
        if 'w:firstLine="720"' not in para or 'w:line="480"' not in para or 'w:val="left"' not in para:
            problems.append("a body paragraph is not double-spaced, indented 0.5 inch, and left aligned")
            break
    for para in paras("SceneBreak"):
        if ">#</w:t>" not in para or 'w:val="center"' not in para or 'w:firstLine="0"' not in para:
            problems.append("a scene break is not a centered #")
            break
    if int(meta["scenes"]) != len(paras("SceneBreak")):
        problems.append("scene-break count drifted")
    titles = paras("Title")
    if len(titles) != 1 or 'w:val="center"' not in titles[0] or f'w:before="{meta["title_before"]}"' not in titles[0]:
        problems.append("title is missing, not centered, or not placed in the note space")
    bylines = paras("Byline")
    if len(bylines) != 1 or 'w:val="center"' not in bylines[0]:
        problems.append("byline is missing or not centered")
    if int(meta["title_before"]) > 0:
        fraction = float(meta["title_fraction"])
        if not (1 / 3 - 0.01) <= fraction <= 0.50 + 0.005:
            problems.append(f"title fraction {fraction} is outside a third to halfway")

    label = f"{meta['header_surname']} / {meta['header_keyword']} / "
    if label not in header or " PAGE " not in header or 'w:val="right"' not in header:
        problems.append("running header is missing surname, keyword, PAGE field, or right alignment")
    if FONT not in header:
        problems.append("running header is not Courier New")
    first_text = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", first)).strip()
    if first_text or "PAGE" in first:
        problems.append("page 1 header is not empty")
    return problems


def report(meta: dict[str, object], ok: bool) -> str:
    lines = [
        f"title: {meta['title']}",
        f"byline: {meta['byline']}",
        f"words: {meta['words']}",
        f"word_count_line: {meta['word_count_line']}",
        f"header: {meta['header']}",
        f"title_position: {meta['title_fraction']} of the page",
        f"scenes: {meta['scenes']}",
        f"italics: {meta['italics']}",
        f"fixes: {json.dumps(meta['fixes'], ensure_ascii=False)}",
    ]
    for warning in meta["warnings"]:
        lines.append(f"warning: {warning}")
    lines.append("VERIFY PASS" if ok else "VERIFY FAIL")
    return "\n".join(lines)


def convert(source: Path, dest: Path) -> dict[str, object]:
    raw = source.read_text(encoding="utf-8")
    data, body = parse_front_matter(raw)
    blocks, meta = build_blocks(data, body)
    parts = render_docx(blocks, meta)
    write_docx(dest, parts)
    problems = verify(dest, meta)
    meta["problems"] = problems
    meta["ok"] = not problems
    return meta


def self_test() -> int:
    failures: list[str] = []
    if round_to(1507, 100) != 1500:
        failures.append("1,507 did not round to 1,500")
    if round_to(1550, 100) != 1600:
        failures.append("1,550 did not round to 1,600")
    if round_to(1740, 500) != 1500:
        failures.append("1,740 did not round to 1,500")

    # The title fraction is measured against the text area, so it must stay in
    # Shunn's "a third to halfway" band on both paper sizes.
    for paper in ("letter", "a4"):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "paper.md"
            source.write_text(
                "---\nlegal_name: Mira Chen\nbyline: Mira Chen\ntitle: The Ragged Right\npaper: "
                + paper
                + "\n---\n\nOne two three four five six seven eight nine ten.\n",
                encoding="utf-8",
            )
            meta = convert(source, root / "paper.docx")
            fraction = float(meta["title_fraction"])
            if not 0.33 <= fraction <= 0.50:
                failures.append(f"title fraction out of range on {paper}: {fraction}")

    if surname_from("Bill Shunn, Jr.") != "Shunn":
        failures.append("suffix was not stripped from the header surname")
    if keyword_from("Proper Manuscript Format") != "Format":
        failures.append(f"keyword heuristic failed: {keyword_from('Proper Manuscript Format')!r}")
    if keyword_from("The Ragged Right") != "Ragged Right":
        failures.append(f"short-title keyword failed: {keyword_from('The Ragged Right')!r}")

    sample = smarten('Knock \'em dead. \'Tis true in the \'90s. "It\'s a \'test,\'" she said.')
    for bad, good in (
        ("'em", "\u2019em"),
        ("'Tis", "\u2019Tis"),
        ("'90s", "\u201990s"),
        ('"It', "\u201cIt"),
        ("said.", None),
    ):
        if good and good not in sample:
            failures.append(f"smarten missed {bad!r} in {sample!r}")
    if "'" in sample or '"' in sample:
        failures.append(f"straight quotes remain: {sample!r}")
    if "\u2018em" in sample or "\u2018Tis" in sample:
        failures.append(f"leading apostrophe opened: {sample!r}")

    story = """\
---
legal_name: Mira Chen
pronouns: she/her
address: |
  18 Margin Street
  Serif, OH 44114
phone: (216) 555-0148
email: mira@example.com
affiliation: Active member, SFWA
byline: A. A. Lovelace
title: Proper Manuscript Format
header_keyword: Format
include_end: true
---

The editor tapped the page.  "One space," she said.


Mira kept the *Ragged Right* in italics—not an underline.

'em and 'tis have to face the right way.

#

***

She stopped.

END
"""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source = root / "story.md"
        dest = root / "story.docx"
        source.write_text(story, encoding="utf-8")
        try:
            meta = convert(source, dest)
        except FormatError as exc:
            print(f"SELF-TEST FAIL\n{exc}")
            return 1
        if not meta["ok"]:
            failures.extend(str(item) for item in meta["problems"])
        if meta["header"] != "Lovelace / Format / #":
            failures.append(f"header guess failed: {meta['header']}")
        if meta["word_count_line"] != f"{meta['rounded']:,} words":
            failures.append("word-count line mismatch")
        if int(meta["words"]) < 20:
            failures.append("word count unexpectedly small")
        if int(meta["scenes"]) != 2:
            failures.append(f"expected 2 scene breaks, got {meta['scenes']}")
        if not meta["fixes"].get("double_spaces"):
            failures.append("double spaces were not recorded as a fix")
        if not meta["fixes"].get("dashes_as_hyphens"):
            failures.append("em dash was not turned into --")
        fraction = float(meta["title_fraction"])
        if not 0.33 <= fraction <= 0.50:
            failures.append(f"title fraction out of range: {fraction}")
        # Classic must not write a file.
        classic = root / "classic.docx"
        with contextlib.redirect_stderr(io.StringIO()):
            code = main(["--classic", str(source), "-o", str(classic)])
        if code != 2 or classic.exists():
            failures.append("classic request was not refused")
        try:
            novel = story.replace("She stopped.", "Chapter 1\n\nShe stopped.", 1)
            source.write_text(novel, encoding="utf-8")
            convert(source, root / "novel.docx")
            failures.append("a chapter heading was accepted")
        except FormatError:
            pass
        if (root / "novel.docx").exists():
            failures.append("novel output was written")
        try:
            source.write_text(story.replace("include_end: true", "include_end: true\nnovella: true", 1), encoding="utf-8")
            convert(source, root / "novella.docx")
            failures.append("novella flag was accepted")
        except FormatError:
            pass
        try:
            convert_copyright = story + "\nCopyright 2026 by Mira Chen.\n"
            source.write_text(convert_copyright, encoding="utf-8")
            convert(source, dest)
            failures.append("copyright paragraph was accepted")
        except FormatError:
            pass

    if failures:
        print("SELF-TEST FAIL")
        print("\n".join(failures))
        return 1
    print("SELF-TEST PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    args_in = list(sys.argv[1:] if argv is None else argv)
    if "--classic" in args_in:
        sys.stderr.write(
            "Refusing Shunn Classic. This skill already sets Courier New, and it keeps "
            "one space between sentences. Classic means a second space after each sentence. "
            "See references/classic-vs-modern.md and https://format.ms/classic\n"
        )
        return 2
    parser = argparse.ArgumentParser(description="Format a short story in Shunn's modern manuscript style.")
    parser.add_argument("source", nargs="?", type=Path, help="Markdown file with YAML-subset front matter")
    parser.add_argument("-o", "--output", type=Path, help="Destination .docx")
    parser.add_argument("--json", action="store_true", help="Print a JSON summary")
    parser.add_argument("--self-test", action="store_true", help="Run the built-in checks")
    args = parser.parse_args(args_in)
    if args.self_test:
        return self_test()
    if args.source is None or args.output is None:
        parser.error("source and -o are required")
    try:
        meta = convert(args.source, args.output)
    except FormatError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1
    public = {
        "title": meta["title"],
        "byline": meta["byline"],
        "words": meta["words"],
        "word_count_line": meta["word_count_line"],
        "header": meta["header"],
        "title_fraction": meta["title_fraction"],
        "scenes": meta["scenes"],
        "italics": meta["italics"],
        "fixes": meta["fixes"],
        "warnings": meta["warnings"],
        "output": str(args.output),
        "ok": meta["ok"],
        "problems": meta["problems"],
    }
    if args.json:
        print(json.dumps(public, ensure_ascii=False, indent=2))
    else:
        print(report(meta, bool(meta["ok"])))
        print(f"output: {args.output}")
        if meta["problems"]:
            print("\n".join(f"problem: {item}" for item in meta["problems"]))
    return 0 if meta["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
