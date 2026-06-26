#!/usr/bin/env python3
"""Capture a tax-relevant natural language event and route it into local tax memory."""

import argparse
import json
import os
import re
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


BASE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tax")
LEDGER_FILE = os.path.join(BASE_DIR, "ledger_events.json")
DOCUMENTS_FILE = os.path.join(BASE_DIR, "documents.json")
EXPENSES_FILE = os.path.join(BASE_DIR, "expenses.json")
NOTICES_FILE = os.path.join(BASE_DIR, "notices.json")
QUESTIONS_FILE = os.path.join(BASE_DIR, "questions_for_cpa.json")


def ensure_base_dir() -> None:
    os.makedirs(BASE_DIR, exist_ok=True)


def load_json(path: str, default: Dict[str, Any]) -> Dict[str, Any]:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path: str, data: Dict[str, Any]) -> None:
    ensure_base_dir()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def infer_tax_year(explicit_tax_year: Optional[int], date_str: str) -> int:
    if explicit_tax_year is not None:
        return explicit_tax_year
    return datetime.strptime(date_str, "%Y-%m-%d").year


def extract_amount(text: str) -> Optional[float]:
    patterns = [
        r"\$([0-9]+(?:\.[0-9]{1,2})?)",
        r"([0-9]+(?:\.[0-9]{1,2})?)\s*(?:dollars|usd|刀)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
    return None


def classify_event(text: str, extracted_amount: Optional[float]) -> str:
    lower = text.lower()

    if extracted_amount is not None:
        return "expense"

    document_keywords = [
        "1099", "w-2", "w2", "k-1", "k1", "tax form", "tax document"
    ]
    if any(keyword in lower for keyword in document_keywords):
        return "document"

    notice_keywords = [
        "irs", "notice", "letter", "state tax", "tax authority", "penalty"
    ]
    if any(keyword in lower for keyword in notice_keywords):
        return "notice"

    question_keywords = [
        "cpa", "accountant", "ask my cpa", "question", "remind me to ask"
    ]
    if any(keyword in lower for keyword in question_keywords):
        return "question"

    return "unknown"


def confidence_for_event(event_type: str) -> float:
    if event_type == "expense":
        return 0.88
    if event_type in ("document", "notice", "question"):
        return 0.78
    return 0.50


def guess_document_type(text: str) -> str:
    upper = text.upper()
    if "1099-NEC" in upper:
        return "1099-NEC"
    if "1099-B" in upper:
        return "1099-B"
    if "1099-K" in upper:
        return "1099-K"
    if "1099" in upper:
        return "1099"
    if "W-2" in upper or "W2" in upper:
        return "W-2"
    if "K-1" in upper or "K1" in upper:
        return "K-1"
    return "unknown_document"


def guess_issuer(text: str) -> str:
    match = re.search(r"\bfrom\s+([A-Za-z0-9&.\- ]+)", text, re.IGNORECASE)
    if not match:
        return "Unknown"

    issuer = match.group(1).strip().rstrip(".")

    trailing_phrases = [
        " today",
        " yesterday",
        " this morning",
        " this afternoon",
        " tonight",
    ]

    lower_issuer = issuer.lower()
    for phrase in trailing_phrases:
        if lower_issuer.endswith(phrase):
            issuer = issuer[: -len(phrase)].strip()
            break

    return issuer or "Unknown"

def guess_notice_authority(text: str) -> str:
    lower = text.lower()
    if "irs" in lower:
        return "IRS"
    if "state" in lower:
        return "State Tax Authority"
    return "Unknown Authority"


def guess_expense_category(text: str) -> str:
    lower = text.lower()
    if any(word in lower for word in ["lunch", "dinner", "meal", "restaurant", "client to lunch"]):
        return "business_meal"
    if any(word in lower for word in ["adobe", "software", "subscription", "saas"]):
        return "software"
    if "travel" in lower:
        return "travel"
    if "ad" in lower or "advertising" in lower:
        return "advertising"
    return "uncategorized"


def create_expense_record(
    text: str,
    date_str: str,
    tax_year: int,
    amount: Optional[float],
) -> Optional[str]:
    if amount is None:
        return None

    data = load_json(EXPENSES_FILE, {"expenses": []})
    expense_id = f"EXP-{str(uuid.uuid4())[:8].upper()}"
    now_iso = datetime.now().isoformat(timespec="seconds")

    expense = {
        "id": expense_id,
        "tax_year": tax_year,
        "date": date_str,
        "amount": amount,
        "currency": "USD",
        "category": guess_expense_category(text),
        "merchant": "Unknown",
        "purpose": "",
        "documentation_status": "receipt_not_confirmed",
        "professional_review_status": "unreviewed",
        "raw_text": text,
        "created_at": now_iso,
    }

    data["expenses"].append(expense)
    save_json(EXPENSES_FILE, data)
    return expense_id


def create_document_record(
    text: str,
    date_str: str,
    tax_year: int,
    amount: Optional[float],
) -> str:
    data = load_json(DOCUMENTS_FILE, {"documents": []})
    doc_id = f"DOC-{str(uuid.uuid4())[:8].upper()}"
    now_iso = datetime.now().isoformat(timespec="seconds")

    document = {
        "id": doc_id,
        "tax_year": tax_year,
        "document_type": guess_document_type(text),
        "issuer": guess_issuer(text),
        "amount": amount,
        "date_received": date_str,
        "status": "received",
        "expected": False,
        "source_channel": "captured_event",
        "notes": text,
        "created_at": now_iso,
    }

    data["documents"].append(document)
    save_json(DOCUMENTS_FILE, data)
    return doc_id


def create_notice_record(
    text: str,
    date_str: str,
    tax_year: int,
) -> str:
    data = load_json(NOTICES_FILE, {"notices": []})
    notice_id = f"NOT-{str(uuid.uuid4())[:8].upper()}"
    now_iso = datetime.now().isoformat(timespec="seconds")

    notice = {
        "id": notice_id,
        "tax_year": tax_year,
        "authority": guess_notice_authority(text),
        "notice_type": "letter",
        "date_received": date_str,
        "summary": text,
        "response_deadline": None,
        "status": "open",
        "professional_review_needed": True,
        "created_at": now_iso,
    }

    data["notices"].append(notice)
    save_json(NOTICES_FILE, data)
    return notice_id


def create_question_record(
    text: str,
    tax_year: int,
) -> str:
    data = load_json(QUESTIONS_FILE, {"questions": []})
    question_id = f"Q-{str(uuid.uuid4())[:8].upper()}"
    now_iso = datetime.now().isoformat(timespec="seconds")

    question = {
        "id": question_id,
        "tax_year": tax_year,
        "question": text,
        "linked_record_ids": [],
        "status": "open",
        "notes": "Created from capture_event.py",
        "created_at": now_iso,
    }

    data["questions"].append(question)
    save_json(QUESTIONS_FILE, data)
    return question_id


def route_event(
    event_type: str,
    text: str,
    date_str: str,
    tax_year: int,
    amount: Optional[float],
) -> List[str]:
    linked_ids: List[str] = []

    if event_type == "expense":
        expense_id = create_expense_record(text, date_str, tax_year, amount)
        if expense_id:
            linked_ids.append(expense_id)

    elif event_type == "document":
        linked_ids.append(create_document_record(text, date_str, tax_year, amount))

    elif event_type == "notice":
        linked_ids.append(create_notice_record(text, date_str, tax_year))

    elif event_type == "question":
        linked_ids.append(create_question_record(text, tax_year))

    return linked_ids


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Capture a tax-relevant natural language event."
    )
    parser.add_argument(
        "--text",
        required=True,
        help="Natural language tax-relevant text to capture",
    )
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Event date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--tax-year",
        type=int,
        default=None,
        help="Related tax year",
    )
    parser.add_argument(
        "--source",
        default="chat",
        help="Source of the event, e.g. chat, note, imported_text",
    )

    args = parser.parse_args()

    extracted_amount = extract_amount(args.text)
    event_type = classify_event(args.text, extracted_amount)
    confidence = confidence_for_event(event_type)
    tax_year = infer_tax_year(args.tax_year, args.date)
    now_iso = datetime.now().isoformat(timespec="seconds")
    event_id = f"EVT-{str(uuid.uuid4())[:8].upper()}"

    linked_record_ids = route_event(
        event_type=event_type,
        text=args.text,
        date_str=args.date,
        tax_year=tax_year,
        amount=extracted_amount,
    )

    event = {
        "id": event_id,
        "tax_year": tax_year,
        "event_type": event_type,
        "raw_text": args.text,
        "date": args.date,
        "amount": extracted_amount,
        "currency": "USD" if extracted_amount is not None else None,
        "source": args.source,
        "confidence": confidence,
        "status": "captured",
        "needs_followup": event_type == "unknown",
        "linked_record_ids": linked_record_ids,
        "created_at": now_iso,
    }

    data = load_json(LEDGER_FILE, {"events": []})
    data["events"].append(event)
    save_json(LEDGER_FILE, data)

    print(f"Captured event: {event_id}")
    print(f"  Tax year: {tax_year}")
    print(f"  Event type: {event_type}")
    print(f"  Date: {args.date}")
    if extracted_amount is not None:
        print(f"  Amount detected: USD {extracted_amount:,.2f}")
    print(f"  Confidence: {confidence:.2f}")
    print(f"  Linked record IDs: {', '.join(linked_record_ids) if linked_record_ids else 'none'}")
    print(f"  Needs follow-up: {'yes' if event['needs_followup'] else 'no'}")
    print(f"  Saved to: {LEDGER_FILE}")


if __name__ == "__main__":
    main()
