#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from lib.ai_audit import audit_with_ai
from lib.analyzers import analyze_static
from lib.discovery import build_skill_target, default_scan_roots, discover_skills, resolve_workspace
from lib.policy import evaluate_findings, load_policy, output_paths
from lib.remediation import remediate_skill
from lib.reporting import build_bundle, build_skill_report, print_text_summary, write_json_report


def scan_target(target, policy: dict, stage: str) -> dict:
    static_result = analyze_static(target, policy)
    ai_result = audit_with_ai(target, policy)
    decision = evaluate_findings(policy, target, static_result, ai_result, stage)
    return build_skill_report(target, stage, static_result, ai_result, decision, policy)


def apply_auto_remediation(
    reports: list[dict],
    policy: dict,
    action: str,
    statuses: set[str],
    *,
    force: bool = False,
    yes: bool = False,
) -> list[dict]:
    normalized_action = action.lower()
    normalized_statuses = {status.upper() for status in statuses}
    if normalized_action == "delete" and (not force or not yes):
        raise ValueError("auto-delete remediation requires both --force and --yes")

    results: list[dict] = []
    for report in reports:
        decision = report["decision"]
        recommendation = str(decision["recommendation"]).upper()
        if recommendation not in normalized_statuses:
            continue
        target_path = Path(report["skill"]["path"]).resolve()
        reason = (
            f"SkillGuard auto-remediation after scan: "
            f"{decision['recommendation']} risk={decision['risk_score']}"
        )
        remediation = remediate_skill(target_path, policy, normalized_action, reason=reason)
        results.append(
            {
                "skill_name": report["skill"]["name"],
                "target_path": str(target_path),
                "recommendation": recommendation,
                "risk_score": decision["risk_score"],
                "action": normalized_action,
                "remediation": remediation,
            }
        )
    return results


def run_scan(args: argparse.Namespace) -> int:
    policy = load_policy(args.policy)
    if args.command == "scan":
        roots = [Path(root).resolve() for root in args.root] if args.root else default_scan_roots(policy)
        targets = discover_skills(policy, roots=roots)
        stage = "scan"
        report_prefix = "scan"
    else:
        target = build_skill_target(Path(args.target).resolve(), policy, resolve_workspace())
        targets = [target]
        stage = {
            "check-install": "install",
            "check-update": "update",
            "check-exec": "exec",
        }[args.command]
        report_prefix = args.command.replace("check-", "")

    reports = [scan_target(target, policy, stage) for target in targets]
    remediation_results: list[dict] = []
    if args.command == "scan" and getattr(args, "auto_remediate", None):
        remediation_results = apply_auto_remediation(
            reports,
            policy,
            args.auto_remediate,
            set(args.remediate_statuses),
            force=args.force,
            yes=args.yes,
        )
    bundle = build_bundle(stage, reports)
    if remediation_results:
        bundle["remediation"] = {
            "action": args.auto_remediate,
            "statuses": sorted(set(args.remediate_statuses)),
            "results": remediation_results,
        }
    report_path = write_json_report(bundle, output_paths(policy)["reports_dir"], report_prefix)

    if args.format == "json":
        print(json.dumps(bundle, indent=2, ensure_ascii=False))
    else:
        print_text_summary(bundle)
        print(f"JSON report written to: {report_path}")

    return 1 if any(report["decision"]["blocked"] for report in reports) else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SkillGuard security scanner")
    parser.add_argument("--policy", help="Path to a custom policy JSON file")
    parser.add_argument("--format", choices=("text", "json"), default="text")

    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan all installed skills")
    scan_parser.add_argument(
        "--root",
        action="append",
        default=[],
        help="Skill root to scan. Can be passed multiple times.",
    )
    scan_parser.add_argument(
        "--auto-remediate",
        choices=("quarantine", "delete"),
        help="Automatically remediate risky skills after scan",
    )
    scan_parser.add_argument(
        "--remediate-statuses",
        nargs="+",
        choices=("WARN", "BLOCK", "QUARANTINE"),
        default=["BLOCK", "QUARANTINE"],
        help="Recommendations that should trigger auto-remediation",
    )
    scan_parser.add_argument("--force", action="store_true", help="Required for destructive delete remediation")
    scan_parser.add_argument("--yes", action="store_true", help="Acknowledge permanent delete remediation")

    for name, help_text in (
        ("check-install", "Check a skill directory before installation"),
        ("check-update", "Check a skill directory before updating"),
        ("check-exec", "Check a skill directory before execution"),
    ):
        command_parser = subparsers.add_parser(name, help=help_text)
        command_parser.add_argument("target", help="Path to the skill directory to inspect")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return run_scan(args)


if __name__ == "__main__":
    sys.exit(main())
