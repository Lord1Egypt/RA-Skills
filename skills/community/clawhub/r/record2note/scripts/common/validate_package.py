#!/usr/bin/env python3
"""Validate record2note skill package contents before publishing."""

from pathlib import Path
import re
import sys


SKILL_DIR = Path(__file__).resolve().parents[2]


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def main() -> int:
    errors = []

    skill_md = SKILL_DIR / "SKILL.md"
    readme = SKILL_DIR / "README.md"

    if not skill_md.exists():
        errors.append("SKILL.md is missing")
    else:
        content = skill_md.read_text(encoding="utf-8")
        match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not match:
            errors.append("SKILL.md is missing YAML frontmatter")
        else:
            frontmatter = match.group(1)
            if not re.search(r"^name:\s*record2note\s*$", frontmatter, re.MULTILINE):
                errors.append("SKILL.md frontmatter must include name: record2note")

            desc = re.search(r"^description:\s*[\"']?(.*?)[\"']?\s*$", frontmatter, re.MULTILINE)
            if not desc:
                errors.append("SKILL.md frontmatter must include description")
            elif not desc.group(1).startswith("Use when "):
                errors.append('SKILL.md description must start with "Use when "')

            tags = re.search(r"^tags:\s*\[(.*?)\]\s*$", frontmatter, re.MULTILINE)
            if not tags:
                errors.append("SKILL.md frontmatter must include tags as a YAML array")

            if not re.search(r"^min_openclaw:\s*\S+\s*$", frontmatter, re.MULTILINE):
                errors.append("SKILL.md frontmatter must include min_openclaw")

    if not readme.exists():
        errors.append("README.md is missing")
    elif "<your repository URL>" in readme.read_text(encoding="utf-8"):
        errors.append("README.md contains placeholder repository URL")

    forbidden_paths = [
        SKILL_DIR / "config.json",
        SKILL_DIR / ".DS_Store",
        SKILL_DIR / "scripts" / ".DS_Store",
    ]
    for path in forbidden_paths:
        if path.exists():
            errors.append(f"local/generated file must not be packaged: {path.relative_to(SKILL_DIR)}")

    for path in SKILL_DIR.rglob("__pycache__"):
        errors.append(f"generated Python cache must not be packaged: {path.relative_to(SKILL_DIR)}")

    for path in SKILL_DIR.rglob("*.plist"):
        errors.append(f"unsupported plist file must not be packaged: {path.relative_to(SKILL_DIR)}")

    for path in SKILL_DIR.glob("*-plan.md"):
        errors.append(f"development plan should not be in package root: {path.name}")

    for path in SKILL_DIR.glob("*-design.md"):
        errors.append(f"development design doc should not be in package root: {path.name}")

    if errors:
        for error in errors:
            fail(error)
        return 1

    print("record2note package is ready to publish")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
