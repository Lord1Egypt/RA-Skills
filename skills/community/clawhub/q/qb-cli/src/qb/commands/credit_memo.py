"""CreditMemo resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks credit memos.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_memos(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all credit memos."""
    fmt = output or _output()
    client = _client()
    result = client.query("SELECT * FROM CreditMemo", max_results=limit)
    memos = result.get("QueryResponse", {}).get("CreditMemo", [])
    format_output(
        memos,
        fmt,
        columns=["Id", "DocNumber", "CustomerRef.name", "TotalAmt", "Balance", "TxnDate"],
    )


@app.command()
def get(
    memo_id: Annotated[str, typer.Argument(help="CreditMemo ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get a credit memo by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"creditmemo/{memo_id}")
    format_output(result.get("CreditMemo"), fmt)


@app.command()
def create(
    customer_id: Annotated[str, typer.Option("--customer-id", help="Customer ID (required)")],
    amount: Annotated[Optional[float], typer.Option("--amount", help="Simple single-line amount")] = None,
    item_id: Annotated[str, typer.Option("--item-id", help="Item/service ID")] = "1",
    line_json: Annotated[Optional[str], typer.Option("--line-json", help="Line items as JSON array")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full credit memo JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a credit memo."""
    fmt = output or _output()
    client = _client()

    if json_input:
        body = json.loads(json_input)
    elif line_json:
        body = {
            "CustomerRef": {"value": customer_id},
            "Line": json.loads(line_json),
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

    result = client.post("creditmemo", body)
    format_output(result.get("CreditMemo"), fmt)


@app.command()
def delete(
    memo_id: Annotated[str, typer.Argument(help="CreditMemo ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Delete a credit memo."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"creditmemo/{memo_id}").get("CreditMemo", {})
    body = {"Id": current["Id"], "SyncToken": current["SyncToken"]}
    result = client.post("creditmemo", body, params={"operation": "delete"})
    format_output(result, fmt)


@app.command()
def void(
    memo_id: Annotated[str, typer.Argument(help="CreditMemo ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Void a credit memo (zeros amounts, keeps record)."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"creditmemo/{memo_id}").get("CreditMemo", {})
    body = {"Id": current["Id"], "SyncToken": current["SyncToken"], "sparse": True}
    result = client.post("creditmemo", body, params={"include": "void"})
    format_output(result.get("CreditMemo", result), fmt)


@app.command()
def send(
    memo_id: Annotated[str, typer.Argument(help="CreditMemo ID")],
    email: Annotated[Optional[str], typer.Option("--email", help="Override recipient email")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Send a credit memo by email."""
    fmt = output or _output()
    client = _client()

    params = {}
    if email:
        params["sendTo"] = email

    result = client.post(f"creditmemo/{memo_id}/send", params=params)
    format_output(result.get("CreditMemo", result), fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against CreditMemo."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM CreditMemo WHERE {sql}"

    result = client.query(sql)
    memos = result.get("QueryResponse", {}).get("CreditMemo", [])
    format_output(
        memos,
        fmt,
        columns=["Id", "DocNumber", "CustomerRef.name", "TotalAmt", "Balance", "TxnDate"],
    )
