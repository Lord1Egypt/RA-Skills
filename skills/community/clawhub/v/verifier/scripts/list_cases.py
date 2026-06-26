#!/usr/bin/env python3
import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_cases

def main():
    parser = argparse.ArgumentParser(description="List verification cases")
    parser.add_argument("--status", help="Optional status filter")
    args = parser.parse_args()

    data = load_cases()
    cases = list(data.get("cases", {}).values())

    if args.status:
        cases = [c for c in cases if c.get("status") == args.status]

    if not cases:
        print("No matching cases found.")
        return

    for case in cases:
        print(f"{case['id']} | {case['type']} | {case['status']} | {case['verdict']} | {case['title']}")

if __name__ == "__main__":
    main()
