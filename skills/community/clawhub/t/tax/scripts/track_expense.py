#!/usr/bin/env python3
"""Record a tax-relevant expense or receipt into local tax memory."""

import argparse
import json
import os
import uuid
from datetime import datetime
from typing import Any, Dict, Optional


BASE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tax")
EXPENSES_FILE = os.path.join(BASE_DIR, "expenses.json")


def ensure_base_dir() -> None:
    os.makedirs(BASE_DIR, exist_ok=True)


def load_expenses() -> Dict[str, Any]:
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"expenses": []}


def save_expenses(data: Dict[str, Any]) -> None:
    ensure_base_dir()
    with open(EXPENSES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def infer_tax_year(date_str: Optional[str], explicit_tax_year: Optional[int]) -> int:
    if explicit_tax_year is not None:
        return explicit_tax_year
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d").year
    return datetime.now().year


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Record a tax-relevant expense or receipt."
    )
    parser.add_argument(
        "--amount",
        type=float,
        required=True,
        help="Expense amount",
    )
    parser.add_argument(
        "--category",
        required=True,
        help="Expense category, e.g. software, business_meal, travel, advertising",
    )
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Expense date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--tax-year",
        type=int,
        default=None,
        help="Tax year the record belongs to",
    )
    parser.add_argument(
        "--merchant",
        default="Unknown",
        help="Merchant or payee name",
    )
    parser.add_argument(
        "--purpose",
        default="",
        help="Optional business or recordkeeping purpose",
    )
    parser.add_argument(
        "--currency",
        default="USD",
        help="Currency code, default USD",
    )
    parser.add_argument(
        "--documentation-status",
        default="receipt_not_confirmed",
        choices=[
            "receipt_not_confirmed",
            "receipt_saved",
            "invoice_saved",
            "statement_only",
            "other_supporting_record",
        ],
        help="Documentation status for the record",
    )
    parser.add_argument(
        "--professional-review-status",
        default="unreviewed",
        choices=["unreviewed", "flagged_for_cpa", "reviewed"],
        help="Professional review status",
    )
    parser.add_argument(
        "--raw-text",
        default="",
        help="Original user wording or source text",
    )

    args = parser.parse_args()

    tax_year = infer_tax_year(args.date, args.tax_year)
    now_iso = datetime.now().isoformat(timespec="seconds")
    expense_id = f"EXP-{str(uuid.uuid4())[:8].upper()}"

    expense = {
        "id": expense_id,
        "tax_year": tax_year,
        "date": args.date,
        "amount": args.amount,
        "currency": args.currency,
        "category": args.category,
        "merchant": args.merchant,
        "purpose": args.purpose,
        "documentation_status": args.documentation_status,
        "professional_review_status": args.professional_review_status,
        "raw_text": args.raw_text,
        "created_at": now_iso,
    }

    data = load_expenses()
    data["expenses"].append(expense)
    save_expenses(data)

    print(f"Recorded expense: {expense_id}")
    print(f"  Tax year: {tax_year}")
    print(f"  Date: {args.date}")
    print(f"  Amount: {args.currency} {args.amount:,.2f}")
    print(f"  Category: {args.category}")
    print(f"  Merchant: {args.merchant}")
    if args.purpose:
        print(f"  Purpose: {args.purpose}")
    print(f"  Documentation status: {args.documentation_status}")
    print(f"  Professional review status: {args.professional_review_status}")
    print(f"  Saved to: {EXPENSES_FILE}")


if __name__ == "__main__":
    main()
