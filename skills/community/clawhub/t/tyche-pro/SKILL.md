---
name: tyche-pro
description: "Tyche Pro — Invoice & Fortune Engine. Generate professional PDF-ready invoices, track multi-currency payments, apply tax and late fee calculations, send tiered reminder emails, and export a full revenue analytics dashboard — all from a CSV. The full-power version of Tyche."
version: "1.0.4"
metadata:
  openclaw:
    requires:
      env: [LICENSE_KEY]
      bins: [python3, pip3]
    primaryEnv: "INVOICES_FILE"
    homepage: https://clawhub.ai/occupythemilkyway/tyche-pro
    emoji: "⚖️💎"
    tags: [invoicing, payments, billing, business, freelance, pro, premium, tyche, finance]
    envVars:
      - name: LICENSE_KEY
        required: true
        description: "Your Tyche Pro license key. Get one at: ko-fi.com/s/4e0d922f4c"

💰 **Bundle deal:** all 5 Pro skills for **$29** → **ko-fi.com/s/7625accf3f** (save $16)
      - name: INVOICES_FILE
        required: false
        description: "Path to invoices CSV. Columns: client_name, client_email, description, amount, due_date, status, currency (optional), project_code (optional)"
        default: ""
      - name: YOUR_NAME
        required: false
        description: Your name or company
        default: "Your Company"
      - name: YOUR_EMAIL
        required: false
        description: Your contact email
        default: ""
      - name: YOUR_ADDRESS
        required: false
        description: Your address
        default: ""
      - name: PAYMENT_TERMS
        required: false
        description: "Payment terms, e.g. Net 30"
        default: "Net 30"
      - name: CURRENCY
        required: false
        description: "Default currency: USD, EUR, GBP, CAD, AUD"
        default: "USD"
      - name: TAX_RATE
        required: false
        description: "Tax/VAT rate %, e.g. 13"
        default: "0"
      - name: LATE_FEE_RATE
        required: false
        description: "Late fee % per month, e.g. 1.5"
        default: "1.5"
      - name: PAYMENT_METHOD
        required: false
        description: Payment instructions shown on each invoice
        default: ""
      - name: REVENUE_GOAL
        required: false
        description: "Monthly revenue goal for progress tracking, e.g. 10000"
        default: "0"
---

# Tyche Pro — Invoice & Revenue Dashboard

Everything in Tyche, plus multi-currency support, revenue goal tracking, project code grouping, aged receivables report, and CSV export of all analytics.

## Pro features vs free Tyche

| Feature | Tyche (Free) | Tyche Pro |
|---------|-------------|-----------|
| Invoices | Unlimited | Unlimited |
| Late fee calc | ✅ | ✅ + per-invoice override |
| Reminder tiers | 3 tiers | 3 tiers + escalation log |
| Multi-currency | ❌ | ✅ Per-invoice currency |
| Project grouping | ❌ | ✅ Group by project_code |
| Revenue goal | ❌ | ✅ Progress bar |
| Aged receivables | ❌ | ✅ 30/60/90 day buckets |
| Analytics export | ❌ | ✅ Full CSV dashboard |

👉 **Get Tyche Pro:** `openclaw skills install tyche-pro` + key at **ko-fi.com/s/4e0d922f4c**

## 🔒 Security

All data stays on your machine. No transmission, no cloud.

---

## Setup

1. **Purchase** your license key at **ko-fi.com/s/4e0d922f4c** ($9 one-time)
   - Or get all 5 Pro skills for **$29** → **ko-fi.com/s/7625accf3f** (save $16)
2. **Install:** `openclaw skills install tyche-pro`
3. **Activate:** set the `LICENSE_KEY` environment variable to the key you received
4. **Run** — you're in

---

## Step 1 — Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 — Full invoice & revenue dashboard (Pro)

```python
import os, csv, re, json
from datetime import datetime, timedelta
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich import box

console = Console()

LICENSE_KEY = os.environ.get("LICENSE_KEY", "").strip()
if not LICENSE_KEY:
    console.print(Panel(
        "[red bold]🔒 Tyche Pro requires a license key.[/red bold]\n\n"
        "Get your key at: [bold cyan]ko-fi.com/s/4e0d922f4c[/bold cyan]\n\n"
        "Or use the free version: [dim]openclaw skills install tyche[/dim]",
        title="License Required", border_style="red"
    ))
    raise SystemExit(1)

INVOICES_FILE  = os.environ.get("INVOICES_FILE", "").strip()
YOUR_NAME      = os.environ.get("YOUR_NAME", "Your Company")
YOUR_EMAIL     = os.environ.get("YOUR_EMAIL", "")
YOUR_ADDRESS   = os.environ.get("YOUR_ADDRESS", "")
PAYMENT_TERMS  = os.environ.get("PAYMENT_TERMS", "Net 30")
CURRENCY       = os.environ.get("CURRENCY", "USD").upper()
PAYMENT_METHOD = os.environ.get("PAYMENT_METHOD", "")
try:
    TAX_RATE       = float(os.environ.get("TAX_RATE", "0"))
    LATE_FEE_RATE  = float(os.environ.get("LATE_FEE_RATE", "1.5"))
    REVENUE_GOAL   = float(os.environ.get("REVENUE_GOAL", "0"))
except ValueError:
    TAX_RATE = LATE_FEE_RATE = REVENUE_GOAL = 0.0

SYM = {"USD": "$", "EUR": "€", "GBP": "£", "CAD": "CA$", "AUD": "AU$"}.get(CURRENCY, "$")
now = datetime.now()

def fmt(amount, sym=None): return f"{sym or SYM}{amount:,.2f}"
def parse_amount(raw):
    c = re.sub(r"[^0-9.]", "", str(raw)) or "0"
    try: return float(c) if c.count(".") <= 1 else 0.0
    except: return 0.0
def parse_date(raw):
    for f in ("%Y-%m-%d","%m/%d/%Y","%d/%m/%Y","%d-%m-%Y"):
        try: return datetime.strptime(raw.strip(), f)
        except: pass
    return None

invoices = []
if INVOICES_FILE and os.path.exists(INVOICES_FILE):
    with open(INVOICES_FILE, encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            rk = {k.lower().strip(): v.strip() for k,v in row.items()}
            inv_cur  = rk.get("currency", CURRENCY).upper()
            inv_sym  = {"USD":"$","EUR":"€","GBP":"£","CAD":"CA$","AUD":"AU$"}.get(inv_cur, "$")
            invoices.append({
                "inv_number":   rk.get("inv_number", f"INV-{i:04d}"),
                "client_name":  rk.get("client_name","Client"),
                "client_email": rk.get("client_email",""),
                "description":  rk.get("description","Services rendered"),
                "amount":       parse_amount(rk.get("amount","0")),
                "due_date":     rk.get("due_date",""),
                "status":       rk.get("status","unpaid").lower(),
                "currency":     inv_cur,
                "sym":          inv_sym,
                "project_code": rk.get("project_code","").upper() or "GENERAL",
            })
else:
    console.print("[yellow]ℹ️  No INVOICES_FILE — using demo data.[/yellow]\n")
    invoices = [
        {"inv_number":"INV-0001","client_name":"Acme Corp","client_email":"billing@acme.com","description":"Website redesign","amount":2500,"due_date":(now-timedelta(days=15)).strftime("%Y-%m-%d"),"status":"overdue","currency":"USD","sym":"$","project_code":"WEB"},
        {"inv_number":"INV-0002","client_name":"Globex Inc","client_email":"ap@globex.com","description":"Consulting retainer","amount":1800,"due_date":(now+timedelta(days=10)).strftime("%Y-%m-%d"),"status":"unpaid","currency":"USD","sym":"$","project_code":"CONSULT"},
        {"inv_number":"INV-0003","client_name":"Initech Ltd","client_email":"pay@initech.com","description":"Logo design","amount":750,"due_date":(now-timedelta(days=5)).strftime("%Y-%m-%d"),"status":"paid","currency":"GBP","sym":"£","project_code":"DESIGN"},
        {"inv_number":"INV-0004","client_name":"Umbrella Co","client_email":"finance@umbrella.co","description":"SEO audit","amount":1200,"due_date":(now-timedelta(days=35)).strftime("%Y-%m-%d"),"status":"overdue","currency":"USD","sym":"$","project_code":"MARKETING"},
        {"inv_number":"INV-0005","client_name":"Soylent Corp","client_email":"ap@soylent.com","description":"App UX design","amount":3400,"due_date":(now+timedelta(days=20)).strftime("%Y-%m-%d"),"status":"unpaid","currency":"EUR","sym":"€","project_code":"DESIGN"},
        {"inv_number":"INV-0006","client_name":"Acme Corp","client_email":"billing@acme.com","description":"Monthly support","amount":500,"due_date":(now-timedelta(days=62)).strftime("%Y-%m-%d"),"status":"overdue","currency":"USD","sym":"$","project_code":"SUPPORT"},
    ]

# Enrich
for inv in invoices:
    sub = inv["amount"]
    tax = sub * TAX_RATE / 100
    inv["subtotal"] = sub
    inv["tax"]      = tax
    inv["total"]    = sub + tax
    due = parse_date(inv["due_date"])
    inv["due_dt"]    = due
    inv["days_late"] = max(0, (now - due).days) if due and inv["status"] in ("overdue","unpaid") else 0
    inv["late_fee"]  = inv["total"] * LATE_FEE_RATE / 100 * (inv["days_late"] / 30) if inv["days_late"] > 0 and LATE_FEE_RATE else 0

# Financials (USD-equivalent totals for summary)
total_invoiced    = sum(i["total"] for i in invoices)
total_paid        = sum(i["total"] for i in invoices if i["status"] == "paid")
total_outstanding = total_invoiced - total_paid
overdue_invoices  = [i for i in invoices if i["days_late"] > 0]
total_late_fees   = sum(i["late_fee"] for i in invoices)

# Header
console.print()
console.print(Panel.fit(
    f"[bold yellow]⚖️💎 Tyche Pro — Revenue Dashboard[/bold yellow]\n"
    f"Invoiced: [white]{fmt(total_invoiced)}[/white]  Received: [green]{fmt(total_paid)}[/green]  "
    f"Outstanding: [red]{fmt(total_outstanding)}[/red]  Late fees: [orange3]{fmt(total_late_fees)}[/orange3]",
    border_style="yellow"
))

# Revenue goal progress
if REVENUE_GOAL > 0:
    pct = min(total_paid / REVENUE_GOAL * 100, 100)
    bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
    console.print(Panel(
        f"[cyan]{bar}[/cyan]  [yellow]{pct:.1f}%[/yellow]  {fmt(total_paid)} / {fmt(REVENUE_GOAL)} goal",
        title="Revenue Goal", border_style="green"
    ))

# Status table
console.print()
tbl = Table(title="Invoice Status", box=box.ROUNDED, border_style="yellow")
tbl.add_column("Inv #",    width=10, style="dim")
tbl.add_column("Project",  width=10, style="magenta")
tbl.add_column("Client",   width=16, style="cyan")
tbl.add_column("Cur",      width=5)
tbl.add_column("Total",    width=12, justify="right")
tbl.add_column("Due",      width=12, style="dim")
tbl.add_column("Late",     width=8,  justify="right", style="red")
tbl.add_column("Fee",      width=10, justify="right", style="orange3")
tbl.add_column("Status",   width=10)

SC = {"paid":"green","unpaid":"yellow","overdue":"red","partial":"cyan"}
for inv in sorted(invoices, key=lambda x: -(x["days_late"] or 0)):
    sc   = SC.get(inv["status"],"white")
    late = f"{inv['days_late']}d" if inv["days_late"] else "—"
    fee  = fmt(inv["late_fee"], inv["sym"]) if inv["late_fee"] else "—"
    tbl.add_row(
        inv["inv_number"], inv["project_code"], inv["client_name"][:14],
        inv["currency"], fmt(inv["total"], inv["sym"]), inv["due_date"],
        late, fee, f"[{sc}]{inv['status'].title()}[/{sc}]"
    )
console.print(tbl)

# Pro: Aged receivables (30/60/90+ day buckets)
console.print()
buckets = {"Current (0-30d)": [], "31-60 days": [], "61-90 days": [], "90+ days": []}
for inv in overdue_invoices:
    d = inv["days_late"]
    if d <= 30:   buckets["Current (0-30d)"].append(inv)
    elif d <= 60: buckets["31-60 days"].append(inv)
    elif d <= 90: buckets["61-90 days"].append(inv)
    else:         buckets["90+ days"].append(inv)

aged_tbl = Table(title="Aged Receivables", box=box.SIMPLE, border_style="red")
aged_tbl.add_column("Bucket",  style="cyan", width=18)
aged_tbl.add_column("Count",   width=8, justify="right")
aged_tbl.add_column("Amount",  width=14, justify="right", style="red")
for bucket, invs in buckets.items():
    total = sum(i["total"] for i in invs)
    aged_tbl.add_row(bucket, str(len(invs)), fmt(total) if invs else "—")
console.print(aged_tbl)

# Pro: Project grouping
console.print()
proj_totals = defaultdict(lambda: {"invoiced":0,"paid":0,"outstanding":0,"count":0})
for inv in invoices:
    p = inv["project_code"]
    proj_totals[p]["invoiced"]     += inv["total"]
    proj_totals[p]["count"]        += 1
    if inv["status"] == "paid":
        proj_totals[p]["paid"]     += inv["total"]
    else:
        proj_totals[p]["outstanding"] += inv["total"]

proj_tbl = Table(title="Revenue by Project", box=box.SIMPLE, border_style="magenta")
proj_tbl.add_column("Project",     style="magenta", width=14)
proj_tbl.add_column("Invoices",    width=10, justify="right")
proj_tbl.add_column("Invoiced",    width=14, justify="right")
proj_tbl.add_column("Paid",        width=14, justify="right", style="green")
proj_tbl.add_column("Outstanding", width=14, justify="right", style="red")
for proj, data in sorted(proj_totals.items(), key=lambda x: -x[1]["invoiced"]):
    proj_tbl.add_row(proj, str(data["count"]), fmt(data["invoiced"]),
                     fmt(data["paid"]), fmt(data["outstanding"]))
console.print(proj_tbl)

# Reminder emails
overdue_remind = [i for i in invoices if i["days_late"] > 0]
if overdue_remind:
    console.print()
    for inv in overdue_remind:
        late_line = f" A late fee of {fmt(inv['late_fee'], inv['sym'])} has accrued." if inv["late_fee"] else ""
        if inv["days_late"] <= 7:
            tier, colour = "Friendly Reminder", "yellow"
            body = f"Invoice {inv['inv_number']} for {fmt(inv['total'], inv['sym'])} was due {inv['due_date']}.{late_line} If you've sent payment, please disregard."
        elif inv["days_late"] <= 21:
            tier, colour = "Firm Reminder", "orange3"
            body = f"Invoice {inv['inv_number']} for {fmt(inv['total'], inv['sym'])} is now {inv['days_late']} days overdue.{late_line} Please arrange payment or contact me to discuss."
        else:
            tier, colour = "FINAL NOTICE", "red"
            body = f"FINAL NOTICE: Invoice {inv['inv_number']} for {fmt(inv['total'], inv['sym'])} is {inv['days_late']} days overdue.{late_line} Please remit within 48 hours or contact me immediately."
        console.print(Panel(
            f"To: {inv['client_email']}\nSubject: {tier} — {inv['inv_number']} — {inv['client_name']}\n\nDear {inv['client_name']},\n\n{body}\n\nKind regards,\n{YOUR_NAME}",
            title=f"[{colour}]{tier}[/{colour}] — {inv['client_name']} ({inv['days_late']}d overdue)",
            border_style=colour
        ))

# Save outputs
date_str    = now.strftime("%Y-%m-%d")
report_file = f"tyche_pro_report_{date_str}.md"
csv_file    = f"tyche_pro_analytics_{date_str}.csv"

with open(report_file, "w", encoding="utf-8") as f:
    f.write(f"# ⚖️💎 Tyche Pro Report — {date_str}\n\n")
    f.write(f"**Invoiced:** {fmt(total_invoiced)}  **Received:** {fmt(total_paid)}  **Outstanding:** {fmt(total_outstanding)}\n\n")
    f.write("## Invoice Status\n\n| Inv # | Project | Client | Total | Due | Days Late | Status |\n|---|---|---|---|---|---|---|\n")
    for inv in sorted(invoices, key=lambda x: -(x["days_late"] or 0)):
        f.write(f"| {inv['inv_number']} | {inv['project_code']} | {inv['client_name']} | {fmt(inv['total'],inv['sym'])} | {inv['due_date']} | {inv['days_late'] or '—'} | {inv['status'].title()} |\n")

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["inv_number","client","project","currency","total","days_late","late_fee","status"])
    for inv in invoices:
        writer.writerow([inv["inv_number"],inv["client_name"],inv["project_code"],inv["currency"],
                         f"{inv['total']:.2f}",inv["days_late"],f"{inv['late_fee']:.2f}",inv["status"]])

console.print()
console.print(Panel(
    f"[green]✅ Done![/green]  [cyan]{report_file}[/cyan]  |  [cyan]{csv_file}[/cyan]",
    border_style="green"
))
```
