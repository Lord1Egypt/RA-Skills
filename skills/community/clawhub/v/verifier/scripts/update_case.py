#!/usr/bin/env python3
import argparse
import os
import sys
import uuid
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_cases, save_cases

VALID_STATUS = ["open", "reviewing", "closed"]
VALID_SUPPORT = ["supports", "contradicts", "neutral"]

def main():
    parser = argparse.ArgumentParser(description="Update a verification case")
    parser.add_argument("--id", required=True, help="Case ID")
    parser.add_argument("--status", choices=VALID_STATUS)
    parser.add_argument("--notes")
    parser.add_argument("--add_evidence")
    parser.add_argument("--evidence_type", default="manual_observation")
    parser.add_argument("--support_level", choices=VALID_SUPPORT, default="neutral")
    parser.add_argument("--source_label", default="Manual update")
    args = parser.parse_args()

    data = load_cases()
    cases = data.get("cases", {})

    if args.id not in cases:
        print(f"Case not found: {args.id}")
        sys.exit(1)

    case = cases[args.id]

    if args.status:
        case["status"] = args.status
    if args.notes is not None:
        case["notes"] = args.notes
    if args.add_evidence:
        case.setdefault("evidence_items", []).append({
            "id": f"EVI-{str(uuid.uuid4())[:4].upper()}",
            "type": args.evidence_type,
            "content": args.add_evidence,
            "support_level": args.support_level,
            "source_label": args.source_label,
            "added_at": datetime.now().isoformat()
        })

    case["updated_at"] = datetime.now().isoformat()
    save_cases(data)

    print(f"✓ Updated {args.id}")
    print(f"  Evidence items: {len(case.get('evidence_items', []))}")
    print(f"  Status: {case.get('status')}")

if __name__ == "__main__":
    main()
