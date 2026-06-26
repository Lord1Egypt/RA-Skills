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
from lib.discovery import build_skill_target, resolve_workspace
from lib.policy import evaluate_findings, load_policy
from lib.remediation import (
    delete_skill,
    list_quarantined,
    quarantine_skill,
    remediate_skill,
    resolve_skill_reference,
    restore_skill,
)


DEFAULT_REMEDIATE_STATUSES = {"BLOCK", "QUARANTINE"}


def inspect_skill(target_reference: str, policy: dict, stage: str = "scan") -> dict:
    target_path = resolve_skill_reference(target_reference, policy)
    target = build_skill_target(target_path, policy, resolve_workspace())
    static_result = analyze_static(target, policy)
    ai_result = audit_with_ai(target, policy)
    decision = evaluate_findings(policy, target, static_result, ai_result, stage)
    return {
        "target_path": str(target_path),
        "skill_name": target.name,
        "static_analysis": static_result,
        "ai_audit": ai_result,
        "decision": decision,
    }


def scan_and_remediate(
    target_reference: str,
    policy: dict,
    action: str,
    statuses: set[str] | None = None,
    *,
    force: bool = False,
    yes: bool = False,
) -> dict:
    statuses = {status.upper() for status in (statuses or DEFAULT_REMEDIATE_STATUSES)}
    inspection = inspect_skill(target_reference, policy, stage="scan")
    recommendation = inspection["decision"]["recommendation"].upper()
    result = {
        "target_path": inspection["target_path"],
        "skill_name": inspection["skill_name"],
        "decision": inspection["decision"],
        "requested_action": action,
        "statuses": sorted(statuses),
    }

    if recommendation not in statuses:
        result["action"] = "noop"
        result["reason"] = f"Recommendation {recommendation} is outside remediation statuses."
        return result

    if action == "delete" and (not force or not yes):
        raise ValueError("delete remediation requires both --force and --yes")

    reason = (
        f"SkillGuard clean: {inspection['decision']['recommendation']} "
        f"risk={inspection['decision']['risk_score']}"
    )
    remediation = remediate_skill(Path(inspection["target_path"]), policy, action, reason=reason)
    result["action"] = action
    result["remediation"] = remediation
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SkillGuard remediation manager")
    parser.add_argument("--policy", help="Path to a custom policy JSON file")
    parser.add_argument("--format", choices=("text", "json"), default="text")

    subparsers = parser.add_subparsers(dest="command", required=True)

    quarantine_parser = subparsers.add_parser("quarantine", help="Move a skill into quarantine")
    quarantine_parser.add_argument("target", help="Skill name or path")
    quarantine_parser.add_argument("--reason", default="Manual quarantine requested")

    restore_parser = subparsers.add_parser("restore", help="Restore a quarantined skill")
    restore_parser.add_argument("target", help="Skill name, original path, or quarantined path")

    delete_parser = subparsers.add_parser("delete", help="Permanently delete a skill")
    delete_parser.add_argument("target", help="Skill name or path")
    delete_parser.add_argument("--force", action="store_true", help="Required for destructive deletion")
    delete_parser.add_argument("--yes", action="store_true", help="Acknowledge permanent deletion")

    for command_name in ("clean", "disinfect"):
        clean_parser = subparsers.add_parser(command_name, help="Scan a skill and remediate if it is risky")
        clean_parser.add_argument("target", help="Skill name or path")
        clean_parser.add_argument("--action", choices=("quarantine", "delete"), default="quarantine")
        clean_parser.add_argument(
            "--statuses",
            nargs="+",
            choices=("WARN", "BLOCK", "QUARANTINE"),
            default=["BLOCK", "QUARANTINE"],
            help="Recommendations that should trigger remediation",
        )
        clean_parser.add_argument("--force", action="store_true", help="Required for destructive deletion")
        clean_parser.add_argument("--yes", action="store_true", help="Acknowledge permanent deletion")

    subparsers.add_parser("list", help="List quarantined skills")
    return parser


def emit(payload, output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    if isinstance(payload, list):
        if not payload:
            print("No quarantined skills.")
            return
        print("Quarantined skills:")
        for item in payload:
            print(f"- {item['skill_name']} :: {item['quarantine_path']} -> {item['original_path']}")
        return

    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main() -> int:
    args = build_parser().parse_args()
    policy = load_policy(args.policy)

    try:
        if args.command == "quarantine":
            target_path = resolve_skill_reference(args.target, policy)
            result = quarantine_skill(target_path, policy, args.reason)
        elif args.command == "restore":
            result = restore_skill(args.target, policy)
        elif args.command == "delete":
            if not args.force or not args.yes:
                raise ValueError("delete requires both --force and --yes")
            result = delete_skill(args.target, policy)
        elif args.command in {"clean", "disinfect"}:
            result = scan_and_remediate(
                args.target,
                policy,
                action=args.action,
                statuses=set(args.statuses),
                force=args.force,
                yes=args.yes,
            )
        else:
            result = list_quarantined(policy)
    except Exception as exc:  # noqa: BLE001
        if args.format == "json":
            print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        else:
            print(f"Error: {exc}")
        return 1

    emit(result, args.format)
    return 0


if __name__ == "__main__":
    sys.exit(main())
