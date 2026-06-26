#!/usr/bin/env bash
# Read-only recurring query helper.
# Usage:
#   find_recurring.sh [query]
#   find_recurring.sh --query capcut --date 2026-03-28
#   find_recurring.sh --query capcut --mode next
#   find_recurring.sh --month 2026-03
set -euo pipefail

QUERY=""
TARGET_DATE="$(date +%F)"
TARGET_MONTH=""
MODE="month"
LIMIT="20"

while (($#)); do
  case "$1" in
    --query)
      QUERY="${2:-}"
      shift 2
      ;;
    --date)
      TARGET_DATE="${2:-}"
      shift 2
      ;;
    --month)
      TARGET_MONTH="${2:-}"
      shift 2
      ;;
    --mode)
      MODE="${2:-month}"
      shift 2
      ;;
    --limit)
      LIMIT="${2:-20}"
      shift 2
      ;;
    *)
      if [[ -z "$QUERY" ]]; then
        QUERY="$1"
      fi
      shift
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=./expense_lib.sh
source "$SCRIPT_DIR/expense_lib.sh"

DATA="$(fetch_recurring_values)"

RECURRING_JSON="$DATA" python3 - "$QUERY" "$TARGET_DATE" "$TARGET_MONTH" "$MODE" "$LIMIT" <<'PY'
import json
import os
import sys
from datetime import date, datetime

query = sys.argv[1].strip().lower()
target_date = datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
target_month_raw = sys.argv[3].strip()
mode = sys.argv[4].strip().lower() or "month"
limit = int(sys.argv[5])

if target_month_raw:
    target_month_start = datetime.strptime(target_month_raw + "-01", "%Y-%m-%d").date()
else:
    target_month_start = target_date.replace(day=1)

def month_end(dt):
    if dt.month == 12:
        return date(dt.year + 1, 1, 1).replace(day=1).fromordinal(date(dt.year + 1, 1, 1).toordinal() - 1)
    return date(dt.year, dt.month + 1, 1).fromordinal(date(dt.year, dt.month + 1, 1).toordinal() - 1)

target_month_end = month_end(target_month_start)

payload = json.loads(os.environ["RECURRING_JSON"])
rows = payload.get("values", [])

def normalize(text):
    return "".join(ch.lower() if ch.isalnum() or ch.isspace() else " " for ch in str(text or "")).strip()

def token_match(needle, *haystacks):
    needle = normalize(needle)
    if not needle:
        return True
    haystack = " ".join(normalize(item) for item in haystacks)
    return all(tok in haystack for tok in needle.split() if tok)

def parse_amount(raw):
    text = str(raw or "").strip().replace("€", "").replace("$", "").replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None

def parse_bool(raw):
    return str(raw).strip().upper() == "TRUE"

def parse_date(raw):
    text = str(raw or "").strip()
    if not text:
        return None
    for fmt in ("%d-%b-%Y", "%m/%d/%Y", "%d %b %Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    return None

def add_months(dt, months, original_day):
    year = dt.year + ((dt.month - 1 + months) // 12)
    month = ((dt.month - 1 + months) % 12) + 1
    last_day = [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]
    return date(year, month, min(original_day, last_day))

def advance_cycle(current, freq, original_day):
    freq = (freq or "Monthly").lower()
    if "quarterly" in freq:
        return add_months(current, 3, original_day)
    if "yearly" in freq or "annual" in freq:
        try:
            return current.replace(year=current.year + 1)
        except ValueError:
            return current.replace(year=current.year + 1, day=28)
    return add_months(current, 1, original_day)

def cycle_for_month(start_date, end_date, frequency, target_month_start):
    original_day = start_date.day
    current = start_date
    while current < target_month_start:
        current = advance_cycle(current, frequency, original_day)
    if current.month != target_month_start.month or current.year != target_month_start.year:
        return None
    if end_date and current > end_date:
        return None
    return current

def next_cycle_from(start_date, end_date, frequency, target_date):
    original_day = start_date.day
    current = start_date
    while current < target_date:
        current = advance_cycle(current, frequency, original_day)
    if end_date and current > end_date:
        return None
    return current

results = []
for idx, row in enumerate(rows):
    padded = row + [""] * (12 - len(row))
    recurring_id = str(padded[0] or "").strip()
    start_date = parse_date(padded[1])
    name = str(padded[2] or "").strip()
    category = str(padded[3] or "").strip()
    item_type = "expense" if parse_bool(padded[4]) else "income"
    frequency = str(padded[5] or "Monthly").strip()
    amount_raw = str(padded[6] or "").strip()
    amount = parse_amount(amount_raw)
    account = str(padded[7] or "").strip() or "Other"
    end_date = parse_date(padded[8])
    notes = str(padded[10] or "").strip()
    source = str(padded[11] or "").strip()

    if not recurring_id or not name or not start_date or amount is None or amount <= 0:
        continue
    if not token_match(query, recurring_id, name, category, account, notes, source, frequency):
        continue

    if mode == "next":
        cycle_date = next_cycle_from(start_date, end_date, frequency, target_date)
    else:
        cycle_date = cycle_for_month(start_date, end_date, frequency, target_month_start)

    if cycle_date is None:
        continue

    results.append({
        "rowNumber": idx + 6,
        "recurringId": recurring_id,
        "name": name,
        "category": category,
        "type": item_type,
        "frequency": frequency,
        "amount": amount_raw,
        "account": account,
        "source": source,
        "notes": notes,
        "startDate": start_date.isoformat(),
        "endDate": end_date.isoformat() if end_date else "",
        "cycleDate": cycle_date.isoformat(),
        "isDue": cycle_date <= target_date,
    })

results.sort(key=lambda item: (item["cycleDate"], item["name"]))
print(json.dumps(results[:limit], ensure_ascii=True))
PY
