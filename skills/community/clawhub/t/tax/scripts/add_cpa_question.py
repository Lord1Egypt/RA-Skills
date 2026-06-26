#!/usr/bin/env python3
"""Record a question for CPA or tax professional review."""

import argparse
import json
import os
import uuid
from datetime import datetime
from typing import Any, Dict, Optional


BASE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tax")
QUESTIONS_FILE = os.path.join(BASE_DIR, "questions_for_cpa.json")


def ensure_base_dir() -> None:
    os.makedirs(BASE_DIR, exist_ok=True)


def load_questions() -> Dict[str, Any]:
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"questions": []}


def save_questions(data: Dict[str, Any]) -> None:
    ensure_base_dir()
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def infer_tax_year(explicit_tax_year: Optional[int]) -> int:
    if explicit_tax_year is not None:
        return explicit_tax_year
    return datetime.now().year


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Record a question for CPA or tax professional review."
    )
    parser.add_argument(
        "--question",
        required=True,
        help="Question to ask the CPA or tax professional",
    )
    parser.add_argument(
        "--tax-year",
        type=int,
        default=None,
        help="Related tax year",
    )
    parser.add_argument(
        "--linked-record-id",
        default="",
        help="Optional linked document, expense, or notice record ID",
    )
    parser.add_argument(
        "--status",
        default="open",
        choices=["open", "asked", "resolved"],
        help="Current status of the question",
    )
    parser.add_argument(
        "--notes",
        default="",
        help="Optional notes",
    )

    args = parser.parse_args()

    tax_year = infer_tax_year(args.tax_year)
    now_iso = datetime.now().isoformat(timespec="seconds")
    question_id = f"Q-{str(uuid.uuid4())[:8].upper()}"

    linked_record_ids = []
    if args.linked_record_id.strip():
        linked_record_ids.append(args.linked_record_id.strip())

    question = {
        "id": question_id,
        "tax_year": tax_year,
        "question": args.question,
        "linked_record_ids": linked_record_ids,
        "status": args.status,
        "notes": args.notes,
        "created_at": now_iso,
    }

    data = load_questions()
    data["questions"].append(question)
    save_questions(data)

    print(f"Recorded CPA question: {question_id}")
    print(f"  Tax year: {tax_year}")
    print(f"  Status: {args.status}")
    if linked_record_ids:
        print(f"  Linked record IDs: {', '.join(linked_record_ids)}")
    print(f"  Saved to: {QUESTIONS_FILE}")


if __name__ == "__main__":
    main()
