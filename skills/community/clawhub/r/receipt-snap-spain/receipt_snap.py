#!/usr/bin/env python3
"""
Receipt Snap - Process receipts for Spanish tax reporting.

SETUP:
  1. Create a Google Drive folder for receipts
  2. Create a Google Sheet with a "log" tab and header row
  3. Set environment variables (see .env.example):
     - RECEIPT_DRIVE_FOLDER_ID
     - RECEIPT_GOOGLE_SHEET_ID
     - RECEIPT_LOG_FILE (optional, defaults to ~/receipts/log.csv)

QUICK START:
  # Set env vars (or copy .env.example to .env and fill in)
  export RECEIPT_DRIVE_FOLDER_ID="your-folder-id"
  export RECEIPT_GOOGLE_SHEET_ID="your-sheet-id"

  # Process a receipt
  python3 receipt_snap.py process receipt.pdf \
    --vendor "Adobe Systems" \
    --date 2026-02-16 \
    --amount 15.12 \
    --currency EUR \
    --category "Software y suscripciones"

  # Check summary
  python3 receipt_snap.py summary
"""

import argparse
import json
import os
import sys
import urllib.request
import subprocess
import re

# ============================================================
# CONFIG — Set via environment variables (see .env.example)
# Never hardcode IDs in this file
# ============================================================
DRIVE_FOLDER_ID = os.environ.get("RECEIPT_DRIVE_FOLDER_ID", "")
GOOGLE_SHEET_ID = os.environ.get("RECEIPT_GOOGLE_SHEET_ID", "")
LOG_FILE = os.environ.get("RECEIPT_LOG_FILE", os.path.expanduser("~/receipts/log.csv"))
# ============================================================

CATEGORIES = [
    "Software y suscripciones",
    "Telecomunicaciones",
    "Combustibles",
    "Viajes y desplazamientos",
    "Manutención y restauración",
    "Material informático",
    "Formación",
    "Otros gastos"
]


def get_exchange_rate(from_currency="USD"):
    """Fetch exchange rate from open.er-api.com"""
    if from_currency == "EUR":
        return 1.0
    try:
        url = f"https://open.er-api.com/v6/latest/{from_currency}"
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read())
            return data["rates"].get("EUR", 1.0)
    except Exception as e:
        print(f"Warning: Could not fetch exchange rate: {e}", file=sys.stderr)
        return None


def sanitize_filename(name):
    """Remove special chars for safe filename"""
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '-', name)
    return name.strip('-_')


def upload_to_drive(file_path):
    """Upload file to Google Drive folder"""
    if not DRIVE_FOLDER_ID:
        print("Error: Set RECEIPT_DRIVE_FOLDER_ID env var before uploading", file=sys.stderr)
        return None

    filename = os.path.basename(file_path)
    result = subprocess.run(
        ["gog", "drive", "upload", file_path, "--parent", DRIVE_FOLDER_ID],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error uploading: {result.stderr}", file=sys.stderr)
        return None

    for line in result.stdout.split('\n'):
        if line.startswith('id\t'):
            file_id = line.split('\t')[1]
            return file_id
    return None


def rename_in_drive(file_id, new_name):
    """Rename file in Google Drive"""
    result = subprocess.run(
        ["gog", "drive", "rename", file_id, new_name],
        capture_output=True, text=True
    )
    return result.returncode == 0


def append_to_sheet(row_data):
    """Append row to Google Sheet"""
    if not GOOGLE_SHEET_ID:
        print("Error: Set RECEIPT_GOOGLE_SHEET_ID env var before logging to Sheets", file=sys.stderr)
        return False

    values_json = json.dumps([[str(x) for x in row_data]])
    result = subprocess.run(
        ["gog", "sheets", "append", GOOGLE_SHEET_ID, "log!A:J",
         "--values-json", values_json, "--insert", "INSERT_ROWS"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error appending to sheet: {result.stderr}", file=sys.stderr)
        return False
    return True


def append_to_log(row_data):
    """Append row to local CSV log"""
    import csv as csv_module
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    header = ["Date", "Vendor", "Description", "Original Amount", "Currency",
              "EUR Amount", "Exchange Rate", "Category", "Drive Link", "Notes"]

    write_header = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv_module.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow([str(x) for x in row_data])

    return True


def cmd_process(args):
    """Process a receipt"""
    rate = 1.0
    if args.currency.upper() != "EUR":
        rate = get_exchange_rate(args.currency)
        if rate is None:
            print("Error: Could not get exchange rate", file=sys.stderr)
            sys.exit(1)

    eur_amount = round(float(args.amount) * rate, 2)

    ext = os.path.splitext(args.file)[1] if args.file else ".pdf"
    if not ext:
        ext = ".pdf"
    filename = f"{sanitize_filename(args.vendor)}_{args.date}_{eur_amount}EUR{ext}"

    link = "N/A"
    if args.file and os.path.exists(args.file):
        if DRIVE_FOLDER_ID:
            file_id = upload_to_drive(args.file)
            if file_id:
                rename_in_drive(file_id, filename)
                link = f"https://drive.google.com/file/d/{file_id}/view"
        else:
            print("Warning: RECEIPT_DRIVE_FOLDER_ID not set — skipping Drive upload")

    row = [
        args.date,
        args.vendor,
        args.description or "",
        args.amount,
        args.currency.upper(),
        eur_amount,
        rate,
        args.category,
        link,
        args.notes or ""
    ]

    append_to_log(row)

    if GOOGLE_SHEET_ID:
        append_to_sheet(row)

    print(f"✅ Processed: {args.vendor} — €{eur_amount}")
    print(f"   Category: {args.category}")
    if link != "N/A":
        print(f"   Drive: {link}")


def cmd_summary(args):
    """Show receipt summary"""
    if not os.path.exists(LOG_FILE):
        print("No receipts logged yet.")
        return

    import csv
    total = 0
    by_category = {}

    with open(LOG_FILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            eur = float(row.get("EUR Amount", 0))
            total += eur
            cat = row.get("Category", "Other")
            by_category[cat] = by_category.get(cat, 0) + eur

    print(f"\n📊 Receipt Summary")
    print(f"   Total: €{total:.2f}")
    print(f"\nBy Category:")
    for cat, amt in sorted(by_category.items(), key=lambda x: -x[1]):
        print(f"   {cat}: €{amt:.2f}")


def cmd_exchange_rate(args):
    """Show current exchange rate"""
    rate = get_exchange_rate("USD")
    print(f"1 USD = {rate:.6f} EUR")


def main():
    parser = argparse.ArgumentParser(description="Receipt Snap — Spanish expense tracker")
    sub = parser.add_subparsers(dest="command")

    p_process = sub.add_parser("process")
    p_process.add_argument("file", nargs="?", help="Receipt file path")
    p_process.add_argument("--vendor", required=True, help="Vendor name")
    p_process.add_argument("--date", required=True, help="Date YYYY-MM-DD")
    p_process.add_argument("--amount", required=True, help="Amount")
    p_process.add_argument("--currency", default="EUR", help="Currency (default: EUR)")
    p_process.add_argument("--category", required=True, help=f"Category: {', '.join(CATEGORIES)}")
    p_process.add_argument("--description", help="Description")
    p_process.add_argument("--notes", help="Notes")

    sub.add_parser("summary")
    sub.add_parser("exchange-rate")

    args = parser.parse_args()

    if args.command == "process":
        cmd_process(args)
    elif args.command == "summary":
        cmd_summary(args)
    elif args.command == "exchange-rate":
        cmd_exchange_rate(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
