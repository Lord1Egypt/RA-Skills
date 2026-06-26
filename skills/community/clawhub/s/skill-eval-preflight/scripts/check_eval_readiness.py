#!/usr/bin/env python3
"""Check whether an OpenClaw skill is ready for first-pass evaluation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PLACEHOLDER_MARKERS = ("[TODO", "TODO:", "<TODO", "placeholder")


def has_placeholder(text: str) -> bool:
    upper = text.upper()
    return any(marker.upper() in upper for marker in PLACEHOLDER_MARKERS)


def load_frontmatter(skill_md_path: Path) -> dict[str, str]:
    content = skill_md_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md is missing YAML frontmatter.")

    end_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end_index = index
            break
    if end_index is None:
        raise ValueError("SKILL.md frontmatter is not closed.")

    frontmatter_lines = lines[1:end_index]
    parsed: dict[str, str] = {}
    current_key: str | None = None
    for raw_line in frontmatter_lines:
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if raw_line[:1].isspace():
            if current_key is None:
                raise ValueError("Invalid frontmatter indentation.")
            current_value = parsed[current_key]
            parsed[current_key] = f"{current_value}\n{stripped}" if current_value else stripped
            continue

        if ":" not in stripped:
            raise ValueError("Unsupported frontmatter syntax.")

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        parsed[key] = value
        current_key = key

    return parsed


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def has_usable_eval_case(evals) -> bool:
    if not isinstance(evals, list):
        return False
    for case in evals:
        if not isinstance(case, dict):
            continue
        prompt = case.get("prompt")
        if isinstance(prompt, str) and prompt.strip() and not has_placeholder(prompt):
            return True
    return False


def has_usable_trigger_case(cases) -> bool:
    if not isinstance(cases, list):
        return False
    for case in cases:
        if not isinstance(case, dict):
            continue
        prompt = case.get("prompt")
        if isinstance(prompt, str) and prompt.strip() and not has_placeholder(prompt):
            return True
    return False


def check_readiness(skill_dir: Path) -> tuple[bool, list[str], list[str]]:
    ok_messages: list[str] = []
    missing_messages: list[str] = []

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return False, ok_messages, [f"SKILL.md not found in {skill_dir}"]

    try:
        frontmatter = load_frontmatter(skill_md)
    except ValueError as exc:
        return False, ok_messages, [str(exc)]

    description = frontmatter.get("description", "")
    if not isinstance(description, str) or not description.strip():
        missing_messages.append("SKILL.md description is missing.")
    elif has_placeholder(description):
        missing_messages.append("SKILL.md description still looks like a placeholder.")
    else:
        ok_messages.append("description looks real")

    evals_path = skill_dir / "evals" / "evals.json"
    if not evals_path.is_file():
        missing_messages.append("evals/evals.json is missing.")
    else:
        try:
            evals = load_json(evals_path)
        except ValueError as exc:
            missing_messages.append(str(exc))
        else:
            if has_usable_eval_case(evals):
                ok_messages.append("1 eval case(s) look usable")
            else:
                missing_messages.append("evals/evals.json needs at least one non-placeholder prompt.")

    triggers_path = skill_dir / "evals" / "triggers.json"
    if not triggers_path.is_file():
        missing_messages.append("evals/triggers.json is missing.")
    else:
        try:
            triggers = load_json(triggers_path)
        except ValueError as exc:
            missing_messages.append(str(exc))
        else:
            should_trigger = triggers.get("should_trigger") if isinstance(triggers, dict) else None
            should_not_trigger = triggers.get("should_not_trigger") if isinstance(triggers, dict) else None
            if has_usable_trigger_case(should_trigger):
                ok_messages.append("1 positive trigger case(s) look usable")
            else:
                missing_messages.append("evals/triggers.json needs at least one positive trigger case.")
            if has_usable_trigger_case(should_not_trigger):
                ok_messages.append("1 negative trigger case(s) look usable")
            else:
                missing_messages.append("evals/triggers.json needs at least one negative trigger case.")

    return not missing_messages, ok_messages, missing_messages


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether a skill is ready for first eval.")
    parser.add_argument("skill_dir", help="Path to the target skill directory")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    if not skill_dir.is_dir():
        raise SystemExit(f"Error: skill directory not found: {skill_dir}")

    ready, ok_messages, missing_messages = check_readiness(skill_dir)
    print(f"Skill: {skill_dir.name}")
    print(f"Ready: {'yes' if ready else 'no'}")
    for message in ok_messages:
        print(f"- OK: {message}")
    for message in missing_messages:
        print(f"- Missing: {message}")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
