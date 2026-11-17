#!/usr/bin/env python3
"""Skill entry point for ue-audit.

Works both in the repository (../src) and in the packaged skill (./src).
"""

from __future__ import annotations

import sys
from pathlib import Path


def _add_src() -> bool:
    here = Path(__file__).resolve()
    candidates = [
        here.parents[1] / "src",  # packaged skill: skill/src
        here.parents[2] / "src",  # repository: <repo>/src
    ]
    for candidate in candidates:
        if (candidate / "ue_audit").is_dir():
            sys.path.insert(0, str(candidate))
            return True
    return False


def main() -> int:
    if not _add_src():
        print("ue-audit: cannot find the ue_audit package next to this script.", file=sys.stderr)
        return 4
    from ue_audit.cli import main as cli_main

    return cli_main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
