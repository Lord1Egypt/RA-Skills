#!/usr/bin/env bash
# Read monthly summary totals from Dontedit without touching ledger rows.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/expense_lib.sh"

target_month=""

while (($#)); do
  case "$1" in
    --month)
      target_month="${2:-}"
      shift 2
      ;;
    *)
      if [[ -z "$target_month" ]]; then
        target_month="$1"
      fi
      shift
      ;;
  esac
done

if [[ -z "$target_month" ]]; then
  target_month="$(date +%Y-%m)"
fi

month_key="$(python3 - "$target_month" <<'PY'
import sys
from datetime import datetime

raw = sys.argv[1].strip()
formats = ("%Y-%m", "%Y%m", "%b %Y", "%B %Y")
for fmt in formats:
    try:
        print(datetime.strptime(raw, fmt).strftime("%Y%m"))
        raise SystemExit(0)
    except ValueError:
        pass
print(raw.replace("-", ""))
PY
)"

TOKEN_LOCAL="$TOKEN"
summary_json="$(
  curl -sf \
    -H "Authorization: Bearer ${TOKEN_LOCAL}" \
    "https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/Dontedit%21C6%3AG200"
)"

SUMMARY_JSON="$summary_json" python3 - "$month_key" <<'PY'
import json
import os
import sys

month_key = sys.argv[1].strip()
rows = json.loads(os.environ["SUMMARY_JSON"]).get("values", [])

for row in rows:
    padded = list(row) + [""] * (5 - len(row))
    helper_key = str(padded[0]).strip()
    if helper_key != month_key:
        continue
    print(json.dumps({
        "monthKey": helper_key,
        "monthLabel": str(padded[1]).strip(),
        "income": str(padded[2]).strip(),
        "spending": str(padded[3]).strip(),
        "savings": str(padded[4]).strip() if len(padded) > 4 else ""
    }, ensure_ascii=False))
    raise SystemExit(0)

print("[]")
PY
