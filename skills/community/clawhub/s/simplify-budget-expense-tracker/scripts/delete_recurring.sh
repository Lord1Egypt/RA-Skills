#!/usr/bin/env bash
# Clears an existing recurring row by recurring ID without deleting the sheet row.
# Usage: delete_recurring.sh <recurring_id>
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: delete_recurring.sh <recurring_id>"
  exit 1
fi

RECURRING_ID="$1"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/expense_lib.sh"

ROW_JSON="$(find_recurring_row_json "$RECURRING_ID")" || {
  echo "Error: recurring ID $RECURRING_ID not found in sheet"
  exit 1
}

SHEET_ROW="$(echo "$ROW_JSON" | jq -r '.rowNumber')"

CLEAR_BODY='{}'
curl -sf -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/Recurring%21C${SHEET_ROW}%3AN${SHEET_ROW}:clear" \
  -d "$CLEAR_BODY" > /dev/null

update_recurring_timestamp

echo "Cleared recurring ${RECURRING_ID} at row ${SHEET_ROW}"
