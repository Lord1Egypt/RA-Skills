#!/usr/bin/env bash
# Clears an existing income row by transaction ID without deleting the row.
# Usage: delete_income.sh <transaction_id>
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: delete_income.sh <transaction_id>"
  exit 1
fi

TRANSACTION_ID="$1"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=./expense_lib.sh
source "$SCRIPT_DIR/expense_lib.sh"

ROW_JSON="$(find_income_row_json "$TRANSACTION_ID")" || {
  echo "Error: transaction ID $TRANSACTION_ID not found in sheet"
  exit 1
}

SHEET_ROW="$(echo "$ROW_JSON" | jq -r '.rowNumber')"

CLEAR_BODY='{}'
curl -sf -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/Income%21D${SHEET_ROW}%3AJ${SHEET_ROW}:clear" \
  -d "$CLEAR_BODY" > /dev/null

update_master_timestamp

echo "Cleared transaction ${TRANSACTION_ID} at row ${SHEET_ROW}"
