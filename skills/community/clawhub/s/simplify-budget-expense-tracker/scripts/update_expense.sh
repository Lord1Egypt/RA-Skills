#!/usr/bin/env bash
# Updates an existing expense row by transaction ID.
# Use __KEEP__ to preserve a field, __CLEAR__ to blank notes.
# Usage: update_expense.sh --id <transaction_id> [--amount <amount|__KEEP__>] [--description <desc|__KEEP__>] [--category <name|__KEEP__>] [--date <YYYY-MM-DD|__KEEP__>] [--account <account|__KEEP__>] [--notes <notes|__KEEP__|__CLEAR__>]
set -euo pipefail

TRANSACTION_ID=""
AMOUNT_INPUT="__KEEP__"
DESCRIPTION_INPUT="__KEEP__"
CATEGORY_INPUT="__KEEP__"
DATE_INPUT="__KEEP__"
ACCOUNT_INPUT="__KEEP__"
NOTES_INPUT="__KEEP__"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --id)          TRANSACTION_ID="$2"; shift 2 ;;
    --amount)      AMOUNT_INPUT="$2";   shift 2 ;;
    --description) DESCRIPTION_INPUT="$2"; shift 2 ;;
    --category)    CATEGORY_INPUT="$2"; shift 2 ;;
    --date)        DATE_INPUT="$2";     shift 2 ;;
    --account)     ACCOUNT_INPUT="$2";  shift 2 ;;
    --notes)       NOTES_INPUT="$2";    shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$TRANSACTION_ID" ]]; then
  echo "Usage: update_expense.sh --id <transaction_id> [--amount ...] [--description ...] [--category ...] [--date ...] [--account ...] [--notes ...]" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=./expense_lib.sh
source "$SCRIPT_DIR/expense_lib.sh"

ROW_JSON="$(find_expense_row_json "$TRANSACTION_ID")" || {
  echo "Error: transaction ID $TRANSACTION_ID not found in sheet"
  exit 1
}

CURRENT_AMOUNT="$(echo "$ROW_JSON" | jq -r '.amountNumber // .amount')"
CURRENT_CATEGORY_FORMULA="$(echo "$ROW_JSON" | jq -r '.categoryFormula // .category')"
CURRENT_CATEGORY_DISPLAY="$(echo "$ROW_JSON" | jq -r '.category')"
CURRENT_DESCRIPTION="$(echo "$ROW_JSON" | jq -r '.description')"
CURRENT_DATE_ISO="$(echo "$ROW_JSON" | jq -r '.dateIso')"
CURRENT_LABEL="$(echo "$ROW_JSON" | jq -r '.label')"
CURRENT_NOTES="$(echo "$ROW_JSON" | jq -r '.notes')"
CURRENT_ACCOUNT="$(echo "$ROW_JSON" | jq -r '.account')"
SHEET_ROW="$(echo "$ROW_JSON" | jq -r '.rowNumber')"

AMOUNT="$CURRENT_AMOUNT"
CATEGORY="$CURRENT_CATEGORY_FORMULA"
CATEGORY_DISPLAY="$CURRENT_CATEGORY_DISPLAY"
DESCRIPTION="$CURRENT_DESCRIPTION"
DATE_ISO="$CURRENT_DATE_ISO"
ACCOUNT="$CURRENT_ACCOUNT"
NOTES="$CURRENT_NOTES"
TRACKER_SYMBOL="$TRACKER_CURRENCY_SYMBOL"

if [ "$CATEGORY_INPUT" != "__KEEP__" ]; then
  CATEGORY_RESULT="$(resolve_category_name "$CATEGORY_INPUT")"
  CATEGORY="$(echo "$CATEGORY_RESULT" | jq -r '.formula')"
  CATEGORY_DISPLAY="$(echo "$CATEGORY_RESULT" | jq -r '.display')"
fi

if [ "$DESCRIPTION_INPUT" != "__KEEP__" ]; then
  DESCRIPTION="$DESCRIPTION_INPUT"
fi

if [ "$DATE_INPUT" != "__KEEP__" ]; then
  DATE_ISO="$DATE_INPUT"
fi

if [ "$ACCOUNT_INPUT" != "__KEEP__" ]; then
  ACCOUNT="$ACCOUNT_INPUT"
fi

if [ "$NOTES_INPUT" = "__CLEAR__" ]; then
  NOTES=""
elif [ "$NOTES_INPUT" != "__KEEP__" ]; then
  NOTES="$NOTES_INPUT"
fi

if [ "$AMOUNT_INPUT" != "__KEEP__" ]; then
  AMOUNT_JSON="$(resolve_amount_and_notes_json "$AMOUNT_INPUT" "$NOTES")"
  AMOUNT="$(echo "$AMOUNT_JSON" | jq -r '.amount')"
  NOTES="$(echo "$AMOUNT_JSON" | jq -r '.notes')"
  TRACKER_SYMBOL="$(echo "$AMOUNT_JSON" | jq -r '.trackerCurrencySymbol')"
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

FORMATTED_DATE="$(iso_to_sheet_display "$DATE_ISO")"
DISPLAY_DATE="$(iso_to_income_display "$DATE_ISO")"

BODY=$(jq -n \
  --arg tid "$TRANSACTION_ID" \
  --arg dt "$FORMATTED_DATE" \
  --argjson amt "$AMOUNT" \
  --arg cat "$CATEGORY" \
  --arg desc "$DESCRIPTION" \
  --arg label "$CURRENT_LABEL" \
  --arg notes "$NOTES" \
  --arg acc "$ACCOUNT" \
  '{"values": [[($tid), ($dt), ($amt), ($cat), ($desc), ($label), ($notes), ($acc)]]}')

curl -sf -X PUT \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/Expenses%21D${SHEET_ROW}%3AK${SHEET_ROW}?valueInputOption=RAW" \
  -d "$BODY" > /dev/null

CAT_BODY=$(jq -n --arg cat "$CATEGORY" '{"values": [[($cat)]]}')
curl -sf -X PUT \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/Expenses%21G${SHEET_ROW}?valueInputOption=USER_ENTERED" \
  -d "$CAT_BODY" > /dev/null

update_master_timestamp

DISPLAY_AMOUNT="${TRACKER_SYMBOL}${AMOUNT}"
echo "CONFIRM: Updated ${DESCRIPTION} — ${DISPLAY_AMOUNT} under ${CATEGORY_DISPLAY} on ${DISPLAY_DATE} (${ACCOUNT})"
