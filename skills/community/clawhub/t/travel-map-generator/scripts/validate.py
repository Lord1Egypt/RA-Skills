#!/usr/bin/env python3
"""Validate skill structure and content against the Agent Skills Open Standard.

Usage:
    python3 scripts/validate.py [SKILL_DIR]

If SKILL_DIR is not provided, validates the current skill directory.
"""

import os
import re
import sys
from pathlib import Path


def validate_frontmatter(skill_dir):
    """Validate SKILL.md frontmatter."""
    errors = []
    warnings = []

    skill_md = Path(skill_dir) / "SKILL.md"
    if not skill_md.exists():
        errors.append("SKILL.md not found")
        return errors, warnings

    content = skill_md.read_text(encoding="utf-8")

    # Check for frontmatter
    if not content.startswith("---"):
        errors.append("SKILL.md must start with YAML frontmatter (---)")
        return errors, warnings

    # Extract frontmatter
    fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not fm_match:
        errors.append("Could not parse frontmatter")
        return errors, warnings

    frontmatter = fm_match.group(1)

    # Required fields
    required = ["name:", "description:", "license:", "metadata:"]
    for field in required:
        if field not in frontmatter:
            errors.append(f"Frontmatter missing required field: {field}")

    # Check name ends with -skill
    name_match = re.search(r'^name:\s*(\S+)', frontmatter, re.MULTILINE)
    if name_match:
        name = name_match.group(1)
        if not name.endswith("-skill"):
            warnings.append(f"Skill name '{name}' should end with '-skill'")
        if len(name) > 64:
            errors.append(f"Skill name '{name}' exceeds 64 characters")

    # Check metadata fields
    metadata_fields = ["version:", "created:", "author:"]
    for field in metadata_fields:
        if field not in frontmatter:
            warnings.append(f"Metadata missing recommended field: {field}")

    return errors, warnings


def validate_structure(skill_dir):
    """Validate directory structure."""
    errors = []
    warnings = []

    required_files = ["SKILL.md"]
    recommended_files = ["README.md", "install.sh"]
    recommended_dirs = ["scripts", "assets", "references"]

    for f in required_files:
        if not (Path(skill_dir) / f).exists():
            errors.append(f"Required file missing: {f}")

    for f in recommended_files:
        if not (Path(skill_dir) / f).exists():
            warnings.append(f"Recommended file missing: {f}")

    for d in recommended_dirs:
        if not (Path(skill_dir) / d).exists():
            warnings.append(f"Recommended directory missing: {d}")

    return errors, warnings


def validate_skill_md(skill_dir):
    """Validate SKILL.md content."""
    errors = []
    warnings = []

    skill_md = Path(skill_dir) / "SKILL.md"
    if not skill_md.exists():
        return errors, warnings

    content = skill_md.read_text(encoding="utf-8")

    # Check line count
    lines = content.split("\n")
    if len(lines) > 500:
        warnings.append(f"SKILL.md is {len(lines)} lines (recommended: <500)")

    # Check for trigger section
    if "## Trigger" not in content:
        warnings.append("SKILL.md missing '## Trigger' section")

    # Check for invocation examples
    if "/" not in content[:1000]:
        warnings.append("SKILL.md should include slash invocation examples")

    # Check body starts with # /skill-name
    body_start = re.search(r"^---\n.*?\n---\n\s*(.*)", content, re.DOTALL)
    if body_start:
        body = body_start.group(1).strip()
        if not re.match(r"^# /", body):
            warnings.append("SKILL.md body should start with '# /skill-name'")

    return errors, warnings


def validate_scripts(skill_dir):
    """Validate Python scripts."""
    errors = []
    warnings = []

    scripts_dir = Path(skill_dir) / "scripts"
    if not scripts_dir.exists():
        return errors, warnings

    for py_file in scripts_dir.glob("*.py"):
        content = py_file.read_text(encoding="utf-8")

        # Check for shebang
        if not content.startswith("#!/usr/bin/env python3"):
            warnings.append(f"{py_file.name} missing shebang")

        # Check for docstring
        if '"""' not in content[:200]:
            warnings.append(f"{py_file.name} missing module docstring")

        # Check for hardcoded paths (basic check)
        if re.search(r"/Users/\w+|/home/\w+|C:\\\\Users\\\\", content):
            warnings.append(f"{py_file.name} may contain hardcoded paths")

    return errors, warnings


def main():
    if len(sys.argv) > 1:
        skill_dir = sys.argv[1]
    else:
        # Default to parent of scripts directory
        skill_dir = Path(__file__).parent.parent

    skill_dir = Path(skill_dir).resolve()

    print(f"Validating skill: {skill_dir}")
    print("=" * 50)

    all_errors = []
    all_warnings = []

    validators = [
        ("Structure", validate_structure),
        ("Frontmatter", validate_frontmatter),
        ("SKILL.md Content", validate_skill_md),
        ("Scripts", validate_scripts),
    ]

    for name, validator in validators:
        errors, warnings = validator(skill_dir)
        all_errors.extend([f"[{name}] {e}" for e in errors])
        all_warnings.extend([f"[{name}] {w}" for w in warnings])

    # Print results
    if all_errors:
        print("\n❌ ERRORS:")
        for e in all_errors:
            print(f"  • {e}")

    if all_warnings:
        print("\n⚠️  WARNINGS:")
        for w in all_warnings:
            print(f"  • {w}")

    if not all_errors and not all_warnings:
        print("\n✅ All validations passed!")
        return 0
    elif not all_errors:
        print(f"\n✅ Validation passed with {len(all_warnings)} warning(s)")
        return 0
    else:
        print(f"\n❌ Validation failed with {len(all_errors)} error(s)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
