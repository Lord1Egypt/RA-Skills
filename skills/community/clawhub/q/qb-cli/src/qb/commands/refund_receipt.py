"""RefundReceipt resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks refund receipts.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_refunds(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all refund receipts."""
    fmt = output or _output()
    client = _client()
    result = client.query("SELECT * FROM RefundReceipt", max_results=limit)
    refunds = result.get("QueryResponse", {}).get("RefundReceipt", [])
    format_output(
        refunds,
        fmt,
        columns=["Id", "DocNumber", "CustomerRef.name", "TotalAmt", "TxnDate"],
    )


@app.command()
def get(
    refund_id: Annotated[str, typer.Argument(help="RefundReceipt ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get a refund receipt by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"refundreceipt/{refund_id}")
    format_output(result.get("RefundReceipt"), fmt)


@app.command()
def create(
    customer_id: Annotated[Optional[str], typer.Option("--customer-id", help="Customer ID")] = None,
    amount: Annotated[Optional[float], typer.Option("--amount", help="Simple single-line amount")] = None,
    item_id: Annotated[str, typer.Option("--item-id", help="Item/service ID")] = "1",
    deposit_from: Annotated[Optional[str], typer.Option("--deposit-from", help="Account the refund is paid from")] = None,
    line_json: Annotated[Optional[str], typer.Option("--line-json", help="Line items as JSON array")] = None,
    txn_date: Annotated[Optional[str], typer.Option("--date", help="Transaction date (YYYY-MM-DD)")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full refund receipt JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a refund receipt."""
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
    # DepositToAccountRef is required; default to Undeposited Funds (ID 4)
    body["DepositToAccountRef"] = {"value": deposit_from or "4"}
    if txn_date:
        body["TxnDate"] = txn_date

    result = client.post("refundreceipt", body)
    format_output(result.get("RefundReceipt"), fmt)


@app.command()
def delete(
    refund_id: Annotated[str, typer.Argument(help="RefundReceipt ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Delete a refund receipt."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"refundreceipt/{refund_id}").get("RefundReceipt", {})
    body = {"Id": current["Id"], "SyncToken": current["SyncToken"]}
    result = client.post("refundreceipt", body, params={"operation": "delete"})
    format_output(result, fmt)


@app.command()
def void(
    refund_id: Annotated[str, typer.Argument(help="RefundReceipt ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Void a refund receipt (zeros amounts, keeps record)."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"refundreceipt/{refund_id}").get("RefundReceipt", {})
    body = {"Id": current["Id"], "SyncToken": current["SyncToken"], "sparse": True}
    result = client.post("refundreceipt", body, params={"include": "void"})
    format_output(result.get("RefundReceipt", result), fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against RefundReceipt."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM RefundReceipt WHERE {sql}"

    result = client.query(sql)
    refunds = result.get("QueryResponse", {}).get("RefundReceipt", [])
    format_output(
        refunds,
        fmt,
        columns=["Id", "DocNumber", "CustomerRef.name", "TotalAmt", "TxnDate"],
    )
