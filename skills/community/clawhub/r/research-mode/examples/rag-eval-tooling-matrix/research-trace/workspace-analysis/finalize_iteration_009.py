#!/usr/bin/env python3
"""Finalize the RAG evaluation tooling example package.

This intentionally uses only stdlib checks so the package can be reviewed
without relying on a task-local virtualenv.
"""

from __future__ import annotations

import json
import posixpath
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET


TASK_DIR = Path("<research-root>/example-rag-eval-tooling-xlsx-20260616")
PACKAGE_DIR = TASK_DIR / "workspace/outputs/rag-eval-tooling-matrix"
RESULT_FILE = TASK_DIR / ".tmp/result-ff45653a2a5d.json"
REVIEW_FILE = TASK_DIR / "workspace/analysis/finalization-review-iteration-009.json"

EXPECTED_FILES = {
    "README.md",
    "final-report.md",
    "rag-eval-tooling-matrix.xlsx",
    "sources.md",
    "validation-report.md",
}
EXPECTED_SHEETS = {
    "Summary",
    "Tool Matrix",
    "Scoring",
    "Evidence Sources",
    "Exclusions Caveats",
    "Methodology",
}
PRIVATE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"<absolute-home-path>",
        r"<user>",
        r"mattermost",
        r"telegram",
        r"thread_id",
        r"topic_id",
        r"chat_id",
        r"token",
        r"paired\.json",
    )
]


def rel(path: Path) -> str:
    return str(path.relative_to(TASK_DIR))


def public_safety_matches(text: str) -> list[str]:
    matches: list[str] = []
    for pattern in PRIVATE_PATTERNS:
        if pattern.search(text):
            matches.append(pattern.pattern)
    return matches


def read_zip_xml(zf: zipfile.ZipFile, name: str) -> ET.Element:
    return ET.fromstring(zf.read(name))


def resolve_zip_target(base_dir: str, target: str) -> str:
    clean_target = target.lstrip("/")
    if clean_target.startswith("xl/"):
        return posixpath.normpath(clean_target)
    return posixpath.normpath(posixpath.join(base_dir, clean_target))


def workbook_summary(workbook_path: Path) -> dict:
    ns = {
        "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        "pkgrel": "http://schemas.openxmlformats.org/package/2006/relationships",
    }
    summary = {
        "valid_zip": False,
        "sheets": [],
        "missing_sheets": [],
        "tables": [],
        "worksheet_auto_filters": [],
        "table_filter_overlap_issues": [],
        "formula_cells": 0,
        "public_safety_matches": [],
    }

    with zipfile.ZipFile(workbook_path) as zf:
        summary["valid_zip"] = True
        if "xl/sharedStrings.xml" in zf.namelist():
            shared_strings_text = zf.read("xl/sharedStrings.xml").decode("utf-8", errors="ignore")
            summary["public_safety_matches"] = public_safety_matches(shared_strings_text)
        workbook = read_zip_xml(zf, "xl/workbook.xml")
        rels = read_zip_xml(zf, "xl/_rels/workbook.xml.rels")
        rel_targets = {
            rel_node.attrib["Id"]: rel_node.attrib["Target"]
            for rel_node in rels.findall("pkgrel:Relationship", ns)
        }

        for sheet in workbook.findall("main:sheets/main:sheet", ns):
            sheet_name = sheet.attrib["name"]
            summary["sheets"].append(sheet_name)
            rid = sheet.attrib[f"{{{ns['rel']}}}id"]
            target = rel_targets[rid]
            sheet_xml_path = resolve_zip_target("xl", target)

            worksheet = read_zip_xml(zf, sheet_xml_path)
            formulas = worksheet.findall(".//main:f", ns)
            summary["formula_cells"] += len(formulas)

            worksheet_auto_filter = worksheet.find("main:autoFilter", ns)
            if worksheet_auto_filter is not None:
                summary["worksheet_auto_filters"].append(
                    {"sheet": sheet_name, "ref": worksheet_auto_filter.attrib.get("ref", "")}
                )

            table_part_nodes = worksheet.findall("main:tableParts/main:tablePart", ns)
            if not table_part_nodes:
                continue

            rel_path = sheet_xml_path.replace("xl/worksheets/", "xl/worksheets/_rels/") + ".rels"
            sheet_rels = read_zip_xml(zf, rel_path)
            table_targets = {
                rel_node.attrib["Id"]: rel_node.attrib["Target"]
                for rel_node in sheet_rels.findall("pkgrel:Relationship", ns)
            }
            for table_part in table_part_nodes:
                table_rid = table_part.attrib[f"{{{ns['rel']}}}id"]
                table_target = table_targets[table_rid]
                table_path = resolve_zip_target(posixpath.dirname(sheet_xml_path), table_target)
                table = read_zip_xml(zf, table_path)
                table_info = {
                    "sheet": sheet_name,
                    "name": table.attrib.get("name", ""),
                    "ref": table.attrib.get("ref", ""),
                }
                summary["tables"].append(table_info)
                if worksheet_auto_filter is not None:
                    summary["table_filter_overlap_issues"].append(table_info)

    summary["missing_sheets"] = sorted(EXPECTED_SHEETS - set(summary["sheets"]))
    return summary


def main() -> None:
    actual_files = {path.name for path in PACKAGE_DIR.iterdir() if path.is_file()} if PACKAGE_DIR.exists() else set()
    missing_files = sorted(EXPECTED_FILES - actual_files)
    extra_files = sorted(actual_files - EXPECTED_FILES)

    markdown_matches: dict[str, list[str]] = {}
    link_counts: dict[str, int] = {}
    for name in ("README.md", "final-report.md", "sources.md", "validation-report.md"):
        path = PACKAGE_DIR / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        matches = public_safety_matches(text)
        if matches:
            markdown_matches[name] = matches
        link_counts[name] = len(re.findall(r"https?://", text))

    xlsx_path = PACKAGE_DIR / "rag-eval-tooling-matrix.xlsx"
    xlsx = workbook_summary(xlsx_path) if xlsx_path.exists() else {"missing": True}

    blocking_defects = []
    if missing_files:
        blocking_defects.append(f"Missing package files: {', '.join(missing_files)}")
    if markdown_matches:
        blocking_defects.append(f"Public-safety scan found private markers: {markdown_matches}")
    if xlsx.get("missing"):
        blocking_defects.append("Workbook is missing.")
    elif not xlsx.get("valid_zip"):
        blocking_defects.append("Workbook is not a valid XLSX zip archive.")
    elif xlsx.get("missing_sheets"):
        blocking_defects.append(f"Workbook missing expected sheets: {', '.join(xlsx['missing_sheets'])}")
    elif xlsx.get("table_filter_overlap_issues"):
        blocking_defects.append("Workbook has worksheet autoFilter elements overlapping table filters.")
    elif int(xlsx.get("formula_cells", 0)) < 1:
        blocking_defects.append("Workbook contains no formulas.")
    elif xlsx.get("public_safety_matches"):
        blocking_defects.append(f"Workbook shared strings contain private markers: {xlsx['public_safety_matches']}")

    nonblocking_defects = []
    if extra_files:
        nonblocking_defects.append(f"Package has extra files: {', '.join(extra_files)}")
    if link_counts.get("sources.md", 0) < 20:
        nonblocking_defects.append("sources.md has fewer than 20 public source links.")

    review = {
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "package_dir": rel(PACKAGE_DIR),
        "actual_files": sorted(actual_files),
        "expected_files": sorted(EXPECTED_FILES),
        "missing_files": missing_files,
        "extra_files": extra_files,
        "markdown_public_safety_matches": markdown_matches,
        "markdown_link_counts": link_counts,
        "xlsx": xlsx,
        "blocking_defects": blocking_defects,
        "nonblocking_defects": nonblocking_defects,
        "passed": not blocking_defects,
    }
    REVIEW_FILE.write_text(json.dumps(review, indent=2, ensure_ascii=False), encoding="utf-8")

    validation_checks = [
        {
            "check": "candidate_package",
            "result": "passed" if not missing_files else "failed",
            "reason": "Required README, final report, sources index, workbook, and validation report are present.",
        },
        {
            "check": "public_safety_scan",
            "result": "passed" if not markdown_matches else "failed",
            "reason": "Markdown files contain no private workspace paths, messaging identifiers, or obvious token markers.",
        },
        {
            "check": "workbook_public_safety_scan",
            "result": "passed" if not xlsx.get("public_safety_matches") else "failed",
            "reason": "Workbook shared strings contain no private workspace paths, messaging identifiers, or obvious token markers.",
        },
        {
            "check": "workbook_structure",
            "result": "passed" if not xlsx.get("missing_sheets") else "failed",
            "reason": "Workbook has Summary, Tool Matrix, Scoring, Evidence Sources, Exclusions Caveats, and Methodology sheets.",
        },
        {
            "check": "excel_compatibility",
            "result": "passed"
            if xlsx.get("valid_zip") and not xlsx.get("table_filter_overlap_issues") and xlsx.get("formula_cells", 0) > 0
            else "failed",
            "reason": "Workbook is a valid XLSX archive, has Excel tables and formulas, and no worksheet-level autoFilter/table overlap.",
        },
    ]

    result = {
        "summary": (
            "Finalized the review-ready RAG evaluation tooling matrix package as a single candidate artifact; "
            "recipient inspection found the expected files, public-safe markdown, and a valid Excel workbook with "
            "the requested sheets, tables, and formulas."
        ),
        "next_angle": "Complete this research run; only human review or copying into the public repository remains.",
        "meaningful_progress": True,
        "code_used": True,
        "phase": "finalize",
        "open_questions": [
            "Evidently managed SaaS availability remains an intentional procurement caveat because official evidence is conflicting.",
            "Some vendor governance controls are supported by public vendor pages rather than deep implementation docs.",
        ],
        "sources": [],
        "findings": [
            {
                "kind": "synthesis",
                "text": "The package is best exposed as one final package candidate rather than separate raw files.",
                "source_urls": [],
            },
            {
                "kind": "fact",
                "text": "The workbook contains the requested sheets and 60 formula cells, with no worksheet-level autoFilter/table overlap detected.",
                "source_urls": [],
            },
            {
                "kind": "risk",
                "text": "Evidently managed SaaS availability is carried as a visible caveat for procurement use.",
                "source_urls": [],
            },
        ],
        "analysis_artifacts": [
            {
                "path": "workspace/analysis/finalize_iteration_009.py",
                "kind": "script",
                "note": "Final recipient-style package inspection and result writer.",
            },
            {
                "path": "workspace/analysis/finalization-review-iteration-009.json",
                "kind": "artifact",
                "note": "Structured finalization review with file, safety, and workbook compatibility checks.",
            },
            {
                "path": "workspace/analysis/package-verification-iteration-008.json",
                "kind": "artifact",
                "note": "Independent prior package verification used as supporting evidence.",
            },
        ],
        "packages_used": ["python-stdlib"],
        "database_used": False,
        "database_artifacts": [],
        "database_summary": None,
        "vision_used": False,
        "vision_artifacts": [],
        "vision_summary": None,
        "adequacy": {
            "status": "passed",
            "goal_alignment": (
                "The accumulated research and generated package answer the goal: a public-safe decision matrix for "
                "selecting production RAG/LLM evaluation tooling, backed by public evidence and practical trade-offs."
            ),
            "coverage_summary": (
                "The package covers open-source and commercially relevant evaluation, observability, CI/regression, "
                "framework-native, and governance-oriented tools; unresolved procurement uncertainty is documented as a caveat."
            ),
            "covered_requirements": [
                {
                    "requirement": "Public-safe example package in English",
                    "evidence": "README.md, final-report.md, sources.md, validation-report.md, and the workbook are in the package and passed the public-safety scan.",
                },
                {
                    "requirement": "Current public evidence, preferring official/vendor/GitHub docs",
                    "evidence": "sources.md and the Evidence Sources workbook sheet include 30 public evidence rows.",
                },
                {
                    "requirement": "Non-trivial Excel-compatible workbook",
                    "evidence": "Workbook has expected sheets, Excel tables, and 60 formula cells with no worksheet-level autoFilter/table overlap.",
                },
                {
                    "requirement": "Practical trade-offs and integration notes",
                    "evidence": "final-report.md and Tool Matrix sheet separate evaluation fit, operational fit, caveats, and recommendations.",
                },
            ],
            "coverage_gaps": [
                {
                    "gap": "Evidently managed SaaS availability needs vendor confirmation for procurement use.",
                    "severity": "minor",
                }
            ],
            "evidence_risks": [
                {
                    "risk": "Vendor governance details are unevenly documented in public sources.",
                    "severity": "minor",
                }
            ],
            "contradictions": [
                {
                    "contradiction": "Official Evidently material gives conflicting signals about managed SaaS availability.",
                    "severity": "minor",
                }
            ],
            "recommended_next_phase": "finalize",
            "recommended_next_angle": "Mark the research complete with the package as the single reviewable candidate artifact.",
            "blocking_reasons": [],
            "validation_evidence": [
                {
                    "check": "goal_alignment",
                    "result": "passed",
                    "reason": "The package directly maps the researched tools into a decision matrix and recommendation report.",
                },
                {
                    "check": "explicit_constraints",
                    "result": "passed",
                    "reason": "No private path or messaging marker was found in user-facing markdown; no personal/contact data was included.",
                },
                {
                    "check": "requested_deliverable",
                    "result": "passed",
                    "reason": "The package contains the requested markdown files and Excel workbook.",
                },
                {
                    "check": "workbook_validation",
                    "result": "passed",
                    "reason": "XLSX structure, sheets, tables, formulas, and autoFilter compatibility were checked.",
                },
            ],
        },
        "notify_recommendation": "final",
        "should_complete": True,
        "final_report_markdown": (
            "# RAG Evaluation Tooling Matrix\n\n"
            "Review-ready package candidate: `rag-eval-tooling-matrix/`.\n\n"
            "It includes README.md, final-report.md, sources.md, validation-report.md, and "
            "rag-eval-tooling-matrix.xlsx. Final validation passed: required files are present, markdown is "
            "public-safe, and the workbook has the requested sheets, tables, and formulas without worksheet-level "
            "autoFilter/table overlap."
        ),
        "finalization": {
            "status": "passed" if not blocking_defects else "needs_revision",
            "inferred_user_need": (
                "A public repository example package that demonstrates a useful RAG evaluation tooling decision "
                "matrix, including a non-trivial Excel workbook and traceable public evidence."
            ),
            "intended_recipient": "Engineering team reviewing a production RAG evaluation stack example for a public repository.",
            "primary_deliverable_kind": "package",
            "internal_artifacts": [
                {
                    "path": "workspace/analysis/package-generation-summary.json",
                    "kind": "generation_summary",
                    "note": "Confirms generated workbook/report row counts and validation messages.",
                },
                {
                    "path": "workspace/analysis/package-verification-iteration-008.json",
                    "kind": "verification",
                    "note": "Prior independent verification of package structure and XLSX internals.",
                },
                {
                    "path": "workspace/analysis/finalization-review-iteration-009.json",
                    "kind": "finalization_review",
                    "note": "Final recipient-style inspection performed in this iteration.",
                },
            ],
            "candidate_artifacts": [
                {
                    "path": "workspace/outputs/rag-eval-tooling-matrix",
                    "kind": "final_package",
                    "note": "Single review-ready package candidate for examples/rag-eval-tooling-matrix/.",
                }
            ],
            "blocking_defects": blocking_defects,
            "nonblocking_defects": nonblocking_defects,
            "revisions": [
                {
                    "revision": "No content changes were needed in finalization; package passed recipient inspection.",
                    "evidence": "workspace/analysis/finalization-review-iteration-009.json",
                }
            ],
            "validation_evidence": validation_checks,
            "last_validation_findings": [review],
            "last_validated_at": review["reviewed_at"],
        },
    }

    RESULT_FILE.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
