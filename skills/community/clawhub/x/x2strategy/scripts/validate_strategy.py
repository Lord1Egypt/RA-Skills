#!/usr/bin/env python3
"""validate.py — Validate a generated strategy file without executing it.

Usage:
    python scripts/validate.py library/pairs_trading/strategy_1.py
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from spec2code.validator import validate_code


def main():
    parser = argparse.ArgumentParser(description="Validate strategy code (syntax + structure).")
    parser.add_argument("strategy", help="Path to the strategy .py file")
    args = parser.parse_args()

    if not os.path.isfile(args.strategy):
        print(f"Error: file not found: {args.strategy}", file=sys.stderr)
        sys.exit(1)

    with open(args.strategy, "r", encoding="utf-8") as f:
        code = f.read()

    result = validate_code(code)

    if result.valid:
        print(f"✅ {args.strategy} — syntax valid")
    else:
        print(f"❌ {args.strategy} — validation failed:")
        for err in result.errors:
            print(f"   ERROR: {err}")

    for w in result.warnings:
        print(f"   WARN: {w}")

    sys.exit(0 if result.valid else 1)


if __name__ == "__main__":
    main()
