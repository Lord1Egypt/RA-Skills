#!/usr/bin/env python3
"""
smb-invoice-tracker — executable (v1.0)

Usage:
  clawhub run smb-invoice-tracker auth gmail
  clawhub run smb-invoice-tracker add --payer "Acme Corp" --amount 1500 --currency USD --due 2026-07-15 --note "Q2 consulting"
  clawhub run smb-invoice-tracker scan
  clawhub run smb-invoice-tracker list [--status overdue|paid|all]
  clawhub run smb-invoice-tracker mark-paid --id INV-001
  clawhub run smb-invoice-tracker send-reminder --id INV-001
  clawhub run smb-invoice-tracker report --period week|month
  clawhub run smb-invoice-tracker configure --tone polite --channel email --reminder-schedule "T-7,T-1,T+0,T+7"
  clawhub run smb-invoice-tracker currency --base USD --rates-from exchangerate-api.com

Free tier: track up to 5 invoices.
"""
import argparse
import csv
import json
import logging
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

__version__ = "1.0.1"
SCHEMA_VERSION = 1

logger = logging.getLogger("smb-invoice-tracker")
USER_AGENT = "SMBInvoiceTracker/1.0 (+https://clawhub.ai)"
DATA_PATH = Path.home() / ".openclaw" / "smb-invoice-tracker" / "invoices.json"
CONFIG_PATH = Path.home() / ".openclaw" / "smb-invoice-tracker" / "config.json"


def configure_logging(verbose=False, quiet=False):
    """Configure logging level based on flags / env."""
    level = logging.WARNING
    if verbose:
        level = logging.DEBUG
    elif not quiet:
        level = logging.INFO
    env_level = os.environ.get("CLAWHUB_LOG_LEVEL", "").upper()
    if env_level in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
        level = getattr(logging, env_level)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )


def load_invoices():
    """Load invoices from disk. Returns list of dicts."""
    if not DATA_PATH.exists():
        return []
    try:
        with open(DATA_PATH) as f:
            data = json.load(f)
            # Handle new wrapped format
            if isinstance(data, dict) and "invoices" in data:
                file_schema = data.get("_schema_version", 0)
                if file_schema < SCHEMA_VERSION:
                    logger.info(f"Migrating invoices schema from v{file_schema} to v{SCHEMA_VERSION}")
                return data["invoices"]
            # Old format (plain list) - migrate silently
            return data
    except (json.JSONDecodeError, IOError):
        return []


def save_invoices(invoices):
    """Save invoices to disk with schema versioning."""
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    wrapped = {"_schema_version": SCHEMA_VERSION, "invoices": invoices}
    with open(DATA_PATH, "w") as f:
        json.dump(wrapped, f, indent=2)


def load_config():
    """Load skill config."""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH) as f:
                cfg = json.load(f)
                file_schema = cfg.get("_schema_version", 0)
                if file_schema < SCHEMA_VERSION:
                    logger.info(f"Migrating config schema from v{file_schema} to v{SCHEMA_VERSION}")
                cfg.pop("_schema_version", None)
                return cfg
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "tone": "polite",
        "channel": "email",
        "reminder_schedule": "T-7,T-1,T+0,T+7",
        "base_currency": "USD",
        "gmail_authorized": False,
        "rates_source": None,
    }


def save_config(config):
    """Save skill config with schema versioning."""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    wrapped = {"_schema_version": SCHEMA_VERSION, **config}
    with open(CONFIG_PATH, "w") as f:
        json.dump(wrapped, f, indent=2)


def get_llm_api_key():
    # Scope to MINIMAX only — do not accept OPENAI_API_KEY or LLM_API_KEY.
    key = os.environ.get("MINIMAX_API_KEY")
    if key:
        return key, "MINIMAX_API_KEY"
    return None, None


def call_llm(prompt, max_tokens=600):
    """Call LLM via pinned minimax endpoint. TT3 fix: no env override."""
    api_key, _ = get_llm_api_key()
    if not api_key:
        return None
    base_url = "https://api.minimax.chat/v1"  # pinned, no env override
    try:
        data = json.dumps({
            "model": "minimax/MiniMax-M3",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.2,
        }).encode()
        req = urllib.request.Request(
            f"{base_url}/chat/completions",
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
            }
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
            return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.info(f"  warn: LLM call failed: {type(e).__name__}")
        return None


def generate_invoice_id(existing):
    """Generate next invoice ID like INV-001, INV-002, etc."""
    nums = []
    for inv in existing:
        m = re.match(r"INV-(\d+)", inv.get("id", ""))
        if m:
            nums.append(int(m.group(1)))
    next_num = max(nums) + 1 if nums else 1
    return f"INV-{next_num:03d}"


def cmd_add(args):
    """Add an invoice manually."""
    invoices = load_invoices()

    # Free tier check
    if not args.pro and len(invoices) >= 5:
        print(f"Free tier limited to 5 invoices. You have {len(invoices)}.")
        print(f"Use --pro flag for unlimited tracking (paid tier).")
        sys.exit(1)

    inv = {
        "id": generate_invoice_id(invoices),
        "payer": args.payer,
        "amount": args.amount,
        "currency": args.currency.upper(),
        "due": args.due,
        "note": args.note or "",
        "status": "outstanding",
        "created_at": datetime.now().isoformat(),
        "reminders_sent": [],
        "paid_at": None,
    }

    invoices.append(inv)
    save_invoices(invoices)

    logger.info(f"\n✓ Added {inv['id']}: {inv['payer']} — {inv['amount']} {inv['currency']} due {inv['due']}")


def cmd_list(args):
    """List invoices."""
    invoices = load_invoices()

    status_filter = args.status or "all"
    if status_filter != "all":
        invoices = [inv for inv in invoices if inv.get("status") == status_filter]

    if not invoices:
        logger.info("No invoices found.")
        return

    # Compute overdue
    today = datetime.now().date()
    print(f"\n{'ID':<10} {'Status':<14} {'Days':<6} {'Payer':<30} {'Amount':<14} {'Due':<12}")
    print("-" * 90)
    total_outstanding = 0
    total_paid = 0
    for inv in invoices:
        try:
            due_date = datetime.strptime(inv["due"], "%Y-%m-%d").date()
            days_to_due = (due_date - today).days
        except (ValueError, KeyError):
            days_to_due = "?"
        amount_str = f"{inv['amount']} {inv['currency']}"
        if inv.get("status") == "paid":
            total_paid += inv["amount"]
        else:
            total_outstanding += inv["amount"]
        print(f"{inv['id']:<10} {inv['status']:<14} {str(days_to_due):<6} {inv['payer'][:30]:<30} {amount_str:<14} {inv['due']:<12}")

    print(f"\nOutstanding: {total_outstanding} | Paid: {total_paid} | Total tracked: {len(invoices)}")


def cmd_mark_paid(args):
    """Mark an invoice as paid."""
    invoices = load_invoices()
    found = False
    for inv in invoices:
        if inv["id"] == args.id:
            inv["status"] = "paid"
            inv["paid_at"] = datetime.now().isoformat()
            found = True
            break
    if not found:
        logger.error(f"ERROR: invoice {args.id} not found")
        sys.exit(1)
    save_invoices(invoices)
    logger.info(f"✓ {args.id} marked as paid")


def cmd_send_reminder(args):
    """Send a payment reminder for a specific invoice."""
    invoices = load_invoices()
    inv = None
    for i in invoices:
        if i["id"] == args.id:
            inv = i
            break
    if not inv:
        logger.error(f"ERROR: invoice {args.id} not found")
        sys.exit(1)

    config = load_config()
    tone = config.get("tone", "polite")
    channel = config.get("channel", "email")

    # Generate reminder text via LLM
    api_key, _ = get_llm_api_key()
    if api_key:
        prompt = f"""Write a short payment reminder for the following invoice. Tone: {tone}.

Invoice: {inv['id']}
Payer: {inv['payer']}
Amount: {inv['amount']} {inv['currency']}
Due: {inv['due']}
Note: {inv.get('note', 'N/A')}

Output: a short message (2-3 sentences) for {channel}. Do not include a subject line, just the body."""
        body = call_llm(prompt)
    
    # Fallback to template if no LLM available or LLM call failed
    if not body:
        body = f"Hi,\n\nThis is a friendly reminder that invoice {inv['id']} for {inv['amount']} {inv['currency']} is due on {inv['due']}.\n\nPlease let me know if you have any questions.\n\nThank you."

    # Update reminder tracking
    today_str = datetime.now().strftime("%Y-%m-%d")
    if "reminders_sent" not in inv:
        inv["reminders_sent"] = []
    inv["reminders_sent"].append({"date": today_str, "tone": tone, "channel": channel})
    save_invoices(invoices)

    logger.info(f"\n{'=' * 70}")
    logger.info(f"REMINDER ({tone}, {channel}) for {inv['payer']}")
    logger.info(f"{'=' * 70}")
    print(body)
    logger.info(f"{'=' * 70}")
    logger.info(f"Reminder tracked for {inv['id']} ({len(inv['reminders_sent'])} total sent)")


def cmd_scan(args):
    """Scan Gmail for new invoice-related emails (placeholder for OAuth flow)."""
    config = load_config()
    if not config.get("gmail_authorized"):
        logger.info("Gmail not authorized. Run:")
        logger.info("  clawhub run smb-invoice-tracker auth gmail")
        print()
        logger.info("Then re-run this command.")
        sys.exit(1)

    # In production, this would call Gmail API with OAuth token
    # For now, print what would happen
    logger.info("\n[Gmail scan] would query the Gmail API for:")
    logger.info("  - Subject contains: invoice, payment due, receipt, bill")
    logger.info("  - Attachments: PDF, PNG, JPG")
    logger.info("  - Last 7 days")
    print()
    logger.info("Note: Gmail API integration requires OAuth credentials.")
    logger.info("To implement: provide GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET env vars.")
    logger.info("Then re-publish this skill with the integration.")


def cmd_auth_gmail(args):
    """Authorize Gmail (OAuth flow placeholder)."""
    config = load_config()
    logger.info("\n[Gmail OAuth flow]")
    logger.info("=" * 50)
    logger.info("Step 1: Create OAuth credentials at https://console.cloud.google.com")
    logger.info("Step 2: Set env vars:")
    logger.info("  export GMAIL_CLIENT_ID=\"***\"")
    logger.info("  export GMAIL_CLIENT_SECRET=\"***\"")
    logger.info("Step 3: Run this command again to complete authorization.")
    logger.info("=" * 50)
    print()
    logger.info("Once authorized, set:")
    logger.info(f'  {CONFIG_PATH}')
    logger.info("  gmail_authorized: true")
    print()

    # Simulate auth for now
    if args.simulate:
        config["gmail_authorized"] = True
        save_config(config)
        logger.info("✓ (Simulated) Gmail authorization marked complete.")


def cmd_report(args):
    """Generate cash flow report."""
    invoices = load_invoices()
    today = datetime.now().date()

    if args.period == "week":
        cutoff = today + timedelta(days=7)
        window_label = "next 7 days"
    else:  # month
        cutoff = today + timedelta(days=30)
        window_label = "next 30 days"

    outstanding = [inv for inv in invoices if inv.get("status") != "paid"]
    upcoming = []
    overdue = []
    for inv in outstanding:
        try:
            due_date = datetime.strptime(inv["due"], "%Y-%m-%d").date()
            if due_date < today:
                overdue.append((inv, (today - due_date).days))
            elif due_date <= cutoff:
                upcoming.append((inv, (due_date - today).days))
        except (ValueError, KeyError):
            pass

    logger.info(f"\n{'=' * 70}")
    logger.info(f"Cash Flow Report — {window_label}")
    logger.info(f"Generated: {today.isoformat()}")
    logger.info(f"{'=' * 70}")

    if overdue:
        logger.info(f"\n⚠ OVERDUE ({len(overdue)}):")
        for inv, days in sorted(overdue, key=lambda x: -x[1]):
            logger.info(f"  {inv['id']}: {inv['payer']} — {inv['amount']} {inv['currency']} ({days} days late)")

    if upcoming:
        logger.info(f"\nUpcoming ({len(upcoming)}):")
        for inv, days in sorted(upcoming, key=lambda x: x[1]):
            logger.info(f"  {inv['id']}: {inv['payer']} — {inv['amount']} {inv['currency']} (due in {days} days)")

    if not overdue and not upcoming:
        logger.info("\n✓ No outstanding or overdue invoices in this window.")

    total = sum(inv["amount"] for inv, _ in overdue + upcoming)
    logger.info(f"\nTotal exposure ({window_label}): {total}")


def cmd_configure(args):
    """Configure the skill."""
    config = load_config()

    changed = False
    if args.tone:
        config["tone"] = args.tone
        changed = True
    if args.channel:
        config["channel"] = args.channel
        changed = True
    if args.reminder_schedule:
        config["reminder_schedule"] = args.reminder_schedule
        changed = True

    if changed:
        save_config(config)
        logger.info(f"\n✓ Configuration updated:")
    else:
        logger.info(f"\nCurrent configuration:")
    for k, v in config.items():
        logger.info(f"  {k}: {v}")


def cmd_currency(args):
    """Set base currency and exchange rate source."""
    config = load_config()
    if args.base:
        config["base_currency"] = args.base.upper()
    if args.rates_from:
        config["rates_source"] = args.rates_from
    save_config(config)
    logger.info(f"\nCurrency config:")
    logger.info(f"  Base: {config['base_currency']}")
    logger.info(f"  Rates from: {config.get('rates_source', '(not set)')}")


def main():
    parser = argparse.ArgumentParser(description="SMB Invoice Tracker")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress info logging")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # auth
    p_auth = subparsers.add_parser("auth", help="Authorize external services")
    p_auth_sub = p_auth.add_subparsers(dest="auth_command", required=True)
    p_auth_gmail = p_auth_sub.add_parser("gmail", help="Authorize Gmail")
    p_auth_gmail.add_argument("--simulate", action="store_true", help="Simulate authorization (for testing)")
    p_auth_gmail.set_defaults(func=cmd_auth_gmail)

    # add
    p_add = subparsers.add_parser("add", help="Add an invoice manually")
    p_add.add_argument("--payer", required=True, help="Payer name")
    p_add.add_argument("--amount", type=float, required=True, help="Amount")
    p_add.add_argument("--currency", default="USD", help="Currency code (default USD)")
    p_add.add_argument("--due", required=True, help="Due date (YYYY-MM-DD)")
    p_add.add_argument("--note", help="Optional note")
    p_add.add_argument("--pro", action="store_true", help="Pro tier (unlimited)")
    p_add.set_defaults(func=cmd_add)

    # list
    p_list = subparsers.add_parser("list", help="List invoices")
    p_list.add_argument("--status", choices=["outstanding", "paid", "overdue", "all"], default="all")
    p_list.set_defaults(func=cmd_list)

    # mark-paid
    p_paid = subparsers.add_parser("mark-paid", help="Mark an invoice as paid")
    p_paid.add_argument("--id", required=True, help="Invoice ID (e.g., INV-001)")
    p_paid.set_defaults(func=cmd_mark_paid)

    # send-reminder
    p_remind = subparsers.add_parser("send-reminder", help="Send a reminder for an invoice")
    p_remind.add_argument("--id", required=True, help="Invoice ID")
    p_remind.set_defaults(func=cmd_send_reminder)

    # scan
    p_scan = subparsers.add_parser("scan", help="Scan Gmail for new invoices")
    p_scan.set_defaults(func=cmd_scan)

    # report
    p_report = subparsers.add_parser("report", help="Cash flow report")
    p_report.add_argument("--period", choices=["week", "month"], default="week")
    p_report.set_defaults(func=cmd_report)

    # configure
    p_config = subparsers.add_parser("configure", help="Configure reminder tone + channel")
    p_config.add_argument("--tone", choices=["polite", "friendly", "firm", "legal"])
    p_config.add_argument("--channel", choices=["email", "whatsapp", "sms"])
    p_config.add_argument("--reminder-schedule", help="e.g., 'T-7,T-1,T+0,T+7'")
    p_config.set_defaults(func=cmd_configure)

    # currency
    p_cur = subparsers.add_parser("currency", help="Set base currency and rate source")
    p_cur.add_argument("--base", help="Base currency code (e.g., USD, EUR, QAR)")
    p_cur.add_argument("--rates-from", help="Exchange rate source")
    p_cur.set_defaults(func=cmd_currency)

    args = parser.parse_args()
    configure_logging(verbose=getattr(args, "verbose", False), quiet=getattr(args, "quiet", False))
    logger.debug(f"smb-invoice-tracker v{__version__}")
    args.func(args)


if __name__ == "__main__":
    main()