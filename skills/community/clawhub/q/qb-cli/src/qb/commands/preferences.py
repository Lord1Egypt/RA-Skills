"""Company preferences commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="View and update QuickBooks company preferences.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command()
def show(
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Show company preferences (fiscal year, class tracking, etc.)."""
    fmt = output or _output()
    client = _client()
    result = client.get("preferences")
    prefs = result.get("Preferences", result)

    # Extract key settings for summary
    if fmt != OutputFormat.json:
        acct = prefs.get("AccountingInfoPrefs", {})
        sales = prefs.get("SalesFormsPrefs", {})
        currency = prefs.get("CurrencyPrefs", {})
        time = prefs.get("TimeTrackingPrefs", {})

        summary = {
            "FiscalYearStartMonth": acct.get("FiscalYearStartMonth"),
            "BookCloseDate": acct.get("BookCloseDate", "Not set"),
            "TrackDepartments": acct.get("TrackDepartments", False),
            "ClassTrackingPerTxn": prefs.get("ClassTrackingPerTxn", False),
            "ClassTrackingPerTxnLine": prefs.get("ClassTrackingPerTxnLine", False),
            "AutoApplyCredit": sales.get("AutoApplyCredit", False),
            "MultiCurrencyEnabled": currency.get("MultiCurrencyEnabled", False),
            "HomeCurrency": currency.get("HomeCurrency", {}).get("value"),
            "UseServices": prefs.get("ProductAndServicesPrefs", {}).get("ForSales", False),
            "TrackInventory": prefs.get("ProductAndServicesPrefs", {}).get("QuantityOnHand", False),
            "UseBillableTime": time.get("UseBillableTimeEntry", False),
        }
        format_output(summary, fmt)
    else:
        format_output(prefs, fmt)


@app.command()
def update(
    json_input: Annotated[str, typer.Option("--json", help="Preferences JSON to update (sparse)")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Update company preferences (sparse update)."""
    fmt = output or _output()
    client = _client()

    # Fetch current to get SyncToken
    current = client.get("preferences").get("Preferences", {})
    body = json.loads(json_input)
    body["SyncToken"] = current.get("SyncToken", "0")
    body["sparse"] = True

    result = client.post("preferences", body)
    format_output(result.get("Preferences", result), fmt)
