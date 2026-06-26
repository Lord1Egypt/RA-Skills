"""Deposit resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks deposits.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_deposits(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all deposits."""
    fmt = output or _output()
    client = _client()
    result = client.query("SELECT * FROM Deposit", max_results=limit)
    deposits = result.get("QueryResponse", {}).get("Deposit", [])
    format_output(
        deposits,
        fmt,
        columns=["Id", "TxnDate", "DepositToAccountRef.name", "TotalAmt"],
    )


@app.command()
def get(
    deposit_id: Annotated[str, typer.Argument(help="Deposit ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get a deposit by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"deposit/{deposit_id}")
    format_output(result.get("Deposit"), fmt)


@app.command()
def create(
    account_id: Annotated[str, typer.Option("--account-id", help="Bank account to deposit into (required)")],
    payment_ids: Annotated[
        Optional[str],
        typer.Option("--payment-ids", help="Comma-separated payment/sales-receipt IDs from Undeposited Funds"),
    ] = None,
    line_json: Annotated[Optional[str], typer.Option("--line-json", help="Line items as JSON array")] = None,
    txn_date: Annotated[Optional[str], typer.Option("--date", help="Deposit date (YYYY-MM-DD)")] = None,
    memo: Annotated[Optional[str], typer.Option("--memo", help="Private note")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full deposit JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a deposit (group payments from Undeposited Funds into a bank deposit).

    From payments: --account-id 35 --payment-ids 182,183,184
    Full control: --json '{...}'
    """
    fmt = output or _output()
    client = _client()

    if json_input:
        body = json.loads(json_input)
    elif line_json:
        body = {
            "DepositToAccountRef": {"value": account_id},
            "Line": json.loads(line_json),
        }
    elif payment_ids:
        ids = [i.strip() for i in payment_ids.split(",")]
        lines = []
        for pid in ids:
            lines.append({
                "LinkedTxn": [{"TxnId": pid, "TxnType": "Payment"}],
            })
        body = {
            "DepositToAccountRef": {"value": account_id},
            "Line": lines,
        }
    else:
        typer.echo(
            json.dumps({"error": True, "message": "Provide --payment-ids, --line-json, or --json"}),
            err=True,
        )
        raise SystemExit(5)

    if txn_date:
        body["TxnDate"] = txn_date
    if memo:
        body["PrivateNote"] = memo

    result = client.post("deposit", body)
    format_output(result.get("Deposit"), fmt)


@app.command()
def delete(
    deposit_id: Annotated[str, typer.Argument(help="Deposit ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Delete a deposit."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"deposit/{deposit_id}").get("Deposit", {})
    body = {"Id": current["Id"], "SyncToken": current["SyncToken"]}
    result = client.post("deposit", body, params={"operation": "delete"})
    format_output(result, fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against Deposit."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM Deposit WHERE {sql}"

    result = client.query(sql)
    deposits = result.get("QueryResponse", {}).get("Deposit", [])
    format_output(
        deposits,
        fmt,
        columns=["Id", "TxnDate", "DepositToAccountRef.name", "TotalAmt"],
    )
