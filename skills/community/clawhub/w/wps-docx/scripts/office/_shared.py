from __future__ import annotations

import shutil
import uuid
import zipfile
from pathlib import Path

from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
MC_NS = "http://schemas.openxmlformats.org/markup-compatibility/2006"
W15_NS = "http://schemas.microsoft.com/office/word/2012/wordml"
XML_NS = "http://www.w3.org/XML/1998/namespace"

NAMESPACES = {
    "w": W_NS,
    "r": R_NS,
    "rel": REL_NS,
    "ct": CT_NS,
    "mc": MC_NS,
    "w15": W15_NS,
    "xml": XML_NS,
}

COMMENTS_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"
COMMENTS_EXTENDED_CONTENT_TYPE = "application/vnd.ms-word.commentsExtended+xml"
COMMENTS_REL_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments"
COMMENTS_EXTENDED_REL_TYPE = "http://schemas.microsoft.com/office/2011/relationships/commentsExtended"

XML_FILES_TO_PRETTY_PRINT = {
    "[Content_Types].xml",
    "word/document.xml",
    "word/comments.xml",
    "word/commentsExtended.xml",
    "word/settings.xml",
    "word/styles.xml",
}


def qn(prefix: str, local_name: str) -> str:
    return f"{{{NAMESPACES[prefix]}}}{local_name}"


def local_name(tag: str) -> str:
    if not isinstance(tag, str):
        return ""
    return tag.split("}", 1)[1] if tag.startswith("{") else tag


def read_xml(path: Path):
    parser = etree.XMLParser(remove_blank_text=True, recover=True)
    return etree.fromstring(path.read_bytes(), parser=parser)


def write_xml(path: Path, root, pretty: bool = False) -> None:
    path.write_bytes(
        etree.tostring(
            root,
            encoding="UTF-8",
            xml_declaration=True,
            pretty_print=pretty,
        )
    )


def iter_word_xml_files(base_dir: Path):
    word_dir = base_dir / "word"
    if not word_dir.exists():
        return []
    return sorted(
        path
        for path in word_dir.rglob("*.xml")
        if "_rels" not in path.parts
    )


def unzip_docx(input_docx: Path, output_dir: Path) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(input_docx, "r") as archive:
        archive.extractall(output_dir)


def zip_dir(source_dir: Path, output_docx: Path) -> None:
    output_docx.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_docx, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source_dir).as_posix())


def ensure_content_type_override(content_types_path: Path, part_name: str, content_type: str) -> None:
    if content_types_path.exists():
        root = read_xml(content_types_path)
    else:
        root = etree.Element(qn("ct", "Types"), nsmap={None: CT_NS})

    for override in root.findall(qn("ct", "Override")):
        if override.get("PartName") == part_name:
            override.set("ContentType", content_type)
            write_xml(content_types_path, root)
            return

    override = etree.SubElement(root, qn("ct", "Override"))
    override.set("PartName", part_name)
    override.set("ContentType", content_type)
    write_xml(content_types_path, root)


def ensure_relationship(rels_path: Path, rel_type: str, target: str) -> str:
    if rels_path.exists():
        root = read_xml(rels_path)
    else:
        rels_path.parent.mkdir(parents=True, exist_ok=True)
        root = etree.Element(qn("rel", "Relationships"), nsmap={None: REL_NS})

    for rel in root.findall(qn("rel", "Relationship")):
        if rel.get("Type") == rel_type and rel.get("Target") == target:
            write_xml(rels_path, root)
            return rel.get("Id") or ""

    max_id = 0
    for rel in root.findall(qn("rel", "Relationship")):
        rel_id = rel.get("Id") or ""
        if rel_id.startswith("rId") and rel_id[3:].isdigit():
            max_id = max(max_id, int(rel_id[3:]))

    new_id = f"rId{max_id + 1}"
    rel = etree.SubElement(root, qn("rel", "Relationship"))
    rel.set("Id", new_id)
    rel.set("Type", rel_type)
    rel.set("Target", target)
    write_xml(rels_path, root)
    return new_id


def next_numeric_id(existing_values: list[int]) -> int:
    return (max(existing_values) + 1) if existing_values else 0


def new_para_id() -> str:
    return uuid.uuid4().hex[:8].upper()
