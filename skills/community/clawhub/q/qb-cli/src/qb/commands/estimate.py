"""Estimate (Quote/Proposal) resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks estimates (quotes/proposals).")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_estimates(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all estimates."""
    fmt = output or _output()
    client = _client()
    result = client.query("SELECT * FROM Estimate", max_results=limit)
    estimates = result.get("QueryResponse", {}).get("Estimate", [])
    format_output(
        estimates,
        fmt,
        columns=["Id", "DocNumber", "CustomerRef.name", "TotalAmt", "TxnStatus", "ExpirationDate"],
    )


@app.command()
def get(
    estimate_id: Annotated[str, typer.Argument(help="Estimate ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get an estimate by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"estimate/{estimate_id}")
    format_output(result.get("Estimate"), fmt)


@app.command()
def create(
    customer_id: Annotated[str, typer.Option("--customer-id", help="Customer ID (required)")],
    amount: Annotated[Optional[float], typer.Option("--amount", help="Simple single-line amount")] = None,
    item_id: Annotated[str, typer.Option("--item-id", help="Item/service ID for simple estimate")] = "1",
    line_json: Annotated[Optional[str], typer.Option("--line-json", help="Line items as JSON array")] = None,
    expiration_date: Annotated[Optional[str], typer.Option("--expiration-date", help="Expiration date (YYYY-MM-DD)")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full estimate JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a new estimate.

    Simple: --customer-id 123 --amount 5000
    Advanced: --customer-id 123 --line-json '[{"Amount":100,...}]'
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
            json.dumps({"error": True, "message": "Provide --amount, --line-json, or --json"}),
            err=True,
        )
        raise SystemExit(5)

    if expiration_date:
        body["ExpirationDate"] = expiration_date

    result = client.post("estimate", body)
    format_output(result.get("Estimate"), fmt)


@app.command()
def update(
    estimate_id: Annotated[str, typer.Argument(help="Estimate ID")],
    json_input: Annotated[str, typer.Option("--json", help="Fields to update as JSON")] = "{}",
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Update an existing estimate. Auto-fetches SyncToken."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"estimate/{estimate_id}").get("Estimate", {})
    body = json.loads(json_input)
    body["Id"] = current["Id"]
    body["SyncToken"] = current["SyncToken"]
    body.setdefault("sparse", True)

    result = client.post("estimate", body)
    format_output(result.get("Estimate"), fmt)


@app.command()
def delete(
    estimate_id: Annotated[str, typer.Argument(help="Estimate ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Delete an estimate."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"estimate/{estimate_id}").get("Estimate", {})
    body = {
        "Id": current["Id"],
        "SyncToken": current["SyncToken"],
    }
    result = client.post("estimate", body, params={"operation": "delete"})
    format_output(result, fmt)


@app.command()
def send(
    estimate_id: Annotated[str, typer.Argument(help="Estimate ID")],
    email: Annotated[Optional[str], typer.Option("--email", help="Override recipient email")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Send an estimate by email."""
    fmt = output or _output()
    client = _client()

    params = {}
    if email:
        params["sendTo"] = email

    result = client.post(f"estimate/{estimate_id}/send", params=params)
    format_output(result.get("Estimate", result), fmt)


@app.command("to-invoice")
def to_invoice(
    estimate_id: Annotated[str, typer.Argument(help="Estimate ID to convert")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Convert an estimate to an invoice."""
    fmt = output or _output()
    client = _client()

    # Fetch estimate to get customer and lines
    est = client.get(f"estimate/{estimate_id}").get("Estimate", {})

    body = {
        "CustomerRef": est["CustomerRef"],
        "Line": est.get("Line", []),
        "LinkedTxn": [{"TxnId": estimate_id, "TxnType": "Estimate"}],
    }

    # Copy optional fields
    for field in ("BillEmail", "BillAddr", "ShipAddr", "DueDate", "SalesTermRef"):
        if field in est:
            body[field] = est[field]

    result = client.post("invoice", body)
    format_output(result.get("Invoice"), fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against Estimate."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM Estimate WHERE {sql}"

    result = client.query(sql)
    estimates = result.get("QueryResponse", {}).get("Estimate", [])
    format_output(
        estimates,
        fmt,
        columns=["Id", "DocNumber", "CustomerRef.name", "TotalAmt", "TxnStatus", "ExpirationDate"],
    )
