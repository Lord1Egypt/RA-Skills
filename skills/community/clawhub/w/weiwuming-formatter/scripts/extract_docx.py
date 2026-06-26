#!/usr/bin/env python3
"""
Extract structured content from Word documents for WeChat article formatting.

This extractor follows the minimax-docx style: detect the container by file
signature, normalize legacy .doc through LibreOffice when possible, and read
.docx as an OOXML ZIP package using Python standard-library XML tools.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "v": "urn:schemas-microsoft-com:vml",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}

ZIP_SIGNATURE = b"PK\x03\x04"
OLE_SIGNATURE = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"


def qn(name: str) -> str:
    prefix, local = name.split(":", 1)
    return f"{{{NS[prefix]}}}{local}"


def detect_container(path: Path) -> str:
    with path.open("rb") as f:
        signature = f.read(8)
    if signature.startswith(ZIP_SIGNATURE):
        return "docx"
    if signature == OLE_SIGNATURE:
        return "doc"
    return "unknown"


def convert_doc_to_docx(path: Path, out_dir: Path) -> Path:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        raise RuntimeError("Legacy .doc input requires LibreOffice/soffice to convert to .docx.")
    subprocess.run(
        [soffice, "--headless", "--convert-to", "docx", "--outdir", str(out_dir), str(path)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    converted = out_dir / f"{path.stem}.docx"
    if not converted.exists():
        matches = list(out_dir.glob("*.docx"))
        if not matches:
            raise RuntimeError("LibreOffice conversion completed but no .docx file was produced.")
        converted = matches[0]
    return converted


def read_xml(zf: zipfile.ZipFile, name: str) -> ET.Element | None:
    try:
        return ET.fromstring(zf.read(name))
    except KeyError:
        return None


def relationship_part_for(part_name: str) -> str:
    part = Path(part_name)
    return str(part.parent / "_rels" / f"{part.name}.rels").replace("\\", "/")


def load_relationships(zf: zipfile.ZipFile, part_name: str) -> dict[str, dict[str, str]]:
    root = read_xml(zf, relationship_part_for(part_name))
    if root is None:
        return {}
    rels: dict[str, dict[str, str]] = {}
    base = Path(part_name).parent
    for rel in root.findall("rel:Relationship", NS):
        rel_id = rel.attrib.get("Id")
        target = rel.attrib.get("Target", "")
        if not rel_id:
            continue
        if target and not target.startswith(("http://", "https://", "/")):
            target = str((base / target).as_posix())
        rels[rel_id] = {
            "type": rel.attrib.get("Type", ""),
            "target": target,
            "target_mode": rel.attrib.get("TargetMode", "Internal"),
        }
    return rels


def load_styles(zf: zipfile.ZipFile) -> dict[str, dict[str, str]]:
    root = read_xml(zf, "word/styles.xml")
    if root is None:
        return {}
    styles: dict[str, dict[str, str]] = {}
    for style in root.findall("w:style", NS):
        style_id = style.attrib.get(qn("w:styleId"))
        if not style_id:
            continue
        name = style.find("w:name", NS)
        styles[style_id] = {
            "id": style_id,
            "name": name.attrib.get(qn("w:val"), style_id) if name is not None else style_id,
            "type": style.attrib.get(qn("w:type"), ""),
        }
    return styles


def style_name(style_id: str, styles: dict[str, dict[str, str]]) -> str:
    return styles.get(style_id, {}).get("name", style_id) if style_id else ""


def paragraph_style_id(p: ET.Element) -> str:
    p_style = p.find("./w:pPr/w:pStyle", NS)
    return p_style.attrib.get(qn("w:val"), "") if p_style is not None else ""


def paragraph_alignment(p: ET.Element) -> str:
    jc = p.find("./w:pPr/w:jc", NS)
    if jc is None:
        return "left"
    val = jc.attrib.get(qn("w:val"), "left")
    return {"center": "center", "right": "right", "both": "justify", "distribute": "justify"}.get(val, "left")


def has_prop(run: ET.Element, prop_name: str) -> bool:
    return run.find(f"./w:rPr/{prop_name}", NS) is not None


def run_font_size(run: ET.Element) -> float | None:
    size = run.find("./w:rPr/w:sz", NS)
    if size is None:
        return None
    val = size.attrib.get(qn("w:val"))
    return int(val) / 2 if val and val.isdigit() else None


def extract_run_text(run: ET.Element) -> str:
    chunks: list[str] = []
    for child in list(run):
        if child.tag == qn("w:t"):
            chunks.append(child.text or "")
        elif child.tag == qn("w:tab"):
            chunks.append("\t")
        elif child.tag in {qn("w:br"), qn("w:cr")}:
            chunks.append("\n")
        elif child.tag == qn("w:noBreakHyphen"):
            chunks.append("-")
    return "".join(chunks)


def extract_images_from_node(node: ET.Element, rels: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    images: list[dict[str, Any]] = []
    for blip in node.findall(".//a:blip", NS):
        rel_id = blip.attrib.get(qn("r:embed")) or blip.attrib.get(qn("r:link"))
        if rel_id:
            rel = rels.get(rel_id, {})
            images.append({"rel_id": rel_id, "target": rel.get("target", ""), "needs_hosted_url": True})
    for image in node.findall(".//v:imagedata", NS):
        rel_id = image.attrib.get(qn("r:id"))
        if rel_id:
            rel = rels.get(rel_id, {})
            images.append({"rel_id": rel_id, "target": rel.get("target", ""), "needs_hosted_url": True})
    return images


def paragraph_runs(p: ET.Element) -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    for r in p.findall("./w:r", NS):
        text = extract_run_text(r)
        if text:
            runs.append({"text": text, "bold": has_prop(r, "w:b"), "italic": has_prop(r, "w:i"), "font_size": run_font_size(r)})
    return runs


def classify_text(text: str, style: str, alignment: str, runs: list[dict[str, Any]]) -> str:
    if not text:
        return "empty"
    style_l = style.lower()
    if "heading" in style_l or "标题" in style:
        return "heading"
    if "toc" in style_l or "目录" in style:
        return "toc_entry"
    if "quote" in style_l or "引用" in style or text.startswith(">"):
        return "quote"
    if "caption" in style_l or "题注" in style:
        return "caption"
    if re.match(r"^[\s.\-—–·•*]+$", text):
        return "divider"
    if re.search(r"(编者按|编者注|Editor's note)", text, re.I):
        return "editor_note"
    if re.search(r"^[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]", text):
        return "note_entry"
    if re.search(r"\^[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]", text):
        return "paragraph_with_note_ref"
    if re.match(r"^(编辑|审校|校对|排版|设计|美工|责编|主编)[：:]", text):
        return "staff"
    if re.search(r"《[^》]+》|『[^』]+』", text):
        return "book_or_title_reference"
    non_empty_runs = [r for r in runs if r["text"].strip()]
    if alignment == "center" and non_empty_runs and all(r.get("bold") for r in non_empty_runs) and len(text) <= 80:
        return "subheading"
    return "paragraph"


def heading_level(style_id: str, style: str) -> int | None:
    for candidate in (style_id, style):
        match = re.search(r"(?:Heading|标题)\s*(\d+)", candidate, re.I)
        if match:
            return int(match.group(1))
    return None


def parse_paragraph(p: ET.Element, index: int, styles: dict[str, dict[str, str]], rels: dict[str, dict[str, str]]) -> dict[str, Any]:
    style_id = paragraph_style_id(p)
    style = style_name(style_id, styles)
    alignment = paragraph_alignment(p)
    runs = paragraph_runs(p)
    text = "".join(run["text"] for run in runs).strip()
    item: dict[str, Any] = {
        "type": classify_text(text, style, alignment, runs),
        "index": index,
        "text": text,
        "style_id": style_id,
        "style_name": style,
        "alignment": alignment,
        "runs": runs,
        "images": extract_images_from_node(p, rels),
    }
    level = heading_level(style_id, style)
    if level is not None:
        item["level"] = level
    return item


def parse_table(table: ET.Element, index: int, styles: dict[str, dict[str, str]], rels: dict[str, dict[str, str]]) -> dict[str, Any]:
    rows: list[list[str]] = []
    cells: list[list[list[dict[str, Any]]]] = []
    para_index = 0
    for tr in table.findall("./w:tr", NS):
        row_text: list[str] = []
        row_cells: list[list[dict[str, Any]]] = []
        for tc in tr.findall("./w:tc", NS):
            paras = [parse_paragraph(p, para_index + i, styles, rels) for i, p in enumerate(tc.findall("./w:p", NS))]
            para_index += len(paras)
            row_cells.append(paras)
            row_text.append("\n".join(p["text"] for p in paras if p["text"]).strip())
        rows.append(row_text)
        cells.append(row_cells)
    return {"type": "table", "index": index, "rows": rows, "cells": cells}


def parse_notes(zf: zipfile.ZipFile, part_name: str) -> list[dict[str, str]]:
    root = read_xml(zf, part_name)
    if root is None:
        return []
    tag_name = "footnote" if "footnotes" in part_name else "endnote"
    notes: list[dict[str, str]] = []
    for note in root.findall(f"w:{tag_name}", NS):
        note_id = note.attrib.get(qn("w:id"), "")
        if note_id.startswith("-"):
            continue
        text = "".join(t.text or "" for t in note.findall(".//w:t", NS)).strip()
        if text:
            notes.append({"id": note_id, "text": text})
    return notes


def parse_document(path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(path) as zf:
        document = read_xml(zf, "word/document.xml")
        if document is None:
            raise RuntimeError("word/document.xml not found; this is not a valid .docx package.")
        styles = load_styles(zf)
        rels = load_relationships(zf, "word/document.xml")
        body = document.find("w:body", NS)
        if body is None:
            raise RuntimeError("word/document.xml has no body.")
        content: list[dict[str, Any]] = []
        paragraphs: list[dict[str, Any]] = []
        tables: list[dict[str, Any]] = []
        images_in_flow: list[dict[str, Any]] = []
        for index, child in enumerate(list(body)):
            if child.tag == qn("w:p"):
                item = parse_paragraph(child, index, styles, rels)
                content.append(item)
                paragraphs.append(item)
                images_in_flow.extend(item["images"])
            elif child.tag == qn("w:tbl"):
                item = parse_table(child, index, styles, rels)
                content.append(item)
                tables.append(item)
                for row in item["cells"]:
                    for cell in row:
                        for para in cell:
                            images_in_flow.extend(para["images"])
        package_images = [
            {"rel_id": rel_id, "target": rel.get("target", ""), "needs_hosted_url": True}
            for rel_id, rel in rels.items()
            if "image" in rel.get("type", "")
        ]
        return {
            "filename": path.name,
            "content_count": len(content),
            "paragraph_count": len(paragraphs),
            "table_count": len(tables),
            "image_count": len(package_images),
            "content": content,
            "paragraphs": paragraphs,
            "tables": tables,
            "images": package_images,
            "images_in_flow": images_in_flow,
            "footnotes": parse_notes(zf, "word/footnotes.xml"),
            "endnotes": parse_notes(zf, "word/endnotes.xml"),
        }


def extract_word_structure(input_path: Path) -> dict[str, Any]:
    container = detect_container(input_path)
    if container == "unknown":
        raise RuntimeError("Unsupported file signature. Provide a valid .docx or legacy .doc file.")
    if container == "docx":
        result = parse_document(input_path)
        result["source_format"] = "docx"
        result["normalized_from_doc"] = False
        return result
    with tempfile.TemporaryDirectory(prefix="wechat_formatter_doc_") as tmp:
        converted = convert_doc_to_docx(input_path, Path(tmp))
        result = parse_document(converted)
        result["source_format"] = "doc"
        result["normalized_from_doc"] = True
        result["normalized_filename"] = converted.name
        result["conversion_note"] = "Legacy .doc was converted to .docx for OOXML extraction."
        return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract structured content from .docx/.doc files.")
    parser.add_argument("file", help="Input .docx or .doc file")
    args = parser.parse_args()
    input_path = Path(args.file)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        return 1
    try:
        result = extract_word_structure(input_path)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
