#!/usr/bin/env python3
"""
Compatibility wrapper.

This legacy skill forwards execution to destiny-fusion-pro.
"""

from __future__ import annotations

import runpy
from pathlib import Path


def main() -> None:
    target = (
        Path(__file__).resolve().parents[2]
        / "destiny-fusion-pro"
        / "scripts"
        / "fortune_fusion.py"
    )
    runpy.run_path(str(target), run_name="__main__")


if __name__ == "__main__":
    main()
