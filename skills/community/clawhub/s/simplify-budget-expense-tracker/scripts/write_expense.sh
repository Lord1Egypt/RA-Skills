#!/usr/bin/env bash
# Writes a new expense row to the Expenses sheet
# Usage: write_expense.sh --amount <amount> --description <description> --category <category_name> --date <YYYY-MM-DD> [--account <account>] [--notes <notes>]
set -euo pipefail

AMOUNT=""
DESCRIPTION=""
CATEGORY_INPUT=""
DATE_INPUT=""
ACCOUNT="Revolut"
NOTES=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --amount)     AMOUNT="$2";         shift 2 ;;
    --description) DESCRIPTION="$2";  shift 2 ;;
    --category)   CATEGORY_INPUT="$2"; shift 2 ;;
    --date)       DATE_INPUT="$2";     shift 2 ;;
    --account)    ACCOUNT="$2";        shift 2 ;;
    --notes)      NOTES="$2";          shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$AMOUNT" || -z "$DESCRIPTION" || -z "$CATEGORY_INPUT" || -z "$DATE_INPUT" ]]; then
  echo "Usage: write_expense.sh --amount <amount> --description <desc> --category <category> --date <YYYY-MM-DD> [--account <account>] [--notes <notes>]" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=./expense_lib.sh
source "$SCRIPT_DIR/expense_lib.sh"

python3 - "$DATE_INPUT" <<'PY'
import sys
from datetime import datetime
datetime.strptime(sys.argv[1].strip(), "%Y-%m-%d")
PY

CATEGORY_RESULT="$(resolve_category_name "$CATEGORY_INPUT")"
CATEGORY_FORMULA="$(echo "$CATEGORY_RESULT" | jq -r '.formula')"
CATEGORY_DISPLAY="$(echo "$CATEGORY_RESULT" | jq -r '.display')"
CATEGORY_FALLBACK="$(echo "$CATEGORY_RESULT" | jq -r '.fallback // false')"

AMOUNT_JSON="$(resolve_amount_and_notes_json "$AMOUNT" "$NOTES")"
AMOUNT_VALUE="$(echo "$AMOUNT_JSON" | jq -r '.amount')"
NOTES="$(echo "$AMOUNT_JSON" | jq -r '.notes')"
TRACKER_SYMBOL="$(echo "$AMOUNT_JSON" | jq -r '.trackerCurrencySymbol')"

TIMESTAMP_MS=$(python3 -c "import time; print(int(time.time() * 1000))")
RANDOM_SUFFIX=$(python3 -c "import random, string; print(''.join(random.choices(string.ascii_lowercase + string.digits, k=5)))")
TRANSACTION_ID="ex-${TIMESTAMP_MS}-${RANDOM_SUFFIX}"

FORMATTED_DATE="$(iso_to_sheet_display "$DATE_INPUT")"
DISPLAY_DATE="$(iso_to_income_display "$DATE_INPUT")"
TARGET_ROW="$(find_next_expense_append_row)"

BODY=$(jq -n \
  --arg tid "$TRANSACTION_ID" \
  --arg dt "$FORMATTED_DATE" \
  --argjson amt "$AMOUNT_VALUE" \
  --arg cat "$CATEGORY_FORMULA" \
  --arg desc "$DESCRIPTION" \
  --arg notes "$NOTES" \
  --arg acc "$ACCOUNT" \
  '{"values": [[($tid), ($dt), ($amt), ($cat), ($desc), "🤖", ($notes), ($acc)]]}')

curl -sf -X PUT \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/Expenses%21D${TARGET_ROW}%3AK${TARGET_ROW}?valueInputOption=USER_ENTERED" \
  -d "$BODY" > /dev/null

ROW_JSON="$(find_expense_row_json "$TRANSACTION_ID")" || {
  curl -sf -X POST \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    "https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/Expenses%21D${TARGET_ROW}%3AK${TARGET_ROW}:clear" \
    -d '{}' > /dev/null || true
  echo "Error: expense write verification failed for transaction ${TRANSACTION_ID}" >&2
  exit 1
}

VERIFIED_ROW="$(echo "$ROW_JSON" | jq -r '.rowNumber')"
VERIFIED_DATE="$(echo "$ROW_JSON" | jq -r '.dateIso')"
VERIFIED_CATEGORY="$(echo "$ROW_JSON" | jq -r '.category')"
VERIFIED_DESCRIPTION="$(echo "$ROW_JSON" | jq -r '.description')"
VERIFIED_ACCOUNT="$(echo "$ROW_JSON" | jq -r '.account')"

if [[ "$VERIFIED_ROW" != "$TARGET_ROW" || -z "$VERIFIED_DATE" || -z "$VERIFIED_CATEGORY" || -z "$VERIFIED_DESCRIPTION" || -z "$VERIFIED_ACCOUNT" ]]; then
  curl -sf -X POST \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    "https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/Expenses%21D${TARGET_ROW}%3AK${TARGET_ROW}:clear" \
    -d '{}' > /dev/null || true
  echo "Error: expense write verification failed for transaction ${TRANSACTION_ID}" >&2
  exit 1
fi

update_master_timestamp

DISPLAY_AMOUNT="${TRACKER_SYMBOL}${AMOUNT_VALUE}"

if [ "$CATEGORY_FALLBACK" = "true" ]; then
  echo "REPLY: ✅ ${DESCRIPTION} — ${DISPLAY_AMOUNT} under ${CATEGORY_DISPLAY} on ${DISPLAY_DATE} (${ACCOUNT}) [category '${CATEGORY_INPUT}' not recognised, used Other]"
else
  echo "REPLY: ✅ ${DESCRIPTION} — ${DISPLAY_AMOUNT} under ${CATEGORY_DISPLAY} on ${DISPLAY_DATE} (${ACCOUNT})"
fi
