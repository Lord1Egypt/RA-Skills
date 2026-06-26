#!/usr/bin/env python3
"""
Weak-model validator for skills.

This validator deliberately stays narrow. It checks only explicit execution-style
sections in SKILL.md so it can enforce weak-model-friendly rules without
over-flagging explanatory prose.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

import quick_validate

NAVIGATION_PATTERN = re.compile(
    r"\bRead\s+(?:\[[^\]]+\]\([^\)]+\.md\)|`[^`]+\.md`|references/[^\s`]+\.md)\s+when\b.*\bPurpose:\s*[^.\n]+",
    re.IGNORECASE,
)
ORDERED_STEP_PATTERN = re.compile(r"^\s*\d+\.\s+")
OUTPUT_HINT_PATTERN = re.compile(
    r"\b(write|save|create|return|output|emit|report|print|store|append|send|patch|set|update)\b|`[^`]+`",
    re.IGNORECASE,
)
STOP_HINT_PATTERN = re.compile(r"\b(stop|exit|abort|otherwise|else|continue|finish|done)\b", re.IGNORECASE)
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*)$")
EXECUTION_HEADINGS = {
    "execution",
    "instructions",
    "runtime fallback",
    "steps to run",
}


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    line: int
    message: str


def _extract_body_with_line_numbers(content: str) -> list[tuple[int, str]]:
    lines = content.splitlines()
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                return [(line_no + 1, line) for line_no, line in enumerate(lines[index + 1 :], start=index + 1)]
    return [(line_no, line) for line_no, line in enumerate(lines, start=1)]


def _normalized_heading(line: str) -> tuple[int, str] | None:
    match = HEADING_PATTERN.match(line)
    if not match:
        return None
    level = len(match.group(1))
    title = match.group(2).strip().lower()
    return level, title


def _is_execution_heading(title: str) -> bool:
    return title in EXECUTION_HEADINGS


def _is_template_line(line: str) -> bool:
    return any(token in line for token in ("{", "}", "[", "]", "<", ">"))


def validate_weak_model_readiness(skill_path: str | Path) -> tuple[bool, list[Issue], str]:
    skill_path = Path(skill_path)
    valid, message = quick_validate.validate_skill(skill_path)
    if not valid:
        return False, [Issue("error", "base-validation", 0, message)], "Base validation failed"

    skill_md = skill_path / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")
    body_lines = _extract_body_with_line_numbers(content)

    issues: list[Issue] = []
    in_code_fence = False
    in_execution_section = False
    execution_heading_found = False
    current_execution_level = 0

    for line_no, raw_line in body_lines:
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue

        heading = _normalized_heading(raw_line)
        if heading is not None:
            level, title = heading
            if _is_execution_heading(title):
                in_execution_section = True
                execution_heading_found = True
                current_execution_level = level
            elif in_execution_section and level <= current_execution_level:
                in_execution_section = False
            continue

        if not in_execution_section or not stripped or _is_template_line(stripped):
            continue

        if stripped.lower().startswith("read ") and not NAVIGATION_PATTERN.search(stripped):
            issues.append(
                Issue(
                    "error",
                    "navigation-cue-format",
                    line_no,
                    "Reference loading should use: Read [filename] when [condition]. Purpose: [verb + noun].",
                )
            )

        if ORDERED_STEP_PATTERN.match(stripped):
            has_output = bool(OUTPUT_HINT_PATTERN.search(stripped))
            has_stop = bool(STOP_HINT_PATTERN.search(stripped))
            if not has_output and not has_stop:
                issues.append(
                    Issue(
                        "warning",
                        "missing-output-or-stop",
                        line_no,
                        "Ordered step does not clearly specify an output or stop condition.",
                    )
                )

    if not execution_heading_found:
        issues.append(
            Issue(
                "warning",
                "no-execution-section",
                0,
                "No execution section found. To enable weak-model validation, add `## Execution`, `## Instructions`, `## Runtime Fallback`, or `## Steps to Run` before instruction steps. This warning appears once per file.",
            )
        )

    error_count = sum(1 for issue in issues if issue.severity == "error")
    warning_count = sum(1 for issue in issues if issue.severity == "warning")
    summary = f"Weak-model validation: {error_count} error(s), {warning_count} warning(s)."
    return error_count == 0, issues, summary


def _print_issues(issues: list[Issue]) -> None:
    for issue in issues:
        prefix = "[ERROR]" if issue.severity == "error" else "[WARN]"
        line_info = f"line {issue.line}" if issue.line else "line ?"
        print(f"{prefix} {line_info} {issue.code}: {issue.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate whether a skill is weak-model-friendly.")
    parser.add_argument("skill_directory", help="Path to the skill directory containing SKILL.md")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures as well as errors.",
    )
    args = parser.parse_args()

    ok, issues, summary = validate_weak_model_readiness(args.skill_directory)
    _print_issues(issues)
    print(summary)

    if not ok:
        return 1
    if args.strict and issues:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
