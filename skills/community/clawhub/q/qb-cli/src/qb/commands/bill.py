"""Bill (Accounts Payable) resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks bills (accounts payable).")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_bills(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all bills."""
    fmt = output or _output()
    client = _client()
    result = client.query("SELECT * FROM Bill", max_results=limit)
    bills = result.get("QueryResponse", {}).get("Bill", [])
    format_output(
        bills,
        fmt,
        columns=["Id", "DocNumber", "VendorRef.name", "TotalAmt", "Balance", "DueDate"],
    )


@app.command()
def get(
    bill_id: Annotated[str, typer.Argument(help="Bill ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get a bill by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"bill/{bill_id}")
    format_output(result.get("Bill"), fmt)


@app.command()
def create(
    vendor_id: Annotated[str, typer.Option("--vendor-id", help="Vendor ID (required)")],
    amount: Annotated[Optional[float], typer.Option("--amount", help="Simple single-line amount")] = None,
    account_id: Annotated[Optional[str], typer.Option("--account-id", help="Expense account ID for simple bill")] = None,
    line_json: Annotated[Optional[str], typer.Option("--line-json", help="Line items as JSON array")] = None,
    due_date: Annotated[Optional[str], typer.Option("--due-date", help="Due date (YYYY-MM-DD)")] = None,
    txn_date: Annotated[Optional[str], typer.Option("--date", help="Bill date (YYYY-MM-DD)")] = None,
    doc_number: Annotated[Optional[str], typer.Option("--doc-number", help="Vendor invoice number")] = None,
    memo: Annotated[Optional[str], typer.Option("--memo", help="Private memo/note")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full bill JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a new bill.

    Simple: --vendor-id 42 --amount 500 --account-id 7
    Advanced: --vendor-id 42 --line-json '[{"Amount":100,...}]'
    Full control: --json '{"VendorRef":{"value":"42"},...}'
    """
    fmt = output or _output()
    client = _client()

    if json_input:
        body = json.loads(json_input)
    elif line_json:
        lines = json.loads(line_json)
        body = {
            "VendorRef": {"value": vendor_id},
            "Line": lines,
        }
    elif amount is not None:
        # AccountRef is required; default to Uncategorized Expense (ID 31) if not specified
        line_detail: dict = {"AccountRef": {"value": account_id or "31"}}
        body = {
            "VendorRef": {"value": vendor_id},
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

    if due_date:
        body["DueDate"] = due_date
    if txn_date:
        body["TxnDate"] = txn_date
    if doc_number:
        body["DocNumber"] = doc_number
    if memo:
        body["PrivateNote"] = memo

    result = client.post("bill", body)
    format_output(result.get("Bill"), fmt)


@app.command()
def update(
    bill_id: Annotated[str, typer.Argument(help="Bill ID")],
    json_input: Annotated[str, typer.Option("--json", help="Fields to update as JSON")] = "{}",
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Update an existing bill. Auto-fetches SyncToken."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"bill/{bill_id}").get("Bill", {})
    body = json.loads(json_input)
    body["Id"] = current["Id"]
    body["SyncToken"] = current["SyncToken"]
    body.setdefault("sparse", True)

    result = client.post("bill", body)
    format_output(result.get("Bill"), fmt)


@app.command()
def delete(
    bill_id: Annotated[str, typer.Argument(help="Bill ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Delete a bill."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"bill/{bill_id}").get("Bill", {})
    body = {
        "Id": current["Id"],
        "SyncToken": current["SyncToken"],
    }
    result = client.post("bill", body, params={"operation": "delete"})
    format_output(result, fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against Bill."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM Bill WHERE {sql}"

    result = client.query(sql)
    bills = result.get("QueryResponse", {}).get("Bill", [])
    format_output(
        bills,
        fmt,
        columns=["Id", "DocNumber", "VendorRef.name", "TotalAmt", "Balance", "DueDate"],
    )
