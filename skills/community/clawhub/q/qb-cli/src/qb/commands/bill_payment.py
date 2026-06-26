"""BillPayment resource commands."""

import json
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Manage QuickBooks bill payments.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("list")
def list_bill_payments(
    limit: Annotated[int, typer.Option(help="Maximum results")] = 100,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List all bill payments."""
    fmt = output or _output()
    client = _client()
    result = client.query("SELECT * FROM BillPayment", max_results=limit)
    payments = result.get("QueryResponse", {}).get("BillPayment", [])
    format_output(
        payments,
        fmt,
        columns=["Id", "TxnDate", "VendorRef.name", "TotalAmt", "PayType"],
    )


@app.command()
def get(
    payment_id: Annotated[str, typer.Argument(help="BillPayment ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Get a bill payment by ID."""
    fmt = output or _output()
    client = _client()
    result = client.get(f"billpayment/{payment_id}")
    format_output(result.get("BillPayment"), fmt)


@app.command()
def create(
    vendor_id: Annotated[str, typer.Option("--vendor-id", help="Vendor ID (required)")],
    amount: Annotated[float, typer.Option("--amount", help="Total payment amount")],
    pay_type: Annotated[str, typer.Option("--pay-type", help="Payment type: Check or CreditCard")],
    account_id: Annotated[str, typer.Option("--account-id", help="Bank or credit card account ID")],
    bill_ids: Annotated[
        Optional[str],
        typer.Option("--bill-ids", help="Comma-separated bill IDs to pay"),
    ] = None,
    bill_amounts: Annotated[
        Optional[str],
        typer.Option("--bill-amounts", help="Comma-separated amounts per bill"),
    ] = None,
    ref_number: Annotated[Optional[str], typer.Option("--ref", help="Check/reference number")] = None,
    txn_date: Annotated[Optional[str], typer.Option("--date", help="Payment date (YYYY-MM-DD)")] = None,
    memo: Annotated[Optional[str], typer.Option("--memo", help="Private memo/note")] = None,
    json_input: Annotated[Optional[str], typer.Option("--json", help="Full bill payment JSON")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Create a bill payment.

    Pay by check: --vendor-id 42 --amount 500 --pay-type Check --account-id 35 --bill-ids 10,11
    Pay by CC: --vendor-id 42 --amount 500 --pay-type CreditCard --account-id 41 --bill-ids 10
    """
    fmt = output or _output()
    client = _client()

    if json_input:
        body = json.loads(json_input)
    else:
        normalized = pay_type.strip().lower()
        if normalized in ("check", "chk"):
            pay_type_val = "Check"
        elif normalized in ("creditcard", "credit_card", "cc"):
            pay_type_val = "CreditCard"
        else:
            pay_type_val = pay_type  # let QB validate

        body: dict = {
            "VendorRef": {"value": vendor_id},
            "TotalAmt": amount,
            "PayType": pay_type_val,
        }

        # Payment method details
        if pay_type_val == "Check":
            check_detail: dict = {"BankAccountRef": {"value": account_id}}
            if ref_number:
                check_detail["PrintStatus"] = "NeedToPrint"
            body["CheckPayment"] = check_detail
        else:
            body["CreditCardPayment"] = {"CCAccountRef": {"value": account_id}}

        # Link to bills (Line is required by QB)
        if bill_ids:
            ids = [i.strip() for i in bill_ids.split(",")]
            if bill_amounts:
                per_bill = [float(a.strip()) for a in bill_amounts.split(",")]
                if len(per_bill) != len(ids):
                    typer.echo(
                        json.dumps({"error": True, "message": "--bill-amounts count must match --bill-ids count"}),
                        err=True,
                    )
                    raise SystemExit(5)
            else:
                # Auto-distribute: equal split across bills (or full amount for single bill)
                per_bill = [round(amount / len(ids), 2)] * len(ids)
                # Fix rounding: adjust last item so total matches
                per_bill[-1] = round(amount - sum(per_bill[:-1]), 2)

            lines = []
            for i, b_id in enumerate(ids):
                lines.append({
                    "Amount": per_bill[i],
                    "LinkedTxn": [{
                        "TxnId": b_id,
                        "TxnType": "Bill",
                    }],
                })
            body["Line"] = lines
        else:
            typer.echo(
                json.dumps({"error": True, "message": "--bill-ids is required (QB requires Line items linking to bills)"}),
                err=True,
            )
            raise SystemExit(5)

        if txn_date:
            body["TxnDate"] = txn_date
        if memo:
            body["PrivateNote"] = memo

    result = client.post("billpayment", body)
    format_output(result.get("BillPayment"), fmt)


@app.command()
def delete(
    payment_id: Annotated[str, typer.Argument(help="BillPayment ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Delete a bill payment."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"billpayment/{payment_id}").get("BillPayment", {})
    body = {
        "Id": current["Id"],
        "SyncToken": current["SyncToken"],
    }
    result = client.post("billpayment", body, params={"operation": "delete"})
    format_output(result, fmt)


@app.command()
def void(
    payment_id: Annotated[str, typer.Argument(help="BillPayment ID")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Void a bill payment (zeros amounts, keeps record)."""
    fmt = output or _output()
    client = _client()

    current = client.get(f"billpayment/{payment_id}").get("BillPayment", {})
    body = {
        "Id": current["Id"],
        "SyncToken": current["SyncToken"],
        "sparse": True,
    }
    result = client.post("billpayment", body, params={"include": "void"})
    format_output(result.get("BillPayment", result), fmt)


@app.command()
def query(
    sql: Annotated[str, typer.Argument(help="SQL-like query")],
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Run a custom query against BillPayment."""
    fmt = output or _output()
    client = _client()

    if not sql.upper().startswith("SELECT"):
        sql = f"SELECT * FROM BillPayment WHERE {sql}"

    result = client.query(sql)
    payments = result.get("QueryResponse", {}).get("BillPayment", [])
    format_output(
        payments,
        fmt,
        columns=["Id", "TxnDate", "VendorRef.name", "TotalAmt", "PayType"],
    )
