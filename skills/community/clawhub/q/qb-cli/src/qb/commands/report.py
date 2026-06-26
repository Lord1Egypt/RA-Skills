"""Financial report commands."""

from typing import Annotated, Optional

import typer

from qb.output import format_report, OutputFormat

app = typer.Typer(help="Run QuickBooks financial reports.")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


def _run_report(
    report_name: str,
    params: dict,
    fmt: OutputFormat,
):
    """Fetch a report and format output."""
    client = _client()
    # Strip None values
    clean = {k: v for k, v in params.items() if v is not None}
    result = client.get(f"reports/{report_name}", params=clean)
    format_report(result, fmt)


@app.command("profit-and-loss")
def profit_and_loss(
    start_date: Annotated[Optional[str], typer.Option("--start-date", help="Start date (YYYY-MM-DD)")] = None,
    end_date: Annotated[Optional[str], typer.Option("--end-date", help="End date (YYYY-MM-DD)")] = None,
    accounting_method: Annotated[Optional[str], typer.Option("--accounting-method", help="Cash or Accrual")] = None,
    summarize_by: Annotated[Optional[str], typer.Option("--summarize-by", help="Total, Month, Quarter, Year")] = None,
    customer: Annotated[Optional[str], typer.Option("--customer", help="Filter by customer ID")] = None,
    department: Annotated[Optional[str], typer.Option("--department", help="Filter by department ID")] = None,
    date_macro: Annotated[Optional[str], typer.Option("--period", help="Date macro (e.g., 'This Month', 'Last Quarter')")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Profit and Loss (Income Statement)."""
    fmt = output or _output()
    _run_report("ProfitAndLoss", {
        "start_date": start_date,
        "end_date": end_date,
        "accounting_method": accounting_method,
        "summarize_column_by": summarize_by,
        "customer": customer,
        "department": department,
        "date_macro": date_macro,
    }, fmt)


@app.command("profit-and-loss-detail")
def profit_and_loss_detail(
    start_date: Annotated[Optional[str], typer.Option("--start-date", help="Start date")] = None,
    end_date: Annotated[Optional[str], typer.Option("--end-date", help="End date")] = None,
    accounting_method: Annotated[Optional[str], typer.Option("--accounting-method", help="Cash or Accrual")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Profit and Loss Detail (transaction-level)."""
    fmt = output or _output()
    _run_report("ProfitAndLossDetail", {
        "start_date": start_date,
        "end_date": end_date,
        "accounting_method": accounting_method,
    }, fmt)


@app.command("balance-sheet")
def balance_sheet(
    date: Annotated[Optional[str], typer.Option("--date", help="As-of date (YYYY-MM-DD)")] = None,
    accounting_method: Annotated[Optional[str], typer.Option("--accounting-method", help="Cash or Accrual")] = None,
    summarize_by: Annotated[Optional[str], typer.Option("--summarize-by", help="Total, Month, Quarter, Year")] = None,
    date_macro: Annotated[Optional[str], typer.Option("--period", help="Date macro")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Balance Sheet."""
    fmt = output or _output()
    params: dict = {
        "accounting_method": accounting_method,
        "summarize_column_by": summarize_by,
        "date_macro": date_macro,
    }
    if date:
        params["start_date"] = date
        params["end_date"] = date
    _run_report("BalanceSheet", params, fmt)


@app.command("cash-flow")
def cash_flow(
    start_date: Annotated[Optional[str], typer.Option("--start-date", help="Start date")] = None,
    end_date: Annotated[Optional[str], typer.Option("--end-date", help="End date")] = None,
    summarize_by: Annotated[Optional[str], typer.Option("--summarize-by", help="Total, Month, Quarter, Year")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Statement of Cash Flows."""
    fmt = output or _output()
    _run_report("CashFlow", {
        "start_date": start_date,
        "end_date": end_date,
        "summarize_column_by": summarize_by,
    }, fmt)


@app.command("trial-balance")
def trial_balance(
    date: Annotated[Optional[str], typer.Option("--date", help="As-of date (YYYY-MM-DD)")] = None,
    accounting_method: Annotated[Optional[str], typer.Option("--accounting-method", help="Cash or Accrual")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Trial Balance."""
    fmt = output or _output()
    params: dict = {"accounting_method": accounting_method}
    if date:
        params["start_date"] = date
        params["end_date"] = date
    _run_report("TrialBalance", params, fmt)


@app.command("general-ledger")
def general_ledger(
    start_date: Annotated[Optional[str], typer.Option("--start-date", help="Start date")] = None,
    end_date: Annotated[Optional[str], typer.Option("--end-date", help="End date")] = None,
    account: Annotated[Optional[str], typer.Option("--account", help="Filter by account ID")] = None,
    accounting_method: Annotated[Optional[str], typer.Option("--accounting-method", help="Cash or Accrual")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """General Ledger."""
    fmt = output or _output()
    _run_report("GeneralLedger", {
        "start_date": start_date,
        "end_date": end_date,
        "account": account,
        "accounting_method": accounting_method,
    }, fmt)


@app.command("ar-aging")
def ar_aging(
    date: Annotated[Optional[str], typer.Option("--date", help="As-of date")] = None,
    customer: Annotated[Optional[str], typer.Option("--customer", help="Filter by customer ID")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Accounts Receivable Aging Summary."""
    fmt = output or _output()
    params: dict = {"customer": customer}
    if date:
        params["report_date"] = date
    _run_report("AgedReceivables", params, fmt)


@app.command("ar-aging-detail")
def ar_aging_detail(
    date: Annotated[Optional[str], typer.Option("--date", help="As-of date")] = None,
    customer: Annotated[Optional[str], typer.Option("--customer", help="Filter by customer ID")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Accounts Receivable Aging Detail."""
    fmt = output or _output()
    params: dict = {"customer": customer}
    if date:
        params["report_date"] = date
    _run_report("AgedReceivableDetail", params, fmt)


@app.command("ap-aging")
def ap_aging(
    date: Annotated[Optional[str], typer.Option("--date", help="As-of date")] = None,
    vendor: Annotated[Optional[str], typer.Option("--vendor", help="Filter by vendor ID")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Accounts Payable Aging Summary."""
    fmt = output or _output()
    params: dict = {"vendor": vendor}
    if date:
        params["report_date"] = date
    _run_report("AgedPayables", params, fmt)


@app.command("ap-aging-detail")
def ap_aging_detail(
    date: Annotated[Optional[str], typer.Option("--date", help="As-of date")] = None,
    vendor: Annotated[Optional[str], typer.Option("--vendor", help="Filter by vendor ID")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Accounts Payable Aging Detail."""
    fmt = output or _output()
    params: dict = {"vendor": vendor}
    if date:
        params["report_date"] = date
    _run_report("AgedPayableDetail", params, fmt)


@app.command("customer-balance")
def customer_balance(
    date: Annotated[Optional[str], typer.Option("--date", help="As-of date")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Customer Balance Summary."""
    fmt = output or _output()
    params: dict = {}
    if date:
        params["report_date"] = date
    _run_report("CustomerBalance", params, fmt)


@app.command("vendor-balance")
def vendor_balance(
    date: Annotated[Optional[str], typer.Option("--date", help="As-of date")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Vendor Balance Summary."""
    fmt = output or _output()
    params: dict = {}
    if date:
        params["report_date"] = date
    _run_report("VendorBalance", params, fmt)


@app.command("customer-income")
def customer_income(
    start_date: Annotated[Optional[str], typer.Option("--start-date", help="Start date")] = None,
    end_date: Annotated[Optional[str], typer.Option("--end-date", help="End date")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Income by Customer."""
    fmt = output or _output()
    _run_report("CustomerIncome", {
        "start_date": start_date,
        "end_date": end_date,
    }, fmt)


@app.command("vendor-expenses")
def vendor_expenses(
    start_date: Annotated[Optional[str], typer.Option("--start-date", help="Start date")] = None,
    end_date: Annotated[Optional[str], typer.Option("--end-date", help="End date")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Expenses by Vendor."""
    fmt = output or _output()
    _run_report("VendorExpenses", {
        "start_date": start_date,
        "end_date": end_date,
    }, fmt)


@app.command("transaction-list")
def transaction_list(
    start_date: Annotated[Optional[str], typer.Option("--start-date", help="Start date")] = None,
    end_date: Annotated[Optional[str], typer.Option("--end-date", help="End date")] = None,
    transaction_type: Annotated[Optional[str], typer.Option("--transaction-type", help="Filter by type")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Transaction List (flat list of all transactions)."""
    fmt = output or _output()
    _run_report("TransactionList", {
        "start_date": start_date,
        "end_date": end_date,
        "transaction_type": transaction_type,
    }, fmt)


@app.command("tax-summary")
def tax_summary(
    start_date: Annotated[Optional[str], typer.Option("--start-date", help="Start date")] = None,
    end_date: Annotated[Optional[str], typer.Option("--end-date", help="End date")] = None,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Tax Summary report."""
    fmt = output or _output()
    _run_report("TaxSummary", {
        "start_date": start_date,
        "end_date": end_date,
    }, fmt)
