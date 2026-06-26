"""Invoice resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks invoices.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_invoices(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all invoices."""
    fmt = output or _output()
    client = _client()
    result = client.query("SELECT * FROM Invoice", max_results=limit)
    invoices = result.get("QueryResponse", {}).get("Invoice", [])
    format_output(
        invoices,
        fmt,
        columns=["Id", "DocNumber", "CustomerRef.name", "TotalAmt", "Balance", "DueDate"],
    )


@app.command()
def get(
    invoice_id: Annotated[str, typer.Argument(help="Invoice ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get an invoice by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"invoice/{invoice_id}")
    format_output(result.get("Invoice"), fmt)


@app.command()
def create(
    customer_id: Annotated[str, typer.Option("--customer-id", help="Customer ID (required)")],
    line_json: Annotated[
        Optional[str],
        typer.Option("--line-json", help="Line items as JSON array"),
    ] = None,
    amount: Annotated[Optional[float], typer.Option("--amount", help="Simple single-line amount")] = None,
    item_id: Annotated[str, typer.Option("--item-id", help="Item/service ID for simple invoice")] = "1",
    due_date: Annotated[Optional[str], typer.Option("--due-date", help="Due date (YYYY-MM-DD)")] = None,
    json_input: Annotated[
        Optional[str],
        typer.Option("--json", help="Full invoice JSON (overrides other flags)"),
    ] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a new invoice.

    Simple usage: --customer-id 123 --amount 500
    Advanced: --customer-id 123 --line-json '[{"Amount":100,...}]'
    Full control: --json '{"CustomerRef":{"value":"123"},...}'
    """
    fmt = output or _output()
    client = _client()

    if json_input:
        body = json.loads(json_input)
    elif line_json:
        lines = json.loads(line_json)
        body = {
            "CustomerRef": {"value": customer_id},
            "Line": lines,
        }
    elif amount is not None:
        body = {
            "CustomerRef": {"value": customer_id},
            "Line": [
                {
                    "Amount": amount,
                    "DetailType": "SalesItemLineDetail",
                    "SalesItemLineDetail": {
                        "ItemRef": {"value": item_id},
                        "Qty": 1,
                        "UnitPrice": amount,
                    },
                }
            ],
        }
    else:
        typer.echo(
            json.dumps({
                "error": True,
                "message": "Provide --amount, --line-json, or --json",
            }),
            err=True,
        )
        raise SystemExit(5)

    if due_date:
        body["DueDate"] = due_date

    result = client.post("invoice", body)
    format_output(result.get("Invoice"), fmt)


@app.command()
def update(
    invoice_id: Annotated[str, typer.Argument(help="Invoice ID")],
    json_input: Annotated[
        str,
        typer.Option("--json", help="Fields to update as JSON"),
    ] = "{}",
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Update an existing invoice. Auto-fetches SyncToken."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"invoice/{invoice_id}").get("Invoice", {})
    body = json.loads(json_input)
    body["Id"] = current["Id"]
    body["SyncToken"] = current["SyncToken"]
    body.setdefault("sparse", True)

    result = client.post("invoice", body)
    format_output(result.get("Invoice"), fmt)


@app.command()
def delete(
    invoice_id: Annotated[str, typer.Argument(help="Invoice ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Delete an invoice."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"invoice/{invoice_id}").get("Invoice", {})
    body = {
        "Id": current["Id"],
        "SyncToken": current["SyncToken"],
    }
    result = client.post("invoice", body, params={"operation": "delete"})
    format_output(result, fmt)


@app.command()
def send(
    invoice_id: Annotated[str, typer.Argument(help="Invoice ID")],
    email: Annotated[
        Optional[str],
        typer.Option("--email", help="Override recipient email"),
    ] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Send an invoice by email to the customer."""
    fmt = output or _output()
    client = _client()

    params = {}
    if email:
        params["sendTo"] = email

    result = client.post(f"invoice/{invoice_id}/send", params=params)
    format_output(result.get("Invoice", result), fmt)


@app.command()
def void(
    invoice_id: Annotated[str, typer.Argument(help="Invoice ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Void an invoice (zeros amounts, keeps record)."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"invoice/{invoice_id}").get("Invoice", {})
    body = {"Id": current["Id"], "SyncToken": current["SyncToken"]}
    result = client.post("invoice", body, params={"operation": "void"})
    format_output(result.get("Invoice", result), fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against Invoice."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM Invoice WHERE {sql}"

    result = client.query(sql)
    invoices = result.get("QueryResponse", {}).get("Invoice", [])
    format_output(
        invoices,
        fmt,
        columns=["Id", "DocNumber", "CustomerRef.name", "TotalAmt", "Balance", "DueDate"],
    )
