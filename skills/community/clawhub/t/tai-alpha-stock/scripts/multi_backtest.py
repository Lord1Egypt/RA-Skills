#!/usr/bin/env python3
"""CLI: compare RSI vs MACD vs BB CAGR; pick top strategy."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tai_alpha.script_entrypoints import multi_backtest_cli

if __name__ == "__main__":
    raise SystemExit(multi_backtest_cli())
