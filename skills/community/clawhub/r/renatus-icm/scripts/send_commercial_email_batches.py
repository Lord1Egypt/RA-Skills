#!/usr/bin/env python3
"""
send_commercial_email_batches.py

Send commercial email to leads in batches with resume capability.
Supports gws and gog CLI. Reads config from config.json (or env / defaults).

Usage:
  # With config.json (auto-loaded from ../config.json or ./config.json)
  python3 scripts/send_commercial_email_batches.py --send

  # Override with CLI flags or env vars
  python3 scripts/send_commercial_email_batches.py --provider gog --account my@gmail.com --send

  # Dry run
  python3 scripts/send_commercial_email_batches.py --dry-run
"""
from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from shutil import which

# ----------------------------------------------------------------------
# Config — import with graceful fallback
# ----------------------------------------------------------------------
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from config_loader import load_config
    _cfg = load_config()
except Exception:
    _cfg = {}

WORKSPACE      = Path(os.environ.get("WORKSPACE", "/home/umbrel/.openclaw/workspace"))
DEFAULT_LOG    = str(WORKSPACE / "logs/email_send_log.json")
DEFAULT_CSV    = str(WORKSPACE / "renatus_leads.csv")


def _cfg_get(key: str, fallback: str = "") -> str:
    v = _cfg.get(key, "") if isinstance(_cfg, dict) else ""
    return v if v and v != "YOUR_" + key.partition("_")[2] else fallback


def _default_provider() -> str:
    for exe in ("gws", "gog"):
        if which(exe):
            return exe
    return "gws"


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def ensure_dir(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def load_sent_log(log_path: str) -> set[str]:
    if not Path(log_path).exists():
        return set()
    try:
        with open(log_path) as f:
            return set(json.load(f).get("sent", []))
    except Exception:
        return set()


def save_sent_log(log_path: str, sent_emails: set[str], stats: dict) -> None:
    data = {
        "sent": list(sent_emails),
        "stats": stats,
        "last_updated": datetime.now().isoformat(),
    }
    ensure_dir(log_path)
    with open(log_path, "w") as f:
        json.dump(data, f, indent=2)


def load_template(template_path: str) -> str:
    p = Path(template_path)
    if p.exists():
        return p.read_text(encoding="utf-8")
    # Try relative to this script
    local = Path(__file__).parent.parent / "assets" / "email" / "commercial-core-day1.html"
    if local.exists():
        return local.read_text(encoding="utf-8")
    raise FileNotFoundError(
        f"Email template not found at {template_path}. "
        "Use --template or set RENATUS_TEMPLATE env var."
    )


def encode_unsubscribe_url(email: str, base_url: str = "https://YOUR_DOMAIN/unsubscribe.html") -> str:
    encoded = base64.urlsafe_b64encode(email.encode()).decode().rstrip("=")
    return f"{base_url}?e={encoded}"


def personalize_email(html: str, email: str, base_url: str = "https://YOUR_DOMAIN/unsubscribe.html") -> str:
    unsub_url = encode_unsubscribe_url(email, base_url)
    html = html.replace("{{recipient_email}}", unsub_url)
    html = html.replace("{{unsubscribe_url}}", unsub_url)
    return html


def get_leads(csv_path: str) -> list[dict]:
    leads = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("email") and "@" in row.get("email", ""):
                leads.append(row)
    return leads


def send_gws(to: str, subject: str, html_body: str) -> tuple[bool, str]:
    cmd = ["gws", "gmail", "+send", "--to", to, "--subject", subject, "--body", html_body, "--html"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        return False, "Timeout (30s)"
    except FileNotFoundError:
        return False, "gws not found in PATH"
    except Exception as e:
        return False, str(e)
    if result.returncode == 0:
        return True, ""
    return False, (result.stderr or result.stdout or "Unknown error").strip()


def send_gog(to: str, subject: str, html_body: str, account: str) -> tuple[bool, str]:
    cmd = ["gog", "gmail", "send", "--account", account, "--to", to, "--subject", subject, "--body-html", html_body]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        return False, "Timeout (30s)"
    except FileNotFoundError:
        return False, "gog not found in PATH"
    except Exception as e:
        return False, str(e)
    if result.returncode == 0:
        return True, ""
    return False, (result.stderr or result.stdout or "Unknown error").strip()


def send_email(provider: str, to: str, subject: str, html_body: str, account: str = "") -> tuple[bool, str]:
    if provider == "gog":
        if not account:
            return False, "gog requires --account"
        return send_gog(to, subject, html_body, account)
    return send_gws(to, subject, html_body)


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Send commercial email to leads in batches. "
        "Supports gws (default) and gog. Config loaded from config.json automatically."
    )
    ap.add_argument("--csv", default=os.environ.get("RENATUS_LEADS_CSV", DEFAULT_CSV))
    ap.add_argument("--template", default=os.environ.get("RENATUS_TEMPLATE",
        _cfg.get("template_path", "email/commercial-core-day1.html")))
    ap.add_argument("--log", default=os.environ.get("EMAIL_SEND_LOG", DEFAULT_LOG))
    ap.add_argument("--subject", default=os.environ.get("RENATUS_SUBJECT",
        _cfg.get("subject", "Free Real Estate Training")))
    ap.add_argument("--unsub-url", dest="unsub_url",
        default=os.environ.get("RENATUS_UNSUB_URL",
            _cfg.get("unsub_url", "https://YOUR_DOMAIN/unsubscribe.html")),
        help="Base URL for unsubscribe link")
    ap.add_argument("--provider", choices=["gws", "gog", "auto"], default="auto")
    ap.add_argument("--account", default=os.environ.get("RENATUS_SENDER",
        _cfg.get("sender", "YOUR_SENDER@gmail.com")),
        help="Gmail account (for gog)")
    ap.add_argument("--batch-size", type=int, default=20)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--send", action="store_true",
        help="Actually send emails (without this flag, only dry-run preview runs)")
    ap.add_argument("--delay", type=float, default=2.0)
    ap.add_argument("--skip-sent", action="store_true", default=True)
    ap.add_argument("--no-skip-sent", dest="skip_sent", action="store_false")
    return ap.parse_args()


def main() -> int:
    args = parse_args()

    if not args.send and not args.dry_run:
        print("No action. Use --dry-run to preview or --send to actually send.")
        return 1

    if args.provider == "auto":
        provider = _default_provider()
        print(f"Auto-detected provider: {provider}")
    else:
        provider = args.provider

    if not which(provider):
        print(f"ERROR: {provider} not found. Install it or use --provider gws/gog.", file=sys.stderr)
        return 1

    if not Path(args.csv).exists():
        print(f"ERROR: CSV not found: {args.csv}", file=sys.stderr)
        print("  Run: python3 scripts/renatus_leads.py --export  to download leads first.")
        return 1

    try:
        template = load_template(args.template)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    leads = get_leads(args.csv)
    total_leads = len(leads)
    print(f"Provider: {provider}")
    print(f"Template: {args.template}")
    print(f"CSV: {args.csv} ({total_leads} leads)")

    sent_emails = load_sent_log(args.log) if args.skip_sent else set()
    if sent_emails:
        print(f"Already sent: {len(sent_emails)} (will skip)")

    batch = leads[args.start: args.start + args.batch_size]
    if not batch:
        print(f"No leads in batch starting at {args.start}")
        return 0

    print(f"\nBatch: {args.start + 1}–{min(args.start + args.batch_size, total_leads)} of {total_leads}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'SEND'}")
    print("-" * 60)

    sent_count = failed_count = skipped_count = 0

    for i, lead in enumerate(batch, args.start + 1):
        email = lead.get("email", "").strip()
        name = lead.get("name", "").strip()

        if not email or "@" not in email:
            print(f"[{i}/{total_leads}] SKIP (no valid email): {name}")
            skipped_count += 1
            continue
        if email in sent_emails:
            print(f"[{i}/{total_leads}] ⏭ SKIP (already sent): {email}")
            skipped_count += 1
            continue

        print(f"[{i}/{total_leads}] {'[DRY RUN] Would send to' if args.dry_run else 'Sending to'}: {name} <{email}>", end=" ")

        if args.dry_run:
            unsub_preview = encode_unsubscribe_url(email, args.unsub_url)[:60] + "..."
            print(f"\n    subject: {args.subject}")
            print(f"    unsub:   {unsub_preview}")
            continue

        html = personalize_email(template, email, args.unsub_url)
        ok, err = send_email(provider, email, args.subject, html, args.account)

        if ok:
            print("✓")
            sent_emails.add(email)
            sent_count += 1
            save_sent_log(args.log, sent_emails, {
                "total": total_leads, "sent": len(sent_emails),
                "last_batch_start": args.start, "provider": provider,
                "last_updated": datetime.now().isoformat(),
            })
        else:
            print(f"✗ FAIL: {err[:80]}")
            failed_count += 1

        if i < args.start + len(batch):
            time.sleep(args.delay)

    print("-" * 60)
    print(f"\nSent: {sent_count}  Failed: {failed_count}  Skipped: {skipped_count}")
    print(f"Total sent (all): {len(sent_emails)}/{total_leads}")

    next_start = args.start + args.batch_size
    if next_start < total_leads:
        print(f"\nNext: python3 scripts/send_commercial_email_batches.py --start {next_start} --batch-size {args.batch_size} --send")
    else:
        print("\n=== COMPLETE ===")
    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
