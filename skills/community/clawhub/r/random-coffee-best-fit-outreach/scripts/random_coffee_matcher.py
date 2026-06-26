#!/usr/bin/env python3
"""Run the repo CLI from the skill wrapper when this skill is used from a clone."""

from __future__ import annotations

import sys
from pathlib import Path


def add_repo_src() -> None:
    for parent in Path(__file__).resolve().parents:
        src = parent / "src"
        package = src / "random_coffee_matcher"
        if package.exists():
            sys.path.insert(0, str(src))
            return
    raise SystemExit(
        "Could not find src/random_coffee_matcher. Run this script from the "
        "random-coffee-best-fit-outreach repo clone or install the package first."
    )


def main() -> int:
    add_repo_src()
    from random_coffee_matcher.cli import main as cli_main

    return cli_main()


if __name__ == "__main__":
    raise SystemExit(main())
