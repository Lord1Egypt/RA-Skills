#!/usr/bin/env python3
"""Log a formal tax document into local tax memory."""

import argparse
import json
import os
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

BASE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tax")
DOCUMENTS_FILE = os.path.join(BASE_DIR, "documents.json")


def ensure_base_dir() -> None:
    os.makedirs(BASE_DIR, exist_ok=True)


def load_documents() -> Dict[str, Any]:
    if os.path.exists(DOCUMENTS_FILE):
        with open(DOCUMENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"documents": []}


def save_documents(data: Dict[str, Any]) -> None:
    ensure_base_dir()
    with open(DOCUMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def infer_tax_year(date_received: Optional[str], explicit_tax_year: Optional[int]) -> int:
    if explicit_tax_year is not None:
        return explicit_tax_year
    if date_received:
        return datetime.strptime(date_received, "%Y-%m-%d").year
    return datetime.now().year


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Log a formal tax document into local tax memory."
    )
    parser.add_argument(
        "--document-type",
        required=True,
        help="Document type, e.g. W-2, 1099-NEC, 1099-B, K-1",
    )
    parser.add_argument(
        "--issuer",
        required=True,
        help="Issuer of the document, e.g. employer, client, brokerage",
    )
    parser.add_argument(
        "--amount",
        type=float,
        default=None,
        help="Amount shown on the document, if known",
    )
    parser.add_argument(
        "--date-received",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Date the document was received in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--tax-year",
        type=int,
        default=None,
        help="Tax year the document belongs to",
    )
    parser.add_argument(
        "--status",
        default="received",
        choices=["received", "awaiting", "needs_review", "archived"],
        help="Current status of the document record",
    )
    parser.add_argument(
        "--source-channel",
        default="unknown",
        help="Where the document was received from, e.g. mail, email, portal",
    )
    parser.add_argument(
        "--notes",
        default="",
        help="Optional notes",
    )
    parser.add_argument(
        "--expected",
        action="store_true",
        help="Mark this document as expected or recurring",
    )

    args = parser.parse_args()

    tax_year = infer_tax_year(args.date_received, args.tax_year)
    now_iso = datetime.now().isoformat(timespec="seconds")
    doc_id = f"DOC-{str(uuid.uuid4())[:8].upper()}"

    document = {
        "id": doc_id,
        "tax_year": tax_year,
        "document_type": args.document_type,
        "issuer": args.issuer,
        "amount": args.amount,
        "date_received": args.date_received,
        "status": args.status,
        "expected": args.expected,
        "source_channel": args.source_channel,
        "notes": args.notes,
        "created_at": now_iso,
    }

    data = load_documents()
    data["documents"].append(document)
    save_documents(data)

    print(f"Recorded document: {doc_id}")
    print(f"  Tax year: {tax_year}")
    print(f"  Type: {args.document_type}")
    print(f"  Issuer: {args.issuer}")
    if args.amount is not None:
        print(f"  Amount: ${args.amount:,.2f}")
    print(f"  Date received: {args.date_received}")
    print(f"  Status: {args.status}")
    print(f"  Expected: {'yes' if args.expected else 'no'}")
    print(f"  Saved to: {DOCUMENTS_FILE}")


if __name__ == "__main__":
    main()
