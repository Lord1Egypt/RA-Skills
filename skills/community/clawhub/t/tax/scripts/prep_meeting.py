#!/usr/bin/env python3
"""Generate a CPA-ready tax handoff summary in Markdown."""

import argparse
import json
import os
from datetime import datetime
from typing import Any, Dict, List


BASE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tax")
DOCUMENTS_FILE = os.path.join(BASE_DIR, "documents.json")
EXPENSES_FILE = os.path.join(BASE_DIR, "expenses.json")
NOTICES_FILE = os.path.join(BASE_DIR, "notices.json")
QUESTIONS_FILE = os.path.join(BASE_DIR, "questions_for_cpa.json")
SUMMARIES_DIR = os.path.join(BASE_DIR, "summaries")


def ensure_dirs() -> None:
    os.makedirs(BASE_DIR, exist_ok=True)
    os.makedirs(SUMMARIES_DIR, exist_ok=True)


def load_json(path: str, default: Dict[str, Any]) -> Dict[str, Any]:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def filter_by_tax_year(items: List[Dict[str, Any]], tax_year: int) -> List[Dict[str, Any]]:
    return [item for item in items if item.get("tax_year") == tax_year]


def format_money(amount: Any, currency: str = "USD") -> str:
    if amount is None:
        return "Unknown"
    try:
        return f"{currency} {float(amount):,.2f}"
    except (ValueError, TypeError):
        return str(amount)


def summarize_expenses(expenses: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    summary: Dict[str, Dict[str, Any]] = {}

    for expense in expenses:
        category = expense.get("category", "uncategorized")
        amount = float(expense.get("amount", 0.0))
        currency = expense.get("currency", "USD")

        if category not in summary:
            summary[category] = {
                "count": 0,
                "total": 0.0,
                "currency": currency,
            }

        summary[category]["count"] += 1
        summary[category]["total"] += amount

    return summary


def build_markdown(
    tax_year: int,
    documents: List[Dict[str, Any]],
    expenses: List[Dict[str, Any]],
    notices: List[Dict[str, Any]],
    questions: List[Dict[str, Any]],
) -> str:
    expense_summary = summarize_expenses(expenses)
    generated_at = datetime.now().isoformat(timespec="seconds")

    lines: List[str] = []
    lines.append(f"# Tax Year {tax_year} CPA Handoff Summary")
    lines.append("")
    lines.append(f"Generated at: {generated_at}")
    lines.append("")

    lines.append("## Filing Snapshot")
    lines.append("")
    lines.append(f"- Tax year: {tax_year}")
    lines.append(f"- Documents recorded: {len(documents)}")
    lines.append(f"- Expense records: {len(expenses)}")
    lines.append(f"- Open notices: {len([n for n in notices if n.get('status') != 'closed'])}")
    lines.append(f"- Open CPA questions: {len([q for q in questions if q.get('status') != 'resolved'])}")
    lines.append("")

    lines.append("## Income and Tax Documents")
    lines.append("")
    if documents:
        lines.append("| Type | Issuer | Amount | Date Received | Status |")
        lines.append("|------|--------|--------|---------------|--------|")
        for doc in documents:
            lines.append(
                f"| {doc.get('document_type', '')} | "
                f"{doc.get('issuer', '')} | "
                f"{format_money(doc.get('amount'))} | "
                f"{doc.get('date_received', '')} | "
                f"{doc.get('status', '')} |"
            )
    else:
        lines.append("_No documents recorded for this tax year._")
    lines.append("")

    lines.append("## Tax-Relevant Expense Summary")
    lines.append("")
    if expense_summary:
        lines.append("| Category | Count | Total |")
        lines.append("|----------|-------|-------|")
        for category in sorted(expense_summary.keys()):
            item = expense_summary[category]
            lines.append(
                f"| {category} | {item['count']} | "
                f"{format_money(item['total'], item['currency'])} |"
            )
    else:
        lines.append("_No expenses recorded for this tax year._")
    lines.append("")

    lines.append("## Notices")
    lines.append("")
    if notices:
        lines.append("| Authority | Type | Date Received | Response Deadline | Status | Summary |")
        lines.append("|-----------|------|---------------|-------------------|--------|---------|")
        for notice in notices:
            lines.append(
                f"| {notice.get('authority', '')} | "
                f"{notice.get('notice_type', '')} | "
                f"{notice.get('date_received', '')} | "
                f"{notice.get('response_deadline') or ''} | "
                f"{notice.get('status', '')} | "
                f"{notice.get('summary', '')} |"
            )
    else:
        lines.append("_No notices recorded for this tax year._")
    lines.append("")

    lines.append("## Questions for My CPA")
    lines.append("")
    if questions:
        unresolved = [q for q in questions if q.get("status") != "resolved"]
        if unresolved:
            for idx, question in enumerate(unresolved, start=1):
                lines.append(f"{idx}. {question.get('question', '')}")
        else:
            lines.append("_No open CPA questions for this tax year._")
    else:
        lines.append("_No CPA questions recorded for this tax year._")
    lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append(
        "This summary is for organization and professional handoff only. "
        "It does not provide tax advice, filing positions, or legal interpretations."
    )
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a CPA-ready tax handoff summary."
    )
    parser.add_argument(
        "--tax-year",
        type=int,
        required=True,
        help="Tax year to summarize",
    )

    args = parser.parse_args()
    tax_year = args.tax_year

    ensure_dirs()

    documents_data = load_json(DOCUMENTS_FILE, {"documents": []})
    expenses_data = load_json(EXPENSES_FILE, {"expenses": []})
    notices_data = load_json(NOTICES_FILE, {"notices": []})
    questions_data = load_json(QUESTIONS_FILE, {"questions": []})

    documents = filter_by_tax_year(documents_data.get("documents", []), tax_year)
    expenses = filter_by_tax_year(expenses_data.get("expenses", []), tax_year)
    notices = filter_by_tax_year(notices_data.get("notices", []), tax_year)
    questions = filter_by_tax_year(questions_data.get("questions", []), tax_year)

    markdown = build_markdown(tax_year, documents, expenses, notices, questions)

    output_path = os.path.join(SUMMARIES_DIR, f"summary_{tax_year}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Generated CPA handoff summary for tax year {tax_year}")
    print(f"  Documents included: {len(documents)}")
    print(f"  Expenses included: {len(expenses)}")
    print(f"  Notices included: {len(notices)}")
    print(f"  Questions included: {len(questions)}")
    print(f"  Saved to: {output_path}")


if __name__ == "__main__":
    main()
