#!/usr/bin/env python3
import argparse
from pathlib import Path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mock audio sender")
    parser.add_argument("--file", required=True)
    parser.add_argument("--out", required=True, help="append output file")
    args = parser.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as f:
        f.write(f"AUDIO:{Path(args.file).resolve()}\n")
