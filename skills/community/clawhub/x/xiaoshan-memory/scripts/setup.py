#!/usr/bin/env python3
"""Xiaoshan Memory Engine - Environment check."""
import sys
from pathlib import Path

def main():
    v = sys.version_info
    print(f"Python {v.major}.{v.minor}.{v.micro}")
    d = Path.home() / ".xiaoshan"
    d.mkdir(exist_ok=True)
    print(f"Data dir: {d}")
    if v >= (3, 10):
        print("[OK] Ready")
        return 0
    print("[Error] Python 3.10+ required")
    return 1

if __name__ == "__main__":
    sys.exit(main())
