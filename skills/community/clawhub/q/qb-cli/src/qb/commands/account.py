"""Account (Chart of Accounts) resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks chart of accounts.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_accounts(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 200,
    active_only: Annotated[bool, typer.Option(help="Only active accounts")] = True,
    account_type: Annotated[Optional[str], typer.Option("--type", help="Filter by AccountType (Bank, Expense, Income, etc.)")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List chart of accounts."""
    fmt = output or _output()
    client = _client()
    clauses = []
    if active_only:
        clauses.append("Active = true")
    if account_type:
        clauses.append(f"AccountType = '{account_type}'")
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    result = client.query(f"SELECT * FROM Account {where}", max_results=limit)
    accounts = result.get("QueryResponse", {}).get("Account", [])
    format_output(
        accounts,
        fmt,
        columns=["Id", "Name", "AccountType", "AccountSubType", "CurrentBalance", "AcctNum", "Active"],
    )


@app.command()
def get(
    account_id: Annotated[str, typer.Argument(help="Account ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get an account by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"account/{account_id}")
    format_output(result.get("Account"), fmt)


@app.command()
def create(
    name: Annotated[str, typer.Option("--name", help="Account name (required)")],
    account_type: Annotated[str, typer.Option("--type", help="AccountType (Bank, Expense, Income, CostOfGoodsSold, etc.)")],
    sub_type: Annotated[Optional[str], typer.Option("--sub-type", help="AccountSubType (Checking, Savings, AdvertisingPromotional, etc.)")] = None,
    acct_num: Annotated[Optional[str], typer.Option("--acct-num", help="Account number")] = None,
    description: Annotated[Optional[str], typer.Option("--description", help="Description")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full account JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a new account."""
    fmt = output or _output()
    client = _client()

    if json_input:
        body = json.loads(json_input)
    else:
        body: dict = {
            "Name": name,
            "AccountType": account_type,
        }
        if sub_type:
            body["AccountSubType"] = sub_type
        if acct_num:
            body["AcctNum"] = acct_num
        if description:
            body["Description"] = description

    result = client.post("account", body)
    format_output(result.get("Account"), fmt)


@app.command()
def update(
    account_id: Annotated[str, typer.Argument(help="Account ID")],
    name: Annotated[Optional[str], typer.Option("--name", help="Account name")] = None,
    description: Annotated[Optional[str], typer.Option("--description", help="Description")] = None,
    acct_num: Annotated[Optional[str], typer.Option("--acct-num", help="Account number")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full update JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Update an account. Auto-fetches current state (Account requires full update)."""
    fmt = output or _output()
    client = _client()

    # Account requires FULL update (not sparse) — fetch entire entity and merge
    current = client.get(f"account/{account_id}").get("Account", {})

    if json_input:
        body = json.loads(json_input)
        body["Id"] = current["Id"]
        body["SyncToken"] = current["SyncToken"]
    else:
        body = dict(current)  # start from full current state
        if name:
            body["Name"] = name
        if description:
            body["Description"] = description
        if acct_num:
            body["AcctNum"] = acct_num

    result = client.post("account", body)
    format_output(result.get("Account"), fmt)


@app.command()
def delete(
    account_id: Annotated[str, typer.Argument(help="Account ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Deactivate an account (soft delete — sets Active=false)."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"account/{account_id}").get("Account", {})
    body = dict(current)
    body["Active"] = False

    result = client.post("account", body)
    format_output(result.get("Account"), fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against Account."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM Account WHERE {sql}"

    result = client.query(sql)
    accounts = result.get("QueryResponse", {}).get("Account", [])
    format_output(
        accounts,
        fmt,
        columns=["Id", "Name", "AccountType", "AccountSubType", "CurrentBalance", "AcctNum", "Active"],
    )
