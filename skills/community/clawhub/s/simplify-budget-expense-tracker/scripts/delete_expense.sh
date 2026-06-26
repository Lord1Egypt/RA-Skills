#!/usr/bin/env bash
# Clears an existing expense row by transaction ID without deleting the row.
# Usage: delete_expense.sh <transaction_id>
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: delete_expense.sh <transaction_id>"
  exit 1
fi

TRANSACTION_ID="$1"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=./expense_lib.sh
source "$SCRIPT_DIR/expense_lib.sh"

ROW_JSON="$(find_expense_row_json "$TRANSACTION_ID")" || {
  echo "Error: transaction ID $TRANSACTION_ID not found in sheet"
  exit 1
}

SHEET_ROW="$(echo "$ROW_JSON" | jq -r '.rowNumber')"
DESCRIPTION="$(echo "$ROW_JSON" | jq -r '.description')"
AMOUNT="$(echo "$ROW_JSON" | jq -r '.amount')"
DATE_DISPLAY="$(echo "$ROW_JSON" | jq -r '.dateDisplay')"

CLEAR_BODY='{}'
curl -sf -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/Expenses%21D${SHEET_ROW}%3AK${SHEET_ROW}:clear" \
  -d "$CLEAR_BODY" > /dev/null

update_master_timestamp

echo "CONFIRM: Deleted ${DESCRIPTION} — ${AMOUNT} on ${DATE_DISPLAY}"
