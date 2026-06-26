#!/usr/bin/env bash
# Writes a new recurring row to the Recurring sheet using first-empty-row reuse.
# Usage: write_recurring.sh <start_date> <name> <category> <expense|income|TRUE|FALSE> <frequency> <amount> [account] [end_date] [notes] [source]
set -euo pipefail

if [ "$#" -lt 6 ]; then
  echo "Usage: write_recurring.sh <start_date> <name> <category> <expense|income|TRUE|FALSE> <frequency> <amount> [account] [end_date] [notes] [source]"
  exit 1
fi

START_DATE_INPUT="$1"
NAME="$2"
CATEGORY="$3"
TYPE_INPUT="$4"
FREQUENCY="$5"
AMOUNT="$6"
ACCOUNT="${7:-Other}"
END_DATE_INPUT="${8:-}"
NOTES="${9:-}"
SOURCE="${10:-}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/expense_lib.sh"

python3 - "$START_DATE_INPUT" "$END_DATE_INPUT" "$FREQUENCY" <<'PY'
import sys
from datetime import datetime

datetime.strptime(sys.argv[1].strip(), "%Y-%m-%d")
if sys.argv[2].strip():
    datetime.strptime(sys.argv[2].strip(), "%Y-%m-%d")
frequency = sys.argv[3].strip().lower()
if frequency not in {"monthly", "quarterly", "yearly"}:
    raise SystemExit("Error: frequency must be Monthly, Quarterly, or Yearly")
PY

case "$(printf '%s' "$TYPE_INPUT" | tr '[:upper:]' '[:lower:]')" in
  true|expense|expenses|1|yes) TYPE_VALUE="TRUE" ;;
  false|income|incomes|0|no) TYPE_VALUE="FALSE" ;;
  *)
    echo "Error: type must be expense/income/TRUE/FALSE"
    exit 1
    ;;
esac

CATEGORY_VALUE="$(resolve_recurring_category_input "$CATEGORY" "$TYPE_VALUE")"

START_DATE_DISPLAY="$(iso_to_income_display "$START_DATE_INPUT")"
END_DATE_DISPLAY=""
if [ -n "$END_DATE_INPUT" ]; then
  END_DATE_DISPLAY="$(iso_to_income_display "$END_DATE_INPUT")"
fi

AMOUNT_JSON="$(resolve_amount_and_notes_json "$AMOUNT" "$NOTES")"
AMOUNT_VALUE="$(echo "$AMOUNT_JSON" | jq -r '.amount')"
NOTES_VALUE="$(echo "$AMOUNT_JSON" | jq -r '.notes')"
AMOUNT_DISPLAY="${TRACKER_CURRENCY_SYMBOL}${AMOUNT_VALUE}"

TIMESTAMP_MS=$(python3 -c "import time; print(int(time.time() * 1000))")
RANDOM_SUFFIX=$(python3 -c "import random, string; print(''.join(random.choices(string.ascii_uppercase + string.digits, k=6)))")
RECURRING_ID="REC-${TIMESTAMP_MS}-${RANDOM_SUFFIX}"

ROW="$(find_next_recurring_append_row)"
BODY=$(jq -n \
  --arg rid "$RECURRING_ID" \
  --arg start "$START_DATE_DISPLAY" \
  --arg name "$NAME" \
  --arg category "$CATEGORY_VALUE" \
  --arg type "$TYPE_VALUE" \
  --arg frequency "$FREQUENCY" \
  --arg amount "$AMOUNT_DISPLAY" \
  --arg account "$ACCOUNT" \
  --arg end "$END_DATE_DISPLAY" \
  --arg label "" \
  --arg notes "$NOTES_VALUE" \
  --arg source "$SOURCE" \
  '{"values": [[($rid), ($start), ($name), ($category), ($type), ($frequency), ($amount), ($account), ($end), ($label), ($notes), ($source)]]}')

RESULT=$(curl -sf -X PUT \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/Recurring%21C${ROW}%3AN${ROW}?valueInputOption=USER_ENTERED" \
  -d "$BODY")

UPDATED_RANGE=$(echo "$RESULT" | jq -r '.updates.updatedRange // "unknown"')

update_recurring_timestamp

echo "recurring_id=${RECURRING_ID}"
echo "range=${UPDATED_RANGE}"
