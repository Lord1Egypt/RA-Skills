#!/usr/bin/env python3
"""CLI: run analyze for multiple tickers; print score line each."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tai_alpha.script_entrypoints import batch_cli

if __name__ == "__main__":
    raise SystemExit(batch_cli())
