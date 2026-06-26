#!/usr/bin/env python3
import argparse
import os
import sys
import uuid
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_cases, save_cases

VALID_TYPES = ["claim", "source", "screenshot", "profile", "offer", "message", "website"]
VALID_STATUS = ["open", "reviewing", "closed"]
VALID_SUPPORT = ["supports", "contradicts", "neutral"]

def make_evidence(content, evidence_type, support_level, source_label):
    if not content:
        return []
    return [{
        "id": f"EVI-{str(uuid.uuid4())[:4].upper()}",
        "type": evidence_type or "manual_observation",
        "content": content,
        "support_level": support_level or "neutral",
        "source_label": source_label or "Initial evidence",
        "added_at": datetime.now().isoformat()
    }]

def main():
    parser = argparse.ArgumentParser(description="Capture a new verification case")
    parser.add_argument("--title", required=True, help="Short case title")
    parser.add_argument("--type", choices=VALID_TYPES, default="claim")
    parser.add_argument("--claim", required=True, help="Claim to verify")
    parser.add_argument("--source_kind", default="", help="email, url, screenshot, chat, etc.")
    parser.add_argument("--status", choices=VALID_STATUS, default="open")
    parser.add_argument("--notes", default="", help="Extra notes")
    parser.add_argument("--initial_evidence", help="Optional first evidence item content")
    parser.add_argument("--initial_evidence_type", default="manual_observation", help="Evidence type")
    parser.add_argument("--initial_support_level", choices=VALID_SUPPORT, default="neutral")
    parser.add_argument("--initial_source_label", default="Initial evidence", help="Evidence source label")
    args = parser.parse_args()

    now = datetime.now().isoformat()
    case_id = f"VER-{str(uuid.uuid4())[:4].upper()}"

    case = {
        "id": case_id,
        "title": args.title,
        "type": args.type,
        "claim": args.claim,
        "source_kind": args.source_kind,
        "status": args.status,
        "created_at": now,
        "updated_at": now,
        "evidence_items": make_evidence(
            args.initial_evidence,
            args.initial_evidence_type,
            args.initial_support_level,
            args.initial_source_label
        ),
        "red_flags": [],
        "green_flags": [],
        "missing_evidence": [],
        "risk_level": "low",
        "confidence": "low",
        "verdict": "inconclusive",
        "notes": args.notes,
        "recommended_next_step": "Add stronger evidence before making a stronger judgment."
    }

    data = load_cases()
    data["cases"][case_id] = case
    save_cases(data)

    print(f"✅ Case captured: [{case_id}]")
    print(f"   Title: {args.title}")
    print(f"   Type: {args.type}")
    print(f"   Initial evidence items: {len(case['evidence_items'])}")

if __name__ == "__main__":
    main()
