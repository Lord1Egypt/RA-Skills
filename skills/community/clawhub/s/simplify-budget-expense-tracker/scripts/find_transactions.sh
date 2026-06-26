#!/usr/bin/env bash
# Finds live expense and income transactions across the ledger.
# Usage: find_transactions.sh [query] [limit]
#    or: find_transactions.sh --query coffee --date 2026-04-08 --limit 20
#    or: find_transactions.sh --month 2026-04 --type expense
set -euo pipefail

QUERY=""
LIMIT="20"
DATE_FILTER=""
MONTH_FILTER=""
TYPE_FILTER=""

while (($#)); do
  case "$1" in
    --query)
      QUERY="${2:-}"
      shift 2
      ;;
    --limit)
      LIMIT="${2:-20}"
      shift 2
      ;;
    --date)
      DATE_FILTER="${2:-}"
      shift 2
      ;;
    --month)
      MONTH_FILTER="${2:-}"
      shift 2
      ;;
    --type)
      TYPE_FILTER="${2:-}"
      shift 2
      ;;
    *)
      if [[ -z "$QUERY" ]]; then
        QUERY="$1"
      elif [[ "$LIMIT" == "20" ]]; then
        LIMIT="$1"
      fi
      shift
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=./expense_lib.sh
source "$SCRIPT_DIR/expense_lib.sh"

EXPENSES_JSON="$(fetch_expenses_values)"
INCOME_JSON="$(fetch_income_values)"

EXPENSES_JSON="$EXPENSES_JSON" INCOME_JSON="$INCOME_JSON" python3 - "$QUERY" "$LIMIT" "$DATE_FILTER" "$MONTH_FILTER" "$TYPE_FILTER" <<'PY'
import json
import os
import sys
from datetime import datetime

query = sys.argv[1].strip().lower()
limit = int(sys.argv[2])
date_filter = sys.argv[3].strip()
month_filter = sys.argv[4].strip()
type_filter = sys.argv[5].strip().lower()
expenses = json.loads(os.environ["EXPENSES_JSON"]).get("values", [])
income = json.loads(os.environ["INCOME_JSON"]).get("values", [])

def to_iso(raw):
    raw = (raw or "").strip()
    if not raw:
        return ""
    for fmt in ("%d-%b-%Y", "%m/%d/%Y", "%d %b %Y"):
        try:
            return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return raw

def normalize(raw):
    raw = (raw or "").strip().lower()
    return "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in raw)

def token_match(needle, *haystacks):
    needle = normalize(needle)
    if not needle:
        return True
    tokens = [tok for tok in needle.split() if tok]
    haystack = " ".join(normalize(item) for item in haystacks)
    return all(tok in haystack for tok in tokens)

def include_date(date_iso):
    if date_filter and date_iso != date_filter:
        return False
    if month_filter and not date_iso.startswith(month_filter):
        return False
    return True

results = []

if type_filter in ("", "expense", "expenses", "all"):
    for idx, row in enumerate(expenses):
        padded = row + [""] * (8 - len(row))
        if not padded[0]:
            continue
        date_iso = to_iso(padded[1])
        if not include_date(date_iso):
            continue
        record = {
            "type": "expense",
            "rowNumber": idx + 5,
            "transactionId": padded[0],
            "dateDisplay": padded[1],
            "dateIso": date_iso,
            "amount": padded[2],
            "category": padded[3],
            "name": padded[4],
            "label": padded[5],
            "notes": padded[6],
            "account": padded[7],
            "source": "",
        }
        if not token_match(query, *(str(v or "") for v in record.values())):
            continue
        results.append(record)

if type_filter in ("", "income", "incomes", "all"):
    for idx, row in enumerate(income):
        padded = row + [""] * (7 - len(row))
        if not padded[0]:
            continue
        date_iso = to_iso(padded[1])
        if not include_date(date_iso):
            continue
        record = {
            "type": "income",
            "rowNumber": idx + 5,
            "transactionId": padded[0],
            "dateDisplay": padded[1],
            "dateIso": date_iso,
            "amount": padded[2],
            "category": "",
            "name": padded[3],
            "label": "",
            "notes": padded[6],
            "account": padded[4],
            "source": padded[5],
        }
        if not token_match(query, *(str(v or "") for v in record.values())):
            continue
        results.append(record)

results.sort(key=lambda item: (item.get("dateIso") or "", item.get("transactionId") or ""), reverse=True)
print(json.dumps(results[:limit], ensure_ascii=True))
PY
