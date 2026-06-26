#!/usr/bin/env python3
import runpy
import sys
from pathlib import Path


if __name__ == "__main__":
    target = Path(__file__).resolve().parent / "somnia" / "nightly_skill_review.py"
    sys.path.insert(0, str(target.parent))
    runpy.run_path(str(target), run_name="__main__")
