"""Item (Products & Services) resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks items (products & services).")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_items(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    active_only: Annotated[bool, typer.Option(help="Only active items")] = True,
    item_type: Annotated[Optional[str], typer.Option("--type", help="Filter by type (Service, Inventory, NonInventory)")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all items (products & services)."""
    fmt = output or _output()
    client = _client()
    clauses = []
    if active_only:
        clauses.append("Active = true")
    if item_type:
        clauses.append(f"Type = '{item_type}'")
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    result = client.query(f"SELECT * FROM Item {where}", max_results=limit)
    items = result.get("QueryResponse", {}).get("Item", [])
    format_output(
        items,
        fmt,
        columns=["Id", "Name", "Type", "UnitPrice", "PurchaseCost", "QtyOnHand", "Active"],
    )


@app.command()
def get(
    item_id: Annotated[str, typer.Argument(help="Item ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get an item by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"item/{item_id}")
    format_output(result.get("Item"), fmt)


@app.command()
def create(
    name: Annotated[str, typer.Option("--name", help="Item name (required)")],
    item_type: Annotated[str, typer.Option("--type", help="Type: Service, Inventory, or NonInventory")] = "Service",
    income_account: Annotated[Optional[str], typer.Option("--income-account", help="Income account ID (for sales)")] = None,
    expense_account: Annotated[Optional[str], typer.Option("--expense-account", help="Expense account ID (for purchases)")] = None,
    asset_account: Annotated[Optional[str], typer.Option("--asset-account", help="Asset account ID (required for Inventory)")] = None,
    price: Annotated[Optional[float], typer.Option("--price", help="Unit sale price")] = None,
    cost: Annotated[Optional[float], typer.Option("--cost", help="Purchase cost")] = None,
    qty: Annotated[Optional[float], typer.Option("--qty", help="Initial quantity on hand (Inventory only)")] = None,
    sku: Annotated[Optional[str], typer.Option("--sku", help="SKU")] = None,
    description: Annotated[Optional[str], typer.Option("--description", help="Sales description")] = None,
    inv_start_date: Annotated[Optional[str], typer.Option("--inv-start-date", help="Inventory start date (YYYY-MM-DD, required for Inventory)")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full item JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a new item (product or service).

    Service: --name "Consulting" --type Service --income-account 1 --price 150
    Inventory: --name "Widget" --type Inventory --income-account 1 --expense-account 2 --asset-account 3 --qty 100 --inv-start-date 2026-01-01
    """
    fmt = output or _output()
    client = _client()

    if json_input:
        body = json.loads(json_input)
    else:
        body: dict = {
            "Name": name,
            "Type": item_type,
        }
        if income_account:
            body["IncomeAccountRef"] = {"value": income_account}
        if expense_account:
            body["ExpenseAccountRef"] = {"value": expense_account}
        if asset_account:
            body["AssetAccountRef"] = {"value": asset_account}
        if price is not None:
            body["UnitPrice"] = price
        if cost is not None:
            body["PurchaseCost"] = cost
        if qty is not None:
            body["QtyOnHand"] = qty
        if sku:
            body["Sku"] = sku
        if description:
            body["Description"] = description
        if inv_start_date:
            body["InvStartDate"] = inv_start_date

    result = client.post("item", body)
    format_output(result.get("Item"), fmt)


@app.command()
def update(
    item_id: Annotated[str, typer.Argument(help="Item ID")],
    name: Annotated[Optional[str], typer.Option("--name", help="Item name")] = None,
    price: Annotated[Optional[float], typer.Option("--price", help="Unit sale price")] = None,
    cost: Annotated[Optional[float], typer.Option("--cost", help="Purchase cost")] = None,
    description: Annotated[Optional[str], typer.Option("--description", help="Sales description")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full update JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Update an existing item. Auto-fetches SyncToken."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"item/{item_id}").get("Item", {})

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
            body["Name"] = name
        if price is not None:
            body["UnitPrice"] = price
        if cost is not None:
            body["PurchaseCost"] = cost
        if description:
            body["Description"] = description

    result = client.post("item", body)
    format_output(result.get("Item"), fmt)


@app.command()
def delete(
    item_id: Annotated[str, typer.Argument(help="Item ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Deactivate an item (soft delete — sets Active=false)."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"item/{item_id}").get("Item", {})
    body = {
        "Id": current["Id"],
        "SyncToken": current["SyncToken"],
        "Active": False,
        "sparse": True,
    }
    result = client.post("item", body)
    format_output(result.get("Item"), fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against Item."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM Item WHERE {sql}"

    result = client.query(sql)
    items = result.get("QueryResponse", {}).get("Item", [])
    format_output(
        items,
        fmt,
        columns=["Id", "Name", "Type", "UnitPrice", "PurchaseCost", "QtyOnHand", "Active"],
    )
