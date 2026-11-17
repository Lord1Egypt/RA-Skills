#!/usr/bin/env python3
"""跨平台 skill-template 脚手架（与 scaffold_skill.ps1 行为一致）。"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

EXCLUDE_DIR_NAMES = {".git", ".pytest_cache", "__pycache__"}
EXCLUDE_FILE_NAMES = {".env", ".env.local"}
KEBAB_SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def _ignore_copy(_dir: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        if name in EXCLUDE_DIR_NAMES or name in EXCLUDE_FILE_NAMES:
            ignored.add(name)
        elif name.endswith(".pyc"):
            ignored.add(name)
    return ignored


def _print_next_steps(target: Path) -> None:
    print()
    print("=== 脚手架复制完成 ===")
    print(f"目标目录: {target}")
    print()
    print("请在本机继续执行（未自动 git init，避免误操作）：")
    print(f'  cd "{target}"')
    print("  Remove-Item -Recurse -Force .git -ErrorAction SilentlyContinue   # 若曾手工复制漏删")
    print("  git init")
    print("  git remote add origin <你的新技能仓库 URL>")
    print("  git remote -v    # 确认 remote 不是 skill-template")
    print("  python tests/run_tests.py -v")
    print()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="从 skill-template 脚手架复制新技能目录")
    parser.add_argument("--slug", required=True, help="kebab-case slug，须与目标目录名一致")
    parser.add_argument("--destination", required=True, help="新技能完整目标路径")
    parser.add_argument("--force", action="store_true", help="目标非空时允许覆盖（目标不得含 .git）")
    args = parser.parse_args(argv)

    slug = args.slug.strip()
    if not KEBAB_SLUG.match(slug):
        print(f"ERROR: Slug 必须是 kebab-case，当前: {slug}", file=sys.stderr)
        return 1

    target = Path(args.destination).resolve()
    if target.name != slug:
        print(
            f"ERROR: 目标目录末段 '{target.name}' 与 slug '{slug}' 不一致。",
            file=sys.stderr,
        )
        return 1

    parent = target.parent
    if not parent.is_dir():
        print(f"ERROR: 父目录不存在: {parent}", file=sys.stderr)
        return 1

    if (target / ".git").exists():
        print(
            f"ERROR: 目标已存在 .git，请先删除: {target / '.git'}",
            file=sys.stderr,
        )
        return 1

    template_root = Path(__file__).resolve().parent.parent
    if target.exists():
        entries = list(target.iterdir())
        if entries and not args.force:
            print(
                f"ERROR: 目标目录已存在且非空: {target}\n请加 --force 或换空目录。",
                file=sys.stderr,
            )
            return 1

    target.mkdir(parents=True, exist_ok=True)
    print(f"复制模板: {template_root} -> {target}")
    for item in template_root.iterdir():
        name = item.name
        if name in EXCLUDE_DIR_NAMES or name in EXCLUDE_FILE_NAMES:
            continue
        if name.endswith(".pyc"):
            continue
        dest = target / name
        if item.is_dir():
            shutil.copytree(item, dest, ignore=_ignore_copy, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)

    marker = target / ".openclaw-skill-template"
    if marker.is_file():
        marker.unlink()

    _print_next_steps(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
