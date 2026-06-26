#!/usr/bin/env bash
# Finds income rows by matching query text or explicit filters across name, notes,
# source, account, amount, date, and transaction id.
# Usage: find_income.sh [query] [limit]
#    or: find_income.sh --query salary --date 2026-03-28 --amount 220 --limit 10
set -euo pipefail

QUERY=""
LIMIT="10"
DATE_FILTER=""
AMOUNT_FILTER=""
NAME_FILTER=""
NOTES_FILTER=""
ACCOUNT_FILTER=""
SOURCE_FILTER=""
TRANSACTION_FILTER=""

while (($#)); do
  case "$1" in
    --query)
      QUERY="${2:-}"
      shift 2
      ;;
    --limit)
      LIMIT="${2:-10}"
      shift 2
      ;;
    --date)
      DATE_FILTER="${2:-}"
      shift 2
      ;;
    --amount)
      AMOUNT_FILTER="${2:-}"
      shift 2
      ;;
    --name|--description)
      NAME_FILTER="${2:-}"
      shift 2
      ;;
    --notes|--note)
      NOTES_FILTER="${2:-}"
      shift 2
      ;;
    --account)
      ACCOUNT_FILTER="${2:-}"
      shift 2
      ;;
    --source)
      SOURCE_FILTER="${2:-}"
      shift 2
      ;;
    --transaction-id|--transaction_id|--id)
      TRANSACTION_FILTER="${2:-}"
      shift 2
      ;;
    *)
      if [[ -z "$QUERY" ]]; then
        QUERY="$1"
      elif [[ "$LIMIT" == "10" ]]; then
        LIMIT="$1"
      fi
      shift
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=./expense_lib.sh
source "$SCRIPT_DIR/expense_lib.sh"

DATA="$(fetch_income_values)"

python3 -c '
import json
import sys
from datetime import datetime

query = sys.argv[1].strip().lower()
limit = int(sys.argv[2])
date_filter = sys.argv[3].strip().lower()
amount_filter = sys.argv[4].strip().lower()
name_filter = sys.argv[5].strip().lower()
notes_filter = sys.argv[6].strip().lower()
account_filter = sys.argv[7].strip().lower()
source_filter = sys.argv[8].strip().lower()
transaction_filter = sys.argv[9].strip().lower()
payload = json.load(sys.stdin)
rows = payload.get("values", [])

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

def token_match(needle, haystack):
    needle = normalize(needle)
    haystack = normalize(haystack)
    if not needle:
        return True
    tokens = [tok for tok in needle.split() if tok]
    if not tokens:
        return True
    return all(tok in haystack for tok in tokens)

results = []
for idx, row in enumerate(rows):
    padded = row + [""] * (7 - len(row))
    if not padded[0]:
      continue
    record = {
        "rowNumber": idx + 5,
        "transactionId": padded[0],
        "dateDisplay": padded[1],
        "dateIso": to_iso(padded[1]),
        "amount": padded[2],
        "name": padded[3],
        "account": padded[4],
        "source": padded[5],
        "notes": padded[6],
    }
    haystack = " ".join(
        str(record[key] or "")
        for key in ("transactionId", "dateDisplay", "dateIso", "amount", "name", "account", "source", "notes")
    )
    if not token_match(query, haystack):
        continue
    if date_filter and not token_match(date_filter, record["dateIso"] + " " + record["dateDisplay"]):
        continue
    if amount_filter and not token_match(amount_filter, record["amount"]):
        continue
    if name_filter and not token_match(name_filter, record["name"]):
        continue
    if notes_filter and not token_match(notes_filter, record["notes"]):
        continue
    if account_filter and not token_match(account_filter, record["account"]):
        continue
    if source_filter and not token_match(source_filter, record["source"]):
        continue
    if transaction_filter and not token_match(transaction_filter, record["transactionId"]):
        continue
    results.append(record)

results = list(reversed(results))[:limit]
print(json.dumps(results, ensure_ascii=True))
' "$QUERY" "$LIMIT" "$DATE_FILTER" "$AMOUNT_FILTER" "$NAME_FILTER" "$NOTES_FILTER" "$ACCOUNT_FILTER" "$SOURCE_FILTER" "$TRANSACTION_FILTER" <<<"$DATA"
