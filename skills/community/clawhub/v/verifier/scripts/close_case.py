#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_cases, save_cases

VALID_VERDICTS = ["verified", "likely_true", "inconclusive", "likely_risky", "false_or_misleading"]

def main():
    parser = argparse.ArgumentParser(description="Close a verification case")
    parser.add_argument("--id", required=True, help="Case ID")
    parser.add_argument("--verdict", choices=VALID_VERDICTS, required=True)
    args = parser.parse_args()

    data = load_cases()
    cases = data.get("cases", {})

    if args.id not in cases:
        print(f"Case not found: {args.id}")
        sys.exit(1)

    case = cases[args.id]
    case["verdict"] = args.verdict
    case["status"] = "closed"
    case["updated_at"] = datetime.now().isoformat()
    save_cases(data)

    print(f"✓ Closed {args.id}")
    print(f"  Verdict: {args.verdict}")

if __name__ == "__main__":
    main()
