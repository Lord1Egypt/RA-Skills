from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree

from .detect import split_formula_segments
from .math_parser import parse_formula
from .omml import M_NS, W_NS, node_to_omath, w_tag


etree.register_namespace("w", W_NS)
etree.register_namespace("m", M_NS)


XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
PROCESSABLE_PARTS = (
    "word/document.xml",
    "word/footnotes.xml",
    "word/endnotes.xml",
    "word/comments.xml",
)


@dataclass
class TransformStats:
    formulas_converted: int = 0
    paragraphs_skipped: int = 0
    runs_merged: int = 0
    parts_changed: list[str] = field(default_factory=list)
    samples: list[str] = field(default_factory=list)


def convert_docx_formulas(
    src: Path,
    dst: Path,
    *,
    skip_bibliography: bool = True,
) -> TransformStats:
    stats = TransformStats()
    dst.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(src, "r") as zin, ZipFile(dst, "w", ZIP_DEFLATED) as zout:
        names = zin.namelist()
        dynamic_parts = [
            name
            for name in names
            if name in PROCESSABLE_PARTS
            or name.startswith("word/header")
            or name.startswith("word/footer")
        ]
        changed_payloads: dict[str, bytes] = {}
        for name in dynamic_parts:
            try:
                root = etree.fromstring(zin.read(name))
            except etree.XMLSyntaxError:
                continue
            before = stats.formulas_converted
            _convert_part(root, stats, skip_bibliography=skip_bibliography)
            if stats.formulas_converted != before:
                stats.parts_changed.append(name)
                changed_payloads[name] = etree.tostring(
                    root,
                    xml_declaration=True,
                    encoding="UTF-8",
                    standalone=False,
                )
        for item in zin.infolist():
            payload = changed_payloads.get(item.filename)
            zout.writestr(item, payload if payload is not None else zin.read(item.filename))
    return stats


def _convert_part(
    root: etree._Element,
    stats: TransformStats,
    *,
    skip_bibliography: bool,
) -> None:
    stats.runs_merged += merge_adjacent_text_runs(root)
    _join_split_nary_scripts(root)
    in_bibliography = False
    for paragraph in root.xpath(".//w:p", namespaces={"w": W_NS}):
        paragraph_text = "".join(paragraph.xpath(".//w:t/text()", namespaces={"w": W_NS})).strip()
        if skip_bibliography and (
            in_bibliography
            or is_bibliography_heading(paragraph_text)
            or is_bibliography_entry(paragraph_text)
        ):
            in_bibliography = in_bibliography or is_bibliography_heading(paragraph_text)
            stats.paragraphs_skipped += 1
            continue
        _convert_paragraph(paragraph, stats)


def _convert_paragraph(paragraph: etree._Element, stats: TransformStats) -> None:
    for t in list(paragraph.xpath(".//w:t", namespaces={"w": W_NS})):
        run = t.getparent()
        if run is None or run.tag != w_tag("r"):
            continue
        text = t.text or ""
        parts = split_formula_segments(text)
        if not any(is_formula for _, is_formula in parts):
            continue
        if not _run_is_simple_text(run, t):
            continue
        parent = run.getparent()
        if parent is None:
            continue
        insert_at = parent.index(run)
        rpr = run.find(w_tag("rPr"))
        new_nodes = []
        for value, is_formula in parts:
            if is_formula:
                try:
                    omath = node_to_omath(parse_formula(value))
                except Exception:
                    new_nodes.append(_make_text_run(value, rpr))
                    continue
                new_nodes.append(omath)
                stats.formulas_converted += 1
                if len(stats.samples) < 20:
                    stats.samples.append(value)
            else:
                new_nodes.append(_make_text_run(value, rpr))
        parent.remove(run)
        for offset, node in enumerate(new_nodes):
            parent.insert(insert_at + offset, node)


def is_bibliography_heading(text: str) -> bool:
    normalized = re.sub(r"[\s:：.。．\[\]【】()（）]", "", text).lower()
    return normalized in {
        "参考文献",
        "参考资料",
        "references",
        "bibliography",
        "workscited",
    }


def is_bibliography_entry(text: str) -> bool:
    if not text:
        return False
    stripped = text.strip()
    if not re.match(r"^(\[\d+\]|\(\d+\)|\d+[.)、])\s*", stripped):
        return False
    reference_markers = (
        "doi.org/",
        "http://",
        "https://",
        "arxiv:",
        "[J]",
        "[M]",
        "[R]",
        "[G]",
        "[C]",
        "[EB/OL]",
        "Journal",
        "Press",
        "Review",
        "Econometrica",
        "University",
        "Working Paper",
    )
    return any(marker in stripped for marker in reference_markers)


def _run_is_simple_text(run: etree._Element, current_text: etree._Element) -> bool:
    for child in run:
        if child.tag == w_tag("rPr"):
            continue
        if child is current_text:
            continue
        return False
    return True


def merge_adjacent_text_runs(root: etree._Element) -> int:
    """Merge adjacent direct text runs with identical run properties.

    This is layout-neutral for simple text runs and greatly improves formula
    detection when Word or LibreOffice split one linear formula across runs.
    """
    merged = 0
    for paragraph in root.xpath(".//w:p", namespaces={"w": W_NS}):
        index = 0
        while index < len(paragraph) - 1:
            left = paragraph[index]
            right = paragraph[index + 1]
            if left.tag != w_tag("r") or right.tag != w_tag("r"):
                index += 1
                continue
            left_t = _single_text_child(left)
            right_t = _single_text_child(right)
            if left_t is None or right_t is None:
                index += 1
                continue
            if _run_properties_key(left) != _run_properties_key(right):
                index += 1
                continue
            left_t.text = (left_t.text or "") + (right_t.text or "")
            _set_space_preserve_if_needed(left_t)
            paragraph.remove(right)
            merged += 1
        # Do not advance after a merge; the new neighbor may also be mergeable.
            continue
    return merged


def _join_split_nary_scripts(root: etree._Element) -> None:
    """Repair common Word/LO run split: text ending in ∑ plus next run starting _i."""
    for paragraph in root.xpath(".//w:p", namespaces={"w": W_NS}):
        runs = paragraph.xpath("./w:r", namespaces={"w": W_NS})
        for left, right in zip(runs, runs[1:]):
            left_t = _single_text_child(left)
            right_t = _single_text_child(right)
            if left_t is None or right_t is None:
                continue
            left_text = left_t.text or ""
            right_text = right_t.text or ""
            if not left_text or not right_text:
                continue
            if left_text[-1] in {"∑", "∏"} and right_text[0] in {"_", "^"}:
                left_t.text = left_text[:-1]
                right_t.text = left_text[-1] + right_text


def _single_text_child(run: etree._Element) -> etree._Element | None:
    text_children = [child for child in run if child.tag == w_tag("t")]
    non_text_children = [
        child for child in run if child.tag not in {w_tag("rPr"), w_tag("t")}
    ]
    if len(text_children) != 1 or non_text_children:
        return None
    return text_children[0]


def _run_properties_key(run: etree._Element) -> bytes:
    rpr = run.find(w_tag("rPr"))
    if rpr is None:
        return b""
    return etree.tostring(rpr, with_tail=False)


def _set_space_preserve_if_needed(t: etree._Element) -> None:
    text = t.text or ""
    if text[:1].isspace() or text[-1:].isspace():
        t.set(XML_SPACE, "preserve")
    elif XML_SPACE in t.attrib:
        del t.attrib[XML_SPACE]


def _make_text_run(text: str, rpr: etree._Element | None) -> etree._Element:
    run = etree.Element(w_tag("r"))
    if rpr is not None:
        run.append(deepcopy(rpr))
    t = etree.SubElement(run, w_tag("t"))
    if text[:1].isspace() or text[-1:].isspace():
        t.set(XML_SPACE, "preserve")
    t.text = text
    return run
