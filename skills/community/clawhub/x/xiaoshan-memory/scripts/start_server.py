#!/usr/bin/env python3
"""Xiaoshan Memory Engine - Server launcher."""
import sys
from pathlib import Path

def main():
    d = Path(__file__).resolve().parent.parent.parent / "xiaoshan-memory-engine"
    if not d.exists():
        d = Path.home() / ".qclaw" / "workspace" / "xiaoshan-memory-engine"
    api = d / "api_server.py"
    if not api.exists():
        print("[Error] Engine not installed. See clawhub.ai/skill/xiaoshan-memory")
        return 1
    print(f"[OK] Found engine at {d}")
    print("  Start manually: python api_server.py")
    return 0

if __name__ == "__main__":
    sys.exit(main())
