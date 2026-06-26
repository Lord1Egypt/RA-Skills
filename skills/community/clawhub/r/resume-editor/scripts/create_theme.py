#!/usr/bin/env python3
"""
Scaffold a reusable custom resume theme from a built-in or existing custom theme.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from resume_utils import DEFAULT_THEME, get_user_theme_root, list_available_themes, resolve_theme_assets


def copy_text_file(source_path, target_path):
    """Copy a UTF-8 text file."""
    target_path.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Create a reusable custom resume theme")
    parser.add_argument("theme_name", help="Name of the new custom theme")
    parser.add_argument(
        "--base",
        default=DEFAULT_THEME,
        help="Base theme name or path to derive from (default: modern)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Optional target directory. Defaults to user-themes/<theme_name> inside this skill.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite the target directory if it exists")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent
    user_theme_root = get_user_theme_root(skill_root).resolve()

    try:
        base_theme = resolve_theme_assets(args.base, skill_root)
    except ValueError as exc:
        print(f"Error: {exc}")
        print(f"Available themes: {', '.join(list_available_themes(skill_root))}")
        sys.exit(1)

    if args.output_dir:
        target_dir = Path(args.output_dir).expanduser()
        if not target_dir.is_absolute():
            target_dir = (Path.cwd() / target_dir).resolve()
    else:
        target_dir = get_user_theme_root(skill_root) / args.theme_name

    if target_dir.exists():
        if not args.force:
            print(f"Error: Target theme directory already exists: {target_dir}")
            print("Use --force to overwrite it.")
            sys.exit(1)
        shutil.rmtree(target_dir)

    target_dir.mkdir(parents=True, exist_ok=True)

    copy_text_file(base_theme["template_path"], target_dir / "template.html")
    copy_text_file(base_theme["css_path"], target_dir / "style.css")

    print(f"Custom theme created: {target_dir}")
    print("Files:")
    print(f"  - {target_dir / 'template.html'}")
    print(f"  - {target_dir / 'style.css'}")
    print("")
    print("Next steps:")
    print("  1. Edit style.css to tune colors, spacing, fonts, and print layout.")
    print("  2. Edit template.html only if you want to change the overall HTML wrapper.")
    try:
        relative_to_user_theme_root = target_dir.resolve().relative_to(user_theme_root)
        reuse_theme_arg = relative_to_user_theme_root.parts[0]
    except ValueError:
        reuse_theme_arg = str(target_dir)
    print(f"  3. Reuse it with: python3 scripts/export_resume.py --theme {reuse_theme_arg} --format html resume.json output.html")


if __name__ == "__main__":
    main()
