"""SalesReceipt resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks sales receipts (cash sales).")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_receipts(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all sales receipts."""
    fmt = output or _output()
    client = _client()
    result = client.query("SELECT * FROM SalesReceipt", max_results=limit)
    receipts = result.get("QueryResponse", {}).get("SalesReceipt", [])
    format_output(
        receipts,
        fmt,
        columns=["Id", "DocNumber", "CustomerRef.name", "TotalAmt", "Balance", "TxnDate"],
    )


@app.command()
def get(
    receipt_id: Annotated[str, typer.Argument(help="SalesReceipt ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get a sales receipt by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"salesreceipt/{receipt_id}")
    format_output(result.get("SalesReceipt"), fmt)


@app.command()
def create(
    customer_id: Annotated[Optional[str], typer.Option("--customer-id", help="Customer ID")] = None,
    amount: Annotated[Optional[float], typer.Option("--amount", help="Simple single-line amount")] = None,
    item_id: Annotated[str, typer.Option("--item-id", help="Item/service ID")] = "1",
    line_json: Annotated[Optional[str], typer.Option("--line-json", help="Line items as JSON array")] = None,
    deposit_to: Annotated[Optional[str], typer.Option("--deposit-to", help="Deposit account ID")] = None,
    payment_method: Annotated[Optional[str], typer.Option("--payment-method", help="Payment method ref ID")] = None,
    txn_date: Annotated[Optional[str], typer.Option("--date", help="Transaction date (YYYY-MM-DD)")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full sales receipt JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a sales receipt (cash sale — payment at time of sale)."""
    fmt = output or _output()
    client = _client()

    if json_input:
        body = json.loads(json_input)
    elif line_json:
        body: dict = {"Line": json.loads(line_json)}
    elif amount is not None:
        body = {
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

    if customer_id:
        body["CustomerRef"] = {"value": customer_id}
    if deposit_to:
        body["DepositToAccountRef"] = {"value": deposit_to}
    if payment_method:
        body["PaymentMethodRef"] = {"value": payment_method}
    if txn_date:
        body["TxnDate"] = txn_date

    result = client.post("salesreceipt", body)
    format_output(result.get("SalesReceipt"), fmt)


@app.command()
def delete(
    receipt_id: Annotated[str, typer.Argument(help="SalesReceipt ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Delete a sales receipt."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"salesreceipt/{receipt_id}").get("SalesReceipt", {})
    body = {"Id": current["Id"], "SyncToken": current["SyncToken"]}
    result = client.post("salesreceipt", body, params={"operation": "delete"})
    format_output(result, fmt)


@app.command()
def void(
    receipt_id: Annotated[str, typer.Argument(help="SalesReceipt ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Void a sales receipt (zeros amounts, keeps record)."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"salesreceipt/{receipt_id}").get("SalesReceipt", {})
    body = {"Id": current["Id"], "SyncToken": current["SyncToken"], "sparse": True}
    result = client.post("salesreceipt", body, params={"include": "void"})
    format_output(result.get("SalesReceipt", result), fmt)


@app.command()
def send(
    receipt_id: Annotated[str, typer.Argument(help="SalesReceipt ID")],
    email: Annotated[Optional[str], typer.Option("--email", help="Override recipient email")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Send a sales receipt by email."""
    fmt = output or _output()
    client = _client()

    params = {}
    if email:
        params["sendTo"] = email

    result = client.post(f"salesreceipt/{receipt_id}/send", params=params)
    format_output(result.get("SalesReceipt", result), fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against SalesReceipt."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM SalesReceipt WHERE {sql}"

    result = client.query(sql)
    receipts = result.get("QueryResponse", {}).get("SalesReceipt", [])
    format_output(
        receipts,
        fmt,
        columns=["Id", "DocNumber", "CustomerRef.name", "TotalAmt", "Balance", "TxnDate"],
    )
