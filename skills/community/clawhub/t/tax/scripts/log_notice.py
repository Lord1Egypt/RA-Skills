#!/usr/bin/env python3
"""Record a tax authority notice into local tax memory."""

import argparse
import json
import os
import uuid
from datetime import datetime
from typing import Any, Dict, Optional


BASE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tax")
NOTICES_FILE = os.path.join(BASE_DIR, "notices.json")


def ensure_base_dir() -> None:
    os.makedirs(BASE_DIR, exist_ok=True)


def load_notices() -> Dict[str, Any]:
    if os.path.exists(NOTICES_FILE):
        with open(NOTICES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"notices": []}


def save_notices(data: Dict[str, Any]) -> None:
    ensure_base_dir()
    with open(NOTICES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def infer_tax_year(
    date_received: Optional[str],
    explicit_tax_year: Optional[int],
) -> int:
    if explicit_tax_year is not None:
        return explicit_tax_year
    if date_received:
        return datetime.strptime(date_received, "%Y-%m-%d").year
    return datetime.now().year


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Record a tax authority notice into local tax memory."
    )
    parser.add_argument(
        "--authority",
        required=True,
        help="Authority name, e.g. IRS, California FTB, local tax office",
    )
    parser.add_argument(
        "--notice-type",
        default="letter",
        help="Notice type, e.g. letter, penalty_notice, verification_request",
    )
    parser.add_argument(
        "--date-received",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Date received in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--tax-year",
        type=int,
        default=None,
        help="Related tax year if known",
    )
    parser.add_argument(
        "--summary",
        required=True,
        help="Short summary of the notice",
    )
    parser.add_argument(
        "--response-deadline",
        default=None,
        help="Optional response deadline in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--status",
        default="open",
        choices=["open", "under_review", "responded", "closed"],
        help="Current notice status",
    )
    parser.add_argument(
        "--professional-review-needed",
        action="store_true",
        help="Flag this notice for professional review",
    )

    args = parser.parse_args()

    tax_year = infer_tax_year(args.date_received, args.tax_year)
    now_iso = datetime.now().isoformat(timespec="seconds")
    notice_id = f"NOT-{str(uuid.uuid4())[:8].upper()}"

    notice = {
        "id": notice_id,
        "tax_year": tax_year,
        "authority": args.authority,
        "notice_type": args.notice_type,
        "date_received": args.date_received,
        "summary": args.summary,
        "response_deadline": args.response_deadline,
        "status": args.status,
        "professional_review_needed": args.professional_review_needed,
        "created_at": now_iso,
    }

    data = load_notices()
    data["notices"].append(notice)
    save_notices(data)

    print(f"Recorded notice: {notice_id}")
    print(f"  Tax year: {tax_year}")
    print(f"  Authority: {args.authority}")
    print(f"  Type: {args.notice_type}")
    print(f"  Date received: {args.date_received}")
    print(f"  Status: {args.status}")
    if args.response_deadline:
        print(f"  Response deadline: {args.response_deadline}")
    print(
        f"  Professional review needed: "
        f"{'yes' if args.professional_review_needed else 'no'}"
    )
    print(f"  Saved to: {NOTICES_FILE}")


if __name__ == "__main__":
    main()
