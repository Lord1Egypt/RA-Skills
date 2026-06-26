#!/usr/bin/env python3
"""Run the workspace doctor from this skill checkout."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from workspace_doctor.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
