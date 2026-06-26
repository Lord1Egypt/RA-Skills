#!/usr/bin/env bash
# Updates an existing recurring row by recurring ID.
# Use __KEEP__ to preserve the current value and __CLEAR__ to blank optional text/date fields.
# Usage: update_recurring.sh <recurring_id> <start_date|__KEEP__> <name|__KEEP__> <category|__KEEP__> <type|__KEEP__> <frequency|__KEEP__> <amount|__KEEP__> [account|__KEEP__] [end_date|__KEEP__|__CLEAR__] [notes|__KEEP__|__CLEAR__] [source|__KEEP__|__CLEAR__]
set -euo pipefail

if [ "$#" -lt 7 ]; then
  echo "Usage: update_recurring.sh <recurring_id> <start_date|__KEEP__> <name|__KEEP__> <category|__KEEP__> <type|__KEEP__> <frequency|__KEEP__> <amount|__KEEP__> [account|__KEEP__] [end_date|__KEEP__|__CLEAR__] [notes|__KEEP__|__CLEAR__] [source|__KEEP__|__CLEAR__]"
  exit 1
fi

RECURRING_ID="$1"
START_DATE_INPUT="$2"
NAME_INPUT="$3"
CATEGORY_INPUT="$4"
TYPE_INPUT="$5"
FREQUENCY_INPUT="$6"
AMOUNT_INPUT="$7"
ACCOUNT_INPUT="${8:-__KEEP__}"
END_DATE_INPUT="${9:-__KEEP__}"
NOTES_INPUT="${10:-__KEEP__}"
SOURCE_INPUT="${11:-__KEEP__}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/expense_lib.sh"

ROW_JSON="$(find_recurring_row_json "$RECURRING_ID")" || {
  echo "Error: recurring ID $RECURRING_ID not found in sheet"
  exit 1
}

SHEET_ROW="$(echo "$ROW_JSON" | jq -r '.rowNumber')"
START_DATE_ISO="$(echo "$ROW_JSON" | jq -r '.startDateIso')"
NAME="$(echo "$ROW_JSON" | jq -r '.name')"
CATEGORY="$(echo "$ROW_JSON" | jq -r '.category')"
TYPE_VALUE="$(echo "$ROW_JSON" | jq -r '.type')"
FREQUENCY="$(echo "$ROW_JSON" | jq -r '.frequency')"
AMOUNT="$(echo "$ROW_JSON" | jq -r '.amount')"
ACCOUNT="$(echo "$ROW_JSON" | jq -r '.account')"
END_DATE_ISO="$(echo "$ROW_JSON" | jq -r '.endDateIso')"
LABEL="$(echo "$ROW_JSON" | jq -r '.label')"
NOTES="$(echo "$ROW_JSON" | jq -r '.notes')"
SOURCE="$(echo "$ROW_JSON" | jq -r '.source')"

if [ "$START_DATE_INPUT" != "__KEEP__" ]; then
  START_DATE_ISO="$START_DATE_INPUT"
fi
if [ "$NAME_INPUT" != "__KEEP__" ]; then
  NAME="$NAME_INPUT"
fi
if [ "$CATEGORY_INPUT" != "__KEEP__" ]; then
  CATEGORY="$CATEGORY_INPUT"
fi
if [ "$TYPE_INPUT" != "__KEEP__" ]; then
  case "$(printf '%s' "$TYPE_INPUT" | tr '[:upper:]' '[:lower:]')" in
    true|expense|expenses|1|yes) TYPE_VALUE="TRUE" ;;
    false|income|incomes|0|no) TYPE_VALUE="FALSE" ;;
    *)
      echo "Error: type must be expense/income/TRUE/FALSE"
      exit 1
      ;;
  esac
fi
if [ "$FREQUENCY_INPUT" != "__KEEP__" ]; then
  FREQUENCY="$FREQUENCY_INPUT"
fi
if [ "$AMOUNT_INPUT" != "__KEEP__" ]; then
  AMOUNT="$AMOUNT_INPUT"
fi
if [ "$ACCOUNT_INPUT" != "__KEEP__" ]; then
  ACCOUNT="$ACCOUNT_INPUT"
fi
if [ "$END_DATE_INPUT" = "__CLEAR__" ]; then
  END_DATE_ISO=""
elif [ "$END_DATE_INPUT" != "__KEEP__" ]; then
  END_DATE_ISO="$END_DATE_INPUT"
fi
if [ "$NOTES_INPUT" = "__CLEAR__" ]; then
  NOTES=""
elif [ "$NOTES_INPUT" != "__KEEP__" ]; then
  NOTES="$NOTES_INPUT"
fi
if [ "$SOURCE_INPUT" = "__CLEAR__" ]; then
  SOURCE=""
elif [ "$SOURCE_INPUT" != "__KEEP__" ]; then
  SOURCE="$SOURCE_INPUT"
fi

if [ "$CATEGORY" != "__KEEP__" ]; then
  CATEGORY="$(resolve_recurring_category_input "$CATEGORY" "$TYPE_VALUE")"
fi

python3 - "$START_DATE_ISO" "$END_DATE_ISO" "$TYPE_VALUE" "$FREQUENCY" <<'PY'
import sys
from datetime import datetime

datetime.strptime(sys.argv[1].strip(), "%Y-%m-%d")
if sys.argv[2].strip():
    datetime.strptime(sys.argv[2].strip(), "%Y-%m-%d")

type_value = sys.argv[3].strip().upper()
if type_value not in {"TRUE", "FALSE"}:
    raise SystemExit("Error: type must be TRUE or FALSE")

frequency = sys.argv[4].strip().lower()
if frequency not in {"monthly", "quarterly", "yearly"}:
    raise SystemExit("Error: frequency must be Monthly, Quarterly, or Yearly")
PY

START_DATE_DISPLAY="$(iso_to_income_display "$START_DATE_ISO")"
END_DATE_DISPLAY=""
if [ -n "$END_DATE_ISO" ]; then
  END_DATE_DISPLAY="$(iso_to_income_display "$END_DATE_ISO")"
fi

BODY=$(jq -n \
  --arg rid "$RECURRING_ID" \
  --arg start "$START_DATE_DISPLAY" \
  --arg name "$NAME" \
  --arg category "$CATEGORY" \
  --arg type "$TYPE_VALUE" \
  --arg frequency "$FREQUENCY" \
  --arg amount "$AMOUNT" \
  --arg account "$ACCOUNT" \
  --arg end "$END_DATE_DISPLAY" \
  --arg label "$LABEL" \
  --arg notes "$NOTES" \
  --arg source "$SOURCE" \
  '{"values": [[($rid), ($start), ($name), ($category), ($type), ($frequency), ($amount), ($account), ($end), ($label), ($notes), ($source)]]}')

curl -sf -X PUT \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/Recurring%21C${SHEET_ROW}%3AN${SHEET_ROW}?valueInputOption=USER_ENTERED" \
  -d "$BODY" > /dev/null

update_recurring_timestamp

echo "Updated recurring ${RECURRING_ID} at row ${SHEET_ROW}"
