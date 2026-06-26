#!/usr/bin/env python3
"""
Create a publish-safe copy of the skill folder.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
EXCLUDED_NAMES = {
    ".DS_Store",
    "__pycache__",
}


def ignore(path: str, names: list[str]) -> set[str]:
    ignored = set()
    for name in names:
        if name in EXCLUDED_NAMES or name.endswith('.pyc'):
            ignored.add(name)
    return ignored


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a publish-safe skill copy")
    parser.add_argument(
        "--dest",
        default=str(SKILL_DIR.parent / "dist" / "research-archive-query"),
        help="Destination directory",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    dest = Path(args.dest).expanduser().resolve()
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SKILL_DIR, dest, ignore=ignore)
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
