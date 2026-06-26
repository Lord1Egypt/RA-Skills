"""Transfer resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks transfers between accounts.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_transfers(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all transfers."""
    fmt = output or _output()
    client = _client()
    result = client.query("SELECT * FROM Transfer", max_results=limit)
    transfers = result.get("QueryResponse", {}).get("Transfer", [])
    format_output(
        transfers,
        fmt,
        columns=["Id", "TxnDate", "FromAccountRef.name", "ToAccountRef.name", "Amount"],
    )


@app.command()
def get(
    transfer_id: Annotated[str, typer.Argument(help="Transfer ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get a transfer by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"transfer/{transfer_id}")
    format_output(result.get("Transfer"), fmt)


@app.command()
def create(
    from_account: Annotated[str, typer.Option("--from", help="Source account ID")],
    to_account: Annotated[str, typer.Option("--to", help="Destination account ID")],
    amount: Annotated[float, typer.Option("--amount", help="Transfer amount")],
    txn_date: Annotated[Optional[str], typer.Option("--date", help="Transfer date (YYYY-MM-DD)")] = None,
    memo: Annotated[Optional[str], typer.Option("--memo", help="Private note")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full transfer JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a transfer between accounts.

    Example: --from 35 --to 36 --amount 1000 --date 2026-02-15
    """
    fmt = output or _output()
    client = _client()

    if json_input:
        body = json.loads(json_input)
    else:
        body = {
            "FromAccountRef": {"value": from_account},
            "ToAccountRef": {"value": to_account},
            "Amount": amount,
        }

    if txn_date:
        body["TxnDate"] = txn_date
    if memo:
        body["PrivateNote"] = memo

    result = client.post("transfer", body)
    format_output(result.get("Transfer"), fmt)


@app.command()
def delete(
    transfer_id: Annotated[str, typer.Argument(help="Transfer ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Delete a transfer."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"transfer/{transfer_id}").get("Transfer", {})
    body = {"Id": current["Id"], "SyncToken": current["SyncToken"]}
    result = client.post("transfer", body, params={"operation": "delete"})
    format_output(result, fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against Transfer."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM Transfer WHERE {sql}"

    result = client.query(sql)
    transfers = result.get("QueryResponse", {}).get("Transfer", [])
    format_output(
        transfers,
        fmt,
        columns=["Id", "TxnDate", "FromAccountRef.name", "ToAccountRef.name", "Amount"],
    )
