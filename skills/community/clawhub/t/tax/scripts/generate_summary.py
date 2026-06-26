#!/usr/bin/env python3
"""Generate annual tax summaries in Markdown and CSV."""

import argparse
import csv
import json
import os
from datetime import datetime
from typing import Any, Dict, List


BASE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tax")
DOCUMENTS_FILE = os.path.join(BASE_DIR, "documents.json")
EXPENSES_FILE = os.path.join(BASE_DIR, "expenses.json")
NOTICES_FILE = os.path.join(BASE_DIR, "notices.json")
QUESTIONS_FILE = os.path.join(BASE_DIR, "questions_for_cpa.json")
YEAR_STATE_FILE = os.path.join(BASE_DIR, "year_state.json")
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


def summarize_expenses(expenses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, Dict[str, Any]] = {}

    for expense in expenses:
        category = expense.get("category", "uncategorized")
        amount = float(expense.get("amount", 0.0))
        currency = expense.get("currency", "USD")

        if category not in grouped:
            grouped[category] = {
                "category": category,
                "count": 0,
                "total": 0.0,
                "currency": currency,
            }

        grouped[category]["count"] += 1
        grouped[category]["total"] += amount

    return [grouped[key] for key in sorted(grouped.keys())]


def count_open_notices(notices: List[Dict[str, Any]]) -> int:
    return len([n for n in notices if n.get("status") != "closed"])


def count_open_questions(questions: List[Dict[str, Any]]) -> int:
    return len([q for q in questions if q.get("status") != "resolved"])


def build_markdown(
    tax_year: int,
    documents: List[Dict[str, Any]],
    expenses: List[Dict[str, Any]],
    notices: List[Dict[str, Any]],
    questions: List[Dict[str, Any]],
    year_state: Dict[str, Any],
) -> str:
    generated_at = datetime.now().isoformat(timespec="seconds")
    expense_summary = summarize_expenses(expenses)

    lines: List[str] = []
    lines.append(f"# Tax Year {tax_year} Annual Summary")
    lines.append("")
    lines.append(f"Generated at: {generated_at}")
    lines.append("")

    lines.append("## Year Overview")
    lines.append("")
    lines.append(f"- Tax year: {tax_year}")
    lines.append(f"- Workflow state: {year_state.get('state', 'unknown')}")
    lines.append(f"- Documents recorded: {len(documents)}")
    lines.append(f"- Expense records: {len(expenses)}")
    lines.append(f"- Open notices: {count_open_notices(notices)}")
    lines.append(f"- Open CPA questions: {count_open_questions(questions)}")
    lines.append("")

    lines.append("## Documents")
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

    lines.append("## Expense Summary by Category")
    lines.append("")
    if expense_summary:
        lines.append("| Category | Count | Total |")
        lines.append("|----------|-------|-------|")
        for row in expense_summary:
            lines.append(
                f"| {row['category']} | {row['count']} | "
                f"{format_money(row['total'], row['currency'])} |"
            )
    else:
        lines.append("_No expenses recorded for this tax year._")
    lines.append("")

    lines.append("## Notices")
    lines.append("")
    if notices:
        lines.append("| Authority | Type | Date Received | Status | Summary |")
        lines.append("|-----------|------|---------------|--------|---------|")
        for notice in notices:
            lines.append(
                f"| {notice.get('authority', '')} | "
                f"{notice.get('notice_type', '')} | "
                f"{notice.get('date_received', '')} | "
                f"{notice.get('status', '')} | "
                f"{notice.get('summary', '')} |"
            )
    else:
        lines.append("_No notices recorded for this tax year._")
    lines.append("")

    lines.append("## Questions for CPA")
    lines.append("")
    if questions:
        for idx, question in enumerate(questions, start=1):
            lines.append(f"{idx}. {question.get('question', '')} ({question.get('status', 'unknown')})")
    else:
        lines.append("_No CPA questions recorded for this tax year._")
    lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append(
        "This summary is for organization, recordkeeping, and professional handoff support only. "
        "It does not provide tax advice or legal interpretations."
    )
    lines.append("")

    return "\n".join(lines)

def write_csv(
    output_path: str,
    tax_year: int,
    documents: List[Dict[str, Any]],
    expenses: List[Dict[str, Any]],
    expense_summary: List[Dict[str, Any]],
    notices: List[Dict[str, Any]],
    questions: List[Dict[str, Any]],
    year_state: Dict[str, Any],
) -> None:
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["section", "field_1", "field_2", "field_3", "field_4", "field_5"])

        writer.writerow(["overview", "tax_year", tax_year, "", "", ""])
        writer.writerow(["overview", "state", year_state.get("state", "unknown"), "", "", ""])
        writer.writerow(["overview", "documents_recorded", len(documents), "", "", ""])
        writer.writerow(["overview", "expense_records", len(expenses), "", "", ""])
        writer.writerow(["overview", "open_notices", count_open_notices(notices), "", "", ""])
        writer.writerow(["overview", "open_questions_for_cpa", count_open_questions(questions), "", "", ""])

        for doc in documents:
            writer.writerow([
                "document",
                doc.get("document_type", ""),
                doc.get("issuer", ""),
                doc.get("amount", ""),
                doc.get("date_received", ""),
                doc.get("status", ""),
            ])

        for row in expense_summary:
            writer.writerow([
                "expense_summary",
                row.get("category", ""),
                row.get("count", 0),
                row.get("total", 0.0),
                row.get("currency", "USD"),
                "",
            ])

        for notice in notices:
            writer.writerow([
                "notice",
                notice.get("authority", ""),
                notice.get("notice_type", ""),
                notice.get("date_received", ""),
                notice.get("status", ""),
                notice.get("summary", ""),
            ])

        for question in questions:
            writer.writerow([
                "question",
                question.get("question", ""),
                question.get("status", ""),
                "",
                "",
                "",
            ])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate annual tax summaries in Markdown and CSV."
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
    year_state_data = load_json(YEAR_STATE_FILE, {"years": {}})

    documents = filter_by_tax_year(documents_data.get("documents", []), tax_year)
    expenses = filter_by_tax_year(expenses_data.get("expenses", []), tax_year)
    notices = filter_by_tax_year(notices_data.get("notices", []), tax_year)
    questions = filter_by_tax_year(questions_data.get("questions", []), tax_year)
    year_state = year_state_data.get("years", {}).get(str(tax_year), {})

    markdown = build_markdown(tax_year, documents, expenses, notices, questions, year_state)
    expense_summary = summarize_expenses(expenses)

    md_path = os.path.join(SUMMARIES_DIR, f"annual_summary_{tax_year}.md")
    csv_path = os.path.join(SUMMARIES_DIR, f"annual_summary_{tax_year}.csv")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    write_csv(csv_path, tax_year, documents, expenses, expense_summary, notices, questions, year_state)
    print(f"Generated annual summary for tax year {tax_year}")
    print(f"  Documents included: {len(documents)}")
    print(f"  Expenses included: {len(expenses)}")
    print(f"  Notices included: {len(notices)}")
    print(f"  Questions included: {len(questions)}")
    print(f"  Markdown saved to: {md_path}")
    print(f"  CSV saved to: {csv_path}")


if __name__ == "__main__":
    main()
