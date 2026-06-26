#!/usr/bin/env python3
from pathlib import Path
import runpy
import sys


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    sys.path.insert(0, str(root / "scripts"))
    runpy.run_path(str(root / "scripts" / "interactive_install.py"), run_name="__main__")
