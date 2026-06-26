#!/usr/bin/env python3
"""Run the external OpenClaw config fixer from this skill checkout."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from workspace_doctor.fix_openclaw_config import main


if __name__ == "__main__":
    raise SystemExit(main())
