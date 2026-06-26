---
name: tyche-lite
description: "Tyche Lite — Invoice Tracker (Free). Process up to 5 invoices from a CSV, see payment status, and get a friendly reminder template. A free preview of what Tyche Pro does for your full client book."
version: "1.0.4"
metadata:
  openclaw:
    requires:
      env: []
      bins: [python3, pip3]
    primaryEnv: "INVOICES_FILE"
    homepage: https://clawhub.ai/occupythemilkyway/tyche-lite
    emoji: "⚖️"
    tags: [invoicing, payments, billing, business, freelance, free, lite, tyche]
    envVars:
      - name: INVOICES_FILE
        required: false
        description: "Path to invoices CSV (client_name, client_email, description, amount, due_date, status). Max 5 rows in Lite."
        default: ""
      - name: YOUR_NAME
        required: false
        description: Your name or company
        default: "Your Name"
      - name: CURRENCY
        required: false
        description: "Currency: USD, EUR, GBP"
        default: "USD"
---

# Tyche Lite — Free Invoice Preview

Track up to 5 invoices and get a friendly reminder template.

## Free vs Pro

| Feature | Tyche Lite (Free) | Tyche Pro |
|---------|------------------|-----------|
| Invoices | **5 max** | Unlimited |
| Tax calculation | ❌ | ✅ |
| Late fee calculation | ❌ | ✅ |
| Reminder tiers | 1 (friendly only) | 3 tiers |
| Multi-currency | ❌ | ✅ |
| Project grouping | ❌ | ✅ |
| Aged receivables | ❌ | ✅ 30/60/90d |
| Analytics export | ❌ | ✅ |

👉 **Upgrade:** `openclaw skills install tyche-pro` — key at **ko-fi.com/s/4e0d922f4c**

💰 **Bundle deal:** all 5 Pro skills for **$29** → **ko-fi.com/s/7625accf3f** (save $16)

---

## Step 1 — Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 — Invoice overview (Lite)

```python
import os, csv, re
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

INVOICES_FILE = os.environ.get("INVOICES_FILE","").strip()
YOUR_NAME     = os.environ.get("YOUR_NAME","Your Name")
CURRENCY      = os.environ.get("CURRENCY","USD").upper()
SYM           = {"USD":"$","EUR":"€","GBP":"£"}.get(CURRENCY,"$")
INVOICE_LIMIT = 5  # Lite cap
now           = datetime.now()

def fmt(a): return f"{SYM}{a:,.2f}"
def parse_amount(r):
    c = re.sub(r"[^0-9.]","",str(r)) or "0"
    try: return float(c) if c.count(".")<=1 else 0.0
    except: return 0.0
def parse_date(raw):
    for f in ("%Y-%m-%d","%m/%d/%Y","%d/%m/%Y"):
        try: return datetime.strptime(raw.strip(),f)
        except: pass
    return None

invoices = []
if INVOICES_FILE and os.path.exists(INVOICES_FILE):
    with open(INVOICES_FILE,encoding="utf-8",errors="replace") as f:
        reader = csv.DictReader(f)
        for i,row in enumerate(reader,1):
            if i > INVOICE_LIMIT:
                console.print(f"[yellow]⚠️  Lite limit: showing first {INVOICE_LIMIT} invoices only. Upgrade to Pro for unlimited.[/yellow]")
                break
            rk = {k.lower().strip():v.strip() for k,v in row.items()}
            invoices.append({
                "inv_number":   rk.get("inv_number",f"INV-{i:04d}"),
                "client_name":  rk.get("client_name","Client"),
                "client_email": rk.get("client_email",""),
                "description":  rk.get("description","Services"),
                "amount":       parse_amount(rk.get("amount","0")),
                "due_date":     rk.get("due_date",""),
                "status":       rk.get("status","unpaid").lower(),
            })
else:
    console.print("[yellow]ℹ️  No INVOICES_FILE — using demo data.[/yellow]\n")
    invoices = [
        {"inv_number":"INV-0001","client_name":"Acme Corp","client_email":"billing@acme.com","description":"Website redesign","amount":2500,"due_date":(now-timedelta(days=15)).strftime("%Y-%m-%d"),"status":"overdue"},
        {"inv_number":"INV-0002","client_name":"Globex Inc","client_email":"ap@globex.com","description":"Consulting","amount":1800,"due_date":(now+timedelta(days=10)).strftime("%Y-%m-%d"),"status":"unpaid"},
        {"inv_number":"INV-0003","client_name":"Initech Ltd","client_email":"pay@initech.com","description":"Logo design","amount":750,"due_date":(now-timedelta(days=5)).strftime("%Y-%m-%d"),"status":"paid"},
    ]

for inv in invoices:
    due = parse_date(inv["due_date"])
    inv["due_dt"]    = due
    inv["days_late"] = max(0,(now-due).days) if due and inv["status"] in ("overdue","unpaid") else 0

total_invoiced    = sum(i["amount"] for i in invoices)
total_paid        = sum(i["amount"] for i in invoices if i["status"]=="paid")
total_outstanding = total_invoiced - total_paid

console.print()
console.print(Panel.fit(
    f"[bold yellow]⚖️  Tyche Lite — Invoice Overview[/bold yellow]\n"
    f"Invoiced: [white]{fmt(total_invoiced)}[/white]  Paid: [green]{fmt(total_paid)}[/green]  Outstanding: [red]{fmt(total_outstanding)}[/red]\n"
    f"[dim]Lite: showing {len(invoices)}/{INVOICE_LIMIT} invoices max[/dim]",
    border_style="yellow"
))

SC = {"paid":"green","unpaid":"yellow","overdue":"red","partial":"cyan"}
console.print()
tbl = Table(title="Invoice Status", box=box.ROUNDED, border_style="yellow")
tbl.add_column("Inv #",   width=10, style="dim")
tbl.add_column("Client",  width=18, style="cyan")
tbl.add_column("Amount",  width=12, justify="right")
tbl.add_column("Due",     width=12, style="dim")
tbl.add_column("Late",    width=8,  style="red", justify="right")
tbl.add_column("Status",  width=10)
for inv in sorted(invoices, key=lambda x: -(x["days_late"] or 0)):
    sc   = SC.get(inv["status"],"white")
    late = f"{inv['days_late']}d" if inv["days_late"] else "—"
    tbl.add_row(inv["inv_number"],inv["client_name"][:16],fmt(inv["amount"]),inv["due_date"],late,f"[{sc}]{inv['status'].title()}[/{sc}]")
console.print(tbl)

# 1 reminder (Lite: friendly only)
overdue = [i for i in invoices if i["days_late"] > 0]
if overdue:
    inv = overdue[0]
    console.print()
    console.print(Panel(
        f"To: {inv['client_email']}\nSubject: Friendly Reminder — Invoice {inv['inv_number']}\n\n"
        f"Dear {inv['client_name']},\n\n"
        f"I hope you're well. Invoice {inv['inv_number']} for {fmt(inv['amount'])} was due {inv['due_date']}. "
        f"Could you confirm when payment will be processed?\n\n"
        f"Kind regards,\n{YOUR_NAME}",
        title=f"[yellow]Friendly Reminder — {inv['client_name']} ({inv['days_late']}d overdue)[/yellow]",
        border_style="yellow"
    ))
    if len(overdue) > 1:
        console.print(f"[dim]+ {len(overdue)-1} more overdue invoice(s) — upgrade to Pro for all reminder tiers.[/dim]")

console.print()
console.print(Panel(
    f"[bold yellow]🔓 Want more?[/bold yellow]\n\n"
    f"Tyche Pro handles [bold]unlimited invoices[/bold], calculates [bold]late fees & tax[/bold], "
    f"sends [bold]3-tier reminders[/bold], groups by project, and gives you an aged receivables dashboard.\n\n"
    f"[bold cyan]openclaw skills install tyche-pro[/bold cyan]\n"
    f"Get your key → [bold]ko-fi.com/s/4e0d922f4c[/bold]",
    title="Upgrade to Tyche Pro",
    border_style="cyan"
))
```
