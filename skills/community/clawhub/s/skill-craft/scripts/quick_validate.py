#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version
"""

import re
import sys
from pathlib import Path

import yaml

MAX_SKILL_NAME_LENGTH = 64


def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    allowed_properties = {"name", "description", "license", "allowed-tools", "metadata"}

    unexpected_keys = set(frontmatter.keys()) - allowed_properties
    if unexpected_keys:
        allowed = ", ".join(sorted(allowed_properties))
        unexpected = ", ".join(sorted(unexpected_keys))
        return (
            False,
            f"Unexpected key(s) in SKILL.md frontmatter: {unexpected}. Allowed properties are: {allowed}",
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return (
                False,
                f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)",
            )
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return (
                False,
                f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens",
            )
        if len(name) > MAX_SKILL_NAME_LENGTH:
            return (
                False,
                f"Name is too long ({len(name)} characters). "
                f"Maximum is {MAX_SKILL_NAME_LENGTH} characters.",
            )

    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > 1024:
            return (
                False,
                f"Description is too long ({len(description)} characters). Maximum is 1024 characters.",
            )

    return True, "Skill is valid!"


def check_optimization_hints(skill_path):
    """Check skill for optimization opportunities. Returns list of warnings."""
    skill_path = Path(skill_path)
    warnings = []

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return warnings

    content = skill_md.read_text()

    # --- D1: Description quality ---
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1))
            if isinstance(frontmatter, dict):
                desc = str(frontmatter.get("description", ""))
                if not re.search(r"Trigger:|Use when", desc, re.IGNORECASE):
                    warnings.append(
                        "D1: Description may lack trigger phrases — "
                        "consider adding 'Trigger:' or 'Use when' keywords"
                    )
        except yaml.YAMLError:
            pass

    # --- D2: Context efficiency (line count) ---
    line_count = content.count("\n")
    if line_count > 500:
        warnings.append(
            f"D2: SKILL.md is {line_count} lines (over 500 limit) — "
            "MUST split into references/"
        )
    elif line_count > 300:
        warnings.append(
            f"D2: SKILL.md is {line_count} lines — "
            "consider splitting content into references/"
        )

    # --- D6: Examples ---
    example_markers = r"Example|示例|### User:"
    if not re.search(example_markers, content):
        warnings.append(
            "D6: No examples found — consider adding at least 1 concrete example"
        )

    # --- D5: Positive constraints ---
    negative_patterns = [
        r"\bdon't\b",
        r"\bdo not\b",
        r"\bnever\b",
        r"\bavoid\b",
    ]
    negative_count = 0
    for pat in negative_patterns:
        negative_count += len(re.findall(pat, content, re.IGNORECASE))
    if negative_count > 3:
        warnings.append(
            f"D5: Found {negative_count} negative constraints — "
            "consider converting to positive framing"
        )

    # --- D7: Verification keywords ---
    verification_keywords = r"verify|check|validate|confirm|确保|验证"
    if not re.search(verification_keywords, content, re.IGNORECASE):
        warnings.append(
            "D7: No verification keywords found — consider adding verification steps"
        )

    # --- D9: Progressive loading ---
    references_dir = skill_path / "references"
    if not references_dir.is_dir() and line_count > 200:
        warnings.append(
            f"D9: SKILL.md is {line_count} lines with no references/ — "
            "consider creating references/ for details"
        )

    # --- D10: Script references without scripts/ directory ---
    scripts_mentioned = bool(re.search(r"scripts/", content))
    scripts_dir = (skill_path / "scripts").is_dir()
    if scripts_mentioned and not scripts_dir:
        warnings.append(
            "D10: SKILL.md references scripts/ but scripts/ directory does not exist"
        )

    # --- D11: Script executability ---
    if scripts_dir:
        import os

        for script_file in (skill_path / "scripts").iterdir():
            if script_file.is_file() and not os.access(script_file, os.X_OK):
                warnings.append(
                    f"D11: Script '{script_file.name}' is not executable — "
                    "run: chmod +x scripts/{script_file.name}"
                )

    # --- D12: State management awareness ---
    # Check if multi-step workflow lacks state tracking
    has_numbered_steps = bool(re.search(r"^\d+\.\s+\*\*", content, re.MULTILINE))
    has_state_tracking = bool(
        re.search(
            r"requires|checkpoint|state|checkbox|\[.\]|\.state\.|phase:",
            content,
            re.IGNORECASE,
        )
    )
    if has_numbered_steps and not has_state_tracking and line_count > 150:
        warnings.append(
            "D12: Multi-step workflow detected without state tracking — "
            "consider adding file existence checks, checkboxes, or state file"
        )

    return warnings


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)

    if valid:
        hints = check_optimization_hints(sys.argv[1])
        if hints:
            print("\nOptimization hints:")
            for hint in hints:
                print(f"  ⚠ {hint}")

    sys.exit(0 if valid else 1)
