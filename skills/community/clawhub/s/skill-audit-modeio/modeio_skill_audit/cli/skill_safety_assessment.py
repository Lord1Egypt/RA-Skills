#!/usr/bin/env python3
"""
skill-audit Skill Safety Assessment (v2).

Thin CLI wrapper over modular skill_safety engine/validation utilities.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from modeio_skill_audit.skill_safety import (
    ContextProfile,
    build_adjudication_prompt,
    build_prompt_payload as _build_prompt_payload,
    enforce_scan_integrity,
    load_scan_file,
    merge_adjudication,
    parse_adjudication_text,
    parse_context_profile,
    scan_repository as _scan_repository,
    validate_assessment_output as _validate_assessment_output,
)

# Backward-compatible re-exports.
scan_repository = _scan_repository
build_prompt_payload = _build_prompt_payload
validate_assessment_output = _validate_assessment_output


def _print_scan_text(scan_result: Dict[str, Any]) -> None:
    summary = scan_result.get("summary", {})
    scoring = scan_result.get("scoring", {})
    run = scan_result.get("run", {})
    precheck = scan_result.get("precheck", {})

    print("Skill Safety Assessment v2 complete")
    print(f"Target: {scan_result.get('target_repo')}")
    print(f"Commit: {run.get('commit_sha', 'unknown')}")
    print(
        "Coverage: "
        f"ratio={summary.get('coverage_ratio', 0.0)} "
        f"scanned={summary.get('files_scanned', 0)} "
        f"candidate={summary.get('candidate_files', 0)} "
        f"partial={summary.get('partial_coverage', False)}"
    )
    print(
        "Risk: "
        f"score={scoring.get('risk_score', 0)} "
        f"confidence={scoring.get('confidence', 'low')} "
        f"decision={scoring.get('suggested_decision', 'caution')}"
    )
    if precheck.get("enabled"):
        print(
            "Precheck: "
            f"decision={precheck.get('decision', 'unavailable')} "
            f"reason={precheck.get('reason', 'n/a')}"
        )

    highlights = scan_result.get("highlights", [])
    if not highlights:
        print("Highlights: none")
        return
    print("Highlights:")
    for item in highlights:
        print(f"- {item.get('summary')}")


def _load_context_profile(
    context_json: Optional[str],
    context_file: Optional[str],
) -> Tuple[Optional[ContextProfile], Optional[str]]:
    profile, errors = parse_context_profile(context_json=context_json, context_file=context_file)
    if errors:
        return None, "; ".join(errors)
    return profile, None


def _add_scan_args(scan_parser: argparse.ArgumentParser) -> None:
    scan_parser.add_argument("--target-repo", required=True, help="Path to repository to evaluate.")
    scan_parser.add_argument(
        "--max-findings",
        type=int,
        default=120,
        help="Maximum findings included in output.",
    )
    scan_parser.add_argument(
        "--context-profile",
        default=None,
        help=(
            "Optional JSON context profile string. "
            "Keys: environment, execution_mode, risk_tolerance, data_sensitivity."
        ),
    )
    scan_parser.add_argument(
        "--context-profile-file",
        default=None,
        help="Optional file path containing context profile JSON.",
    )
    scan_parser.add_argument(
        "--github-osint-timeout",
        type=float,
        default=6.0,
        help="Per-request timeout in seconds for default GitHub OSINT precheck calls.",
    )
    scan_parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    scan_parser.add_argument("--output", default=None, help="Optional file path to write JSON output.")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Skill Safety Assessment v2 utilities: layered deterministic evaluate, "
            "prompt payload rendering, and output validation."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate_parser = subparsers.add_parser("evaluate", help="Run layered v2 skill safety evaluation.")
    _add_scan_args(evaluate_parser)

    scan_parser = subparsers.add_parser("scan", help="Compatibility alias to v2 evaluate.")
    _add_scan_args(scan_parser)

    prompt_parser = subparsers.add_parser("prompt", help="Render model prompt payload from scan/evaluate result.")
    prompt_parser.add_argument("--target-repo", required=True, help="Path to repository being assessed.")
    prompt_parser.add_argument("--context", default=None, help="Optional environment/use-case context.")
    prompt_parser.add_argument("--focus", default=None, help="Optional concerns to prioritize.")
    prompt_parser.add_argument(
        "--scan-file",
        default=None,
        help="Optional existing scan/evaluate JSON file. If omitted, evaluate runs inline.",
    )
    prompt_parser.add_argument(
        "--max-findings",
        type=int,
        default=120,
        help="Maximum findings when evaluate runs inline.",
    )
    prompt_parser.add_argument(
        "--include-full-findings",
        action="store_true",
        help="Include full findings in SCRIPT_SCAN_JSON payload.",
    )
    prompt_parser.add_argument(
        "--context-profile",
        default=None,
        help="Optional JSON context profile used when inline evaluate runs.",
    )
    prompt_parser.add_argument(
        "--context-profile-file",
        default=None,
        help="Optional context profile JSON file used when inline evaluate runs.",
    )
    prompt_parser.add_argument(
        "--github-osint-timeout",
        type=float,
        default=6.0,
        help="Per-request timeout in seconds for default GitHub OSINT precheck calls.",
    )

    validate_parser = subparsers.add_parser("validate", help="Validate assessment output against scan evidence.")
    validate_parser.add_argument("--scan-file", required=True, help="Scan/evaluate JSON file.")
    validate_parser.add_argument(
        "--assessment-file",
        default=None,
        help="Assessment output file. If omitted, reads from stdin.",
    )
    validate_parser.add_argument("--json", action="store_true", help="Emit JSON validation report.")
    validate_parser.add_argument(
        "--target-repo",
        default=None,
        help="Target repo path for integrity re-scan during validate.",
    )
    validate_parser.add_argument(
        "--rescan-on-validate",
        action="store_true",
        help="Re-run evaluate and compare integrity metadata against --scan-file.",
    )
    validate_parser.add_argument(
        "--max-findings",
        type=int,
        default=120,
        help="Maximum findings when --rescan-on-validate is enabled.",
    )

    adjudicate_parser = subparsers.add_parser(
        "adjudicate",
        help=(
            "Context-aware adjudication bridge for LLM review. "
            "Without --assessment-file prints adjudication prompt; with file merges decisions."
        ),
    )
    adjudicate_parser.add_argument("--scan-file", required=True, help="Scan/evaluate JSON file.")
    adjudicate_parser.add_argument(
        "--assessment-file",
        default=None,
        help="Optional LLM adjudication output file (JSON or markdown containing JSON).",
    )
    adjudicate_parser.add_argument(
        "--context-profile",
        default=None,
        help="Optional JSON context profile override for adjudication prompt output.",
    )
    adjudicate_parser.add_argument(
        "--context-profile-file",
        default=None,
        help="Optional context profile JSON file override for adjudication prompt output.",
    )
    adjudicate_parser.add_argument("--json", action="store_true", help="Emit JSON output.")

    return parser


def _run_scan_command(args: argparse.Namespace) -> int:
    target_repo = Path(args.target_repo).expanduser().resolve()
    if not target_repo.exists() or not target_repo.is_dir():
        print(f"Error: --target-repo must be an existing directory: {target_repo}", file=sys.stderr)
        return 2

    profile, profile_error = _load_context_profile(args.context_profile, args.context_profile_file)
    if profile_error:
        print(f"Error: {profile_error}", file=sys.stderr)
        return 2
    assert profile is not None

    result = scan_repository(
        target_repo=target_repo,
        max_findings=max(0, int(args.max_findings)),
        context_profile=profile,
        github_osint_timeout=max(1.0, float(args.github_osint_timeout)),
    )
    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_scan_text(result)
    return 0


def _run_prompt_command(args: argparse.Namespace) -> int:
    target_repo = Path(args.target_repo).expanduser().resolve()
    if not target_repo.exists() or not target_repo.is_dir():
        print(f"Error: --target-repo must be an existing directory: {target_repo}", file=sys.stderr)
        return 2

    if args.scan_file:
        scan_result, load_error = load_scan_file(args.scan_file)
        if load_error:
            print(f"Error: {load_error}", file=sys.stderr)
            return 2
        assert scan_result is not None
    else:
        profile, profile_error = _load_context_profile(args.context_profile, args.context_profile_file)
        if profile_error:
            print(f"Error: {profile_error}", file=sys.stderr)
            return 2
        assert profile is not None
        scan_result = scan_repository(
            target_repo=target_repo,
            max_findings=max(0, int(args.max_findings)),
            context_profile=profile,
            github_osint_timeout=max(1.0, float(args.github_osint_timeout)),
        )

    prompt_text = build_prompt_payload(
        scan_result=scan_result,
        target_repo=str(target_repo),
        context=args.context,
        focus=args.focus,
        include_full_findings=bool(args.include_full_findings),
    )
    print(prompt_text)
    return 0


def _run_validate_command(args: argparse.Namespace) -> int:
    scan_result, load_error = load_scan_file(args.scan_file)
    if load_error:
        print(f"Error: {load_error}", file=sys.stderr)
        return 2
    assert scan_result is not None

    if args.assessment_file:
        assessment_path = Path(args.assessment_file).expanduser().resolve()
        try:
            assessment_text = assessment_path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"Error: failed to read --assessment-file: {exc}", file=sys.stderr)
            return 2
    else:
        assessment_text = sys.stdin.read()

    report = validate_assessment_output(assessment_text=assessment_text, scan_result=scan_result)

    if args.rescan_on_validate:
        if not args.target_repo:
            print("Error: --rescan-on-validate requires --target-repo.", file=sys.stderr)
            return 2
        target_repo = Path(args.target_repo).expanduser().resolve()
        if not target_repo.exists() or not target_repo.is_dir():
            print(f"Error: --target-repo must be an existing directory: {target_repo}", file=sys.stderr)
            return 2

        integrity_errors, integrity_warnings = enforce_scan_integrity(
            scan_result=scan_result,
            target_repo=target_repo,
            max_findings=max(0, int(args.max_findings)),
        )
        if integrity_errors:
            report.setdefault("errors", []).extend(integrity_errors)
        if integrity_warnings:
            report.setdefault("warnings", []).extend(integrity_warnings)
        report["valid"] = len(report.get("errors", [])) == 0

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("Validation result:", "valid" if report.get("valid") else "invalid")
        if report.get("errors"):
            print("Errors:")
            for item in report["errors"]:
                print(f"- {item}")
        if report.get("warnings"):
            print("Warnings:")
            for item in report["warnings"]:
                print(f"- {item}")

    return 0 if report.get("valid") else 1


def _run_adjudicate_command(args: argparse.Namespace) -> int:
    scan_result, load_error = load_scan_file(args.scan_file)
    if load_error:
        print(f"Error: {load_error}", file=sys.stderr)
        return 2
    assert scan_result is not None

    if args.assessment_file:
        assessment_path = Path(args.assessment_file).expanduser().resolve()
        try:
            assessment_text = assessment_path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"Error: failed to read --assessment-file: {exc}", file=sys.stderr)
            return 2

        adjudication_payload, parse_error = parse_adjudication_text(assessment_text)
        if parse_error:
            print(f"Error: {parse_error}", file=sys.stderr)
            return 2
        assert adjudication_payload is not None

        merged = merge_adjudication(scan_result=scan_result, adjudication=adjudication_payload)
        if args.json:
            print(json.dumps(merged, ensure_ascii=False, indent=2))
        else:
            print("Adjudication result:", "valid" if merged.get("valid") else "invalid")
            for item in merged.get("errors", []):
                print(f"- ERROR: {item}")
            for item in merged.get("warnings", []):
                print(f"- WARN: {item}")
            if merged.get("valid"):
                decision = merged.get("adjudicated", {})
                print(
                    "Final decision: "
                    + f"decision={decision.get('suggested_decision')} "
                    + f"score={decision.get('risk_score')} "
                    + f"findings={decision.get('finding_count')}"
                )
        return 0 if merged.get("valid") else 1

    profile: Optional[ContextProfile] = None
    override_profile, profile_error = _load_context_profile(args.context_profile, args.context_profile_file)
    if profile_error:
        print(f"Error: {profile_error}", file=sys.stderr)
        return 2
    if override_profile and override_profile.to_dict() != ContextProfile().to_dict():
        profile = override_profile
    else:
        payload = scan_result.get("context_profile")
        if isinstance(payload, dict):
            profile_json = json.dumps(payload)
            derived, _ = parse_context_profile(context_json=profile_json)
            profile = derived

    prompt_text = build_adjudication_prompt(
        scan_result=scan_result,
        profile=profile.to_dict() if profile else None,
    )
    if args.json:
        print(
            json.dumps(
                {
                    "prompt": prompt_text,
                    "context_profile": profile.to_dict() if profile else {},
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(prompt_text)
    return 0


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command in {"evaluate", "scan"}:
        return _run_scan_command(args)
    if args.command == "prompt":
        return _run_prompt_command(args)
    if args.command == "validate":
        return _run_validate_command(args)
    if args.command == "adjudicate":
        return _run_adjudicate_command(args)

    print("Error: unknown command", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
