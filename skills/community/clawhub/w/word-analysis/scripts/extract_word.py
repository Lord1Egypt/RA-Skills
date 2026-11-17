#!/usr/bin/env python3
import json
import os
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

MAX_ARCHIVE_ENTRIES = 500
MAX_ARCHIVE_BYTES = 32 * 1024 * 1024
MAX_ENTRY_BYTES = 8 * 1024 * 1024
MAX_COMPRESSION_RATIO = 100
MAX_SEGMENTS = 2000
MAX_CHARACTERS = 120000


def reject(message: str) -> None:
    raise SystemExit(message)


def validate_archive(archive: zipfile.ZipFile) -> None:
    infos = archive.infolist()
    if len(infos) > MAX_ARCHIVE_ENTRIES:
        raise ValueError("too many entries")
    if len({info.filename for info in infos}) != len(infos):
        raise ValueError("duplicate entries")

    total = 0
    for info in infos:
        if info.flag_bits & 0x1:
            raise ValueError("encrypted entry")
        total += info.file_size
        if info.file_size > MAX_ENTRY_BYTES or total > MAX_ARCHIVE_BYTES:
            raise ValueError("expanded archive too large")
        if info.file_size and info.file_size / max(1, info.compress_size) > MAX_COMPRESSION_RATIO:
            raise ValueError("unsafe compression ratio")


if len(sys.argv) != 2:
    reject("用法: extract_word.py FILE.docx")
path = sys.argv[1]
if not os.path.isfile(path) or os.path.getsize(path) > 10 * 1024 * 1024:
    reject("DOCX 不存在或超过 10 MB。")

try:
    with zipfile.ZipFile(path) as archive:
        validate_archive(archive)
        if "word/document.xml" not in archive.namelist():
            raise ValueError("missing document")
        raw = archive.read("word/document.xml")
    root = ET.fromstring(raw)
except (ET.ParseError, KeyError, OSError, ValueError, zipfile.BadZipFile, zipfile.LargeZipFile):
    reject("文件不是有效的 DOCX，可能已损坏、加密或超过安全解析限制。")

namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
segments = []
total = 0
for paragraph in root.iter(namespace + "p"):
    text = "".join(
        (node.text or "") if node.tag == namespace + "t" else ("\t" if node.tag == namespace + "tab" else "\n")
        for node in paragraph.iter()
        if node.tag in (namespace + "t", namespace + "tab", namespace + "br")
    ).strip()
    if not text:
        continue
    total += len(text)
    if len(segments) >= MAX_SEGMENTS or total > MAX_CHARACTERS:
        reject("DOCX 内容超过限制。")
    segments.append({"location": f"第 {len(segments) + 1} 段", "text": text})

if total < 20:
    reject("DOCX 没有足够的可读取文字。")
name = re.sub(r'[\x00-\x1f\\/]+', '-', os.path.basename(path))[:180]
print(json.dumps({"name": name, "total_characters": total, "segments": segments}, ensure_ascii=False))
