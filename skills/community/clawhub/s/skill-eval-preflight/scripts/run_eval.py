#!/usr/bin/env python3
"""Run first-pass eval checks for an OpenClaw skill."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from check_eval_readiness import (
    check_readiness,
    has_placeholder,
    load_frontmatter,
    load_json,
)


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S-%f")


def ensure_skill_dir(skill_dir: Path) -> None:
    if not skill_dir.is_dir():
        raise SystemExit(f"Error: skill directory not found: {skill_dir}")
    if not (skill_dir / "SKILL.md").is_file():
        raise SystemExit(f"Error: SKILL.md not found in {skill_dir}")


def resolve_run_dirs(skill_dir: Path, run_group: str | None, mode: str) -> tuple[str, Path]:
    resolved_group = run_group or run_stamp()
    run_root = skill_dir / "evals" / "runs" / resolved_group
    run_dir = run_root / mode
    run_dir.mkdir(parents=True, exist_ok=False)
    return resolved_group, run_dir


def evaluate_trigger_cases(cases, label: str) -> tuple[bool, list[dict], list[str]]:
    case_results = []
    errors = []

    if not isinstance(cases, list) or not cases:
        errors.append(f"{label} is missing or empty.")
        return False, case_results, errors

    for index, case in enumerate(cases, start=1):
        case_id = f"{label}-{index}"
        if not isinstance(case, dict):
            case_results.append({"id": case_id, "passed": False, "reason": "case must be an object"})
            continue
        raw_id = case.get("id")
        if isinstance(raw_id, str) and raw_id.strip():
            case_id = raw_id.strip()
        prompt = case.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            case_results.append({"id": case_id, "passed": False, "reason": "prompt is missing or empty"})
            continue
        if has_placeholder(prompt):
            case_results.append({"id": case_id, "passed": False, "reason": "prompt still contains placeholder text"})
            continue
        case_results.append({"id": case_id, "passed": True, "reason": "prompt looks usable"})

    passed = all(item["passed"] for item in case_results) and not errors
    return passed, case_results, errors


def check_triggers(skill_dir: Path) -> dict:
    errors = []
    notes = []

    try:
        frontmatter = load_frontmatter(skill_dir / "SKILL.md")
    except ValueError as exc:
        return {"passed": False, "notes": notes, "errors": [str(exc)], "positive_cases": [], "negative_cases": []}

    description = frontmatter.get("description", "")
    if not isinstance(description, str) or not description.strip():
        errors.append("Frontmatter description is missing or empty.")
    elif has_placeholder(description):
        errors.append("Frontmatter description still looks like a placeholder.")
    else:
        notes.append("description looks usable for trigger coverage review")

    triggers_path = skill_dir / "evals" / "triggers.json"
    if not triggers_path.is_file():
        return {"passed": False, "notes": notes, "errors": errors + ["evals/triggers.json is missing."], "positive_cases": [], "negative_cases": []}

    try:
        triggers = load_json(triggers_path)
    except ValueError as exc:
        return {"passed": False, "notes": notes, "errors": errors + [str(exc)], "positive_cases": [], "negative_cases": []}

    if not isinstance(triggers, dict):
        return {"passed": False, "notes": notes, "errors": errors + ["evals/triggers.json must be an object."], "positive_cases": [], "negative_cases": []}

    positive_ok, positive_cases, positive_errors = evaluate_trigger_cases(triggers.get("should_trigger"), "should_trigger")
    negative_ok, negative_cases, negative_errors = evaluate_trigger_cases(triggers.get("should_not_trigger"), "should_not_trigger")

    errors.extend(positive_errors)
    errors.extend(negative_errors)
    if positive_cases:
        notes.append(f"{sum(1 for item in positive_cases if item['passed'])}/{len(positive_cases)} positive trigger case(s) usable")
    if negative_cases:
        notes.append(f"{sum(1 for item in negative_cases if item['passed'])}/{len(negative_cases)} negative trigger case(s) usable")

    return {
        "passed": not errors and positive_ok and negative_ok,
        "notes": notes,
        "errors": errors,
        "positive_cases": positive_cases,
        "negative_cases": negative_cases,
    }


def evaluate_artifact_cases(evals) -> tuple[bool, list[dict], list[str], list[str]]:
    case_results = []
    errors = []
    notes = []

    if not isinstance(evals, list) or not evals:
        return False, case_results, ["evals/evals.json is missing or empty."], notes

    for index, case in enumerate(evals, start=1):
        case_id = f"eval-{index}"
        case_errors = []
        if not isinstance(case, dict):
            case_results.append({"id": case_id, "passed": False, "reason": "case must be an object"})
            continue

        raw_id = case.get("id")
        if isinstance(raw_id, str) and raw_id.strip():
            case_id = raw_id.strip()

        prompt = case.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            case_errors.append("prompt is missing or empty")
        elif has_placeholder(prompt):
            case_errors.append("prompt still contains placeholder text")

        expected_artifacts = case.get("expected_artifacts")
        valid_artifacts = []
        if not isinstance(expected_artifacts, list) or not expected_artifacts:
            case_errors.append("expected_artifacts is missing or empty")
        else:
            for artifact in expected_artifacts:
                if not isinstance(artifact, str):
                    continue
                text = artifact.strip()
                if not text or has_placeholder(text):
                    continue
                valid_artifacts.append(text)
            if not valid_artifacts:
                case_errors.append("expected_artifacts needs at least one non-placeholder string")

        if case_errors:
            case_results.append({"id": case_id, "passed": False, "reason": "; ".join(case_errors)})
            continue

        notes.append(f"{case_id} defines {len(valid_artifacts)} usable expected artifact(s)")
        case_results.append({"id": case_id, "passed": True, "reason": f"{len(valid_artifacts)} usable expected artifact(s)"})

    return not errors and all(item["passed"] for item in case_results), case_results, errors, notes


def check_artifacts(skill_dir: Path) -> dict:
    evals_path = skill_dir / "evals" / "evals.json"
    if not evals_path.is_file():
        return {"passed": False, "notes": [], "errors": ["evals/evals.json is missing."], "cases": []}

    try:
        evals = load_json(evals_path)
    except ValueError as exc:
        return {"passed": False, "notes": [], "errors": [str(exc)], "cases": []}

    passed, case_results, errors, notes = evaluate_artifact_cases(evals)
    if case_results:
        notes.insert(0, f"{sum(1 for item in case_results if item['passed'])}/{len(case_results)} eval case(s) have usable expected artifacts")
    return {"passed": passed, "notes": notes, "errors": errors, "cases": case_results}


def evaluate_file_cases(evals) -> tuple[bool, list[dict], list[str], list[str]]:
    case_results = []
    errors = []
    notes = []
    declared_case_count = 0

    if not isinstance(evals, list) or not evals:
        return False, case_results, ["evals/evals.json is missing or empty."], notes

    for index, case in enumerate(evals, start=1):
        case_id = f"eval-{index}"
        if not isinstance(case, dict):
            case_results.append({"id": case_id, "passed": False, "reason": "case must be an object"})
            continue

        raw_id = case.get("id")
        if isinstance(raw_id, str) and raw_id.strip():
            case_id = raw_id.strip()

        files = case.get("files", [])
        if files is None:
            files = []
        if not isinstance(files, list):
            case_results.append({"id": case_id, "passed": False, "reason": "files must be a list when present"})
            continue

        if not files:
            case_results.append({"id": case_id, "passed": True, "reason": "no file constraints declared"})
            continue

        declared_case_count += 1
        invalid_entries = []
        for item in files:
            if not isinstance(item, str):
                invalid_entries.append("non-string file entry")
                continue
            stripped = item.strip()
            if not stripped or has_placeholder(stripped):
                invalid_entries.append("placeholder or empty file path")

        if invalid_entries:
            case_results.append({"id": case_id, "passed": False, "reason": "; ".join(sorted(set(invalid_entries)))})
            continue

        notes.append(f"{case_id} declares {len(files)} file path(s)")
        case_results.append({"id": case_id, "passed": True, "reason": f"{len(files)} file path(s) declared cleanly"})

    notes.insert(0, f"{declared_case_count}/{len(case_results)} eval case(s) declare file paths")
    return not errors and all(item["passed"] for item in case_results), case_results, errors, notes


def check_files(skill_dir: Path) -> dict:
    evals_path = skill_dir / "evals" / "evals.json"
    if not evals_path.is_file():
        return {"passed": False, "notes": [], "errors": ["evals/evals.json is missing."], "cases": []}

    try:
        evals = load_json(evals_path)
    except ValueError as exc:
        return {"passed": False, "notes": [], "errors": [str(exc)], "cases": []}

    passed, case_results, errors, notes = evaluate_file_cases(evals)
    return {"passed": passed, "notes": notes, "errors": errors, "cases": case_results}


def serialize_readiness(skill_dir: Path) -> dict:
    ready, ok_messages, missing_messages = check_readiness(skill_dir)
    return {"passed": ready, "notes": ok_messages, "errors": missing_messages}


def build_checks(skill_dir: Path, selected_checks: list[str]) -> dict[str, dict]:
    checks = {}
    for check_name in selected_checks:
        if check_name == "readiness":
            checks[check_name] = serialize_readiness(skill_dir)
        elif check_name == "triggers":
            checks[check_name] = check_triggers(skill_dir)
        elif check_name == "artifacts":
            checks[check_name] = check_artifacts(skill_dir)
        elif check_name == "files":
            checks[check_name] = check_files(skill_dir)
        else:
            raise SystemExit(f"Error: unsupported check: {check_name}")
    return checks


def make_summary_md(skill_name: str, summary: dict) -> str:
    lines = [
        f"# Skill Eval Summary: {skill_name}",
        "",
        f"- Generated: {summary['generated_at']}",
        f"- Mode: {summary['mode']}",
        f"- Run group: {summary['run_group']}",
        f"- Overall: {'pass' if summary['overall_passed'] else 'fail'}",
        "",
    ]

    for check_name, result in summary["checks"].items():
        lines.append(f"## {check_name}")
        lines.append("")
        lines.append(f"- Status: {'pass' if result['passed'] else 'fail'}")
        for note in result.get("notes", []):
            lines.append(f"- Note: {note}")
        for error in result.get("errors", []):
            lines.append(f"- Error: {error}")
        for key in ("positive_cases", "negative_cases", "cases"):
            for case in result.get(key, []):
                status = "pass" if case.get("passed") else "fail"
                lines.append(f"- Case {case.get('id', 'unknown')}: {status} ({case.get('reason', 'no reason')})")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run static eval checks for a skill.")
    parser.add_argument("skill_dir", help="Path to the target skill directory")
    parser.add_argument(
        "--check",
        action="append",
        choices=["readiness", "triggers", "artifacts", "files"],
        help="Specific check(s) to run. Defaults to all.",
    )
    parser.add_argument("--mode", default="with-skill", choices=["with-skill", "without-skill"])
    parser.add_argument("--run-group", help="Optional run-group name under evals/runs/")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    ensure_skill_dir(skill_dir)

    checks_to_run = args.check or ["readiness", "triggers", "artifacts", "files"]
    run_group, run_dir = resolve_run_dirs(skill_dir, args.run_group, args.mode)
    checks = build_checks(skill_dir, checks_to_run)
    overall_passed = all(result.get("passed", False) for result in checks.values())

    summary = {
        "skill_name": skill_dir.name,
        "generated_at": iso_now(),
        "mode": args.mode,
        "run_group": run_group,
        "overall_passed": overall_passed,
        "checks": checks,
    }
    run_metadata = {
        "skill_name": skill_dir.name,
        "skill_dir": str(skill_dir),
        "generated_at": summary["generated_at"],
        "run_group": run_group,
        "mode": args.mode,
        "checks_run": checks_to_run,
        "execution_kind": "static-eval-mvp",
        "notes": [
            "This run does not execute the skill inside the OpenClaw runtime.",
            "with-skill and without-skill are mode labels for a stable baseline directory model.",
        ],
    }

    (run_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    (run_dir / "summary.md").write_text(make_summary_md(skill_dir.name, summary))
    (run_dir / "run_metadata.json").write_text(json.dumps(run_metadata, ensure_ascii=False, indent=2) + "\n")

    print(f"Skill: {skill_dir.name}")
    print(f"Overall: {'pass' if overall_passed else 'fail'}")
    print(f"Mode: {args.mode}")
    print(f"Run group: {run_group}")
    print(f"Run dir: {run_dir}")
    for check_name, result in checks.items():
        print(f"- {check_name}: {'pass' if result['passed'] else 'fail'}")
    return 0 if overall_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
