"""Config commands: init, show, set."""

import json
from typing import Annotated, Optional

import typer

from qb.config import load_config, save_config, get_config_dir
from qb.output import format_output, OutputFormat

app = typer.Typer(help="Configuration management.")


@app.command()
def init(
    config_dir: Annotated[Optional[str], typer.Option(hidden=True)] = None,
    non_interactive: Annotated[
        bool, typer.Option("--non-interactive", help="Use env vars only")
    ] = False,
    output: Annotated[OutputFormat, typer.Option("-o")] = OutputFormat.json,
):
    """Initialize QuickBooks configuration.

    In interactive mode, prompts for Client ID and Secret.
    In non-interactive mode, reads from QB_CLIENT_ID and QB_CLIENT_SECRET env vars.
    """
    import os
    from pathlib import Path

    cfg_dir = Path(config_dir) if config_dir else None

    if non_interactive:
        client_id = os.environ.get("QB_CLIENT_ID", "")
        client_secret = os.environ.get("QB_CLIENT_SECRET", "")
        environment = os.environ.get("QB_ENVIRONMENT", "sandbox")
    else:
        client_id = typer.prompt("QuickBooks Client ID")
        client_secret = typer.prompt("QuickBooks Client Secret", hide_input=True)
        environment = typer.prompt(
            "Environment (sandbox/production)", default="sandbox"
        )

    if not client_id or not client_secret:
        typer.echo(
            json.dumps(
                {
                    "error": True,
                    "message": "Client ID and Client Secret are required.",
                    "hint": "Get them from https://developer.intuit.com/app/developer/dashboard",
                },
                indent=2,
            ),
            err=True,
        )
        raise SystemExit(2)

    config = {
        "client_id": client_id,
        "client_secret": client_secret,
        "environment": environment,
    }

    path = save_config(config, cfg_dir)
    format_output(
        {"status": "configured", "config_file": str(path), "environment": environment},
        output,
    )


@app.command()
def show(
    config_dir: Annotated[Optional[str], typer.Option(hidden=True)] = None,
    output: Annotated[OutputFormat, typer.Option("-o")] = OutputFormat.json,
):
    """Display current configuration (secrets are masked)."""
    from pathlib import Path

    cfg_dir = Path(config_dir) if config_dir else None
    config = load_config(cfg_dir)

    # Mask secrets
    masked = dict(config)
    if masked.get("client_id"):
        cid = masked["client_id"]
        masked["client_id"] = cid[:8] + "..." + cid[-4:] if len(cid) > 12 else "***"
    if masked.get("client_secret"):
        masked["client_secret"] = "********"

    masked["config_dir"] = str(get_config_dir(cfg_dir))
    format_output(masked, output)
