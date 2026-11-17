#!/usr/bin/env python3
"""Create a basic editable DOCX from UTF-8 Markdown using only stdlib."""

from __future__ import annotations

import argparse
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def run_xml(text: str, bold: bool = False, size: int = 22) -> str:
    props = [
        '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
        'w:eastAsia="宋体"/>',
        f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>',
    ]
    if bold:
        props.append("<w:b/>")
    preserved = ' xml:space="preserve"' if text[:1].isspace() or text[-1:].isspace() else ""
    return f"<w:r><w:rPr>{''.join(props)}</w:rPr><w:t{preserved}>{escape(text)}</w:t></w:r>"


def inline_runs(text: str, size: int = 22) -> str:
    parts = re.split(r"(\*\*.+?\*\*)", text)
    output = []
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            output.append(run_xml(part[2:-2], bold=True, size=size))
        elif part:
            output.append(run_xml(part, size=size))
    return "".join(output)


def paragraph(text: str, style: str | None = None, before: int = 0, after: int = 120) -> str:
    ppr = [f'<w:spacing w:before="{before}" w:after="{after}" w:line="360" w:lineRule="auto"/>']
    if style:
        ppr.insert(0, f'<w:pStyle w:val="{style}"/>')
    if not style:
        ppr.append('<w:ind w:firstLine="480"/>')
        ppr.append('<w:jc w:val="both"/>')
    return f"<w:p><w:pPr>{''.join(ppr)}</w:pPr>{inline_runs(text)}</w:p>"


def heading(text: str, level: int) -> str:
    style = "Title" if level == 1 else f"Heading{min(level - 1, 3)}"
    return paragraph(text, style=style, before=160, after=120)


def bullet(text: str) -> str:
    ppr = (
        '<w:spacing w:after="60" w:line="320" w:lineRule="auto"/>'
        '<w:ind w:left="480" w:hanging="240"/>'
    )
    return f"<w:p><w:pPr>{ppr}</w:pPr>{run_xml('•  ')}{inline_runs(text)}</w:p>"


def table(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    width = max(len(row) for row in rows)
    normalized = [row + [""] * (width - len(row)) for row in rows]
    borders = (
        "<w:tblBorders>"
        '<w:top w:val="single" w:sz="4" w:color="808080"/>'
        '<w:left w:val="single" w:sz="4" w:color="808080"/>'
        '<w:bottom w:val="single" w:sz="4" w:color="808080"/>'
        '<w:right w:val="single" w:sz="4" w:color="808080"/>'
        '<w:insideH w:val="single" w:sz="4" w:color="BFBFBF"/>'
        '<w:insideV w:val="single" w:sz="4" w:color="BFBFBF"/>'
        "</w:tblBorders>"
    )
    xml_rows = []
    for row_index, row in enumerate(normalized):
        cells = []
        for cell in row:
            shade = '<w:shd w:fill="E7EEF8"/>' if row_index == 0 else ""
            content = inline_runs(cell.strip(), size=20)
            cells.append(
                f"<w:tc><w:tcPr>{shade}<w:tcMar>"
                '<w:top w:w="80" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
                '<w:bottom w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/>'
                f"</w:tcMar></w:tcPr><w:p>{content}</w:p></w:tc>"
            )
        xml_rows.append(f"<w:tr>{''.join(cells)}</w:tr>")
    return f"<w:tbl><w:tblPr><w:tblW w:w=\"0\" w:type=\"auto\"/>{borders}</w:tblPr>{''.join(xml_rows)}</w:tbl>"


def parse_markdown(text: str) -> list[str]:
    blocks: list[str] = []
    lines = text.replace("\r\n", "\n").split("\n")
    i = 0
    paragraph_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph_lines:
            content = " ".join(item.strip() for item in paragraph_lines if item.strip())
            if content:
                blocks.append(paragraph(content))
            paragraph_lines.clear()

    while i < len(lines):
        line = lines[i].rstrip()
        if re.match(r"^\|.*\|$", line):
            flush_paragraph()
            table_lines = []
            while i < len(lines) and re.match(r"^\|.*\|$", lines[i].rstrip()):
                table_lines.append(lines[i].strip())
                i += 1
            parsed = [[cell.strip() for cell in item.strip("|").split("|")] for item in table_lines]
            if len(parsed) > 1 and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in parsed[1]):
                parsed.pop(1)
            blocks.append(table(parsed))
            continue
        match = re.match(r"^(#{1,4})\s+(.+)$", line)
        if match:
            flush_paragraph()
            blocks.append(heading(match.group(2).strip(), len(match.group(1))))
        elif re.match(r"^\s*[-*]\s+", line):
            flush_paragraph()
            blocks.append(bullet(re.sub(r"^\s*[-*]\s+", "", line)))
        elif not line.strip():
            flush_paragraph()
        else:
            paragraph_lines.append(line)
        i += 1
    flush_paragraph()
    return blocks


def styles_xml() -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{W_NS}">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="宋体"/><w:sz w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="240" w:after="240"/></w:pPr>
    <w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="黑体"/><w:sz w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:pPr><w:keepNext/><w:outlineLvl w:val="0"/></w:pPr>
    <w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="黑体"/><w:sz w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:pPr><w:keepNext/><w:outlineLvl w:val="1"/></w:pPr>
    <w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="黑体"/><w:sz w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:pPr><w:keepNext/><w:outlineLvl w:val="2"/></w:pPr>
    <w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="黑体"/><w:sz w:val="22"/></w:rPr>
  </w:style>
</w:styles>'''


def create_docx(markdown: str, output: Path, title: str | None) -> None:
    blocks = parse_markdown(markdown)
    if title and not markdown.lstrip().startswith("# "):
        blocks.insert(0, heading(title, 1))
    body = "".join(blocks)
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{W_NS}">
  <w:body>{body}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''
    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''
    doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    core = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{escape(title or output.stem)}</dc:title>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''
    app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>OpenClaw Literature Review Skill</Application>
</Properties>'''
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", root_rels)
        archive.writestr("word/document.xml", document)
        archive.writestr("word/styles.xml", styles_xml())
        archive.writestr("word/_rels/document.xml.rels", doc_rels)
        archive.writestr("docProps/core.xml", core)
        archive.writestr("docProps/app.xml", app)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 Markdown input")
    parser.add_argument("output", type=Path, help="DOCX output path")
    parser.add_argument("--title", help="Document title when Markdown has no H1")
    args = parser.parse_args()
    if args.output.suffix.lower() != ".docx":
        parser.error("output must end with .docx")
    markdown = args.input.read_text(encoding="utf-8")
    create_docx(markdown, args.output, args.title)
    if not args.output.is_file() or args.output.stat().st_size == 0:
        raise SystemExit("DOCX creation failed")
    with zipfile.ZipFile(args.output) as archive:
        required = {"[Content_Types].xml", "_rels/.rels", "word/document.xml", "word/styles.xml"}
        missing = required.difference(archive.namelist())
        if missing:
            raise SystemExit(f"Invalid DOCX; missing: {sorted(missing)}")
    print(args.output.resolve())


if __name__ == "__main__":
    main()
