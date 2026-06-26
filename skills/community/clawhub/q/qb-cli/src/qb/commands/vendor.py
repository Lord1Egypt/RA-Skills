"""Vendor resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks vendors.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_vendors(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    active_only: Annotated[bool, typer.Option(help="Only active vendors")] = True,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all vendors."""
    fmt = output or _output()
    client = _client()
    where = "WHERE Active = true" if active_only else ""
    result = client.query(f"SELECT * FROM Vendor {where}", max_results=limit)
    vendors = result.get("QueryResponse", {}).get("Vendor", [])
    format_output(
        vendors,
        fmt,
        columns=["Id", "DisplayName", "CompanyName", "PrimaryEmailAddr.Address", "Balance", "Vendor1099"],
    )


@app.command()
def get(
    vendor_id: Annotated[str, typer.Argument(help="Vendor ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get a vendor by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"vendor/{vendor_id}")
    format_output(result.get("Vendor"), fmt)


@app.command()
def search(
    term: Annotated[str, typer.Argument(help="Search term (name, company, or email)")],
    include_inactive: Annotated[bool, typer.Option("--include-inactive", help="Include inactive vendors")] = False,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Search vendors by name, company, or email."""
    fmt = output or _output()
    client = _client()

    from qb.api.query import escape_query_value

    fields = ["DisplayName", "CompanyName", "PrimaryEmailAddr"]
    escaped = escape_query_value(term)
    seen_ids = set()
    results = []

    for field in fields:
        where = f"{field} LIKE '%{escaped}%'"
        if not include_inactive:
            where += " AND Active = true"
        try:
            resp = client.query(f"SELECT * FROM Vendor WHERE {where}")
            for v in resp.get("QueryResponse", {}).get("Vendor", []):
                if v["Id"] not in seen_ids:
                    seen_ids.add(v["Id"])
                    results.append(v)
        except Exception:
            continue

    format_output(
        results,
        fmt,
        columns=["Id", "DisplayName", "CompanyName", "PrimaryEmailAddr.Address", "Balance", "Vendor1099"],
    )


@app.command()
def create(
    name: Annotated[Optional[str], typer.Option("--name", help="Display name")] = None,
    email: Annotated[Optional[str], typer.Option("--email", help="Email address")] = None,
    phone: Annotated[Optional[str], typer.Option("--phone", help="Phone number")] = None,
    company_name: Annotated[Optional[str], typer.Option("--company", help="Company name")] = None,
    tax_id: Annotated[Optional[str], typer.Option("--tax-id", help="Tax identifier (SSN/EIN)")] = None,
    is_1099: Annotated[bool, typer.Option("--1099", help="Track as 1099 vendor")] = False,
    acct_num: Annotated[Optional[str], typer.Option("--acct-num", help="Account number")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full vendor JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a new vendor."""
    fmt = output or _output()
    client = _client()

    if json_input:
        body = json.loads(json_input)
    else:
        if not name:
            typer.echo(
                json.dumps({"error": True, "message": "--name is required (or use --json)"}),
                err=True,
            )
            raise SystemExit(5)
        body: dict = {"DisplayName": name}
        if email:
            body["PrimaryEmailAddr"] = {"Address": email}
        if phone:
            body["PrimaryPhone"] = {"FreeFormNumber": phone}
        if company_name:
            body["CompanyName"] = company_name
        if tax_id:
            body["TaxIdentifier"] = tax_id
        if is_1099:
            body["Vendor1099"] = True
        if acct_num:
            body["AcctNum"] = acct_num

    result = client.post("vendor", body)
    format_output(result.get("Vendor"), fmt)


@app.command()
def update(
    vendor_id: Annotated[str, typer.Argument(help="Vendor ID")],
    name: Annotated[Optional[str], typer.Option("--name", help="Display name")] = None,
    email: Annotated[Optional[str], typer.Option("--email", help="Email")] = None,
    phone: Annotated[Optional[str], typer.Option("--phone", help="Phone")] = None,
    is_1099: Annotated[Optional[bool], typer.Option("--1099", help="Track as 1099 vendor")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full update JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Update an existing vendor. Auto-fetches SyncToken."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"vendor/{vendor_id}").get("Vendor", {})

    if json_input:
        body = json.loads(json_input)
        body["Id"] = current["Id"]
        body["SyncToken"] = current["SyncToken"]
    else:
        body = {
            "Id": current["Id"],
            "SyncToken": current["SyncToken"],
            "sparse": True,
        }
        if name:
            body["DisplayName"] = name
        if email:
            body["PrimaryEmailAddr"] = {"Address": email}
        if phone:
            body["PrimaryPhone"] = {"FreeFormNumber": phone}
        if is_1099 is not None:
            body["Vendor1099"] = is_1099

    result = client.post("vendor", body)
    format_output(result.get("Vendor"), fmt)


@app.command()
def delete(
    vendor_id: Annotated[str, typer.Argument(help="Vendor ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Deactivate a vendor (soft delete — sets Active=false)."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"vendor/{vendor_id}").get("Vendor", {})
    body = {
        "Id": current["Id"],
        "SyncToken": current["SyncToken"],
        "Active": False,
        "sparse": True,
    }
    result = client.post("vendor", body)
    format_output(result.get("Vendor"), fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against Vendor."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM Vendor WHERE {sql}"

    result = client.query(sql)
    vendors = result.get("QueryResponse", {}).get("Vendor", [])
    format_output(
        vendors,
        fmt,
        columns=["Id", "DisplayName", "CompanyName", "PrimaryEmailAddr.Address", "Balance", "Vendor1099"],
    )
