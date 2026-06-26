#!/usr/bin/env bash
# Writes a new income row to the Income sheet
# Usage: write_income.sh <amount|amount with currency> <name> <YYYY-MM-DD> [account] [source] [notes]
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: write_income.sh <amount|amount with currency> <name> <YYYY-MM-DD> [account] [source] [notes]"
  exit 1
fi

AMOUNT="$1"
NAME="$2"
DATE_INPUT="$3"
ACCOUNT="${4:-Other}"
SOURCE="${5:-Other}"
NOTES="${6:-}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=./expense_lib.sh
source "$SCRIPT_DIR/expense_lib.sh"

python3 - "$DATE_INPUT" <<'PY'
import sys
from datetime import datetime

datetime.strptime(sys.argv[1].strip(), "%Y-%m-%d")
PY

AMOUNT_JSON="$(resolve_amount_and_notes_json "$AMOUNT" "$NOTES")"
AMOUNT="$(echo "$AMOUNT_JSON" | jq -r '.amount')"
NOTES="$(echo "$AMOUNT_JSON" | jq -r '.notes')"

TIMESTAMP_MS=$(python3 -c "import time; print(int(time.time() * 1000))")
TRANSACTION_ID="INC-${TIMESTAMP_MS}"
FORMATTED_DATE="$(iso_to_income_display "$DATE_INPUT")"

BODY=$(jq -n \
  --arg tid "$TRANSACTION_ID" \
  --arg dt "$FORMATTED_DATE" \
  --argjson amt "$AMOUNT" \
  --arg name "$NAME" \
  --arg acc "$ACCOUNT" \
  --arg src "$SOURCE" \
  --arg notes "$NOTES" \
  '{"values": [[($tid), ($dt), ($amt), ($name), ($acc), ($src), ($notes)]]}')

RESULT=$(curl -sf -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/Income%21D5%3AJ:append?valueInputOption=USER_ENTERED&insertDataOption=OVERWRITE" \
  -d "$BODY")

UPDATED_RANGE=$(echo "$RESULT" | jq -r '.updates.updatedRange // "unknown"')

update_master_timestamp

TRACKER_SYMBOL_VAL="$(echo "$AMOUNT_JSON" | jq -r '.trackerCurrencySymbol')"
DISPLAY_AMOUNT="${TRACKER_SYMBOL_VAL}${AMOUNT}"
DISPLAY_DATE="$(iso_to_income_display "$DATE_INPUT")"
echo "CONFIRM: Logged income ${NAME} — ${DISPLAY_AMOUNT} on ${DISPLAY_DATE} (${ACCOUNT})"
