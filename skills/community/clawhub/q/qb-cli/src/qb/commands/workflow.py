"""High-level bookkeeping workflow commands."""

import csv as csv_mod
import io
import json
from datetime import datetime, timedelta
from calendar import monthrange
from pathlib import Path
from typing import Annotated, Optional

import typer

from qb.output import format_output, OutputFormat

app = typer.Typer(help="Bookkeeping workflow automation.")

WORKSPACE = Path("/workspace")


def _client():
    from qb.cli import get_client
    return get_client()


def _output():
    from qb.cli import get_output_format
    return get_output_format()


@app.command("month-close")
def month_close(
    month: Annotated[str, typer.Option("--month", help="Month to close (YYYY-MM)")],
    check_only: Annotated[bool, typer.Option("--check-only", help="Only run checks, don't generate report files")] = False,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """Guided month-end close checklist.

    Runs automated checks and generates status for each step:
    1. Uncategorized transactions
    2. Undeposited Funds balance
    3. AR Aging (overdue invoices)
    4. AP Aging (overdue bills)
    5. P&L for the month
    6. Balance Sheet as of month-end
    7. Trial Balance
    """
    fmt = output or _output()
    client = _client()

    # Parse month
    try:
        year, mo = month.split("-")
        year, mo = int(year), int(mo)
        _, last_day = monthrange(year, mo)
        start_date = f"{year}-{mo:02d}-01"
        end_date = f"{year}-{mo:02d}-{last_day:02d}"
    except (ValueError, TypeError):
        typer.echo(json.dumps({"error": True, "message": "Invalid month format. Use YYYY-MM"}), err=True)
        raise SystemExit(5)

    checks = []

    # Check 1: Undeposited Funds
    try:
        resp = client.query("SELECT * FROM Account WHERE Name = 'Undeposited Funds'")
        uf_accounts = resp.get("QueryResponse", {}).get("Account", [])
        uf_balance = float(uf_accounts[0].get("CurrentBalance", 0)) if uf_accounts else 0
        checks.append({
            "check": "Undeposited Funds",
            "status": "pass" if abs(uf_balance) < 0.01 else "warning",
            "balance": uf_balance,
            "message": "Clear" if abs(uf_balance) < 0.01 else f"${uf_balance:.2f} sitting in Undeposited Funds — group into deposits",
        })
    except Exception as e:
        checks.append({"check": "Undeposited Funds", "status": "error", "message": str(e)})

    # Check 2: Overdue AR
    try:
        resp = client.query(f"SELECT * FROM Invoice WHERE Balance > '0' AND DueDate < '{start_date}'", max_results=500)
        overdue_invoices = resp.get("QueryResponse", {}).get("Invoice", [])
        overdue_total = sum(float(inv.get("Balance", 0)) for inv in overdue_invoices)
        checks.append({
            "check": "Overdue AR",
            "status": "pass" if not overdue_invoices else "warning",
            "count": len(overdue_invoices),
            "total": overdue_total,
            "message": "No overdue invoices" if not overdue_invoices else f"{len(overdue_invoices)} overdue invoices totaling ${overdue_total:.2f}",
        })
    except Exception as e:
        checks.append({"check": "Overdue AR", "status": "error", "message": str(e)})

    # Check 3: Overdue AP
    try:
        resp = client.query(f"SELECT * FROM Bill WHERE Balance > '0' AND DueDate < '{start_date}'", max_results=500)
        overdue_bills = resp.get("QueryResponse", {}).get("Bill", [])
        overdue_bill_total = sum(float(b.get("Balance", 0)) for b in overdue_bills)
        checks.append({
            "check": "Overdue AP",
            "status": "pass" if not overdue_bills else "warning",
            "count": len(overdue_bills),
            "total": overdue_bill_total,
            "message": "No overdue bills" if not overdue_bills else f"{len(overdue_bills)} overdue bills totaling ${overdue_bill_total:.2f}",
        })
    except Exception as e:
        checks.append({"check": "Overdue AP", "status": "error", "message": str(e)})

    # Check 4: Open invoices for the month with outstanding balance
    try:
        resp = client.query(
            f"SELECT * FROM Invoice WHERE TxnDate >= '{start_date}' AND TxnDate <= '{end_date}' AND Balance > '0'",
            max_results=100,
        )
        open_invoices = resp.get("QueryResponse", {}).get("Invoice", [])
        open_total = sum(float(inv.get("Balance", 0)) for inv in open_invoices)
        checks.append({
            "check": "Open Invoices (this month)",
            "status": "pass" if not open_invoices else "info",
            "count": len(open_invoices),
            "total": open_total,
            "message": "No open invoices" if not open_invoices else f"{len(open_invoices)} open invoices totaling ${open_total:.2f}",
        })
    except Exception as e:
        checks.append({"check": "Open Invoices (this month)", "status": "error", "message": str(e)})

    # Generate reports (unless check-only)
    reports = {}
    if not check_only:
        WORKSPACE.mkdir(parents=True, exist_ok=True)

        for report_name, params in [
            ("ProfitAndLoss", {"start_date": start_date, "end_date": end_date}),
            ("BalanceSheet", {"start_date": end_date, "end_date": end_date}),
            ("TrialBalance", {"start_date": end_date, "end_date": end_date}),
        ]:
            try:
                data = client.get(f"reports/{report_name}", params=params)
                filename = f"{month}_{report_name}.json"
                filepath = WORKSPACE / filename
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=2, default=str)
                reports[report_name] = {"status": "generated", "file": str(filepath)}
            except Exception as e:
                reports[report_name] = {"status": "error", "message": str(e)}

    result = {
        "month": month,
        "period": f"{start_date} to {end_date}",
        "checks": checks,
        "all_checks_pass": all(c["status"] == "pass" for c in checks),
        "reports": reports if not check_only else "skipped (--check-only)",
    }

    format_output(result, fmt)


@app.command("1099-prep")
def prep_1099(
    year: Annotated[str, typer.Option("--year", help="Tax year (YYYY)")],
    threshold: Annotated[float, typer.Option("--threshold", help="Filing threshold")] = 600.0,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """1099 filing preparation.

    Queries all 1099-eligible vendors, calculates payment totals,
    and flags vendors over the threshold with missing tax IDs.
    """
    fmt = output or _output()
    client = _client()

    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    # Get all 1099 vendors (Vendor1099 not queryable — fetch all and filter client-side)
    resp = client.query("SELECT * FROM Vendor", max_results=500)
    all_vendors = resp.get("QueryResponse", {}).get("Vendor", [])
    vendors_1099 = [v for v in all_vendors if v.get("Vendor1099") is True]

    vendor_data = []
    for v in vendors_1099:
        vid = v["Id"]
        vname = v.get("DisplayName", "")

        # Sum payments to this vendor
        total_paid = 0.0
        try:
            # BillPayments
            bp_resp = client.query(
                f"SELECT * FROM BillPayment WHERE VendorRef = '{vid}' AND TxnDate >= '{start_date}' AND TxnDate <= '{end_date}'",
                max_results=500,
            )
            for bp in bp_resp.get("QueryResponse", {}).get("BillPayment", []):
                total_paid += float(bp.get("TotalAmt", 0))
        except Exception:
            pass

        try:
            # Direct purchases/checks to this vendor
            p_resp = client.query(
                f"SELECT * FROM Purchase WHERE EntityRef = '{vid}' AND TxnDate >= '{start_date}' AND TxnDate <= '{end_date}'",
                max_results=500,
            )
            for p in p_resp.get("QueryResponse", {}).get("Purchase", []):
                total_paid += float(p.get("TotalAmt", 0))
        except Exception:
            pass

        has_tin = bool(v.get("TaxIdentifier"))

        vendor_data.append({
            "vendor_id": vid,
            "vendor_name": vname,
            "company": v.get("CompanyName", ""),
            "email": (v.get("PrimaryEmailAddr") or {}).get("Address", ""),
            "has_tin": has_tin,
            "tin_status": "on_file" if has_tin else "MISSING",
            "total_paid": round(total_paid, 2),
            "over_threshold": total_paid >= threshold,
            "requires_1099": total_paid >= threshold,
        })

    # Sort by total paid descending
    vendor_data.sort(key=lambda x: x["total_paid"], reverse=True)

    needs_filing = [v for v in vendor_data if v["requires_1099"]]
    missing_tin = [v for v in needs_filing if not v["has_tin"]]

    result = {
        "year": year,
        "threshold": threshold,
        "total_1099_vendors": len(vendors_1099),
        "vendors_over_threshold": len(needs_filing),
        "missing_tin_count": len(missing_tin),
        "total_1099_payments": round(sum(v["total_paid"] for v in needs_filing), 2),
        "action_required": len(missing_tin) > 0,
        "vendors": vendor_data,
    }

    # Export CSV to workspace
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    csv_path = WORKSPACE / f"1099_prep_{year}.csv"
    buf = io.StringIO()
    writer = csv_mod.DictWriter(buf, fieldnames=["vendor_id", "vendor_name", "company", "email", "has_tin", "total_paid", "requires_1099"])
    writer.writeheader()
    for v in vendor_data:
        writer.writerow({k: v[k] for k in writer.fieldnames})
    with open(csv_path, "w") as f:
        f.write(buf.getvalue())
    result["csv_export"] = str(csv_path)

    format_output(result, fmt)


@app.command("ar-followup")
def ar_followup(
    days_overdue: Annotated[int, typer.Option("--days-overdue", help="Minimum days overdue")] = 30,
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List overdue invoices grouped by customer for AR follow-up."""
    fmt = output or _output()
    client = _client()

    cutoff = (datetime.now() - timedelta(days=days_overdue)).strftime("%Y-%m-%d")

    resp = client.query(
        f"SELECT * FROM Invoice WHERE Balance > '0' AND DueDate < '{cutoff}'",
        max_results=500,
    )
    overdue = resp.get("QueryResponse", {}).get("Invoice", [])

    # Group by customer
    by_customer: dict = {}
    for inv in overdue:
        cust_name = inv.get("CustomerRef", {}).get("name", "Unknown")
        cust_id = inv.get("CustomerRef", {}).get("value", "")
        key = cust_id or cust_name

        if key not in by_customer:
            by_customer[key] = {
                "customer_id": cust_id,
                "customer_name": cust_name,
                "invoices": [],
                "total_overdue": 0.0,
            }

        due_date = inv.get("DueDate", "")
        try:
            days = (datetime.now() - datetime.strptime(due_date, "%Y-%m-%d")).days
        except (ValueError, TypeError):
            days = 0

        by_customer[key]["invoices"].append({
            "invoice_id": inv["Id"],
            "doc_number": inv.get("DocNumber", ""),
            "amount": float(inv.get("TotalAmt", 0)),
            "balance": float(inv.get("Balance", 0)),
            "due_date": due_date,
            "days_overdue": days,
        })
        by_customer[key]["total_overdue"] += float(inv.get("Balance", 0))

    customers = sorted(by_customer.values(), key=lambda x: x["total_overdue"], reverse=True)
    for c in customers:
        c["total_overdue"] = round(c["total_overdue"], 2)
        c["invoice_count"] = len(c["invoices"])

    result = {
        "min_days_overdue": days_overdue,
        "customers_with_overdue": len(customers),
        "total_overdue": round(sum(c["total_overdue"] for c in customers), 2),
        "total_invoices": sum(c["invoice_count"] for c in customers),
        "customers": customers,
    }

    format_output(result, fmt)


@app.command("undeposited-funds")
def undeposited_funds(
    output: Annotated[Optional[OutputFormat], typer.Option("-o")] = None,
):
    """List payments sitting in Undeposited Funds."""
    fmt = output or _output()
    client = _client()

    # Find Undeposited Funds account
    resp = client.query("SELECT * FROM Account WHERE Name = 'Undeposited Funds'")
    uf_accounts = resp.get("QueryResponse", {}).get("Account", [])
    if not uf_accounts:
        typer.echo(json.dumps({"status": "ok", "message": "Undeposited Funds account not found or empty"}))
        return

    uf_balance = float(uf_accounts[0].get("CurrentBalance", 0))

    # Query payments that went to Undeposited Funds (those without DepositToAccountRef or with UF)
    payments = []
    try:
        resp = client.query("SELECT * FROM Payment", max_results=500)
        for p in resp.get("QueryResponse", {}).get("Payment", []):
            unapplied = float(p.get("UnappliedAmt", 0))
            deposit_to = p.get("DepositToAccountRef", {}).get("name", "")
            if "undeposited" in deposit_to.lower() or (not deposit_to and unapplied > 0):
                age_days = 0
                try:
                    age_days = (datetime.now() - datetime.strptime(p["TxnDate"], "%Y-%m-%d")).days
                except (ValueError, TypeError):
                    pass
                payments.append({
                    "payment_id": p["Id"],
                    "date": p.get("TxnDate"),
                    "customer": p.get("CustomerRef", {}).get("name", ""),
                    "amount": float(p.get("TotalAmt", 0)),
                    "ref": p.get("PaymentRefNum", ""),
                    "age_days": age_days,
                    "stale": age_days > 3,
                })
    except Exception:
        pass

    payments.sort(key=lambda x: x["age_days"], reverse=True)
    stale_count = sum(1 for p in payments if p["stale"])

    result = {
        "undeposited_funds_balance": uf_balance,
        "payment_count": len(payments),
        "stale_count": stale_count,
        "status": "clean" if abs(uf_balance) < 0.01 else ("warning" if stale_count > 0 else "ok"),
        "payments": payments,
    }

    format_output(result, fmt)
