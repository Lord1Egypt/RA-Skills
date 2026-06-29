#!/usr/bin/env python3
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


PACKAGE_DIR = Path(
    "<research-root>/example-rag-eval-tooling-xlsx-20260616/workspace/outputs/rag-eval-tooling-matrix"
)
OUTPUT_PATH = Path(
    "<research-root>/example-rag-eval-tooling-xlsx-20260616/workspace/analysis/package-verification-iteration-008.json"
)

EXPECTED_FILES = {
    "README.md",
    "final-report.md",
    "sources.md",
    "validation-report.md",
    "rag-eval-tooling-matrix.xlsx",
}
EXPECTED_SHEETS = {
    "Summary",
    "Tool Matrix",
    "Scoring",
    "Evidence Sources",
    "Exclusions Caveats",
    "Methodology",
}
PUBLIC_SAFETY_PATTERNS = [
    r"<absolute-home-path>",
    r"<user>",
    r"\bclawd\b",
    r"chat-system",
    r"chat-system",
    r"chat_id",
    r"thread_id",
    r"topic_id",
    r"paired\.json",
    r"<ssh-authorized-keys>",
    r"private key",
    r"personal memor",
    r"OpenClaw",
    r"state\.json",
    r"sources\.jsonl",
    r"findings\.jsonl",
    r"\.tmp/",
    r"iterations/",
]
PUBLIC_SAFETY_REGEXES = [re.compile(p, re.IGNORECASE) for p in PUBLIC_SAFETY_PATTERNS]

NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "office_rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def read_xml(zf: zipfile.ZipFile, name: str) -> ET.Element:
    return ET.fromstring(zf.read(name))


def parse_range(ref: str):
    start, end = ref.split(":")
    return start, end


def range_overlaps(a: str, b: str) -> bool:
    def split_cell(cell: str):
        match = re.fullmatch(r"([A-Z]+)([0-9]+)", cell)
        if not match:
            raise ValueError(f"Unsupported cell reference: {cell}")
        col = 0
        for ch in match.group(1):
            col = col * 26 + (ord(ch) - ord("A") + 1)
        return int(match.group(2)), col

    a_start, a_end = parse_range(a)
    b_start, b_end = parse_range(b)
    ar1, ac1 = split_cell(a_start)
    ar2, ac2 = split_cell(a_end)
    br1, bc1 = split_cell(b_start)
    br2, bc2 = split_cell(b_end)
    return not (ar2 < br1 or br2 < ar1 or ac2 < bc1 or bc2 < ac1)


def scan_public_safety(path: Path, content: str):
    matches = []
    for regex in PUBLIC_SAFETY_REGEXES:
        for match in regex.finditer(content):
            line = content.count("\n", 0, match.start()) + 1
            matches.append({"file": path.name, "pattern": regex.pattern, "line": line})
    return matches


def inspect_xlsx(path: Path):
    result = {
        "valid_zip": False,
        "sheets": [],
        "missing_sheets": [],
        "tables": [],
        "worksheet_auto_filters": [],
        "formula_cells": 0,
        "table_filter_overlap_issues": [],
        "public_safety_matches": [],
    }
    with zipfile.ZipFile(path) as zf:
        result["valid_zip"] = True
        workbook = read_xml(zf, "xl/workbook.xml")
        rels = read_xml(zf, "xl/_rels/workbook.xml.rels")
        rid_to_target = {
            rel.attrib["Id"]: rel.attrib["Target"].lstrip("/")
            for rel in rels.findall("rel:Relationship", NS)
        }
        if any(not target.startswith("xl/") for target in rid_to_target.values()):
            rid_to_target = {
                rid: (target if target.startswith("xl/") else f"xl/{target}")
                for rid, target in rid_to_target.items()
            }

        sheet_files = {}
        for sheet in workbook.findall("main:sheets/main:sheet", NS):
            name = sheet.attrib["name"]
            rid = sheet.attrib[f"{{{NS['office_rel']}}}id"]
            target = rid_to_target[rid]
            result["sheets"].append(name)
            sheet_files[name] = target

        result["missing_sheets"] = sorted(EXPECTED_SHEETS - set(result["sheets"]))

        for name, sheet_file in sheet_files.items():
            root = read_xml(zf, sheet_file)
            formulas = root.findall(".//main:f", NS)
            result["formula_cells"] += len(formulas)
            sheet_filters = [node.attrib.get("ref", "") for node in root.findall("main:autoFilter", NS)]
            for ref in sheet_filters:
                result["worksheet_auto_filters"].append({"sheet": name, "ref": ref})

            rel_path = str(Path(sheet_file).parent / "_rels" / (Path(sheet_file).name + ".rels"))
            table_refs = []
            if rel_path in zf.namelist():
                sheet_rels = read_xml(zf, rel_path)
                for rel in sheet_rels.findall("rel:Relationship", NS):
                    if not rel.attrib.get("Type", "").endswith("/table"):
                        continue
                    target = rel.attrib["Target"].lstrip("/")
                    if target.startswith("../"):
                        table_file = "xl/" + target[3:]
                    elif target.startswith("xl/"):
                        table_file = target
                    else:
                        table_file = str(Path(sheet_file).parent / target)
                    table = read_xml(zf, table_file)
                    table_ref = table.attrib["ref"]
                    table_info = {
                        "sheet": name,
                        "name": table.attrib.get("name") or table.attrib.get("displayName"),
                        "ref": table_ref,
                    }
                    result["tables"].append(table_info)
                    table_refs.append(table_ref)
            for filter_ref in sheet_filters:
                for table_ref in table_refs:
                    if filter_ref and table_ref and range_overlaps(filter_ref, table_ref):
                        result["table_filter_overlap_issues"].append(
                            {"sheet": name, "worksheet_filter": filter_ref, "table": table_ref}
                        )

        text_blob_parts = []
        for name in zf.namelist():
            if name.endswith(".xml") or name.endswith(".rels"):
                try:
                    text_blob_parts.append(zf.read(name).decode("utf-8", "replace"))
                except UnicodeDecodeError:
                    continue
        result["public_safety_matches"] = scan_public_safety(path, "\n".join(text_blob_parts))
    return result


def main():
    package_files = {p.name for p in PACKAGE_DIR.iterdir() if p.is_file()}
    markdown_matches = []
    for name in sorted(package_files):
        path = PACKAGE_DIR / name
        if path.suffix.lower() == ".md":
            markdown_matches.extend(scan_public_safety(path, path.read_text(encoding="utf-8")))

    xlsx_path = PACKAGE_DIR / "rag-eval-tooling-matrix.xlsx"
    xlsx_result = inspect_xlsx(xlsx_path)
    result = {
        "package_dir": str(PACKAGE_DIR),
        "expected_files": sorted(EXPECTED_FILES),
        "actual_files": sorted(package_files),
        "missing_files": sorted(EXPECTED_FILES - package_files),
        "extra_files": sorted(package_files - EXPECTED_FILES),
        "markdown_public_safety_matches": markdown_matches,
        "xlsx": xlsx_result,
        "passed": False,
    }
    result["passed"] = (
        not result["missing_files"]
        and not result["extra_files"]
        and not markdown_matches
        and xlsx_result["valid_zip"]
        and not xlsx_result["missing_sheets"]
        and len(xlsx_result["tables"]) >= 6
        and xlsx_result["formula_cells"] >= 1
        and not xlsx_result["worksheet_auto_filters"]
        and not xlsx_result["table_filter_overlap_issues"]
        and not xlsx_result["public_safety_matches"]
    )
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
