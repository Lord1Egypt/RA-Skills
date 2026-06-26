#!/usr/bin/env python3
"""CLI: print formatted report from SQLite run (score_json / collect_json)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tai_alpha.report_text import main

if __name__ == "__main__":
    raise SystemExit(main())
