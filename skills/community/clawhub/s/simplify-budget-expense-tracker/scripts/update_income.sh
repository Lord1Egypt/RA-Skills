#!/usr/bin/env bash
# Updates an existing income row by transaction ID.
# Use __KEEP__ to preserve the current value and __CLEAR__ to blank notes.
# Usage: update_income.sh <transaction_id> <amount|amount with currency|__KEEP__> <name|__KEEP__> <YYYY-MM-DD|__KEEP__> [account|__KEEP__] [source|__KEEP__] [notes|__KEEP__|__CLEAR__]
set -euo pipefail

if [ "$#" -lt 4 ]; then
  echo "Usage: update_income.sh <transaction_id> <amount|amount with currency|__KEEP__> <name|__KEEP__> <YYYY-MM-DD|__KEEP__> [account|__KEEP__] [source|__KEEP__] [notes|__KEEP__|__CLEAR__]"
  exit 1
fi

TRANSACTION_ID="$1"
AMOUNT_INPUT="$2"
NAME_INPUT="$3"
DATE_INPUT="$4"
ACCOUNT_INPUT="${5:-__KEEP__}"
SOURCE_INPUT="${6:-__KEEP__}"
NOTES_INPUT="${7:-__KEEP__}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=./expense_lib.sh
source "$SCRIPT_DIR/expense_lib.sh"

ROW_JSON="$(find_income_row_json "$TRANSACTION_ID")" || {
  echo "Error: transaction ID $TRANSACTION_ID not found in sheet"
  exit 1
}

CURRENT_AMOUNT="$(echo "$ROW_JSON" | jq -r '.amountNumber // .amount')"
CURRENT_NAME="$(echo "$ROW_JSON" | jq -r '.name')"
CURRENT_DATE_ISO="$(echo "$ROW_JSON" | jq -r '.dateIso')"
CURRENT_ACCOUNT="$(echo "$ROW_JSON" | jq -r '.account')"
CURRENT_SOURCE="$(echo "$ROW_JSON" | jq -r '.source')"
CURRENT_NOTES="$(echo "$ROW_JSON" | jq -r '.notes')"
SHEET_ROW="$(echo "$ROW_JSON" | jq -r '.rowNumber')"

AMOUNT="$CURRENT_AMOUNT"
if [ "$AMOUNT_INPUT" != "__KEEP__" ]; then
  AMOUNT_JSON="$(resolve_amount_and_notes_json "$AMOUNT_INPUT" "$CURRENT_NOTES")"
  AMOUNT="$(echo "$AMOUNT_JSON" | jq -r '.amount')"
  CURRENT_NOTES="$(echo "$AMOUNT_JSON" | jq -r '.notes')"
fi

NAME="$CURRENT_NAME"
if [ "$NAME_INPUT" != "__KEEP__" ]; then
  NAME="$NAME_INPUT"
fi

DATE_ISO="$CURRENT_DATE_ISO"
if [ "$DATE_INPUT" != "__KEEP__" ]; then
  DATE_ISO="$DATE_INPUT"
fi

ACCOUNT="$CURRENT_ACCOUNT"
if [ "$ACCOUNT_INPUT" != "__KEEP__" ]; then
  ACCOUNT="$ACCOUNT_INPUT"
fi

SOURCE="$CURRENT_SOURCE"
if [ "$SOURCE_INPUT" != "__KEEP__" ]; then
  SOURCE="$SOURCE_INPUT"
fi

NOTES="$CURRENT_NOTES"
if [ "$NOTES_INPUT" = "__CLEAR__" ]; then
  NOTES=""
elif [ "$NOTES_INPUT" != "__KEEP__" ]; then
  NOTES="$NOTES_INPUT"
fi

python3 - "$AMOUNT" "$DATE_ISO" <<'PY'
import sys
from datetime import datetime

try:
    float(sys.argv[1].strip())
except ValueError:
    raise SystemExit("Error: amount must be numeric")

datetime.strptime(sys.argv[2].strip(), "%Y-%m-%d")
PY

FORMATTED_DATE="$(iso_to_income_display "$DATE_ISO")"

BODY=$(jq -n \
  --arg tid "$TRANSACTION_ID" \
  --arg dt "$FORMATTED_DATE" \
  --argjson amt "$AMOUNT" \
  --arg name "$NAME" \
  --arg acc "$ACCOUNT" \
  --arg src "$SOURCE" \
  --arg notes "$NOTES" \
  '{"values": [[($tid), ($dt), ($amt), ($name), ($acc), ($src), ($notes)]]}')

curl -sf -X PUT \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/Income%21D${SHEET_ROW}%3AJ${SHEET_ROW}?valueInputOption=RAW" \
  -d "$BODY" > /dev/null

update_master_timestamp

echo "Updated transaction ${TRANSACTION_ID} at row ${SHEET_ROW}"
echo "date=${FORMATTED_DATE}"
echo "notes=${NOTES}"
