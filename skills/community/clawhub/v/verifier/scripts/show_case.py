#!/usr/bin/env python3
import argparse
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_cases

def main():
    parser = argparse.ArgumentParser(description="Show one verification case")
    parser.add_argument("--id", required=True, help="Case ID")
    args = parser.parse_args()

    data = load_cases()
    cases = data.get("cases", {})

    if args.id not in cases:
        print(f"Case not found: {args.id}")
        sys.exit(1)

    print(json.dumps(cases[args.id], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
