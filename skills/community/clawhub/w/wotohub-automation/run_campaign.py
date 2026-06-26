#!/usr/bin/env python3
"""
Canonical WotoHub campaign entrypoint.

Use this file as the single public entrypoint for:
- text / URL product analysis
- model-first payload compilation
- WotoHub search
- recommendation generation
- outreach email preview generation

The implementation lives in scripts/run_campaign.py; this wrapper keeps a
stable root-level command for users and docs.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from run_campaign import main as _main  # type: ignore


if __name__ == "__main__":
    sys.exit(_main())
