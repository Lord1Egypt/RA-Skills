"""Payment resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks payments.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_payments(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all payments."""
    fmt = output or _output()
    client = _client()
    result = client.query("SELECT * FROM Payment", max_results=limit)
    payments = result.get("QueryResponse", {}).get("Payment", [])
    format_output(
        payments,
        fmt,
        columns=["Id", "TxnDate", "CustomerRef.name", "TotalAmt", "PaymentRefNum"],
    )


@app.command()
def get(
    payment_id: Annotated[str, typer.Argument(help="Payment ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get a payment by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"payment/{payment_id}")
    format_output(result.get("Payment"), fmt)


@app.command()
def create(
    customer_id: Annotated[str, typer.Option("--customer-id", help="Customer ID (required)")],
    amount: Annotated[float, typer.Option("--amount", help="Total payment amount")],
    invoice_ids: Annotated[
        Optional[str],
        typer.Option("--invoice-ids", help="Comma-separated invoice IDs to apply payment to"),
    ] = None,
    invoice_amounts: Annotated[
        Optional[str],
        typer.Option("--invoice-amounts", help="Comma-separated amounts per invoice (must match --invoice-ids count)"),
    ] = None,
    payment_method: Annotated[
        Optional[str],
        typer.Option("--method", help="Payment method ref ID"),
    ] = None,
    ref_number: Annotated[
        Optional[str],
        typer.Option("--ref", help="Payment reference number (e.g., check number, ACH trace)"),
    ] = None,
    txn_date: Annotated[
        Optional[str],
        typer.Option("--date", help="Payment date (YYYY-MM-DD)"),
    ] = None,
    memo: Annotated[
        Optional[str],
        typer.Option("--memo", help="Private memo/note"),
    ] = None,
    deposit_account: Annotated[
        Optional[str],
        typer.Option("--deposit-to", help="Deposit account ID"),
    ] = None,
    json_input: Annotated[
        Optional[str],
        typer.Option("--json", help="Full payment JSON (overrides other flags)"),
    ] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a payment. Links to invoices via --invoice-ids.

    Simple: --customer-id 58 --amount 500 --invoice-ids 148,149
    With per-invoice amounts: --invoice-ids 148,149 --invoice-amounts 250,250
    Full control: --json '{...}'
    """
    fmt = output or _output()
    client = _client()

    if json_input:
        body = json.loads(json_input)
    else:
        body = {
            "CustomerRef": {"value": customer_id},
            "TotalAmt": amount,
        }

        if invoice_ids:
            ids = [i.strip() for i in invoice_ids.split(",")]
            amounts = None
            if invoice_amounts:
                amounts = [float(a.strip()) for a in invoice_amounts.split(",")]
                if len(amounts) != len(ids):
                    typer.echo(
                        json.dumps({"error": True, "message": "--invoice-amounts count must match --invoice-ids count"}),
                        err=True,
                    )
                    raise SystemExit(5)

            lines = []
            for i, inv_id in enumerate(ids):
                line = {
                    "Amount": amounts[i] if amounts else None,
                    "LinkedTxn": [{
                        "TxnId": inv_id,
                        "TxnType": "Invoice",
                    }],
                }
                # If no per-invoice amounts, let QB auto-apply
                if line["Amount"] is None:
                    del line["Amount"]
                lines.append(line)
            body["Line"] = lines

        if payment_method:
            body["PaymentMethodRef"] = {"value": payment_method}
        if ref_number:
            body["PaymentRefNum"] = ref_number
        if txn_date:
            body["TxnDate"] = txn_date
        if memo:
            body["PrivateNote"] = memo
        if deposit_account:
            body["DepositToAccountRef"] = {"value": deposit_account}

    result = client.post("payment", body)
    format_output(result.get("Payment"), fmt)


@app.command()
def delete(
    payment_id: Annotated[str, typer.Argument(help="Payment ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Delete a payment."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"payment/{payment_id}").get("Payment", {})
    body = {
        "Id": current["Id"],
        "SyncToken": current["SyncToken"],
    }
    result = client.post("payment", body, params={"operation": "delete"})
    format_output(result, fmt)


@app.command()
def void(
    payment_id: Annotated[str, typer.Argument(help="Payment ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Void a payment (zeros amounts, keeps record)."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"payment/{payment_id}").get("Payment", {})
    body = {"Id": current["Id"], "SyncToken": current["SyncToken"], "sparse": True}
    result = client.post("payment", body, params={"include": "void"})
    format_output(result.get("Payment", result), fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against Payment."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM Payment WHERE {sql}"

    result = client.query(sql)
    payments = result.get("QueryResponse", {}).get("Payment", [])
    format_output(
        payments,
        fmt,
        columns=["Id", "TxnDate", "CustomerRef.name", "TotalAmt", "PaymentRefNum"],
    )
