"""Company resource commands."""

from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="QuickBooks company information.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command()
def info(
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get company information."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"companyinfo/{client.realm_id}")
    format_output(result.get("CompanyInfo"), fmt)
