#!/usr/bin/env python3
"""
Skill Packager - Creates a distributable .zip file of a skill folder

Usage:
    python utils/package_skill.py <path/to/skill-folder> [output-directory] [--todo <todo-file>]

Example:
    python utils/package_skill.py skills/public/my-skill
    python utils/package_skill.py skills/public/my-skill ./output
    python utils/package_skill.py skills/public/my-skill ./output --todo ./output/skill-creation.todo.md
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path
from quick_validate import validate_skill

REQUIRED_TODO_TASKS = ("T0", "T1", "T2", "T3", "T4")


def validate_todo_gates(todo_path):
    """
    Validate required plan-with-files TODO gates before packaging.

    Required completed tasks: T0-T4.
    Completion marker format: line contains "[x] Tn" (case-insensitive for x).
    """
    todo_file = Path(todo_path).resolve()
    if not todo_file.exists():
        return False, f"TODO file not found: {todo_file}"

    try:
        content = todo_file.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Failed to read TODO file: {e}"

    completed = set()
    for line in content.splitlines():
        match = re.search(r"\[[xX]\]\s*(T\d+)\b", line)
        if match:
            completed.add(match.group(1).upper())

    missing = [task for task in REQUIRED_TODO_TASKS if task not in completed]
    if missing:
        return (
            False,
            "TODO gate check failed. Missing completed tasks: "
            + ", ".join(missing)
            + ". Mark them as '[x] Tn ...' before packaging.",
        )

    if "[x] confirmed" not in content.lower():
        return False, "TODO gate check failed. User confirmation is not marked as '[x] confirmed'."

    return True, "TODO gate validation passed."


def package_skill(skill_path, output_dir=None, todo_path=None):
    """
    Package a skill folder into a .zip file.

    Args:
        skill_path: Path to the skill folder
        output_dir: Optional output directory for the .zip file (defaults to ./output in current directory)
        todo_path: Optional path to plan-with-files TODO file for pre-packaging gate checks

    Returns:
        Path to the created .zip file, or None if error
    """
    skill_path = Path(skill_path).resolve()

    # Validate skill folder exists
    if not skill_path.exists():
        print(f"❌ Error: Skill folder not found: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        return None

    # Validate SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ Error: SKILL.md not found in {skill_path}")
        return None

    # Validate TODO gates (optional but strongly recommended for skill-creator workflow)
    if todo_path:
        print(f"🧭 Validating TODO gates: {todo_path}")
        todo_ok, todo_message = validate_todo_gates(todo_path)
        if not todo_ok:
            print(f"❌ {todo_message}")
            return None
        print(f"✅ {todo_message}\n")

    # Run validation before packaging
    print("🔍 Validating skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ Validation failed: {message}")
        print("   Please fix the validation errors before packaging.")
        return None
    print(f"✅ {message}\n")

    # Determine output location
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
    else:
        output_path = (Path.cwd() / "output").resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    skill_filename = output_path / f"{skill_name}.zip"

    # Create the .zip file
    try:
        with zipfile.ZipFile(skill_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the skill directory
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    # Calculate the relative path within the zip
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  Added: {arcname}")

        print(f"\n✅ Successfully packaged skill to: {skill_filename}")
        return skill_filename

    except Exception as e:
        print(f"❌ Error creating .zip file: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Package a skill folder into a distributable .zip file"
    )
    parser.add_argument("skill_path", help="Path to the skill folder")
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=None,
        help="Optional output directory (default: ./output)",
    )
    parser.add_argument(
        "--todo",
        dest="todo_path",
        default=None,
        help="Optional plan-with-files TODO file path for gate validation",
    )
    args = parser.parse_args()

    skill_path = args.skill_path
    output_dir = args.output_dir
    todo_path = args.todo_path

    print(f"📦 Packaging skill: {skill_path}")
    if output_dir:
        print(f"   Output directory: {output_dir}")
    if todo_path:
        print(f"   TODO file: {todo_path}")
    print()

    result = package_skill(skill_path, output_dir, todo_path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
