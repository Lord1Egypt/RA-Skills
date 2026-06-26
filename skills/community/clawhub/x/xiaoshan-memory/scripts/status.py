#!/usr/bin/env python3
"""Xiaoshan Memory Engine - Status check."""
import json, sys
from pathlib import Path

def main():
    d = Path.home() / ".xiaoshan"
    info = {"data_dir": str(d), "exists": d.exists()}
    db = d / "memory.db"
    if db.exists():
        info["database"] = True
    f = d / "activation.json"
    if f.exists():
        info["activated"] = True
    print(json.dumps(info, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
