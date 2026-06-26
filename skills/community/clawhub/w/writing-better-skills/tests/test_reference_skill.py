#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> int:
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    print(result.stdout, end="")
    if result.returncode != 0:
        print(result.stderr, end="")
    return result.returncode


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    validator = root / "scripts" / "quick_validate.py"
    ref_skill = root / "reference-skills" / "release-notes-generator"
    ref_test = ref_skill / "tests" / "test_generate_release_notes.py"

    if run([sys.executable, str(validator), str(ref_skill)]) != 0:
        return 1
    if run([sys.executable, str(ref_test)]) != 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
