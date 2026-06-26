#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main entrypoint for the WeChat Article Assistant skill."""

from __future__ import annotations

import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from cli import main


if __name__ == "__main__":
    raise SystemExit(main())
