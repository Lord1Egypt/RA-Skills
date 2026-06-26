#!/usr/bin/env python3
"""Print the compact Taiyi persona injection for another agent/session."""
from __future__ import annotations
from pathlib import Path
base=Path(__file__).resolve().parents[1]
print((base/'persona'/'TAIYI_CORE.md').read_text(encoding='utf-8'))
