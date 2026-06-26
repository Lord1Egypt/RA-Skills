"""Customer resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks customers.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_customers(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    active_only: Annotated[bool, typer.Option(help="Only active customers")] = True,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all customers."""
    fmt = output or _output()
    client = _client()
    where = "WHERE Active = true" if active_only else ""
    result = client.query(f"SELECT * FROM Customer {where}", max_results=limit)
    customers = result.get("QueryResponse", {}).get("Customer", [])
    format_output(
        customers,
        fmt,
        columns=["Id", "DisplayName", "PrimaryEmailAddr.Address", "Balance"],
    )


@app.command()
def get(
    customer_id: Annotated[str, typer.Argument(help="Customer ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get a customer by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"customer/{customer_id}")
    format_output(result.get("Customer"), fmt)


@app.command()
def search(
    term: Annotated[str, typer.Argument(help="Search term (name, company, email, or phone)")],
    include_inactive: Annotated[bool, typer.Option("--include-inactive", help="Include inactive customers")] = False,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Search customers by name, company, email, or phone.

    Searches across DisplayName, CompanyName, PrimaryEmailAddr, and
    PrimaryPhone. Much easier than writing raw queries.
    """
    fmt = output or _output()
    client = _client()

    from qb.api.query import escape_query_value

    # QB doesn't support OR in queries, so we run multiple queries and deduplicate.
    # Note: QB query language only supports LIKE on certain text fields.
    # PrimaryPhone is not directly queryable via LIKE, so we fetch all and filter.
    fields = ["DisplayName", "CompanyName", "PrimaryEmailAddr"]
    escaped = escape_query_value(term)

    seen_ids = set()
    results = []

    for field in fields:
        where = f"{field} LIKE '%{escaped}%'"
        if not include_inactive:
            where += " AND Active = true"

        try:
            resp = client.query(f"SELECT * FROM Customer WHERE {where}")
            for cust in resp.get("QueryResponse", {}).get("Customer", []):
                if cust["Id"] not in seen_ids:
                    seen_ids.add(cust["Id"])
                    results.append(cust)
        except Exception:
            continue  # Skip fields that error (e.g., no email indexed)

    # Phone is not queryable via LIKE in QB — do client-side filter
    if not results:
        try:
            active_clause = "WHERE Active = true" if not include_inactive else ""
            resp = client.query(f"SELECT * FROM Customer {active_clause}", max_results=500)
            for cust in resp.get("QueryResponse", {}).get("Customer", []):
                phone = (cust.get("PrimaryPhone") or {}).get("FreeFormNumber", "")
                if term.lower() in phone.lower() and cust["Id"] not in seen_ids:
                    seen_ids.add(cust["Id"])
                    results.append(cust)
        except Exception:
            pass

    format_output(
        results,
        fmt,
        columns=["Id", "DisplayName", "CompanyName", "PrimaryEmailAddr.Address", "PrimaryPhone.FreeFormNumber", "Balance"],
    )


@app.command()
def create(
    name: Annotated[Optional[str], typer.Option("--name", help="Display name")] = None,
    email: Annotated[Optional[str], typer.Option("--email", help="Email address")] = None,
    phone: Annotated[Optional[str], typer.Option("--phone", help="Phone number")] = None,
    company_name: Annotated[Optional[str], typer.Option("--company", help="Company name")] = None,
    json_input: Annotated[
        Optional[str],
        typer.Option("--json", help="Full customer JSON (overrides other flags)"),
    ] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a new customer."""
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

    result = client.post("customer", body)
    format_output(result.get("Customer"), fmt)


@app.command()
def update(
    customer_id: Annotated[str, typer.Argument(help="Customer ID")],
    name: Annotated[Optional[str], typer.Option("--name", help="Display name")] = None,
    email: Annotated[Optional[str], typer.Option("--email", help="Email")] = None,
    phone: Annotated[Optional[str], typer.Option("--phone", help="Phone")] = None,
    json_input: Annotated[
        Optional[str],
        typer.Option("--json", help="Full update JSON (must include sparse fields)"),
    ] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Update an existing customer. Auto-fetches SyncToken."""
    fmt = output or _output()
    client = _client()

    # Fetch current to get SyncToken
    current = client.get(f"customer/{customer_id}").get("Customer", {})

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

    result = client.post("customer", body)
    format_output(result.get("Customer"), fmt)


@app.command()
def delete(
    customer_id: Annotated[str, typer.Argument(help="Customer ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Deactivate a customer (soft delete — sets Active=false)."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"customer/{customer_id}").get("Customer", {})
    body = {
        "Id": current["Id"],
        "SyncToken": current["SyncToken"],
        "Active": False,
        "sparse": True,
    }
    result = client.post("customer", body)
    format_output(result.get("Customer"), fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query (e.g., \"SELECT * FROM Customer WHERE ...\")")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against Customer."""
    fmt = output or _output()
    client = _client()

    # Ensure query targets Customer if user just wrote a WHERE clause
    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM Customer WHERE {sql}"

    result = client.query(sql)
    customers = result.get("QueryResponse", {}).get("Customer", [])
    format_output(
        customers,
        fmt,
        columns=["Id", "DisplayName", "PrimaryEmailAddr.Address", "Balance"],
    )
