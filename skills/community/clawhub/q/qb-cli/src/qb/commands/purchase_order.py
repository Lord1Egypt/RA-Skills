"""PurchaseOrder resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks purchase orders.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_pos(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all purchase orders."""
    fmt = output or _output()
    client = _client()
    result = client.query("SELECT * FROM PurchaseOrder", max_results=limit)
    pos = result.get("QueryResponse", {}).get("PurchaseOrder", [])
    format_output(
        pos,
        fmt,
        columns=["Id", "DocNumber", "VendorRef.name", "TotalAmt", "POStatus", "TxnDate"],
    )


@app.command()
def get(
    po_id: Annotated[str, typer.Argument(help="PurchaseOrder ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get a purchase order by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"purchaseorder/{po_id}")
    format_output(result.get("PurchaseOrder"), fmt)


@app.command()
def create(
    vendor_id: Annotated[str, typer.Option("--vendor-id", help="Vendor ID (required)")],
    line_json: Annotated[Optional[str], typer.Option("--line-json", help="Line items as JSON array")] = None,
    amount: Annotated[Optional[float], typer.Option("--amount", help="Simple single-line amount")] = None,
    item_id: Annotated[Optional[str], typer.Option("--item-id", help="Item ID for simple PO")] = None,
    txn_date: Annotated[Optional[str], typer.Option("--date", help="PO date (YYYY-MM-DD)")] = None,
    memo: Annotated[Optional[str], typer.Option("--memo", help="Vendor-visible memo (printed on PO)")] = None,
    private_note: Annotated[Optional[str], typer.Option("--note", help="Private internal note")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full PO JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a purchase order."""
    fmt = output or _output()
    client = _client()

    if json_input:
        body = json.loads(json_input)
    elif line_json:
        body = {
            "VendorRef": {"value": vendor_id},
            "Line": json.loads(line_json),
        }
    elif amount is not None:
        if item_id:
            # Item-based line (requires ItemRef)
            line: dict = {
                "Amount": amount,
                "DetailType": "ItemBasedExpenseLineDetail",
                "ItemBasedExpenseLineDetail": {
                    "ItemRef": {"value": item_id},
                    "Qty": 1,
                    "UnitPrice": amount,
                },
            }
        else:
            # No item specified — error out since PO requires ItemRef
            typer.echo(
                json.dumps({"error": True, "message": "--item-id is required for PO line items (use --line-json for custom lines)"}),
                err=True,
            )
            raise SystemExit(5)
        body = {
            "VendorRef": {"value": vendor_id},
            "Line": [line],
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
        body["Memo"] = memo
    if private_note:
        body["PrivateNote"] = private_note

    result = client.post("purchaseorder", body)
    format_output(result.get("PurchaseOrder"), fmt)


@app.command()
def update(
    po_id: Annotated[str, typer.Argument(help="PurchaseOrder ID")],
    json_input: Annotated[str, typer.Option("--json", help="Fields to update as JSON")] = "{}",
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Update a purchase order. Auto-fetches SyncToken."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"purchaseorder/{po_id}").get("PurchaseOrder", {})
    body = json.loads(json_input)
    body["Id"] = current["Id"]
    body["SyncToken"] = current["SyncToken"]
    body.setdefault("sparse", True)

    result = client.post("purchaseorder", body)
    format_output(result.get("PurchaseOrder"), fmt)


@app.command()
def delete(
    po_id: Annotated[str, typer.Argument(help="PurchaseOrder ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Delete a purchase order."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"purchaseorder/{po_id}").get("PurchaseOrder", {})
    body = {"Id": current["Id"], "SyncToken": current["SyncToken"]}
    result = client.post("purchaseorder", body, params={"operation": "delete"})
    format_output(result, fmt)


@app.command()
def send(
    po_id: Annotated[str, typer.Argument(help="PurchaseOrder ID")],
    email: Annotated[Optional[str], typer.Option("--email", help="Override recipient email")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Send a purchase order by email to the vendor."""
    fmt = output or _output()
    client = _client()

    params = {}
    if email:
        params["sendTo"] = email

    result = client.post(f"purchaseorder/{po_id}/send", params=params)
    format_output(result.get("PurchaseOrder", result), fmt)


@app.command("to-bill")
def to_bill(
    po_id: Annotated[str, typer.Argument(help="PurchaseOrder ID to convert")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Convert a purchase order to a bill (upon receiving goods)."""
    fmt = output or _output()
    client = _client()

    po = client.get(f"purchaseorder/{po_id}").get("PurchaseOrder", {})

    body = {
        "VendorRef": po["VendorRef"],
        "Line": po.get("Line", []),
        "LinkedTxn": [{"TxnId": po_id, "TxnType": "PurchaseOrder"}],
    }

    for field in ("DueDate", "APAccountRef", "SalesTermRef"):
        if field in po:
            body[field] = po[field]

    result = client.post("bill", body)
    format_output(result.get("Bill"), fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against PurchaseOrder."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM PurchaseOrder WHERE {sql}"

    result = client.query(sql)
    pos = result.get("QueryResponse", {}).get("PurchaseOrder", [])
    format_output(
        pos,
        fmt,
        columns=["Id", "DocNumber", "VendorRef.name", "TotalAmt", "POStatus", "TxnDate"],
    )
