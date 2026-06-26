"""Purchase (Expense/Check/CreditCard) resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks expenses (purchases, checks, CC charges).")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_expenses(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all expenses/purchases."""
    fmt = output or _output()
    client = _client()
    result = client.query("SELECT * FROM Purchase", max_results=limit)
    purchases = result.get("QueryResponse", {}).get("Purchase", [])
    format_output(
        purchases,
        fmt,
        columns=["Id", "TxnDate", "AccountRef.name", "EntityRef.name", "TotalAmt", "PaymentType"],
    )


@app.command()
def get(
    expense_id: Annotated[str, typer.Argument(help="Purchase/Expense ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get an expense by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"purchase/{expense_id}")
    format_output(result.get("Purchase"), fmt)


@app.command()
def create(
    account_id: Annotated[str, typer.Option("--account-id", help="Payment account ID (bank or CC)")],
    pay_type: Annotated[str, typer.Option("--pay-type", help="Cash, Check, or CreditCard")],
    amount: Annotated[Optional[float], typer.Option("--amount", help="Simple single-line amount")] = None,
    expense_account: Annotated[Optional[str], typer.Option("--expense-account", help="Expense GL account for simple entry")] = None,
    vendor_id: Annotated[Optional[str], typer.Option("--vendor-id", help="Vendor/payee ID")] = None,
    line_json: Annotated[Optional[str], typer.Option("--line-json", help="Line items as JSON array")] = None,
    txn_date: Annotated[Optional[str], typer.Option("--date", help="Transaction date (YYYY-MM-DD)")] = None,
    doc_number: Annotated[Optional[str], typer.Option("--doc-number", help="Check number or reference")] = None,
    memo: Annotated[Optional[str], typer.Option("--memo", help="Private memo/note")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full purchase JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create an expense (check, cash expense, or CC charge).

    Simple: --account-id 35 --pay-type Check --amount 250 --expense-account 7 --vendor-id 42
    Advanced: --account-id 35 --pay-type CreditCard --line-json '[...]'
    """
    fmt = output or _output()
    client = _client()

    if json_input:
        body = json.loads(json_input)
    elif line_json:
        lines = json.loads(line_json)
        body = {
            "AccountRef": {"value": account_id},
            "PaymentType": pay_type,
            "Line": lines,
        }
    elif amount is not None:
        # AccountRef is required; default to Uncategorized Expense (ID 31) if not specified
        line_detail: dict = {"AccountRef": {"value": expense_account or "31"}}
        body = {
            "AccountRef": {"value": account_id},
            "PaymentType": pay_type,
            "Line": [
                {
                    "Amount": amount,
                    "DetailType": "AccountBasedExpenseLineDetail",
                    "AccountBasedExpenseLineDetail": line_detail,
                }
            ],
        }
    else:
        typer.echo(
            json.dumps({"error": True, "message": "Provide --amount, --line-json, or --json"}),
            err=True,
        )
        raise SystemExit(5)

    if vendor_id:
        body["EntityRef"] = {"value": vendor_id, "type": "Vendor"}
    if txn_date:
        body["TxnDate"] = txn_date
    if doc_number:
        body["DocNumber"] = doc_number
    if memo:
        body["PrivateNote"] = memo

    result = client.post("purchase", body)
    format_output(result.get("Purchase"), fmt)


@app.command()
def update(
    expense_id: Annotated[str, typer.Argument(help="Purchase/Expense ID")],
    json_input: Annotated[str, typer.Option("--json", help="Fields to update as JSON")] = "{}",
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Update an existing expense. Auto-fetches SyncToken."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"purchase/{expense_id}").get("Purchase", {})
    body = json.loads(json_input)
    body["Id"] = current["Id"]
    body["SyncToken"] = current["SyncToken"]
    body.setdefault("sparse", True)

    result = client.post("purchase", body)
    format_output(result.get("Purchase"), fmt)


@app.command()
def delete(
    expense_id: Annotated[str, typer.Argument(help="Purchase/Expense ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Delete an expense."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"purchase/{expense_id}").get("Purchase", {})
    body = {
        "Id": current["Id"],
        "SyncToken": current["SyncToken"],
    }
    result = client.post("purchase", body, params={"operation": "delete"})
    format_output(result, fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against Purchase."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM Purchase WHERE {sql}"

    result = client.query(sql)
    purchases = result.get("QueryResponse", {}).get("Purchase", [])
    format_output(
        purchases,
        fmt,
        columns=["Id", "TxnDate", "AccountRef.name", "EntityRef.name", "TotalAmt", "PaymentType"],
    )
