#!/usr/bin/env python3
"""Compare two mode runs inside one skill-eval run-group."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_skill_dir(skill_dir: Path) -> None:
    if not skill_dir.is_dir():
        raise SystemExit(f"Error: skill directory not found: {skill_dir}")
    if not (skill_dir / "SKILL.md").is_file():
        raise SystemExit(f"Error: SKILL.md not found in {skill_dir}")


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Error: invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Error: expected object JSON in {path}")
    return data


def listify_strings(values) -> list[str]:
    if not isinstance(values, list):
        return []
    result = []
    for value in values:
        if isinstance(value, str):
            stripped = value.strip()
            if stripped:
                result.append(stripped)
    return result


def compare_check(left: dict, right: dict) -> dict:
    left_passed = bool(left.get("passed", False))
    right_passed = bool(right.get("passed", False))
    left_errors = listify_strings(left.get("errors", []))
    right_errors = listify_strings(right.get("errors", []))
    left_notes = listify_strings(left.get("notes", []))
    right_notes = listify_strings(right.get("notes", []))
    return {
        "left_passed": left_passed,
        "right_passed": right_passed,
        "status": "same" if left_passed == right_passed else "changed",
        "left_only_errors": sorted(set(left_errors) - set(right_errors)),
        "right_only_errors": sorted(set(right_errors) - set(left_errors)),
        "left_only_notes": sorted(set(left_notes) - set(right_notes)),
        "right_only_notes": sorted(set(right_notes) - set(left_notes)),
    }


def compare_summaries(left_summary: dict, right_summary: dict, left_mode: str, right_mode: str) -> dict:
    left_checks = left_summary.get("checks", {})
    right_checks = right_summary.get("checks", {})
    if not isinstance(left_checks, dict):
        left_checks = {}
    if not isinstance(right_checks, dict):
        right_checks = {}

    all_check_names = sorted(set(left_checks.keys()) | set(right_checks.keys()))
    checks = {
        name: compare_check(left_checks.get(name, {}), right_checks.get(name, {}))
        for name in all_check_names
    }

    left_overall = bool(left_summary.get("overall_passed", False))
    right_overall = bool(right_summary.get("overall_passed", False))
    return {
        "generated_at": iso_now(),
        "left_mode": left_mode,
        "right_mode": right_mode,
        "overall": {
            "left_passed": left_overall,
            "right_passed": right_overall,
            "status": "same" if left_overall == right_overall else "changed",
        },
        "checks": checks,
    }


def make_md(skill_name: str, run_group: str, comparison: dict) -> str:
    left_mode = comparison["left_mode"]
    right_mode = comparison["right_mode"]
    overall = comparison["overall"]
    lines = [
        f"# Skill Eval Comparison: {skill_name}",
        "",
        f"- Run group: {run_group}",
        f"- Generated: {comparison['generated_at']}",
        f"- Left mode: {left_mode}",
        f"- Right mode: {right_mode}",
        f"- Overall status: {overall['status']}",
        f"- {left_mode}: {'pass' if overall['left_passed'] else 'fail'}",
        f"- {right_mode}: {'pass' if overall['right_passed'] else 'fail'}",
        "",
    ]

    for check_name, check in comparison["checks"].items():
        lines.append(f"## {check_name}")
        lines.append("")
        lines.append(f"- Status: {check['status']}")
        lines.append(f"- {left_mode}: {'pass' if check['left_passed'] else 'fail'}")
        lines.append(f"- {right_mode}: {'pass' if check['right_passed'] else 'fail'}")
        for err in check["left_only_errors"]:
            lines.append(f"- Only in {left_mode} errors: {err}")
        for err in check["right_only_errors"]:
            lines.append(f"- Only in {right_mode} errors: {err}")
        for note in check["left_only_notes"]:
            lines.append(f"- Only in {left_mode} notes: {note}")
        for note in check["right_only_notes"]:
            lines.append(f"- Only in {right_mode} notes: {note}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def missing_summary_message(run_group_dir: Path, left_mode: str, right_mode: str, left_summary_path: Path, right_summary_path: Path) -> str:
    missing = []
    if not left_summary_path.is_file():
        missing.append(f"- missing {left_mode}: {left_summary_path}")
    if not right_summary_path.is_file():
        missing.append(f"- missing {right_mode}: {right_summary_path}")

    available_modes = []
    for mode_dir in sorted(path for path in run_group_dir.iterdir() if path.is_dir()):
        if (mode_dir / "summary.json").is_file():
            available_modes.append(mode_dir.name)

    lines = ["Error: compare_runs needs finished run outputs for both modes."]
    lines.extend(missing)
    lines.append(f"- available summaries: {', '.join(available_modes) if available_modes else 'none'}")
    lines.append("- next step: run the missing mode(s) with run_eval.py, then retry compare_runs.py")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two mode runs in one run-group.")
    parser.add_argument("skill_dir", help="Path to the target skill directory")
    parser.add_argument("--run-group", required=True, help="Run group name under evals/runs/")
    parser.add_argument("--left-mode", default="with-skill", choices=["with-skill", "without-skill"])
    parser.add_argument("--right-mode", default="without-skill", choices=["with-skill", "without-skill"])
    args = parser.parse_args()

    if args.left_mode == args.right_mode:
        raise SystemExit("Error: left-mode and right-mode must be different.")

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    ensure_skill_dir(skill_dir)

    run_group_dir = skill_dir / "evals" / "runs" / args.run_group
    if not run_group_dir.is_dir():
        raise SystemExit(
            f"Error: run group not found: {run_group_dir}\n"
            "- next step: run run_eval.py first, then retry compare_runs.py"
        )

    left_summary_path = run_group_dir / args.left_mode / "summary.json"
    right_summary_path = run_group_dir / args.right_mode / "summary.json"
    if not left_summary_path.is_file() or not right_summary_path.is_file():
        raise SystemExit(
            missing_summary_message(
                run_group_dir,
                args.left_mode,
                args.right_mode,
                left_summary_path,
                right_summary_path,
            )
        )

    left_summary = load_json(left_summary_path)
    right_summary = load_json(right_summary_path)
    comparison = compare_summaries(left_summary, right_summary, args.left_mode, args.right_mode)

    comparison_json_path = run_group_dir / "comparison.json"
    comparison_md_path = run_group_dir / "comparison.md"
    comparison_json_path.write_text(json.dumps(comparison, ensure_ascii=False, indent=2) + "\n")
    comparison_md_path.write_text(make_md(skill_dir.name, args.run_group, comparison))

    print(f"Skill: {skill_dir.name}")
    print(f"Run group: {args.run_group}")
    print(f"Compared: {args.left_mode} vs {args.right_mode}")
    print(f"Output: {comparison_json_path}")
    print(f"Overall status: {comparison['overall']['status']}")
    for check_name, check in comparison["checks"].items():
        print(f"- {check_name}: {check['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
