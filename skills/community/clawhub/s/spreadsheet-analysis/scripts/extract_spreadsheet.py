#!/usr/bin/env python3
import csv
import json
import os
import posixpath
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

MAX_ARCHIVE_ENTRIES = 500
MAX_ARCHIVE_BYTES = 32 * 1024 * 1024
MAX_ENTRY_BYTES = 16 * 1024 * 1024
MAX_COMPRESSION_RATIO = 100
MAX_SEGMENTS = 2000
MAX_CHARACTERS = 120000
MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def reject(message: str) -> None:
    raise SystemExit(message)


def column_name(index: int) -> str:
    value = index + 1
    result = ""
    while value:
        value, remainder = divmod(value - 1, 26)
        result = chr(65 + remainder) + result
    return result


def validate_archive(archive: zipfile.ZipFile) -> None:
    infos = archive.infolist()
    if len(infos) > MAX_ARCHIVE_ENTRIES or len({info.filename for info in infos}) != len(infos):
        raise ValueError("invalid entry list")
    total = 0
    for info in infos:
        if info.flag_bits & 0x1:
            raise ValueError("encrypted entry")
        total += info.file_size
        if info.file_size > MAX_ENTRY_BYTES or total > MAX_ARCHIVE_BYTES:
            raise ValueError("expanded archive too large")
        if info.file_size and info.file_size / max(1, info.compress_size) > MAX_COMPRESSION_RATIO:
            raise ValueError("unsafe compression ratio")


def add_segment(segments: list[dict[str, str]], location: str, values: list[str], total: int) -> int:
    if not values:
        return total
    text = " | ".join(values)
    total += len(text)
    if len(segments) >= MAX_SEGMENTS or total > MAX_CHARACTERS:
        reject("表格内容超过限制。")
    segments.append({"location": location, "text": text})
    return total


if len(sys.argv) != 2:
    reject("用法: extract_spreadsheet.py FILE.xlsx|FILE.csv")
path = sys.argv[1]
extension = os.path.splitext(path)[1].lower()
if not os.path.isfile(path) or os.path.getsize(path) > 10 * 1024 * 1024:
    reject("表格不存在或超过 10 MB。")

segments: list[dict[str, str]] = []
total = 0
if extension == ".csv":
    try:
        with open(path, encoding="utf-8-sig", newline="") as stream:
            for number, row in enumerate(csv.reader(stream), 1):
                values = [f"{column_name(index)}={value}" for index, value in enumerate(row) if value != ""]
                total = add_segment(segments, f"CSV!第{number}行", values, total)
    except (OSError, UnicodeDecodeError, csv.Error):
        reject("CSV 必须是可读取的 UTF-8 文件。")
elif extension == ".xlsx":
    try:
        with zipfile.ZipFile(path) as archive:
            validate_archive(archive)
            names = set(archive.namelist())
            required = {"xl/workbook.xml", "xl/_rels/workbook.xml.rels"}
            if not required.issubset(names):
                raise ValueError("missing workbook metadata")

            namespace = {"m": MAIN_NS, "r": REL_NS}
            shared = []
            if "xl/sharedStrings.xml" in names:
                shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
                shared = [
                    "".join(node.text or "" for node in item.iter(f"{{{MAIN_NS}}}t"))
                    for item in shared_root
                ]
            workbook = ET.fromstring(archive.read("xl/workbook.xml"))
            relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
            relation_map = {item.attrib["Id"]: item.attrib["Target"] for item in relationships}
            sheets = workbook.find("m:sheets", namespace)
            if sheets is None:
                raise ValueError("missing sheets")

            for sheet in sheets:
                sheet_name = sheet.attrib.get("name", "Sheet")
                relation_id = sheet.attrib[f"{{{REL_NS}}}id"]
                target = relation_map[relation_id].lstrip("/")
                target = target if target.startswith("xl/") else "xl/" + target
                target = posixpath.normpath(target)
                if not target.startswith("xl/worksheets/") or target not in names:
                    raise ValueError("unsafe worksheet target")
                root = ET.fromstring(archive.read(target))
                for row in root.findall(".//m:sheetData/m:row", namespace):
                    row_number = int(row.attrib.get("r", "0"))
                    if row_number < 1 or row_number > 1_048_576:
                        raise ValueError("invalid row number")
                    values = []
                    for cell in row.findall("m:c", namespace):
                        reference = cell.attrib.get("r", "?")
                        value = cell.findtext("m:v", default="", namespaces=namespace)
                        if cell.attrib.get("t") == "s":
                            if not value.isdigit() or int(value) >= len(shared):
                                raise ValueError("invalid shared string")
                            value = shared[int(value)]
                        elif cell.attrib.get("t") == "inlineStr":
                            value = "".join(node.text or "" for node in cell.findall(".//m:t", namespace))
                        column = re.sub(r"\d+$", "", reference)
                        if value != "":
                            values.append(f"{column}={value}")
                    total = add_segment(segments, f"{sheet_name}!第{row_number}行", values, total)
    except (ET.ParseError, KeyError, OSError, ValueError, zipfile.BadZipFile, zipfile.LargeZipFile):
        reject("XLSX 无法解析，可能已损坏、加密或超过安全解析限制。")
else:
    reject("仅支持 XLSX 和 CSV。")

if total < 20:
    reject("表格没有足够的可读取内容。")
name = re.sub(r'[\x00-\x1f\\/]+', '-', os.path.basename(path))[:180]
print(json.dumps({"name": name, "total_characters": total, "segments": segments}, ensure_ascii=False))
