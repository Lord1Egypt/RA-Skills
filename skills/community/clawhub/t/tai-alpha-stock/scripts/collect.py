#!/usr/bin/env python3
"""CLI: fetch normalized data for one ticker."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tai_alpha.collect import main

if __name__ == "__main__":
    raise SystemExit(main())
