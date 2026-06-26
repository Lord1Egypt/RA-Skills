from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET

if sys.platform == "win32":
    import winreg


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}
BUNDLE_PATH = Path(__file__).resolve().parent.parent / "assets" / "template-bundle.json"

CORE_FONTS = [
    "方正小标宋简体",
    "仿宋_GB2312",
    "黑体",
    "楷体_GB2312",
    "宋体",
    "Times New Roman",
]

FONT_ALIASES = {
    "方正小标宋简体": {"方正小标宋简体", "fzxiaobiaosong-b05s", "fzxiaobiaosong"},
    "仿宋_GB2312": {"仿宋_gb2312", "仿宋", "fangsong", "fangsong_gb2312", "华文仿宋", "fangsong"},
    "黑体": {"黑体", "simhei"},
    "楷体_GB2312": {"楷体_gb2312", "楷体", "kaiti", "kaiti_gb2312", "华文楷体"},
    "宋体": {"宋体", "simsun", "nsimsun", "华文宋体"},
    "Times New Roman": {"timesnewroman", "timesnewromanregular", "times new roman"},
}

KIND_RULES = {
    "title": {"font": "方正小标宋简体", "size": 44, "jc": "center", "indent": False, "bold": False},
    "body": {"font": "仿宋_GB2312", "size": 32, "jc": "both", "indent": True, "bold": False},
    "heading1": {"font": "黑体", "size": 32, "jc": "left", "indent": False, "bold": False},
    "heading2": {"font": "楷体_GB2312", "size": 32, "jc": "left", "indent": False, "bold": False},
    "heading3": {"font": "仿宋_GB2312", "size": 32, "jc": "left", "indent": False, "bold": True},
    "heading4": {"font": "仿宋_GB2312", "size": 32, "jc": "left", "indent": False, "bold": False},
    "attachment": {"font": "黑体", "size": 32, "jc": "left", "indent": False, "bold": False},
    "signature": {"font": "仿宋_GB2312", "size": 32, "jc": "center", "indent": False, "bold": False},
    "date": {"font": "仿宋_GB2312", "size": 32, "jc": "center", "indent": False, "bold": False},
    "table_header": {"font": "黑体", "size": 28, "jc": "center", "indent": False, "bold": False},
    "table_body": {"font": "仿宋_GB2312", "size": 28, "jc": "left", "indent": False, "bold": False},
}


def qn(tag: str) -> str:
    return f"{{{W_NS}}}{tag}"


def normalize_font_name(name: str) -> str:
    cleaned = name.strip().lower()
    cleaned = re.sub(r"\(truetype\)", "", cleaned)
    cleaned = cleaned.replace(" ", "").replace("_", "").replace("-", "")
    return cleaned


def split_font_variants(name: str) -> Iterable[str]:
    stripped = re.sub(r"\(.*?\)", "", name)
    for piece in re.split(r"[,&/]", stripped):
        piece = piece.strip()
        if piece:
            yield piece


def enumerate_installed_fonts() -> set[str]:
    fonts: set[str] = set()
    if sys.platform != "win32":
        return fonts

    registry_paths = [
        r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts",
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Fonts",
    ]
    for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        for reg_path in registry_paths:
            try:
                key = winreg.OpenKey(hive, reg_path)
            except OSError:
                continue
            index = 0
            while True:
                try:
                    value_name, _, _ = winreg.EnumValue(key, index)
                except OSError:
                    break
                for variant in split_font_variants(value_name):
                    fonts.add(normalize_font_name(variant))
                index += 1
            winreg.CloseKey(key)

    font_dir = Path(r"C:\Windows\Fonts")
    if font_dir.exists():
        for item in font_dir.iterdir():
            if item.is_file():
                fonts.add(normalize_font_name(item.stem))
    return fonts


def find_missing_fonts(installed_fonts: set[str]) -> list[str]:
    missing = []
    for font_name in CORE_FONTS:
        aliases = {normalize_font_name(font_name)}
        aliases.update(normalize_font_name(alias) for alias in FONT_ALIASES.get(font_name, set()))
        if aliases.isdisjoint(installed_fonts):
            missing.append(font_name)
    return missing


def read_zip_entries(docx_path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(docx_path, "r") as archive:
        return {name: archive.read(name) for name in archive.namelist()}


def load_template_bundle(bundle_path: Path) -> dict[str, str]:
    return json.loads(bundle_path.read_text(encoding="utf-8"))


def get_xml(entries: dict[str, bytes], name: str) -> ET.Element:
    try:
        return ET.fromstring(entries[name])
    except KeyError as exc:
        raise ValueError(f"Missing OOXML part: {name}") from exc


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join((text_node.text or "") for text_node in paragraph.findall(".//w:t", NS)).strip()


def looks_like_title_line(text: str) -> bool:
    if not text or len(text) > 28:
        return False
    if re.search(r"[。！？；：:]", text):
        return False
    if re.match(r"^(附件\d*|[一二三四五六七八九十]+、|（[一二三四五六七八九十]+）|\d+[\.、]|（\d+）)", text):
        return False
    return True


def classify_paragraph(text: str, state: dict[str, object]) -> str:
    if not text:
        return "body"
    if re.fullmatch(r"附件\d*", text):
        state["body_started"] = True
        return "attachment"
    if re.fullmatch(r"（\d{4}年\d{1,2}月\d{1,2}日）", text):
        return "date"
    if re.match(r"^[一二三四五六七八九十]+、", text):
        state["body_started"] = True
        return "heading1"
    if re.match(r"^（[一二三四五六七八九十]+）", text):
        state["body_started"] = True
        return "heading2"
    if re.match(r"^\d+[\.．、]", text):
        state["body_started"] = True
        return "heading3"
    if re.match(r"^（\d+）", text):
        state["body_started"] = True
        return "heading4"

    if not state["body_started"]:
        if looks_like_title_line(text):
            state["title_lines"] = int(state["title_lines"]) + 1
            return "title"
        if int(state["title_lines"]) > 0 and len(text) <= 40:
            return "signature"

    state["body_started"] = True
    return "body"


def clear_children(parent: ET.Element, tag_names: set[str]) -> None:
    for child in list(parent):
        local_name = child.tag.split("}", 1)[-1]
        if local_name in tag_names:
            parent.remove(child)


def set_paragraph_properties(paragraph: ET.Element, kind: str) -> None:
    rule = KIND_RULES[kind]
    p_pr = paragraph.find("w:pPr", NS)
    if p_pr is None:
        p_pr = ET.Element(qn("pPr"))
        paragraph.insert(0, p_pr)
    else:
        clear_children(p_pr, {"ind", "jc", "spacing"})

    spacing = ET.SubElement(p_pr, qn("spacing"))
    spacing.set(qn("before"), "0")
    spacing.set(qn("after"), "0")
    spacing.set(qn("line"), "560")
    spacing.set(qn("lineRule"), "exact")

    if rule["indent"]:
        ind = ET.SubElement(p_pr, qn("ind"))
        ind.set(qn("firstLineChars"), "200")

    jc = ET.SubElement(p_pr, qn("jc"))
    jc.set(qn("val"), str(rule["jc"]))


def set_run_style(run: ET.Element, kind: str) -> None:
    text = "".join((node.text or "") for node in run.findall(".//w:t", NS)).strip()
    rule = KIND_RULES[kind]
    font_name = rule["font"]
    if kind == "body" and re.fullmatch(r"[（(].*[)）]", text):
        font_name = "楷体_GB2312"
    ascii_font = "Times New Roman" if re.search(r"\d", text) else font_name

    r_pr = run.find("w:rPr", NS)
    if r_pr is None:
        r_pr = ET.Element(qn("rPr"))
        run.insert(0, r_pr)
    else:
        clear_children(r_pr, {"rFonts", "b", "bCs", "sz", "szCs", "color", "highlight", "spacing", "kern", "lang"})

    r_fonts = ET.SubElement(r_pr, qn("rFonts"))
    r_fonts.set(qn("ascii"), ascii_font)
    r_fonts.set(qn("hAnsi"), ascii_font)
    r_fonts.set(qn("eastAsia"), font_name)
    r_fonts.set(qn("cs"), ascii_font)

    if rule["bold"]:
        ET.SubElement(r_pr, qn("b"))
        ET.SubElement(r_pr, qn("bCs"))

    size = ET.SubElement(r_pr, qn("sz"))
    size.set(qn("val"), str(rule["size"]))
    size_cs = ET.SubElement(r_pr, qn("szCs"))
    size_cs.set(qn("val"), str(rule["size"]))


def format_paragraph(paragraph: ET.Element, kind: str) -> None:
    set_paragraph_properties(paragraph, kind)
    for run in paragraph.findall(".//w:r", NS):
        set_run_style(run, kind)


def set_table_borders(table: ET.Element) -> None:
    tbl_pr = table.find("w:tblPr", NS)
    if tbl_pr is None:
        tbl_pr = ET.Element(qn("tblPr"))
        table.insert(0, tbl_pr)
    clear_children(tbl_pr, {"tblBorders"})
    borders = ET.SubElement(tbl_pr, qn("tblBorders"))
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        border = ET.SubElement(borders, qn(edge))
        border.set(qn("val"), "single")
        border.set(qn("sz"), "8")
        border.set(qn("space"), "0")
        border.set(qn("color"), "000000")


def format_table(table: ET.Element) -> None:
    set_table_borders(table)
    rows = table.findall("w:tr", NS)
    for row_index, row in enumerate(rows):
        kind = "table_header" if row_index == 0 else "table_body"
        for paragraph in row.findall(".//w:p", NS):
            format_paragraph(paragraph, kind)


def rebuild_document_xml(source_entries: dict[str, bytes], template_bundle: dict[str, str]) -> bytes:
    source_root = get_xml(source_entries, "word/document.xml")
    source_body = source_root.find("w:body", NS)
    if source_body is None:
        raise ValueError("document.xml is missing w:body")

    state: dict[str, object] = {"body_started": False, "title_lines": 0}
    for child in list(source_body):
        local_name = child.tag.split("}", 1)[-1]
        if local_name == "sectPr":
            source_body.remove(child)
            continue
        if local_name == "p":
            text = paragraph_text(child)
            format_paragraph(child, classify_paragraph(text, state))
        elif local_name == "tbl":
            format_table(child)

    sect_xml = template_bundle.get("word/sectPr.xml", "")
    if sect_xml:
        source_body.append(ET.fromstring(sect_xml))

    return ET.tostring(source_root, encoding="utf-8", xml_declaration=True)


def convert(input_path: Path, output_path: Path, bundle_path: Path) -> list[str]:
    installed_fonts = enumerate_installed_fonts()
    missing_fonts = find_missing_fonts(installed_fonts)
    if missing_fonts:
        return missing_fonts

    source_entries = read_zip_entries(input_path)
    template_bundle = load_template_bundle(bundle_path)
    source_entries["word/document.xml"] = rebuild_document_xml(source_entries, template_bundle)

    for part_name in ("word/styles.xml", "word/settings.xml", "word/fontTable.xml", "word/theme/theme1.xml"):
        content = template_bundle.get(part_name)
        if content is not None:
            source_entries[part_name] = content.encode("utf-8")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, payload in source_entries.items():
            archive.writestr(name, payload)
    return []


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a DOCX into the OpenClaw house style.")
    parser.add_argument("--input", required=True, type=Path, help="Source DOCX path.")
    parser.add_argument("--output", required=True, type=Path, help="Output DOCX path.")
    parser.add_argument("--bundle", type=Path, default=BUNDLE_PATH, help="Template bundle JSON path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.input.suffix.lower() != ".docx":
        print("ERROR: input must be a .docx file", file=sys.stderr)
        return 1
    if not args.input.exists():
        print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
        return 1
    if not args.bundle.exists():
        print(f"ERROR: template bundle not found: {args.bundle}", file=sys.stderr)
        return 1

    try:
        missing_fonts = convert(args.input, args.output, args.bundle)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if missing_fonts:
        print("MISSING_FONTS: " + ", ".join(missing_fonts), file=sys.stderr)
        return 2

    print(f"OK: wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
