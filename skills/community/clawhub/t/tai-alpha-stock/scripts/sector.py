#!/usr/bin/env python3
"""CLI: ticker vs sector ETF alpha (CAGR difference)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tai_alpha.sector_analysis import main

if __name__ == "__main__":
    raise SystemExit(main())
