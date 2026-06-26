"""Auth commands: login, status, refresh, logout."""

import json
import webbrowser
from typing import Annotated, Optional

import typer

from qb.auth.oauth import (
    generate_auth_url,
    wait_for_callback,
    exchange_code_for_tokens,
    refresh_access_token,
    revoke_token,
    parse_callback_url,
    OAuthError,
)
from qb.auth.tokens import TokenManager, AuthNotConfiguredError
from qb.config import load_config, get_config_dir
from qb.models.errors import handle_error, ExitCode
from qb.output import format_output, OutputFormat

app = typer.Typer(help="Authentication management.")


@app.command()
def login(
    print_url: Annotated[
        bool,
        typer.Option("--print-url", help="Print auth URL instead of opening browser"),
    ] = False,
    callback_url: Annotated[
        Optional[str],
        typer.Option(
            "--callback-url",
            help="Paste the full redirect URL (for headless/SSH use)",
        ),
    ] = None,
    config_dir: Annotated[Optional[str], typer.Option(hidden=True)] = None,
    environment: Annotated[
        str, typer.Option("-e", help="sandbox or production")
    ] = "sandbox",
    output: Annotated[OutputFormat, typer.Option("-o")] = OutputFormat.json,
):
    """Authenticate with QuickBooks via OAuth 2.0.

    For SSH/headless environments, use --print-url to get the authorization URL,
    open it in any browser, authorize, then copy the redirect URL and pass it
    back with --callback-url.
    """
    from pathlib import Path

    cfg_dir = Path(config_dir) if config_dir else None
    config = load_config(cfg_dir)

    client_id = config.get("client_id", "")
    client_secret = config.get("client_secret", "")

    if not client_id or not client_secret:
        handle_error(
            ExitCode.CONFIG_ERROR,
            "QuickBooks not configured",
            detail="QB_CLIENT_ID and QB_CLIENT_SECRET must be set.",
            hint="qb config init",
        )

    auth_url, state = generate_auth_url(client_id)

    if callback_url:
        # Headless mode: user already has the redirect URL
        try:
            result = parse_callback_url(callback_url)
        except OAuthError as e:
            handle_error(ExitCode.AUTH_ERROR, str(e))
    elif print_url:
        # Print URL for user to open manually
        typer.echo(json.dumps({
            "action": "open_url",
            "url": auth_url,
            "instructions": (
                "Open this URL in a browser, authorize QuickBooks, then "
                "copy the full redirect URL from the browser address bar "
                "and run: qb auth login --callback-url '<URL>'"
            ),
        }, indent=2))
        return
    else:
        # Interactive mode: open browser and wait for callback
        typer.echo("Opening browser for QuickBooks authorization...")
        typer.echo(f"If the browser doesn't open, visit: {auth_url}")
        try:
            webbrowser.open(auth_url)
        except Exception:
            pass  # webbrowser.open can fail in headless environments

        typer.echo("Waiting for authorization callback...")
        try:
            result = wait_for_callback(state, timeout=120)
        except OAuthError as e:
            handle_error(ExitCode.AUTH_ERROR, str(e))

    # Exchange code for tokens
    try:
        tokens = exchange_code_for_tokens(
            client_id, client_secret, result["code"]
        )
    except OAuthError as e:
        handle_error(ExitCode.AUTH_ERROR, f"Token exchange failed: {e}")

    # Save tokens
    token_manager = TokenManager(cfg_dir)
    token_manager.save_tokens(tokens, result["realm_id"], environment)

    format_output(
        {
            "status": "authenticated",
            "realm_id": result["realm_id"],
            "environment": environment,
            "access_token_expires_in": tokens.get("expires_in", 3600),
        },
        output,
    )


@app.command()
def status(
    config_dir: Annotated[Optional[str], typer.Option(hidden=True)] = None,
    output: Annotated[OutputFormat, typer.Option("-o")] = OutputFormat.json,
):
    """Show current authentication status."""
    from pathlib import Path

    cfg_dir = Path(config_dir) if config_dir else None
    token_manager = TokenManager(cfg_dir)
    format_output(token_manager.token_status, output)


@app.command()
def refresh(
    config_dir: Annotated[Optional[str], typer.Option(hidden=True)] = None,
    output: Annotated[OutputFormat, typer.Option("-o")] = OutputFormat.json,
):
    """Manually refresh the access token."""
    from pathlib import Path

    cfg_dir = Path(config_dir) if config_dir else None
    config = load_config(cfg_dir)
    token_manager = TokenManager(cfg_dir)

    try:
        tokens = token_manager.load_tokens()
        new_tokens = refresh_access_token(
            config["client_id"],
            config["client_secret"],
            tokens["refresh_token"],
        )
        token_manager.save_tokens(
            new_tokens, tokens["realm_id"], tokens["environment"]
        )
        format_output(
            {"status": "refreshed", "expires_in": new_tokens.get("expires_in", 3600)},
            output,
        )
    except (AuthNotConfiguredError, OAuthError) as e:
        handle_error(ExitCode.AUTH_ERROR, str(e), hint="qb auth login")


@app.command()
def logout(
    config_dir: Annotated[Optional[str], typer.Option(hidden=True)] = None,
    output: Annotated[OutputFormat, typer.Option("-o")] = OutputFormat.json,
):
    """Revoke tokens and delete stored credentials."""
    from pathlib import Path

    cfg_dir = Path(config_dir) if config_dir else None
    config = load_config(cfg_dir)
    token_manager = TokenManager(cfg_dir)

    try:
        tokens = token_manager.load_tokens()
        # Attempt to revoke the refresh token
        try:
            revoke_token(
                config["client_id"],
                config["client_secret"],
                tokens["refresh_token"],
            )
        except OAuthError:
            pass  # Best-effort revocation
    except AuthNotConfiguredError:
        pass

    token_manager.clear()
    format_output({"status": "logged_out"}, output)
