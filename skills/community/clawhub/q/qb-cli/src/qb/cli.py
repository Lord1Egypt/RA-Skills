"""Root CLI application with Typer."""

from pathlib import Path
from typing import Annotated, Optional

import typer

from qb import __version__
from qb.auth.tokens import TokenManager, AuthNotConfiguredError
from qb.api.client import QBClient, QBApiError
from qb.config import load_config, get_config_dir
from qb.models.errors import handle_error, ExitCode
from qb.output import OutputFormat

app = typer.Typer(
    name="qb",
    help="QuickBooks Online CLI — manage your books from the terminal.",
    no_args_is_help=True,
    invoke_without_command=True,
    pretty_exceptions_enable=False,
)

# Global state set by the main callback
_client: Optional[QBClient] = None
_config_dir: Optional[Path] = None
_output_format: OutputFormat = OutputFormat.json
_verbose: bool = False


def get_client() -> QBClient:
    """Get the configured QBClient. Called by command modules."""
    if _client is None:
        handle_error(
            ExitCode.CONFIG_ERROR,
            "QuickBooks not configured or not authenticated.",
            hint="qb config init && qb auth login",
        )
    return _client


def get_output_format() -> OutputFormat:
    """Get the globally-configured output format."""
    return _output_format


# Register sub-apps (imported here to avoid circular imports)
from qb.commands import auth as auth_cmd
from qb.commands import config_cmd
from qb.commands import customer
from qb.commands import invoice
from qb.commands import company
from qb.commands import payment
from qb.commands import vendor
from qb.commands import bill
from qb.commands import bill_payment
from qb.commands import account
from qb.commands import item
from qb.commands import purchase
from qb.commands import vendor_credit
from qb.commands import estimate
from qb.commands import credit_memo
from qb.commands import sales_receipt
from qb.commands import refund_receipt
from qb.commands import journal
from qb.commands import deposit
from qb.commands import transfer
from qb.commands import report
from qb.commands import import_cmd
from qb.commands import reconcile
from qb.commands import workflow
from qb.commands import purchase_order
from qb.commands import batch
from qb.commands import preferences
from qb.commands import tax
from qb.commands import attachment

app.add_typer(auth_cmd.app, name="auth")
app.add_typer(config_cmd.app, name="config")
app.add_typer(customer.app, name="customer")
app.add_typer(invoice.app, name="invoice")
app.add_typer(company.app, name="company")
app.add_typer(payment.app, name="payment")
app.add_typer(vendor.app, name="vendor")
app.add_typer(bill.app, name="bill")
app.add_typer(bill_payment.app, name="bill-payment")
app.add_typer(account.app, name="account")
app.add_typer(item.app, name="item")
app.add_typer(purchase.app, name="expense")
app.add_typer(vendor_credit.app, name="vendor-credit")
app.add_typer(estimate.app, name="estimate")
app.add_typer(credit_memo.app, name="credit-memo")
app.add_typer(sales_receipt.app, name="sales-receipt")
app.add_typer(refund_receipt.app, name="refund-receipt")
app.add_typer(journal.app, name="journal")
app.add_typer(deposit.app, name="deposit")
app.add_typer(transfer.app, name="transfer")
app.add_typer(report.app, name="report")
app.add_typer(import_cmd.app, name="import")
app.add_typer(reconcile.app, name="reconcile")
app.add_typer(workflow.app, name="workflow")
app.add_typer(purchase_order.app, name="purchase-order")
app.add_typer(batch.app, name="batch")
app.add_typer(preferences.app, name="preferences")
app.add_typer(tax.app, name="tax")
app.add_typer(attachment.app, name="attachment")


@app.callback()
def main(
    ctx: typer.Context,
    config_dir: Annotated[
        Optional[Path],
        typer.Option("--config-dir", help="Config directory override"),
    ] = None,
    environment: Annotated[
        Optional[str],
        typer.Option("-e", "--environment", help="sandbox or production"),
    ] = None,
    output: Annotated[
        OutputFormat,
        typer.Option("-o", "--output", help="Output format"),
    ] = OutputFormat.json,
    non_interactive: Annotated[
        bool,
        typer.Option("--non-interactive", help="Suppress prompts (for agent use)"),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("-v", "--verbose", help="Verbose HTTP logging"),
    ] = False,
    version: Annotated[
        bool,
        typer.Option("--version", help="Show version and exit", is_eager=True),
    ] = False,
):
    """QuickBooks Online CLI — manage your books from the terminal."""
    global _client, _config_dir, _output_format, _verbose

    if version:
        typer.echo(f"qb-cli v{__version__}")
        raise typer.Exit()

    _config_dir = config_dir
    _output_format = output
    _verbose = verbose

    # Store in context for subcommands
    ctx.ensure_object(dict)
    ctx.obj["config_dir"] = config_dir
    ctx.obj["output"] = output
    ctx.obj["non_interactive"] = non_interactive
    ctx.obj["verbose"] = verbose
    ctx.obj["environment"] = environment

    # Skip client setup for auth/config commands
    if ctx.invoked_subcommand in ("auth", "config"):
        return

    # Set up the API client for data commands
    try:
        config = load_config(config_dir)
        client_id = config.get("client_id", "")
        client_secret = config.get("client_secret", "")

        if not client_id or not client_secret:
            handle_error(
                ExitCode.CONFIG_ERROR,
                "QuickBooks not configured",
                detail="QB_CLIENT_ID and QB_CLIENT_SECRET not set.",
                hint="qb config init",
            )

        token_manager = TokenManager(config_dir)
        if not token_manager.is_authenticated:
            handle_error(
                ExitCode.AUTH_ERROR,
                "Not authenticated",
                detail="No stored tokens found.",
                hint="qb auth login",
            )

        _client = QBClient(
            token_manager=token_manager,
            client_id=client_id,
            client_secret=client_secret,
            environment=environment,
            verbose=verbose,
        )
    except AuthNotConfiguredError as e:
        handle_error(ExitCode.AUTH_ERROR, str(e), hint="qb auth login")


def main_entrypoint():
    """Entry point for the CLI (used by pyproject.toml scripts)."""
    try:
        app()
    except QBApiError as e:
        code = ExitCode.API_ERROR
        if e.status_code == 401:
            code = ExitCode.AUTH_ERROR
        elif e.status_code == 404:
            code = ExitCode.NOT_FOUND
        handle_error(
            code,
            e.message,
            detail=e.detail,
            intuit_tid=e.intuit_tid,
        )
    except AuthNotConfiguredError as e:
        handle_error(ExitCode.AUTH_ERROR, str(e), hint="qb auth login")
