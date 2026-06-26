"""VendorCredit resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks vendor credits.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_credits(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all vendor credits."""
    fmt = output or _output()
    client = _client()
    result = client.query("SELECT * FROM VendorCredit", max_results=limit)
    credits = result.get("QueryResponse", {}).get("VendorCredit", [])
    format_output(
        credits,
        fmt,
        columns=["Id", "TxnDate", "VendorRef.name", "TotalAmt", "Balance"],
    )


@app.command()
def get(
    credit_id: Annotated[str, typer.Argument(help="VendorCredit ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get a vendor credit by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"vendorcredit/{credit_id}")
    format_output(result.get("VendorCredit"), fmt)


@app.command()
def create(
    vendor_id: Annotated[str, typer.Option("--vendor-id", help="Vendor ID (required)")],
    amount: Annotated[Optional[float], typer.Option("--amount", help="Simple single-line amount")] = None,
    account_id: Annotated[Optional[str], typer.Option("--account-id", help="Expense account ID")] = None,
    line_json: Annotated[Optional[str], typer.Option("--line-json", help="Line items as JSON array")] = None,
    txn_date: Annotated[Optional[str], typer.Option("--date", help="Credit date (YYYY-MM-DD)")] = None,
    memo: Annotated[Optional[str], typer.Option("--memo", help="Private memo/note")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full vendor credit JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a vendor credit."""
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

    if txn_date:
        body["TxnDate"] = txn_date
    if memo:
        body["PrivateNote"] = memo

    result = client.post("vendorcredit", body)
    format_output(result.get("VendorCredit"), fmt)


@app.command()
def delete(
    credit_id: Annotated[str, typer.Argument(help="VendorCredit ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Delete a vendor credit."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"vendorcredit/{credit_id}").get("VendorCredit", {})
    body = {
        "Id": current["Id"],
        "SyncToken": current["SyncToken"],
    }
    result = client.post("vendorcredit", body, params={"operation": "delete"})
    format_output(result, fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against VendorCredit."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM VendorCredit WHERE {sql}"

    result = client.query(sql)
    credits = result.get("QueryResponse", {}).get("VendorCredit", [])
    format_output(
        credits,
        fmt,
        columns=["Id", "TxnDate", "VendorRef.name", "TotalAmt", "Balance"],
    )
