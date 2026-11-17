#!/usr/bin/env python3
"""Validate the portable frontmatter of a skill directory."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}


def validate(skill_dir: Path) -> None:
    skill_file = skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")

    try:
        raw_frontmatter, _ = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError("SKILL.md frontmatter is not closed") from exc

    frontmatter = yaml.safe_load(raw_frontmatter)
    if not isinstance(frontmatter, dict):
        raise ValueError("frontmatter must be a mapping")

    missing = {"name", "description"} - frontmatter.keys()
    if missing:
        raise ValueError(f"missing required keys: {sorted(missing)}")

    unknown = set(frontmatter) - ALLOWED_KEYS
    if unknown:
        raise ValueError(f"unsupported frontmatter keys: {sorted(unknown)}")

    if frontmatter["name"] != skill_dir.resolve().name:
        raise ValueError("frontmatter name must match the skill directory")

    description = frontmatter["description"]
    if not isinstance(description, str) or not description.strip():
        raise ValueError("description must be a non-empty string")
    if len(description) > 1024:
        raise ValueError("description must contain at most 1024 characters")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", nargs="?", default=".")
    args = parser.parse_args()
    validate(Path(args.skill_dir))
    print("Skill frontmatter is valid.")


if __name__ == "__main__":
    main()
