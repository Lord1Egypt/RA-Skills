#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    validator = root / "scripts" / "quick_validate.py"

    result = subprocess.run(
        [sys.executable, str(validator), str(root)],
        capture_output=True,
        text=True,
        check=False,
    )
    print(result.stdout, end="")
    if result.returncode != 0:
        print(result.stderr, end="")
        return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
