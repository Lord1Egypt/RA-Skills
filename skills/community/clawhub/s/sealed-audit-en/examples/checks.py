"""Checking rules. Same level as the entry script; MGC's import hook routes it
after sealing.

Rules only — no path handling, no file writes, so they stay independently
testable.
"""

import sqlite3

# Columns the ledger must provide
REQUIRED_COLUMNS = {
    "id": "INTEGER",
    "entry_date": "TEXT",
    "account": "TEXT",
    "amount": "REAL",
    "counterparty": "TEXT",
    "invoice_no": "TEXT",
}

# Sensitivity threshold for the large-amount sample rule
LARGE_AMOUNT_THRESHOLD = 100000.0


def check_schema(con: sqlite3.Connection) -> list[dict]:
    """Verify the table has every required column with the expected type."""
    rows = con.execute("PRAGMA table_info(ledger)").fetchall()
    actual = {row[1]: row[2] for row in rows}
    findings = []

    for column, expected_type in REQUIRED_COLUMNS.items():
        if column not in actual:
            findings.append(
                {
                    "rule": "schema.missing_column",
                    "level": "high",
                    "detail": f"missing column {column}",
                }
            )
        elif actual[column].upper() != expected_type:
            findings.append(
                {
                    "rule": "schema.type_mismatch",
                    "level": "medium",
                    "detail": f"{column} is {actual[column]}, expected {expected_type}",
                }
            )
    return findings


def check_ledger(con: sqlite3.Connection, sample: int = 50) -> list[dict]:
    """Sampled checks: negative amounts, missing invoice numbers, duplicates, large amounts."""
    findings = []

    for row in con.execute(
        "SELECT id, entry_date, amount FROM ledger WHERE amount < 0 LIMIT ?",
        (sample,),
    ):
        findings.append(
            {
                "rule": "ledger.negative_amount",
                "level": "medium",
                "detail": f"record {row[0]} ({row[1]}) has negative amount {row[2]}",
            }
        )

    for row in con.execute(
        "SELECT id, entry_date FROM ledger"
        " WHERE invoice_no IS NULL OR TRIM(invoice_no) = '' LIMIT ?",
        (sample,),
    ):
        findings.append(
            {
                "rule": "ledger.missing_invoice",
                "level": "medium",
                "detail": f"record {row[0]} ({row[1]}) has no invoice number",
            }
        )

    for row in con.execute(
        "SELECT invoice_no, COUNT(*) AS n FROM ledger"
        " WHERE invoice_no IS NOT NULL AND TRIM(invoice_no) != ''"
        " GROUP BY invoice_no HAVING n > 1 LIMIT ?",
        (sample,),
    ):
        findings.append(
            {
                "rule": "ledger.duplicate_invoice",
                "level": "high",
                "detail": f"invoice {row[0]} appears {row[1]} times",
            }
        )

    for row in con.execute(
        "SELECT id, entry_date, amount FROM ledger"
        " WHERE amount >= ? LIMIT ?",
        (LARGE_AMOUNT_THRESHOLD, sample),
    ):
        findings.append(
            {
                "rule": "ledger.large_amount",
                "level": "low",
                "detail": f"record {row[0]} ({row[1]}) large amount {row[2]}",
            }
        )

    return findings


def summarize(findings: list[dict]) -> dict:
    """Counts only, no detail — this is what travels back."""
    counts = {"high": 0, "medium": 0, "low": 0}
    for item in findings:
        counts[item["level"]] = counts.get(item["level"], 0) + 1
    return {
        "total": len(findings),
        "high": counts["high"],
        "medium": counts["medium"],
        "low": counts["low"],
        "conclusion": "pass" if counts["high"] == 0 else "review_required",
    }
