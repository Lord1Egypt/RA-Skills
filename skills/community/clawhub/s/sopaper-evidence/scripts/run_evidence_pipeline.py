#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the Sopaper Evidence helper pipeline: build evidence ledger, bootstrap claim map, "
            "and generate an experiment gap report."
        )
    )
    parser.add_argument(
        "--sources",
        nargs="+",
        required=True,
        help="Source markdown/text files used to build the evidence ledger.",
    )
    parser.add_argument(
        "--claims",
        required=True,
        help="Markdown file containing candidate claims.",
    )
    parser.add_argument(
        "--result-artifacts",
        nargs="*",
        default=[],
        help="Structured result-artifact files to ingest alongside source files.",
    )
    parser.add_argument(
        "--result-dir",
        nargs="*",
        default=[],
        help="Directories to scan recursively for .csv, .tsv, and .json result artifacts.",
    )
    parser.add_argument(
        "--fetch-external",
        action="store_true",
        help="Fetch external URLs from the source inputs into structured source-note drafts before building the ledger.",
    )
    parser.add_argument(
        "--verify-fetched",
        action="store_true",
        help="Run a conservative verification pass over fetched source-note drafts before ledger construction.",
    )
    parser.add_argument(
        "--output-dir",
        default="output/evidence-pipeline",
        help="Directory for generated outputs. Default: output/evidence-pipeline",
    )
    parser.add_argument(
        "--prefix",
        default="draft",
        help="Filename prefix for generated files. Default: draft",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parent.parent
    sources = [Path(value).expanduser().resolve() for value in args.sources]
    explicit_result_artifacts = [Path(value).expanduser().resolve() for value in args.result_artifacts]
    result_dirs = [Path(value).expanduser().resolve() for value in args.result_dir]
    discovered_result_artifacts = discover_result_artifacts(result_dirs)
    result_artifacts = dedupe_paths([*explicit_result_artifacts, *discovered_result_artifacts])
    claims = Path(args.claims).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    missing = [str(path) for path in sources + explicit_result_artifacts + [claims] if not path.exists()]
    missing.extend(str(path) for path in result_dirs if not path.exists() or not path.is_dir())
    if missing:
        for item in missing:
            print(f"Missing input: {item}", file=sys.stderr)
        return 1

    validate_result_artifacts(root, result_artifacts)

    generated_notes: list[Path] = []
    if args.fetch_external:
        fetched_dir = output_dir / "fetched-sources"
        generated_notes = run_fetch_external(root, sources, fetched_dir)
        if args.verify_fetched and generated_notes:
            verified_dir = output_dir / "verified-sources"
            generated_notes = run_verify_fetched(root, generated_notes, verified_dir)
        sources = sources + generated_notes

    sources = sources + result_artifacts

    ledger_path = output_dir / f"{args.prefix}-ledger.md"
    claim_map_path = output_dir / f"{args.prefix}-claim-map.md"
    gap_report_path = output_dir / f"{args.prefix}-gap-report.md"
    fairness_report_path = output_dir / f"{args.prefix}-fairness-review.md"
    summary_path = output_dir / f"{args.prefix}-summary.md"

    run_python(
        root / "scripts" / "build_evidence_ledger.py",
        [str(path) for path in sources] + ["-o", str(ledger_path)],
    )
    run_python(
        root / "scripts" / "bootstrap_claim_map.py",
        [str(claims), str(ledger_path), "-o", str(claim_map_path)],
    )
    run_python(
        root / "scripts" / "triage_evidence_gaps.py",
        [str(claims), str(ledger_path), "-o", str(gap_report_path)],
    )
    run_python(
        root / "scripts" / "review_comparison_fairness.py",
        [str(claims), str(ledger_path), "-o", str(fairness_report_path)],
    )

    write_summary(
        summary_path=summary_path,
        sources=[path for path in sources if path not in result_artifacts],
        claims=claims,
        ledger_path=ledger_path,
        claim_map_path=claim_map_path,
        gap_report_path=gap_report_path,
        fairness_report_path=fairness_report_path,
        generated_notes=generated_notes,
        result_artifacts=result_artifacts,
        result_dirs=result_dirs,
        discovered_result_artifacts=discovered_result_artifacts,
    )

    print("Pipeline complete.")
    print(f"summary: {summary_path}")
    print(f"ledger: {ledger_path}")
    print(f"claim_map: {claim_map_path}")
    print(f"gap_report: {gap_report_path}")
    print(f"fairness_report: {fairness_report_path}")
    return 0


def run_python(script: Path, arguments: list[str]) -> None:
    subprocess.run(
        [sys.executable, str(script), *arguments],
        check=True,
    )


def run_fetch_external(root: Path, sources: list[Path], output_dir: Path) -> list[Path]:
    script = root / "scripts" / "fetch_external_sources.py"
    result = subprocess.run(
        [sys.executable, str(script), *[str(path) for path in sources], "--output-dir", str(output_dir)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 and "No external URLs found." not in result.stderr:
        raise subprocess.CalledProcessError(result.returncode, result.args, result.stdout, result.stderr)
    return sorted(output_dir.glob("*.md"))


def run_verify_fetched(root: Path, notes: list[Path], output_dir: Path) -> list[Path]:
    script = root / "scripts" / "verify_source_notes.py"
    subprocess.run(
        [sys.executable, str(script), *[str(path) for path in notes], "--output-dir", str(output_dir)],
        check=True,
    )
    return sorted(output_dir.glob("*.md"))


def validate_result_artifacts(root: Path, artifacts: list[Path]) -> None:
    if not artifacts:
        return
    validator = root / "scripts" / "validate_input_bundle.py"
    for artifact in artifacts:
        subprocess.run(
            [sys.executable, str(validator), "result-artifact", str(artifact)],
            check=True,
            capture_output=True,
            text=True,
        )


def discover_result_artifacts(directories: list[Path]) -> list[Path]:
    allowed_suffixes = {".csv", ".tsv", ".json"}
    artifacts: list[Path] = []
    for directory in directories:
        if not directory.exists() or not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*")):
            if path.is_file() and path.suffix.lower() in allowed_suffixes:
                artifacts.append(path.resolve())
    return artifacts


def dedupe_paths(paths: list[Path]) -> list[Path]:
    deduped: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        key = str(path.resolve())
        if key not in seen:
            seen.add(key)
            deduped.append(path.resolve())
    return deduped


def write_summary(
    *,
    summary_path: Path,
    sources: list[Path],
    claims: Path,
    ledger_path: Path,
    claim_map_path: Path,
    gap_report_path: Path,
    fairness_report_path: Path,
    generated_notes: list[Path],
    result_artifacts: list[Path],
    result_dirs: list[Path],
    discovered_result_artifacts: list[Path],
) -> None:
    lines = [
        "# Evidence Pipeline Summary",
        "",
        "This summary was generated by `scripts/run_evidence_pipeline.py`.",
        "",
        "## Inputs",
        "",
        f"- Claims file: `{claims}`",
    ]

    for source in sources:
        lines.append(f"- Source file: `{source}`")

    if result_dirs:
        lines.extend(
            [
                "",
                "## Result directories",
                "",
            ]
        )
        for directory in result_dirs:
            lines.append(f"- Result directory: `{directory}`")

    if discovered_result_artifacts:
        lines.extend(
            [
                "",
                "## Discovered result artifacts",
                "",
            ]
        )
        for artifact in discovered_result_artifacts:
            lines.append(f"- Discovered artifact: `{artifact}`")

    if result_artifacts:
        lines.extend(
            [
                "",
                "## Result artifacts",
                "",
            ]
        )
        for artifact in result_artifacts:
            lines.append(f"- Result artifact: `{artifact}`")

    if generated_notes:
        lines.extend(
            [
                "",
                "## Fetched source notes",
                "",
            ]
        )
        for note in generated_notes:
            lines.append(f"- Generated note: `{note}`")

    lines.extend(
        [
            "",
            "## Outputs",
            "",
            f"- Ledger draft: `{ledger_path}`",
            f"- Claim map draft: `{claim_map_path}`",
            f"- Gap report draft: `{gap_report_path}`",
            f"- Fairness review draft: `{fairness_report_path}`",
            "",
            "## Review checklist",
            "",
            "- Replace placeholder `TODO:` statements in the ledger with reviewed summaries.",
            "- Verify all external sources before using them for research claims.",
            "- Remove or narrow unsupported claims in the claim map.",
            "- Resolve blocker and major gaps before drafting downstream text.",
            "- Review the fairness report before keeping comparative or benchmark-win language.",
            "",
            "## Next step",
            "",
            "After reviewing these drafts, continue with the evidence brief, related work matrix, and downstream outline workflow.",
            "",
        ]
    )

    summary_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
