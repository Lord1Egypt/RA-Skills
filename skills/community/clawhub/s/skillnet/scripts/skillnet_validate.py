#!/usr/bin/env python3
"""skillnet_validate.py — Lightweight offline structural validation for a skill directory.

Usage:
  python skillnet_validate.py path/to/skill-dir
  python skillnet_validate.py path/to/skill-dir --strict

Checks SKILL.md frontmatter, directory layout, and naming conventions.
Does NOT require API_KEY or network access — purely local validation.
"""
import argparse
import os
import re
import sys
from typing import Dict, List, Optional

REQUIRED_FRONTMATTER = {"name", "description"}
NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]*[a-z0-9]$")
MAX_DESCRIPTION_LINES = 15
MAX_SKILL_MD_LINES = 500


def parse_frontmatter(text: str) -> Optional[Dict[str, str]]:
    """Extract YAML-ish frontmatter from SKILL.md (between --- delimiters)."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip()
    result = {}
    current_key = None
    for line in block.split("\n"):
        if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "|":
                current_key = key
                result[key] = ""
            else:
                current_key = None
                result[key] = val
        elif current_key and (line.startswith("  ") or line.startswith("\t")):
            result[current_key] += line.strip() + "\n"
    for k in result:
        if isinstance(result[k], str):
            result[k] = result[k].strip()
    return result


def validate(skill_dir: str, strict: bool = False) -> List[str]:
    """Return list of issues found (empty = all good)."""
    issues = []
    skill_md = os.path.join(skill_dir, "SKILL.md")

    # --- SKILL.md existence ---
    if not os.path.isfile(skill_md):
        issues.append("SKILL.md not found")
        return issues

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    if len(lines) > MAX_SKILL_MD_LINES:
        issues.append(f"SKILL.md is {len(lines)} lines (recommended ≤{MAX_SKILL_MD_LINES})")

    # --- Frontmatter ---
    fm = parse_frontmatter(content)
    if fm is None:
        issues.append("No YAML frontmatter (expected --- delimiters)")
        return issues

    for field in REQUIRED_FRONTMATTER:
        if field not in fm or not fm[field]:
            issues.append(f"Missing required frontmatter field: {field}")

    name = fm.get("name", "")
    if name and not NAME_PATTERN.match(name):
        issues.append(f"Name '{name}' should be lowercase alphanumeric with hyphens (e.g., my-skill)")

    desc = fm.get("description", "")
    if desc:
        desc_lines = [l for l in desc.split("\n") if l.strip()]
        if len(desc_lines) > MAX_DESCRIPTION_LINES:
            issues.append(f"Description is {len(desc_lines)} lines (recommended ≤{MAX_DESCRIPTION_LINES})")

    # --- Directory layout ---
    if strict:
        refs_dir = os.path.join(skill_dir, "references")
        scripts_dir = os.path.join(skill_dir, "scripts")
        if not os.path.isdir(refs_dir):
            issues.append("Missing references/ directory (recommended for progressive disclosure)")
        if not os.path.isdir(scripts_dir):
            issues.append("Missing scripts/ directory (recommended for automation)")

    # --- Empty files ---
    for root, _dirs, files in os.walk(skill_dir):
        for fname in files:
            fpath = os.path.join(root, fname)
            if os.path.getsize(fpath) == 0:
                rel = os.path.relpath(fpath, skill_dir)
                issues.append(f"Empty file: {rel}")

    return issues


def main():
    parser = argparse.ArgumentParser(
        description="Validate skill directory structure (offline, no API_KEY needed).",
        epilog="Use --strict to also check for references/ and scripts/ directories.",
    )
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument("--strict", action="store_true",
                        help="Also check for references/ and scripts/ dirs")
    args = parser.parse_args()

    if not os.path.isdir(args.skill_dir):
        print(f"ERROR: Not a directory: {args.skill_dir}", file=sys.stderr)
        sys.exit(1)

    issues = validate(args.skill_dir, strict=args.strict)

    if not issues:
        print(f"✅ {os.path.basename(args.skill_dir)}: all checks passed")
        sys.exit(0)
    else:
        print(f"⚠️  {os.path.basename(args.skill_dir)}: {len(issues)} issue(s) found:")
        for issue in issues:
            print(f"   • {issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
