#!/usr/bin/env python3
"""Xiaoshan Memory Engine - License activation helper."""
import json, sys
from pathlib import Path

DATA = Path.home() / ".xiaoshan"
DATA.mkdir(exist_ok=True)

def main():
    f = DATA / "activation.json"
    if len(sys.argv) < 2:
        print(json.dumps({"activated": f.exists()}, indent=2))
        return 0
    f.write_text(json.dumps({"key": sys.argv[1].strip(), "active": True}))
    print("[OK] Saved")
    return 0

if __name__ == "__main__":
    sys.exit(main())
