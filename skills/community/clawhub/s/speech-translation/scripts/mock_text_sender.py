#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mock text sender")
    parser.add_argument("--out", required=True, help="append output file")
    args = parser.parse_args()

    text = sys.stdin.read().strip()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as f:
        f.write(text)
        f.write("\n\n====\n\n")
