#!/usr/bin/env python3
"""CLI: watchlist target/stop — list | add | check."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tai_alpha.alerts_store import main

if __name__ == "__main__":
    raise SystemExit(main())
