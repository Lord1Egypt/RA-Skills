"""Tax code and tax rate commands."""

from typing import Annotated, Optional

import typer

from qb.output import format_output, format_report, OutputFormat

app = typer.Typer(help="View QuickBooks tax codes and rates.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command()
def codes(
    active_only: Annotated[bool, typer.Option(help="Only active tax codes")] = True,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List tax codes."""
    fmt = output or _output()
    client = _client()
    where = "WHERE Active = true" if active_only else ""
    result = client.query(f"SELECT * FROM TaxCode {where}", max_results=100)
    codes = result.get("QueryResponse", {}).get("TaxCode", [])
    format_output(
        codes,
        fmt,
        columns=["Id", "Name", "Description", "Taxable", "Active"],
    )


@app.command()
def rates(
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List tax rates."""
    fmt = output or _output()
    client = _client()
    result = client.query("SELECT * FROM TaxRate", max_results=100)
    rates_list = result.get("QueryResponse", {}).get("TaxRate", [])
    format_output(
        rates_list,
        fmt,
        columns=["Id", "Name", "RateValue", "AgencyRef.value", "Active"],
    )


@app.command()
def summary(
    start_date: Annotated[Optional[str], typer.Option("--start-date", help="Start date")] = None,
    end_date: Annotated[Optional[str], typer.Option("--end-date", help="End date")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Tax Summary report."""
    fmt = output or _output()
    client = _client()
    params = {k: v for k, v in {"start_date": start_date, "end_date": end_date}.items() if v}
    result = client.get("reports/TaxSummary", params=params)
    format_report(result, fmt)
