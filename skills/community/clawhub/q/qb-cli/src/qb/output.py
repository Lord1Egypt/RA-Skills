"""Output formatting for CLI results."""

import csv
import io
import json
from enum import Enum
from typing import Any, Optional

import typer
from rich.console import Console
from rich.table import Table


class OutputFormat(str, Enum):
    json = "json"
    table = "table"
    csv = "csv"


def format_output(
    data: Any,
    fmt: OutputFormat = OutputFormat.json,
    columns: Optional[list[str]] = None,
) -> None:
    """Format and print data in the requested format."""
    if data is None:
        typer.echo("{}")
        return

    if fmt == OutputFormat.json:
        typer.echo(json.dumps(data, indent=2, default=str))
    elif fmt == OutputFormat.table:
        _print_table(data, columns)
    elif fmt == OutputFormat.csv:
        _print_csv(data, columns)


def _resolve_nested(obj: dict, key: str) -> Any:
    """Resolve dotted key path like 'PrimaryEmailAddr.Address'."""
    parts = key.split(".")
    current = obj
    for part in parts:
        if isinstance(current, dict):
            current = current.get(part, "")
        else:
            return ""
    return current


def _print_table(data: Any, columns: Optional[list[str]] = None) -> None:
    """Print data as a rich table."""
    console = Console()
    if isinstance(data, list):
        if not data:
            typer.echo("(no results)")
            return
        cols = columns or list(data[0].keys())[:8]
        table = Table()
        for col in cols:
            table.add_column(col.split(".")[-1])
        for row in data:
            table.add_row(*[str(_resolve_nested(row, c)) for c in cols])
        console.print(table)
    elif isinstance(data, dict):
        table = Table(show_header=False)
        table.add_column("Field")
        table.add_column("Value")
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                table.add_row(str(k), json.dumps(v, default=str))
            else:
                table.add_row(str(k), str(v))
        console.print(table)


def _print_csv(data: Any, columns: Optional[list[str]] = None) -> None:
    """Print data as CSV."""
    if isinstance(data, list):
        if not data:
            return
        cols = columns or list(data[0].keys())
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        for row in data:
            flat = {c: _resolve_nested(row, c) for c in cols}
            writer.writerow(flat)
        typer.echo(output.getvalue().strip())
    elif isinstance(data, dict):
        cols = columns or list(data.keys())
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        writer.writerow(data)
        typer.echo(output.getvalue().strip())


def format_report(data: dict, fmt: OutputFormat = OutputFormat.json) -> None:
    """Format and print a QB report response."""
    if fmt == OutputFormat.json:
        typer.echo(json.dumps(data, indent=2, default=str))
    elif fmt == OutputFormat.table:
        _print_report_table(data)
    elif fmt == OutputFormat.csv:
        _print_report_csv(data)


def _extract_report_rows(rows: list, depth: int = 0) -> list[dict]:
    """Recursively extract report rows into flat list with indent depth."""
    result = []
    for row in rows:
        row_type = row.get("type", "")
        if row_type == "Section":
            header = row.get("Header", {})
            if header.get("ColData"):
                result.append({"depth": depth, "cols": header["ColData"], "style": "header"})
            for sub in row.get("Rows", {}).get("Row", []):
                result.extend(_extract_report_rows([sub], depth + 1))
            summary = row.get("Summary", {})
            if summary.get("ColData"):
                result.append({"depth": depth, "cols": summary["ColData"], "style": "summary"})
        elif row_type == "Data":
            if row.get("ColData"):
                result.append({"depth": depth, "cols": row["ColData"], "style": "data"})
        else:
            if row.get("ColData"):
                result.append({"depth": depth, "cols": row["ColData"], "style": "data"})
            if row.get("Header", {}).get("ColData"):
                result.append({"depth": depth, "cols": row["Header"]["ColData"], "style": "header"})
            for sub in row.get("Rows", {}).get("Row", []):
                result.extend(_extract_report_rows([sub], depth + 1))
            if row.get("Summary", {}).get("ColData"):
                result.append({"depth": depth, "cols": row["Summary"]["ColData"], "style": "summary"})
    return result


def _print_report_table(data: dict) -> None:
    """Print a QB report as a rich table with indentation."""
    console = Console()
    header = data.get("Header", {})
    report_name = header.get("ReportName", "Report")
    period = header.get("DateMacro", header.get("StartPeriod", ""))
    if header.get("EndPeriod"):
        period = f"{header.get('StartPeriod', '')} to {header['EndPeriod']}"

    console.print(f"\n[bold]{report_name}[/bold]")
    if period:
        console.print(f"[dim]{period}[/dim]")

    # Get column headers
    col_defs = data.get("Columns", {}).get("Column", [])
    col_names = [c.get("ColTitle", "") for c in col_defs]

    table = Table(show_header=True, header_style="bold")
    for i, name in enumerate(col_names):
        justify = "left" if name == "" or i == 0 else "right"
        table.add_column(name or "Account", justify=justify)

    # Extract rows
    report_rows = data.get("Rows", {}).get("Row", [])
    flat = _extract_report_rows(report_rows)

    for row in flat:
        cols = row["cols"]
        values = [c.get("value", "") for c in cols]
        # Indent the first column based on depth
        indent = "  " * row["depth"]
        if values:
            style = ""
            if row["style"] == "header":
                style = "bold"
            elif row["style"] == "summary":
                style = "bold dim"
            values[0] = f"{indent}{values[0]}"
            table.add_row(*values, style=style)

    console.print(table)


def _print_report_csv(data: dict) -> None:
    """Print a QB report as CSV."""
    col_defs = data.get("Columns", {}).get("Column", [])
    col_names = [c.get("ColTitle", "Account") or "Account" for c in col_defs]

    report_rows = data.get("Rows", {}).get("Row", [])
    flat = _extract_report_rows(report_rows)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(col_names)
    for row in flat:
        cols = row["cols"]
        values = [c.get("value", "") for c in cols]
        writer.writerow(values)
    typer.echo(output.getvalue().strip())
