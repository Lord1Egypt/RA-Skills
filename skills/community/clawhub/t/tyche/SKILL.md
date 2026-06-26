---
name: tyche
description: "Tyche — Goddess of Fortune. Generate professional invoice documents, track payment status, calculate late fees, and send automated overdue reminders — all from a simple CSV list of clients and work. Each client gets a ready-to-send invoice. Fortune favours the organised."
version: "1.0.4"
metadata:
  openclaw:
    requires:
      env: []
      bins: [python3, pip3]
    primaryEnv: "INVOICES_FILE"
    homepage: https://clawhub.ai/occupythemilkyway/tyche
    emoji: "⚖️💸"
    tags: [invoicing, payments, billing, business, freelance, tyche, finance, reminders]
    envVars:
      - name: INVOICES_FILE
        required: false
        description: "Path to a CSV file with columns: client_name, client_email, description, amount, due_date, status. Leave blank to use demo data."
        default: ""
      - name: YOUR_NAME
        required: false
        description: "Your name or company name (appears on invoices)"
        default: "Your Name"
      - name: YOUR_EMAIL
        required: false
        description: "Your contact email (appears on invoices)"
        default: ""
      - name: YOUR_ADDRESS
        required: false
        description: "Your address (appears on invoices)"
        default: ""
      - name: PAYMENT_TERMS
        required: false
        description: "Payment terms text, e.g. 'Net 30', 'Due on receipt'"
        default: "Net 30"
      - name: CURRENCY
        required: false
        description: "Currency code: USD, EUR, GBP, CAD, AUD"
        default: "USD"
      - name: TAX_RATE
        required: false
        description: "Tax/VAT rate as a percentage, e.g. 13 for 13%"
        default: "0"
      - name: LATE_FEE_RATE
        required: false
        description: "Late fee as a percentage of invoice amount per month, e.g. 1.5"
        default: "0"
      - name: PAYMENT_METHOD
        required: false
        description: "Payment instructions shown on invoices, e.g. 'Bank transfer to: BSB 123-456 Account 7890'"
        default: ""
---

# Tyche — Invoice & Payment Tracker

Generate professional invoices, track overdue payments, calculate late fees, and get 3-tier reminder scripts — all from a simple CSV file.

## What you get

- **Professional invoice text** per client — ready to paste into email or PDF
- **Payment status dashboard** — paid vs. outstanding vs. overdue at a glance
- **Overdue report** — who owes what, how many days late, and late fees owed
- **3-tier reminder templates** — Friendly · Firm · Final Notice
- **Revenue summary** — total invoiced, received, and outstanding

## Input CSV format

Create a file `invoices.csv`:
```
client_name,client_email,description,amount,due_date,status
Acme Corp,billing@acme.com,Website redesign,2500,2025-02-01,unpaid
Globex Inc,accounts@globex.com,Consulting Feb,1800,2025-01-15,overdue
Initech Ltd,pay@initech.com,Logo design,750,2025-02-10,paid
```

**Status values:** `paid` · `unpaid` · `overdue` · `partial`

## 🔒 Security

Runs entirely locally. No data transmitted. Your client data stays on your machine.

---

## Step 1 — Install

```bash
pip3 install rich --break-system-packages --quiet
```

---


---

## ⚡ Upgrade to Tyche Pro

👉 **Get Tyche Pro** → **ko-fi.com/s/4e0d922f4c** — $9 one-time

```bash
openclaw skills install tyche-pro
# Set LICENSE_KEY env var to your key from Ko-fi, then run
```

💰 **Bundle deal:** all 5 Pro skills for **$29** → **ko-fi.com/s/7625accf3f** (save $16)

## Step 2 — Generate invoices and payment reminders

```python
import os, csv, re
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

FENCE = chr(96) * 3

console = Console()

INVOICES_FILE  = os.environ.get("INVOICES_FILE", "").strip()
YOUR_NAME      = os.environ.get("YOUR_NAME", "Your Name / Company")
YOUR_EMAIL     = os.environ.get("YOUR_EMAIL", "")
YOUR_ADDRESS   = os.environ.get("YOUR_ADDRESS", "")
PAYMENT_TERMS  = os.environ.get("PAYMENT_TERMS", "Net 30")
CURRENCY       = os.environ.get("CURRENCY", "USD").upper()
PAYMENT_METHOD = os.environ.get("PAYMENT_METHOD", "")
try:
    TAX_RATE = float(os.environ.get("TAX_RATE", "0"))
except ValueError:
    console.print("[yellow]⚠️  TAX_RATE must be a number — defaulting to 0[/yellow]")
    TAX_RATE = 0.0
try:
    LATE_FEE_RATE = float(os.environ.get("LATE_FEE_RATE", "0"))
except ValueError:
    console.print("[yellow]⚠️  LATE_FEE_RATE must be a number — defaulting to 0[/yellow]")
    LATE_FEE_RATE = 0.0

CURRENCY_SYMBOL = {"USD": "$", "EUR": "€", "GBP": "£", "CAD": "CA$", "AUD": "AU$"}.get(CURRENCY, "$")

def fmt(amount: float) -> str:
    return f"{CURRENCY_SYMBOL}{amount:,.2f}"

def parse_amount(raw: str) -> float:
    cleaned = re.sub(r"[^0-9.]", "", str(raw)) or "0"
    try:
        return float(cleaned) if cleaned.count(".") <= 1 else 0.0
    except ValueError:
        return 0.0

def parse_date(raw: str) -> datetime | None:
    for fmt_str in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%d-%m-%Y", "%b %d %Y", "%B %d %Y"):
        try:
            return datetime.strptime(raw.strip(), fmt_str)
        except ValueError:
            pass
    return None

invoices = []

if INVOICES_FILE and os.path.exists(INVOICES_FILE):
    with open(INVOICES_FILE, encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            console.print("[red]❌ CSV file is empty or has no headers.[/red]")
            raise SystemExit(1)
        headers = [h.lower().strip() for h in reader.fieldnames]
        required = ["client_name", "amount"]
        missing  = [r for r in required if not any(r in h for h in headers)]
        if missing:
            console.print(f"[red]❌ CSV is missing required columns: {missing}\nFound: {headers}[/red]")
            raise SystemExit(1)
        for i, row in enumerate(reader, 1):
            rk = {k.lower().strip(): v for k, v in row.items()}
            invoices.append({
                "inv_number":   rk.get("inv_number", f"INV-{i:04d}"),
                "client_name":  rk.get("client_name", "Client"),
                "client_email": rk.get("client_email", ""),
                "description":  rk.get("description", "Services rendered"),
                "amount":       parse_amount(rk.get("amount", "0")),
                "due_date":     rk.get("due_date", ""),
                "status":       rk.get("status", "unpaid").lower().strip(),
            })
elif INVOICES_FILE:
    console.print(f"[red]❌ File not found: {INVOICES_FILE}[/red]")
    raise SystemExit(1)
else:
    console.print("[yellow]ℹ️  No INVOICES_FILE set — running with demo data.[/yellow]")
    console.print("[dim]Set INVOICES_FILE=path/to/invoices.csv to use your own data.\n[/dim]")
    today = datetime.now()
    invoices = [
        {"inv_number": "INV-0001", "client_name": "Acme Corp",    "client_email": "billing@acme.com",    "description": "Website redesign — Q1 2025",       "amount": 2500.00, "due_date": (today - timedelta(days=15)).strftime("%Y-%m-%d"), "status": "overdue"},
        {"inv_number": "INV-0002", "client_name": "Globex Inc",   "client_email": "accounts@globex.com", "description": "Monthly consulting retainer",       "amount": 1800.00, "due_date": (today + timedelta(days=10)).strftime("%Y-%m-%d"), "status": "unpaid"},
        {"inv_number": "INV-0003", "client_name": "Initech Ltd",  "client_email": "pay@initech.com",     "description": "Logo & brand identity package",     "amount":  750.00, "due_date": (today - timedelta(days=5)).strftime("%Y-%m-%d"),  "status": "paid"},
        {"inv_number": "INV-0004", "client_name": "Umbrella Co",  "client_email": "finance@umbrella.co", "description": "SEO audit and content strategy",    "amount": 1200.00, "due_date": (today - timedelta(days=32)).strftime("%Y-%m-%d"), "status": "overdue"},
        {"inv_number": "INV-0005", "client_name": "Soylent Corp", "client_email": "ap@soylent.com",      "description": "Mobile app UX design, 3 screens",   "amount": 3400.00, "due_date": (today + timedelta(days=20)).strftime("%Y-%m-%d"), "status": "unpaid"},
    ]

if not invoices:
    console.print("[yellow]No invoices found — check your CSV.[/yellow]")
    raise SystemExit(0)

now = datetime.now()

# ── Enrich with computed fields ───────────────────────────────────────────────
for inv in invoices:
    sub     = inv["amount"]
    tax     = sub * TAX_RATE / 100
    inv["subtotal"] = sub
    inv["tax"]      = tax
    inv["total"]    = sub + tax

    due = parse_date(inv["due_date"])
    inv["due_dt"]    = due
    inv["days_late"] = max(0, (now - due).days) if due and inv["status"] in ("overdue", "unpaid") else 0
    inv["late_fee"]  = inv["total"] * LATE_FEE_RATE / 100 * (inv["days_late"] / 30) if inv["days_late"] > 0 and LATE_FEE_RATE else 0

# ── Header ────────────────────────────────────────────────────────────────────
total_invoiced   = sum(i["total"] for i in invoices)
total_paid       = sum(i["total"] for i in invoices if i["status"] == "paid")
total_outstanding = total_invoiced - total_paid
overdue_invoices  = [i for i in invoices if i["status"] == "overdue" or i["days_late"] > 0]

console.print()
console.print(Panel.fit(
    f"[bold yellow]⚖️  Tyche — Invoice Dashboard[/bold yellow]\n"
    f"Total invoiced: [white]{fmt(total_invoiced)}[/white]  |  "
    f"Received: [green]{fmt(total_paid)}[/green]  |  "
    f"Outstanding: [red]{fmt(total_outstanding)}[/red]  |  "
    f"Overdue: [red]{len(overdue_invoices)}[/red]",
    border_style="yellow"
))

# ── Payment status table ──────────────────────────────────────────────────────
console.print()
status_table = Table(title="Invoice Status", box=box.ROUNDED, border_style="yellow")
status_table.add_column("Inv #",     style="dim",    width=10)
status_table.add_column("Client",    style="cyan",   width=18)
status_table.add_column("Description",style="white", width=30)
status_table.add_column("Total",     style="white",  width=12, justify="right")
status_table.add_column("Due Date",  style="dim",    width=12)
status_table.add_column("Days Late", style="red",    width=10, justify="right")
status_table.add_column("Status",    style="white",  width=12)

STATUS_COLOURS = {"paid": "green", "unpaid": "yellow", "overdue": "red", "partial": "cyan"}
for inv in sorted(invoices, key=lambda x: -(x["days_late"] or 0)):
    sc   = STATUS_COLOURS.get(inv["status"], "white")
    late = f"[red]{inv['days_late']}d[/red]" if inv["days_late"] > 0 else "—"
    status_table.add_row(
        inv["inv_number"],
        inv["client_name"][:16],
        inv["description"][:28],
        fmt(inv["total"]),
        inv["due_date"] or "—",
        late,
        f"[{sc}]{inv['status'].title()}[/{sc}]",
    )
console.print(status_table)

# ── Invoice texts ─────────────────────────────────────────────────────────────
console.print()
for inv in invoices:
    tax_line = f"\nTax ({TAX_RATE}%):    {fmt(inv['tax'])}" if TAX_RATE else ""
    payment_line = f"\n\nPayment method:\n{PAYMENT_METHOD}" if PAYMENT_METHOD else ""
    address_line = f"\n{YOUR_ADDRESS}" if YOUR_ADDRESS else ""
    invoice_text = (
        f"{'─'*50}\n"
        f"INVOICE {inv['inv_number']}\n"
        f"{'─'*50}\n"
        f"From:  {YOUR_NAME}\n"
        f"       {YOUR_EMAIL}{address_line}\n\n"
        f"To:    {inv['client_name']}\n"
        f"       {inv['client_email']}\n\n"
        f"Description: {inv['description']}\n\n"
        f"Subtotal:    {fmt(inv['subtotal'])}{tax_line}\n"
        f"TOTAL DUE:   {fmt(inv['total'])}\n\n"
        f"Due date:    {inv['due_date'] or 'Upon receipt'}\n"
        f"Terms:       {PAYMENT_TERMS}\n"
        f"{payment_line}"
    )
    status_colour = STATUS_COLOURS.get(inv["status"], "white")
    console.print(Panel(
        invoice_text,
        title=f"[bold]{inv['inv_number']} — {inv['client_name']}[/bold]  [{status_colour}]({inv['status'].title()})[/{status_colour}]",
        border_style="cyan"
    ))

# ── Reminder templates ────────────────────────────────────────────────────────
overdue_with_reminders = [i for i in invoices if i["status"] in ("overdue", "unpaid") and i["days_late"] > 0]
if overdue_with_reminders:
    console.print()
    for inv in overdue_with_reminders:
        late_line = f" A late fee of {fmt(inv['late_fee'])} has been applied." if inv["late_fee"] else ""
        if inv["days_late"] <= 7:
            tier, colour = "Friendly Reminder", "yellow"
            body = (
                f"I hope this message finds you well. This is a friendly reminder that invoice "
                f"{inv['inv_number']} for {fmt(inv['total'])} was due on {inv['due_date']}. "
                f"If you've already sent payment, please disregard this message. "
                f"Otherwise, I'd appreciate payment at your earliest convenience."
            )
        elif inv["days_late"] <= 21:
            tier, colour = "Firm Reminder", "orange3"
            body = (
                f"This is a follow-up regarding invoice {inv['inv_number']} for {fmt(inv['total'])}, "
                f"which is now {inv['days_late']} days past its due date of {inv['due_date']}.{late_line} "
                f"Please arrange payment or contact me to discuss if there is an issue."
            )
        else:
            tier, colour = "Final Notice", "red"
            body = (
                f"FINAL NOTICE: Invoice {inv['inv_number']} for {fmt(inv['total'])} is {inv['days_late']} days overdue.{late_line} "
                f"Please remit payment within 48 hours to avoid further action. "
                f"Contact me immediately if you wish to discuss a payment arrangement."
            )
        reminder_text = (
            f"To: {inv['client_email']}\n"
            f"Subject: {tier} — Invoice {inv['inv_number']} — {inv['client_name']}\n\n"
            f"Dear {inv['client_name']},\n\n{body}\n\n"
            f"Kind regards,\n{YOUR_NAME}"
        )
        console.print(Panel(
            reminder_text,
            title=f"[bold][{colour}]{tier}[/{colour}] — {inv['client_name']} ({inv['days_late']}d late)[/bold]",
            border_style=colour
        ))

# ── Save report ───────────────────────────────────────────────────────────────
report_date = now.strftime("%Y-%m-%d")
report_file = f"invoice_report_{report_date}.md"

with open(report_file, "w", encoding="utf-8") as f:
    f.write(f"# ⚖️ Tyche Invoice Report — {report_date}\n\n")
    f.write(f"**Total invoiced:** {fmt(total_invoiced)}  ")
    f.write(f"**Received:** {fmt(total_paid)}  ")
    f.write(f"**Outstanding:** {fmt(total_outstanding)}  ")
    f.write(f"**Overdue count:** {len(overdue_invoices)}\n\n")
    f.write("## Invoice Status\n\n| Inv # | Client | Total | Due | Days Late | Status |\n")
    f.write("|-------|--------|-------|-----|-----------|--------|\n")
    for inv in sorted(invoices, key=lambda x: -(x["days_late"] or 0)):
        late_str = f"{inv['days_late']}d" if inv["days_late"] else "—"
        f.write(f"| {inv['inv_number']} | {inv['client_name']} | {fmt(inv['total'])} | {inv['due_date']} | {late_str} | {inv['status'].title()} |\n")
    f.write("\n## Invoice Texts\n\n")
    for inv in invoices:
        tax_line = f"\nTax ({TAX_RATE}%): {fmt(inv['tax'])}" if TAX_RATE else ""
        f.write(f"### {inv['inv_number']} — {inv['client_name']}\n\n{FENCE}\n")
        f.write(f"INVOICE {inv['inv_number']}\nFrom: {YOUR_NAME}\nTo: {inv['client_name']} <{inv['client_email']}>\n")
        f.write(f"Description: {inv['description']}\nSubtotal: {fmt(inv['subtotal'])}{tax_line}\nTOTAL: {fmt(inv['total'])}\n")
        f.write(f"Due: {inv['due_date']}  Terms: {PAYMENT_TERMS}\n{FENCE}\n\n")

console.print()
console.print(Panel(
    f"[green]✅ Done![/green]  Report saved to [cyan]{report_file}[/cyan]",
    border_style="green"
))
```
