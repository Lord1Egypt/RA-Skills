#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_cases, save_cases
from lib.scoring import score_case

def main():
    parser = argparse.ArgumentParser(description="Score one verification case")
    parser.add_argument("--id", required=True, help="Case ID")
    args = parser.parse_args()

    data = load_cases()
    cases = data.get("cases", {})

    if args.id not in cases:
        print(f"Case not found: {args.id}")
        sys.exit(1)

    case = cases[args.id]
    result = score_case(case)

    case["verdict"] = result["verdict"]
    case["confidence"] = result["confidence"]
    case["risk_level"] = result["risk_level"]
    case["red_flags"] = result["red_flags"]
    case["green_flags"] = result["green_flags"]
    case["missing_evidence"] = result["missing_evidence"]
    case["recommended_next_step"] = result["recommended_next_step"]
    case["updated_at"] = datetime.now().isoformat()

    save_cases(data)

    print(f"✅ Case scored: [{args.id}]")
    print(json.dumps({
        "verdict": case["verdict"],
        "confidence": case["confidence"],
        "risk_level": case["risk_level"],
        "red_flags": case["red_flags"],
        "green_flags": case["green_flags"],
        "missing_evidence": case["missing_evidence"],
        "recommended_next_step": case["recommended_next_step"]
    }, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
