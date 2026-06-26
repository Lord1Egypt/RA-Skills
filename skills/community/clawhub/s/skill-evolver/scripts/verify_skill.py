#!/usr/bin/env python3
"""
Verify skill installation.

Checks that a skill is properly installed and has valid structure.

Usage:
    python scripts/verify_skill.py --skill ./skills/<name> --output ./output/02-verify.md
"""

import argparse
import re
from pathlib import Path
from typing import Tuple


def verify_skill(skill_path: str, output_path: str) -> Tuple[str, str]:
    """
    Verify skill installation.

    Returns:
        Tuple of (result, message)
        - result: "PASS" or "FAIL"
        - message: Description of result
    """
    skill_path = Path(skill_path)
    output_path = Path(output_path)

    checks = []
    all_passed = True

    # Check 1: Directory exists
    if not skill_path.exists():
        checks.append(("Directory exists", "FAIL", "Skill directory not found"))
        all_passed = False
    else:
        checks.append(("Directory exists", "PASS", f"Found: {skill_path}"))

    # Check 2: SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        checks.append(("SKILL.md exists", "FAIL", "SKILL.md not found"))
        all_passed = False
    else:
        checks.append(("SKILL.md exists", "PASS", f"Found: {skill_md}"))

        # Check 3: SKILL.md has valid frontmatter
        try:
            content = skill_md.read_text(encoding="utf-8")
            frontmatter_match = re.match(r"^---\s*\n(.+?)\n---", content, re.DOTALL)

            if not frontmatter_match:
                checks.append(("Valid frontmatter", "FAIL", "No YAML frontmatter found"))
                all_passed = False
            else:
                fm = frontmatter_match.group(1)

                # Check for required fields
                has_name = re.search(r"^name:\s*.+$", fm, re.MULTILINE)
                has_desc = re.search(r"^description:\s*.+$", fm, re.MULTILINE | re.DOTALL)

                if not has_name:
                    checks.append(("Frontmatter: name", "FAIL", "Missing 'name' field"))
                    all_passed = False
                else:
                    checks.append(("Frontmatter: name", "PASS", "Found 'name' field"))

                if not has_desc:
                    checks.append(("Frontmatter: description", "FAIL", "Missing 'description' field"))
                    all_passed = False
                else:
                    checks.append(("Frontmatter: description", "PASS", "Found 'description' field"))

        except Exception as e:
            checks.append(("Valid frontmatter", "FAIL", f"Error reading SKILL.md: {e}"))
            all_passed = False

    # Check 4: Directory is not empty
    if skill_path.exists():
        files = list(skill_path.iterdir())
        if len(files) == 0:
            checks.append(("Non-empty directory", "FAIL", "Skill directory is empty"))
            all_passed = False
        else:
            checks.append(("Non-empty directory", "PASS", f"Contains {len(files)} file(s)"))

    # Generate report
    report_lines = [
        "# Skill Verification Report",
        "",
        f"## Skill: {skill_path.name}",
        f"## Path: `{skill_path}`",
        "",
        "## Checks",
        "",
        "| Check | Result | Details |",
        "|-------|--------|---------|",
    ]

    for check_name, result, details in checks:
        icon = "✅" if result == "PASS" else "❌"
        report_lines.append(f"| {check_name} | {icon} {result} | {details} |")

    report_lines.extend(["", "## Summary", ""])

    if all_passed:
        report_lines.extend([
            "### Result: PASS",
            "",
            "Skill is properly installed and ready to use.",
        ])
        final_result = "PASS"
        final_message = f"Skill '{skill_path.name}' verified successfully."
    else:
        report_lines.extend([
            "### Result: FAIL",
            "",
            "Skill installation is incomplete or corrupted.",
            "",
            "## Action",
            "Select an alternative skill from candidates.",
        ])
        final_result = "FAIL"
        final_message = f"Skill '{skill_path.name}' verification failed."

    # Write report
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(report_lines), encoding="utf-8")

    return final_result, final_message


def main():
    parser = argparse.ArgumentParser(description="Verify skill installation")
    parser.add_argument("--skill", required=True, help="Path to skill directory")
    parser.add_argument("--output", required=True, help="Output path for verification report")
    args = parser.parse_args()

    result, message = verify_skill(args.skill, args.output)

    print(f"[{result}] {message}")
    print(f"Report: {args.output}")

    if result == "FAIL":
        exit(1)


if __name__ == "__main__":
    main()
