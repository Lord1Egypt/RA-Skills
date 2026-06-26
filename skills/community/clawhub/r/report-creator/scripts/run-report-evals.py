#!/usr/bin/env python3
"""Run lightweight report evals for repo-contained cases."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evals.contract_checks import (  # noqa: E402
    RECOMMENDED_FRONTMATTER_FIELDS,
    collect_heading_lines,
    component_counts,
    iter_blocks,
    parse_frontmatter,
    validate_block,
)


REQUIRED_HTML_MARKERS = [
    'id="toc-toggle-btn"',
    'id="toc-sidebar"',
    'id="card-mode-btn"',
    'id="sc-overlay"',
    'id="export-btn"',
    'id="export-menu"',
    'id="report-summary"',
    'id="export-print"',
    'id="export-png-desktop"',
    'id="export-png-mobile"',
    'id="export-im-share"',
    'id="edit-hotzone"',
    'id="edit-toggle"',
    'type="application/json"',
    'data-report-mode=',
    '"title"',
    '"sections"',
    '"kpis"',
]


@dataclass(frozen=True)
class LayerCheck:
    layer: str
    ok: bool
    detail: str


@dataclass(frozen=True)
class CaseSummary:
    case_id: str
    ok: bool
    checks: list[LayerCheck]
    rubric_ready: bool
    packet_path: str | None


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def resolve(root: Path, relative_path: str) -> Path:
    return (root / relative_path).resolve()


def read_required(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def check_compression(case: dict[str, str], ir_text: str) -> tuple[list[LayerCheck], dict[str, object]]:
    frontmatter, body = parse_frontmatter(ir_text)
    checks: list[LayerCheck] = []
    missing = [field for field in RECOMMENDED_FRONTMATTER_FIELDS if field not in frontmatter or not frontmatter[field]]
    checks.append(
        LayerCheck(
            layer="compression",
            ok=not missing,
            detail="frontmatter complete" if not missing else "missing frontmatter fields: " + ", ".join(missing),
        )
    )
    checks.append(
        LayerCheck(
            layer="compression",
            ok=frontmatter.get("lang") == case["lang"],
            detail=f"lang={frontmatter.get('lang')!r}, expected {case['lang']!r}",
        )
    )
    checks.append(
        LayerCheck(
            layer="compression",
            ok=frontmatter.get("report_class") == case["report_class"],
            detail=f"report_class={frontmatter.get('report_class')!r}, expected {case['report_class']!r}",
        )
    )
    checks.append(
        LayerCheck(
            layer="compression",
            ok=bool(body.strip()),
            detail="IR body present" if body.strip() else "IR body is empty",
        )
    )
    return checks, frontmatter


def check_ir_contract(case: dict[str, str], ir_text: str) -> tuple[list[LayerCheck], dict[str, int], list[str]]:
    headings = collect_heading_lines(ir_text)
    blocks = iter_blocks(ir_text)
    counts = component_counts(ir_text)
    checks = [
        LayerCheck(
            layer="ir_contract",
            ok=len(headings) >= 2,
            detail=f"{len(headings)} heading(s) found",
        ),
        LayerCheck(
            layer="ir_contract",
            ok=bool(blocks),
            detail=f"{len(blocks)} component block(s) found",
        ),
    ]
    failures: list[str] = []
    for index, block in enumerate(blocks, start=1):
        validation = validate_block(block, report_class=case["report_class"])
        ok = validation["status"] == "valid"
        detail = f"{block.tag}#{index}: {validation['status']}"
        if not ok and "auto_downgrade_target" in validation:
            detail += f" -> {validation['auto_downgrade_target']}"
            failures.append(detail)
        checks.append(LayerCheck(layer="ir_contract", ok=ok, detail=detail))
    return checks, counts, headings


def check_render_integrity(html_text: str) -> list[LayerCheck]:
    checks: list[LayerCheck] = []
    missing = [marker for marker in REQUIRED_HTML_MARKERS if marker not in html_text]
    checks.append(
        LayerCheck(
            layer="render_integrity",
            ok=not missing,
            detail="all required shell markers present" if not missing else "missing HTML markers: " + ", ".join(missing),
        )
    )
    checks.append(
        LayerCheck(
            layer="render_integrity",
            ok=":::" not in html_text,
            detail="no raw IR block markers leaked" if ":::" not in html_text else "raw IR markers leaked into HTML",
        )
    )
    return checks


def build_rubric_packet(
    case: dict[str, str],
    frontmatter: dict[str, object],
    headings: list[str],
    counts: dict[str, int],
    source_text: str,
    ir_text: str,
    html_path: Path,
) -> dict[str, object]:
    return {
        "case_id": case["case_id"],
        "lang": case["lang"],
        "report_class": case["report_class"],
        "rubric_schema": "evals/rubric.schema.json",
        "frontmatter": frontmatter,
        "headings": headings,
        "component_counts": counts,
        "source_excerpt": source_text[:1200],
        "ir_excerpt": ir_text[:1600],
        "html_path": str(html_path),
    }


def evaluate_case(root: Path, case: dict[str, str], packet_dir: Path | None) -> CaseSummary:
    source_path = resolve(root, case["source_path"])
    ir_path = resolve(root, case["ir_path"])
    html_path = resolve(root, case["html_path"])

    source_text = read_required(source_path)
    ir_text = read_required(ir_path)
    html_text = read_required(html_path)

    checks: list[LayerCheck] = [
        LayerCheck(layer="compression", ok=bool(source_text.strip()), detail="source present" if source_text.strip() else "source is empty"),
    ]
    compression_checks, frontmatter = check_compression(case, ir_text)
    checks.extend(compression_checks)
    ir_checks, counts, headings = check_ir_contract(case, ir_text)
    checks.extend(ir_checks)
    checks.extend(check_render_integrity(html_text))

    packet_path: str | None = None
    rubric_ready = bool(frontmatter) and bool(headings)
    if rubric_ready and packet_dir is not None:
        packet_dir.mkdir(parents=True, exist_ok=True)
        target = packet_dir / f"{case['case_id']}.json"
        target.write_text(
            json.dumps(
                build_rubric_packet(case, frontmatter, headings, counts, source_text, ir_text, html_path),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        packet_path = str(target)

    ok = all(check.ok for check in checks)
    return CaseSummary(
        case_id=case["case_id"],
        ok=ok,
        checks=checks,
        rubric_ready=rubric_ready,
        packet_path=packet_path,
    )


def print_text(results: list[CaseSummary]) -> int:
    failures = 0
    for case in results:
        status = "PASS" if case.ok else "FAIL"
        rubric = "RUBRIC_READY" if case.rubric_ready else "RUBRIC_BLOCKED"
        print(f"{status} {case.case_id} [{rubric}]")
        for check in case.checks:
            check_status = "ok" if check.ok else "x"
            print(f"  - {check_status} {check.layer}: {check.detail}")
        if case.packet_path:
            print(f"  - packet: {case.packet_path}")
        if not case.ok:
            failures += 1
    print()
    print(f"Summary: {len(results) - failures} passed, {failures} failed.")
    return 0 if failures == 0 else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--manifest", default="evals/report-cases.csv", help="Relative path to the case manifest.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    parser.add_argument("--json-out", help="Optional path to write the full JSON result.")
    parser.add_argument("--packet-dir", help="Optional directory to write rubric-ready packets.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    manifest = resolve(root, args.manifest)
    packet_dir = Path(args.packet_dir).resolve() if args.packet_dir else None

    cases = load_manifest(manifest)
    results = [evaluate_case(root, case, packet_dir) for case in cases]
    payload = {
        "cases": [asdict(result) for result in results],
        "summary": {
            "total": len(results),
            "passed": sum(1 for result in results if result.ok),
            "failed": sum(1 for result in results if not result.ok),
            "rubric_ready": sum(1 for result in results if result.rubric_ready),
        },
    }

    if args.json_out:
        target = Path(args.json_out).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if payload["summary"]["failed"] == 0 else 1
    return print_text(results)


if __name__ == "__main__":
    sys.exit(main())
