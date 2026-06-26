#!/usr/bin/env python3
"""Quick validation for a skill directory.

This validator intentionally stays lightweight and dependency-free.
It checks core frontmatter quality plus a few structural promises that the
repo's own guidance depends on.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata"}
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
BACKTICK_PATH_RE = re.compile(r"`([^`]+)`")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str] | tuple[None, str]:
    if not text.startswith("---\n"):
        return None, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not match:
        return None, "Invalid frontmatter format"

    raw_frontmatter = match.group(1)
    body = match.group(2)
    data: dict[str, str] = {}

    for line in raw_frontmatter.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            return None, f"Invalid frontmatter line: {line}"
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            return None, f"Invalid frontmatter key in line: {line}"
        data[key] = value

    return data, body


def referenced_markdown_links(skill_path: Path, text: str) -> list[str]:
    refs: list[str] = []
    for target in MARKDOWN_LINK_RE.findall(text):
        target = target.strip()
        if not target or "://" in target or target.startswith("#"):
            continue
        refs.append(target)
    return refs


def referenced_backtick_paths(text: str) -> list[str]:
    refs: list[str] = []
    for token in BACKTICK_PATH_RE.findall(text):
        token = token.strip()
        if "/" in token or token.endswith(".md") or token.endswith(".py") or token.endswith(".sh"):
            refs.append(token)
    return refs


def script_test_pairs(skill_path: Path) -> list[str]:
    scripts_dir = skill_path / "scripts"
    tests_dir = skill_path / "tests"
    issues: list[str] = []

    if not scripts_dir.exists() or not tests_dir.exists():
        return issues

    for script in sorted(p for p in scripts_dir.iterdir() if p.is_file() and p.suffix in {".py", ".sh"}):
        expected = tests_dir / f"test_{script.stem}{script.suffix}"
        if not expected.exists():
            issues.append(f"Missing paired test for script: {script.relative_to(skill_path)} -> expected {expected.relative_to(skill_path)}")
    return issues


def validate_skill(skill_path: str | Path):
    skill_path = Path(skill_path).resolve()

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    text = skill_md.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    if frontmatter is None:
        return False, body

    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    name = frontmatter.get("name", "").strip()
    description = frontmatter.get("description", "").strip()

    if not name:
        return False, "Missing 'name' in frontmatter"
    if not re.fullmatch(r"[a-z0-9-]+", name):
        return False, f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)"
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
    if len(name) > 64:
        return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    if not description:
        return False, "Missing 'description' in frontmatter"
    if len(description) > 1024:
        return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."
    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets (< or >)"

    issues: list[str] = []

    if "project.skill.template.md" in text and not (skill_path / "project.skill.template.md").exists():
        issues.append("SKILL.md references `project.skill.template.md` but the file is missing")

    if "project.md" in text:
        issues.append("Found `project.md` reference. Use `project.skill.template.md` / `project.skill.md` instead")

    for ref in referenced_markdown_links(skill_path, text):
        if not (skill_path / ref).exists():
            issues.append(f"Broken markdown link in SKILL.md: {ref}")

    for ref in referenced_backtick_paths(text):
        if ref in {"project.skill.md", "SKILL.md"}:
            continue
        candidate = skill_path / ref
        if ref.startswith("examples/") or ref.startswith("references/") or ref.startswith("scripts/") or ref.startswith("tests/") or ref.startswith("self-healing/"):
            if not candidate.exists():
                issues.append(f"Referenced path in SKILL.md is missing: {ref}")

    issues.extend(script_test_pairs(skill_path))

    if issues:
        return False, "; ".join(issues)

    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 quick_validate.py <skill_directory>")
        raise SystemExit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    raise SystemExit(0 if valid else 1)
