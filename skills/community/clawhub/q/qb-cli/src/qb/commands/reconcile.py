"""Bank reconciliation helper commands."""

import json
from datetime import datetime
from pathlib import Path
from typing import Annotated, Optional

import typer

from qb.output import format_output, format_report, OutputFormat

app = typer.Typer(help="Bank reconciliation helpers.")

WORKSPACE = Path("/workspace")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command()
def start(
    account_id: Annotated[str, typer.Option("--account-id", help="Bank/CC account ID")],
    statement_date: Annotated[str, typer.Option("--statement-date", help="Statement ending date (YYYY-MM-DD)")],
    statement_balance: Annotated[float, typer.Option("--statement-balance", help="Statement ending balance")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Start a reconciliation session.

    Queries uncleared transactions and calculates the difference
    between QB and the bank statement.
    """
    fmt = output or _output()
    client = _client()

    # Get account info
    acct = client.get(f"account/{account_id}").get("Account", {})
    acct_name = acct.get("Name", f"Account {account_id}")
    qb_balance = float(acct.get("CurrentBalance", 0))

    # Query all transactions for this account up to statement date
    # We query various transaction types that affect this account
    uncleared = []
    for entity in ["Purchase", "Deposit", "Transfer", "Payment", "SalesReceipt", "BillPayment"]:
        try:
            sql = f"SELECT * FROM {entity} WHERE TxnDate <= '{statement_date}'"
            resp = client.query(sql, max_results=1000)
            for item in resp.get("QueryResponse", {}).get(entity, []):
                uncleared.append({
                    "type": entity,
                    "id": item.get("Id"),
                    "date": item.get("TxnDate"),
                    "amount": float(item.get("TotalAmt", item.get("Amount", 0))),
                    "doc_number": item.get("DocNumber", ""),
                    "memo": item.get("PrivateNote", ""),
                    "ref": item.get("PaymentRefNum", item.get("DocNumber", "")),
                })
        except Exception:
            continue

    difference = round(statement_balance - qb_balance, 2)

    session = {
        "account_id": account_id,
        "account_name": acct_name,
        "statement_date": statement_date,
        "statement_balance": statement_balance,
        "qb_balance": qb_balance,
        "difference": difference,
        "status": "balanced" if abs(difference) < 0.01 else "unbalanced",
        "transaction_count": len(uncleared),
        "started_at": datetime.now().isoformat(),
    }

    # Save session state
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    session_file = WORKSPACE / f"reconcile_{account_id}_{statement_date}.json"
    with open(session_file, "w") as f:
        json.dump(session, f, indent=2)

    result = {
        **session,
        "session_file": str(session_file),
        "recent_transactions": uncleared[:20],
    }

    format_output(result, fmt)


@app.command()
def status(
    account_id: Annotated[str, typer.Option("--account-id", help="Bank/CC account ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Show current reconciliation status for an account."""
    fmt = output or _output()

    # Find most recent session file
    sessions = sorted(WORKSPACE.glob(f"reconcile_{account_id}_*.json"), reverse=True)
    if not sessions:
        typer.echo(json.dumps({"status": "none", "message": f"No reconciliation in progress for account {account_id}"}))
        return

    with open(sessions[0]) as f:
        session = json.load(f)

    format_output(session, fmt)


@app.command()
def match(
    account_id: Annotated[str, typer.Option("--account-id", help="Bank/CC account ID")],
    statement_file: Annotated[str, typer.Option("--statement-file", help="Bank statement file (OFX/CSV)")],
    tolerance: Annotated[int, typer.Option("--tolerance", help="Date matching tolerance in days")] = 3,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Match bank statement against QB transactions.

    Cross-references imported statement data against QB transactions
    and reports matched, unmatched-on-statement, and unmatched-in-QB items.
    """
    fmt = output or _output()
    client = _client()

    # Parse statement
    from qb.commands.import_cmd import _detect_format, _parse_ofx, _parse_csv
    detected = _detect_format(statement_file)
    if detected == "ofx":
        stmt_txns = _parse_ofx(statement_file)
    else:
        stmt_txns = _parse_csv(statement_file, "Date", "Amount", "Description", False)

    if not stmt_txns:
        typer.echo(json.dumps({"status": "empty", "message": "No transactions in statement file"}))
        return

    # Get date range
    dates = [t["date"][:10] for t in stmt_txns if t["date"]]
    min_date = min(dates)
    max_date = max(dates)

    # Query QB transactions
    qb_txns = []
    for entity in ["Purchase", "Deposit", "Transfer", "Payment", "SalesReceipt", "JournalEntry"]:
        try:
            sql = f"SELECT * FROM {entity} WHERE TxnDate >= '{min_date}' AND TxnDate <= '{max_date}'"
            resp = client.query(sql, max_results=500)
            for item in resp.get("QueryResponse", {}).get(entity, []):
                item["_entity_type"] = entity
                qb_txns.append(item)
        except Exception:
            continue

    # Match
    from qb.commands.import_cmd import _match_transactions
    result = _match_transactions(stmt_txns, qb_txns, tolerance)

    # Find QB transactions not on statement
    matched_qb_ids = set()
    for m in result["matched"] + result["probable"]:
        matched_qb_ids.add(m["existing"].get("Id"))

    outstanding_in_qb = [
        {
            "type": t.get("_entity_type"),
            "id": t.get("Id"),
            "date": t.get("TxnDate"),
            "amount": float(t.get("TotalAmt", t.get("Amount", 0))),
            "doc_number": t.get("DocNumber", ""),
        }
        for t in qb_txns if t.get("Id") not in matched_qb_ids
    ]

    report = {
        "statement_file": statement_file,
        "statement_transactions": len(stmt_txns),
        "qb_transactions": len(qb_txns),
        "matched": len(result["matched"]),
        "probable_matches": len(result["probable"]),
        "unmatched_on_statement": len(result["unmatched"]),
        "outstanding_in_qb": len(outstanding_in_qb),
        "details": {
            "matched": [
                {"stmt": m["imported"], "qb_id": m["existing"].get("Id"), "qb_type": m["existing"].get("_entity_type")}
                for m in result["matched"]
            ],
            "probable": [
                {"stmt": p["imported"], "qb_id": p["existing"].get("Id"), "qb_type": p["existing"].get("_entity_type")}
                for p in result["probable"]
            ],
            "unmatched_on_statement": result["unmatched"],
            "outstanding_in_qb": outstanding_in_qb,
        },
    }

    format_output(report, fmt)


@app.command("report")
def recon_report(
    account_id: Annotated[str, typer.Option("--account-id", help="Bank/CC account ID")],
    start_date: Annotated[Optional[str], typer.Option("--start-date", help="Start date (YYYY-MM-DD)")] = None,
    end_date: Annotated[Optional[str], typer.Option("--end-date", help="End date (YYYY-MM-DD)")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Generate a reconciliation-style report for an account.

    Shows beginning balance, cleared transactions, ending balance,
    and outstanding items.
    """
    fmt = output or _output()
    client = _client()

    # Get account
    acct = client.get(f"account/{account_id}").get("Account", {})

    # Use TransactionList report filtered by account
    params: dict = {"account": account_id}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date

    try:
        report_data = client.get("reports/TransactionList", params=params)
        if fmt == OutputFormat.json:
            # Augment with account info
            report_data["_account"] = {
                "id": account_id,
                "name": acct.get("Name"),
                "current_balance": acct.get("CurrentBalance"),
            }
        format_report(report_data, fmt)
    except Exception as e:
        typer.echo(json.dumps({"error": True, "message": str(e)}), err=True)
        raise SystemExit(1)
