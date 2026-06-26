#!/usr/bin/env python3
"""CLI: 7-day return estimate (RandomForest on recent returns)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tai_alpha.script_entrypoints import ml_cli

if __name__ == "__main__":
    raise SystemExit(ml_cli())
