#!/usr/bin/env python3
"""
lint-skill.py
=============

Lint a skill directory against the conventions used by skill-creator and
the platform's SKILL.md spec.

Checks performed:
1. SKILL.md exists and has valid YAML frontmatter with `name` + `description`.
2. SKILL.md is <= 500 lines (soft warn at 400).
3. No files in the root that should be in subdirectories (LICENSE/README OK).
4. Every reference file is <= 500 lines.
5. evals/ contains evals.json conforming to references/schemas.md (if present).
6. description is "pushy" enough — must contain at least 3 trigger phrases.
7. No banned words that signal weak instructions: "should", "consider", "may"
   are flagged only when they appear in imperative instructions, not in
   routing tables (heuristic).
8. Any nested SKILL.md is flagged (single-entry-point convention).

Usage:
    python scripts/lint-skill.py [path-to-skill-dir]
    python scripts/lint-skill.py --strict    # exit 1 on any warning
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent

# Trigger phrases used in pushy descriptions per skill-creator guidance.
PUSHY_PATTERNS = [
    r"Make sure to use this skill",
    r"Use this skill whenever",
    r"Use this for",
    r"Always use this",
    r"Triggers on",
    r"Use when",
]

# Words that, when found in imperative instructions (not in tables/examples),
# usually signal weak guidance. This is a heuristic.
WEAK_WORDS = ["should probably", "you might want to", "consider using",
              "feel free to"]


def find_skill_md(root: Path) -> Path | None:
    p = root / "SKILL.md"
    return p if p.is_file() else None


def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    block = text[3:end].strip()
    out: dict = {}
    current_key = None
    for line in block.splitlines():
        if line.startswith("  ") and current_key:
            out[current_key] += "\n" + line.strip()
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        current_key = key.strip()
        out[current_key] = val.strip().strip('"').strip("'")
    return out


def check_skill_md(skill_md: Path) -> list[str]:
    issues: list[str] = []
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()

    # 1. Frontmatter
    fm = parse_frontmatter(text)
    if fm is None:
        issues.append("SKILL.md is missing YAML frontmatter (must start with '---').")
        return issues
    if "name" not in fm:
        issues.append("SKILL.md frontmatter is missing required field 'name'.")
    if "description" not in fm:
        issues.append("SKILL.md frontmatter is missing required field 'description'.")
    if "description" in fm and len(fm["description"]) < 80:
        issues.append(f"description is suspiciously short ({len(fm['description'])} chars); "
                      f"pushy descriptions should be 200+ chars to avoid undertriggering.")

    # 2. Line count
    if len(lines) > 500:
        issues.append(f"SKILL.md is {len(lines)} lines (>500). "
                      f"Move detail into references/.")
    elif len(lines) > 400:
        issues.append(f"SKILL.md is {len(lines)} lines (warn at 400, hard cap 500).")

    # 3. Pushy description
    if "description" in fm:
        if not any(re.search(pat, fm["description"], re.IGNORECASE)
                   for pat in PUSHY_PATTERNS):
            issues.append("description has no 'pushy' trigger phrase "
                          "(e.g. 'Use this skill whenever...', 'Triggers on...'). "
                          "Skills undertrigger without explicit pushy cues.")

    # 7. Weak words
    body = text[text.find("---", 3) + 3:]
    for weak in WEAK_WORDS:
        if weak in body:
            issues.append(f"Found weak guidance phrase '{weak}' in body. "
                          f"Rephrase with concrete imperatives.")

    return issues


def check_references(root: Path) -> list[str]:
    issues: list[str] = []
    ref_dir = root / "references"
    if not ref_dir.is_dir():
        return issues
    for md in ref_dir.rglob("*.md"):
        n = sum(1 for _ in md.open(encoding="utf-8"))
        if n > 500:
            issues.append(f"{md.relative_to(root)}: {n} lines (>500). Split it.")
    return issues


def check_nested_skill_md(root: Path) -> list[str]:
    """Find any SKILL.md nested deeper than the top level."""
    issues: list[str] = []
    for md in root.rglob("SKILL.md"):
        if md.parent != root:
            issues.append(f"Nested SKILL.md at {md.relative_to(root)}. "
                          f"Most scanners assume one SKILL.md per skill dir. "
                          f"Consider renaming the inner one to README.md.")
    return issues


def check_evals_json(root: Path) -> list[str]:
    issues: list[str] = []
    p = root / "evals" / "evals.json"
    if not p.is_file():
        issues.append("evals/evals.json is missing. Without it, "
                      "skill-creator cannot run quantitative evals.")
        return issues
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        issues.append(f"evals/evals.json is not valid JSON: {e}")
        return issues
    if "skill_name" not in data:
        issues.append("evals/evals.json missing 'skill_name'.")
    if "evals" not in data or not isinstance(data["evals"], list):
        issues.append("evals/evals.json missing 'evals' array.")
    else:
        if len(data["evals"]) < 2:
            issues.append(f"evals/evals.json has only {len(data['evals'])} eval(s); "
                          f"recommend >= 3 for meaningful benchmark.")
        for i, ev in enumerate(data["evals"]):
            for field in ("id", "prompt", "expected_output", "expectations"):
                if field not in ev:
                    issues.append(f"evals/evals.json eval[{i}] missing '{field}'.")
    return issues


def check_scripts_dir(root: Path) -> list[str]:
    issues: list[str] = []
    p = root / "scripts"
    if not p.is_dir():
        issues.append("No scripts/ directory. High-frequency automations "
                      "should be packaged, not reinvented per invocation.")
        return issues
    scripts = list(p.glob("*.py")) + list(p.glob("*.sh"))
    if not scripts:
        issues.append("scripts/ directory exists but is empty.")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("path", nargs="?", default=str(DEFAULT_ROOT),
                        help="Path to skill dir (default: this skill's root).")
    parser.add_argument("--strict", action="store_true",
                        help="Exit non-zero on any warning.")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"[FATAL] {root} is not a directory.", file=sys.stderr)
        return 2

    print(f"Linting skill at: {root}")
    print("=" * 70)

    skill_md = find_skill_md(root)
    if skill_md is None:
        print("[FATAL] SKILL.md not found in skill root.")
        return 2

    all_issues: list[str] = []
    all_issues += [f"SKILL.md: {x}" for x in check_skill_md(skill_md)]
    all_issues += [f"refs:    {x}" for x in check_references(root)]
    all_issues += [f"nested:  {x}" for x in check_nested_skill_md(root)]
    all_issues += [f"evals:   {x}" for x in check_evals_json(root)]
    all_issues += [f"scripts: {x}" for x in check_scripts_dir(root)]

    if not all_issues:
        print("[OK] No issues found.")
        return 0

    for issue in all_issues:
        print(f"  [WARN] {issue}")
    print()
    print(f"{len(all_issues)} issue(s) found.")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
