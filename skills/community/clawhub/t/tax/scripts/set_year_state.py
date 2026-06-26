#!/usr/bin/env python3
"""Set and update annual tax workflow state."""

import argparse
import json
import os
from datetime import datetime
from typing import Any, Dict, List


BASE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tax")
YEAR_STATE_FILE = os.path.join(BASE_DIR, "year_state.json")
DOCUMENTS_FILE = os.path.join(BASE_DIR, "documents.json")
EXPENSES_FILE = os.path.join(BASE_DIR, "expenses.json")
NOTICES_FILE = os.path.join(BASE_DIR, "notices.json")
QUESTIONS_FILE = os.path.join(BASE_DIR, "questions_for_cpa.json")


VALID_STATES = {
    "capturing",
    "reconciling",
    "pre_filing",
    "filed",
    "archived",
    "notice_followup",
}


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


def filter_by_tax_year(items: List[Dict[str, Any]], tax_year: int) -> List[Dict[str, Any]]:
    return [item for item in items if item.get("tax_year") == tax_year]


def count_open_notices(notices: List[Dict[str, Any]]) -> int:
    return len([n for n in notices if n.get("status") != "closed"])


def count_open_questions(questions: List[Dict[str, Any]]) -> int:
    return len([q for q in questions if q.get("status") != "resolved"])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Set and update annual tax workflow state."
    )
    parser.add_argument(
        "--tax-year",
        type=int,
        required=True,
        help="Tax year to update",
    )
    parser.add_argument(
        "--state",
        required=True,
        choices=sorted(VALID_STATES),
        help="New workflow state",
    )

    args = parser.parse_args()

    tax_year = args.tax_year
    state = args.state
    now_iso = datetime.now().isoformat(timespec="seconds")

    documents_data = load_json(DOCUMENTS_FILE, {"documents": []})
    expenses_data = load_json(EXPENSES_FILE, {"expenses": []})
    notices_data = load_json(NOTICES_FILE, {"notices": []})
    questions_data = load_json(QUESTIONS_FILE, {"questions": []})
    year_state_data = load_json(YEAR_STATE_FILE, {"years": {}})

    documents = filter_by_tax_year(documents_data.get("documents", []), tax_year)
    expenses = filter_by_tax_year(expenses_data.get("expenses", []), tax_year)
    notices = filter_by_tax_year(notices_data.get("notices", []), tax_year)
    questions = filter_by_tax_year(questions_data.get("questions", []), tax_year)

    year_state_data["years"][str(tax_year)] = {
        "state": state,
        "documents_received_count": len(documents),
        "expense_records_count": len(expenses),
        "open_notices_count": count_open_notices(notices),
        "open_questions_for_cpa_count": count_open_questions(questions),
        "updated_at": now_iso,
    }

    save_json(YEAR_STATE_FILE, year_state_data)

    print(f"Updated tax year state: {tax_year}")
    print(f"  State: {state}")
    print(f"  Documents recorded: {len(documents)}")
    print(f"  Expense records: {len(expenses)}")
    print(f"  Open notices: {count_open_notices(notices)}")
    print(f"  Open CPA questions: {count_open_questions(questions)}")
    print(f"  Saved to: {YEAR_STATE_FILE}")


if __name__ == "__main__":
    main()
