"""Bank statement import commands (OFX/QFX/CSV)."""

import csv as csv_mod
import io
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(name="import", help="Import bank/credit card statements.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


def _parse_ofx(file_path: str) -> list[dict]:
    """Parse an OFX/QFX file into normalized transaction dicts."""
    from ofxparse import OfxParser

    with open(file_path, "rb") as f:
        ofx = OfxParser.parse(f)

    txns = []
    for acct in getattr(ofx, "accounts", [ofx.account]) if hasattr(ofx, "accounts") else [ofx.account]:
        for txn in acct.statement.transactions:
            txns.append({
                "date": txn.date.strftime("%Y-%m-%d") if txn.date else "",
                "amount": float(txn.amount),
                "fitid": txn.id or "",
                "name": txn.payee or txn.memo or "",
                "memo": txn.memo or "",
                "type": txn.type or "",
                "check_number": txn.checknum or "",
            })
    return txns


def _parse_csv(file_path: str, date_col: str, amount_col: str, desc_col: str, skip_header: bool) -> list[dict]:
    """Parse a CSV bank statement into normalized transaction dicts."""
    txns = []
    with open(file_path, "r") as f:
        reader = csv_mod.DictReader(f)
        for row in reader:
            try:
                amt = float(row.get(amount_col, "0").replace(",", "").replace("$", ""))
            except ValueError:
                continue
            txns.append({
                "date": row.get(date_col, ""),
                "amount": amt,
                "fitid": "",
                "name": row.get(desc_col, ""),
                "memo": "",
                "type": "debit" if amt < 0 else "credit",
                "check_number": "",
            })
    return txns


def _detect_format(file_path: str) -> str:
    """Auto-detect file format by extension and content."""
    p = Path(file_path)
    ext = p.suffix.lower()
    if ext in (".ofx", ".qfx", ".qbo"):
        return "ofx"
    if ext == ".csv":
        return "csv"
    # Try reading first bytes
    with open(file_path, "rb") as f:
        head = f.read(500)
    if b"<OFX" in head or b"OFXHEADER" in head:
        return "ofx"
    return "csv"


def _match_transactions(imported: list[dict], existing: list[dict], tolerance_days: int = 3) -> dict:
    """Match imported transactions against existing QB transactions.

    Returns dict with 'matched', 'probable', 'unmatched' lists.
    """
    matched = []
    probable = []
    unmatched = []

    for imp in imported:
        imp_amt = imp["amount"]
        imp_date = imp["date"]
        imp_fitid = imp.get("fitid", "")
        imp_check = imp.get("check_number", "")

        best_match = None
        match_type = None

        for ex in existing:
            ex_amt = float(ex.get("TotalAmt", ex.get("Amount", 0)))
            # QB stores positive amounts; debits are negative in import
            # Normalize: for purchases/expenses, QB amount is positive, import is negative
            ex_date = ex.get("TxnDate", "")
            ex_doc = ex.get("DocNumber", "")

            # Check amount match (exact)
            if abs(abs(imp_amt) - abs(ex_amt)) > 0.01:
                continue

            # Check date proximity
            try:
                d_imp = datetime.strptime(imp_date[:10], "%Y-%m-%d")
                d_ex = datetime.strptime(ex_date[:10], "%Y-%m-%d")
                days_diff = abs((d_imp - d_ex).days)
            except (ValueError, TypeError):
                days_diff = 999

            if days_diff > tolerance_days:
                continue

            # Exact match: amount + date + (FITID or check number)
            if days_diff == 0 and (
                (imp_fitid and imp_fitid == ex.get("_fitid", ""))
                or (imp_check and imp_check == ex_doc)
            ):
                best_match = ex
                match_type = "exact"
                break

            # Probable match: amount + date within tolerance
            if best_match is None or days_diff < abs((datetime.strptime(imp_date[:10], "%Y-%m-%d") - datetime.strptime(best_match.get("TxnDate", "1900-01-01")[:10], "%Y-%m-%d")).days):
                best_match = ex
                match_type = "probable"

        if match_type == "exact":
            matched.append({"imported": imp, "existing": best_match, "match_type": "exact"})
        elif match_type == "probable":
            probable.append({"imported": imp, "existing": best_match, "match_type": "probable"})
        else:
            unmatched.append(imp)

    return {"matched": matched, "probable": probable, "unmatched": unmatched}


@app.command()
def preview(
    file_path: Annotated[str, typer.Argument(help="Path to bank statement file")],
    fmt: Annotated[Optional[str], typer.Option("--format", help="File format: auto, ofx, csv")] = "auto",
    date_col: Annotated[str, typer.Option("--date-col", help="CSV date column name")] = "Date",
    amount_col: Annotated[str, typer.Option("--amount-col", help="CSV amount column name")] = "Amount",
    desc_col: Annotated[str, typer.Option("--desc-col", help="CSV description column name")] = "Description",
    skip_header: Annotated[bool, typer.Option("--skip-header", help="Skip CSV header row")] = False,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Preview transactions from a bank statement file without importing."""
    out_fmt = output or _output()

    detected = fmt if fmt != "auto" else _detect_format(file_path)

    if detected == "ofx":
        txns = _parse_ofx(file_path)
    else:
        txns = _parse_csv(file_path, date_col, amount_col, desc_col, skip_header)

    summary = {
        "file": file_path,
        "format": detected,
        "transaction_count": len(txns),
        "total_debits": sum(t["amount"] for t in txns if t["amount"] < 0),
        "total_credits": sum(t["amount"] for t in txns if t["amount"] >= 0),
        "date_range": {
            "start": min((t["date"] for t in txns), default=""),
            "end": max((t["date"] for t in txns), default=""),
        },
        "transactions": txns,
    }

    format_output(summary if out_fmt == OutputFormat.json else txns, out_fmt,
                  columns=["date", "amount", "name", "type", "fitid", "check_number"])


@app.command()
def bank(
    file_path: Annotated[str, typer.Argument(help="Path to bank statement file")],
    account_id: Annotated[str, typer.Option("--account-id", help="QB bank/CC account ID to import into")],
    fmt: Annotated[Optional[str], typer.Option("--format", help="File format: auto, ofx, csv")] = "auto",
    date_col: Annotated[str, typer.Option("--date-col", help="CSV date column name")] = "Date",
    amount_col: Annotated[str, typer.Option("--amount-col", help="CSV amount column name")] = "Amount",
    desc_col: Annotated[str, typer.Option("--desc-col", help="CSV description column name")] = "Description",
    skip_header: Annotated[bool, typer.Option("--skip-header", help="Skip CSV header row")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Show what would be imported without creating transactions")] = False,
    tolerance: Annotated[int, typer.Option("--tolerance", help="Date matching tolerance in days")] = 3,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Import a bank statement and match/create transactions.

    1. Parses the statement file (OFX/QFX/CSV)
    2. Queries QB for existing transactions in the date range
    3. Matches imported transactions against existing QB transactions
    4. Reports: matched (skip), probable (flag), unmatched (create)
    5. In --dry-run mode, shows report without creating anything
    """
    out_fmt = output or _output()
    client = _client()

    # Parse file
    detected = fmt if fmt != "auto" else _detect_format(file_path)
    if detected == "ofx":
        txns = _parse_ofx(file_path)
    else:
        txns = _parse_csv(file_path, date_col, amount_col, desc_col, skip_header)

    if not txns:
        typer.echo(json.dumps({"status": "empty", "message": "No transactions found in file"}))
        return

    # Get date range for QB query
    dates = [t["date"][:10] for t in txns if t["date"]]
    min_date = min(dates)
    max_date = max(dates)

    # Expand range by tolerance
    try:
        start = (datetime.strptime(min_date, "%Y-%m-%d") - timedelta(days=tolerance)).strftime("%Y-%m-%d")
        end = (datetime.strptime(max_date, "%Y-%m-%d") + timedelta(days=tolerance)).strftime("%Y-%m-%d")
    except ValueError:
        start, end = min_date, max_date

    from qb.api.query import escape_query_value

    # Query existing transactions in QB for this account and date range
    safe_start = escape_query_value(start)
    safe_end = escape_query_value(end)
    existing = []
    for entity in ["Purchase", "Deposit", "Transfer", "JournalEntry"]:
        try:
            sql = f"SELECT * FROM {entity} WHERE TxnDate >= '{safe_start}' AND TxnDate <= '{safe_end}'"
            resp = client.query(sql, max_results=500)
            for item in resp.get("QueryResponse", {}).get(entity, []):
                existing.append(item)
        except Exception:
            continue

    # Match
    result = _match_transactions(txns, existing, tolerance)

    # Create unmatched transactions (if not dry run)
    created = []
    if not dry_run:
        for txn in result["unmatched"]:
            try:
                if txn["amount"] < 0:
                    # Debit = expense (paid from imported account)
                    body = {
                        "AccountRef": {"value": account_id},
                        "PaymentType": "Cash",
                        "TxnDate": txn["date"][:10],
                        "Line": [{
                            "Amount": abs(txn["amount"]),
                            "DetailType": "AccountBasedExpenseLineDetail",
                            "AccountBasedExpenseLineDetail": {
                                "AccountRef": {"value": "31"},  # Uncategorized Expense
                            },
                        }],
                        "PrivateNote": f"Imported: {txn['name']}",
                    }
                    if txn.get("check_number"):
                        body["DocNumber"] = txn["check_number"]
                    resp = client.post("purchase", body)
                    created.append({"txn": txn, "qb_entity": "Purchase", "qb_id": resp.get("Purchase", {}).get("Id")})
                else:
                    # Credit = deposit (into imported account, from Uncategorized Income)
                    body = {
                        "DepositToAccountRef": {"value": account_id},
                        "TxnDate": txn["date"][:10],
                        "Line": [{
                            "Amount": txn["amount"],
                            "DetailType": "DepositLineDetail",
                            "DepositLineDetail": {
                                "AccountRef": {"value": "32"},  # Uncategorized Income
                            },
                        }],
                        "PrivateNote": f"Imported: {txn['name']}",
                    }
                    resp = client.post("deposit", body)
                    created.append({"txn": txn, "qb_entity": "Deposit", "qb_id": resp.get("Deposit", {}).get("Id")})
            except Exception as e:
                created.append({"txn": txn, "error": str(e)})

    report = {
        "file": file_path,
        "format": detected,
        "total_imported": len(txns),
        "matched": len(result["matched"]),
        "probable_matches": len(result["probable"]),
        "unmatched": len(result["unmatched"]),
        "created": len(created) if not dry_run else 0,
        "dry_run": dry_run,
        "details": {
            "matched": [{"imported": m["imported"], "qb_id": m["existing"].get("Id")} for m in result["matched"]],
            "probable": [{"imported": p["imported"], "qb_id": p["existing"].get("Id")} for p in result["probable"]],
            "unmatched": result["unmatched"],
            "created": created if not dry_run else [],
        },
    }

    format_output(report, out_fmt)
