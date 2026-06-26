#!/usr/bin/env bash
# Reads active categories from Dontedit sheet L10:O39
# Output format: stableId<TAB>fullName (one per line)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOKEN=$("$SCRIPT_DIR/get_token.sh")

RANGE="Dontedit%21L10%3AO39"
URL="https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/${RANGE}"

curl -sf -H "Authorization: Bearer ${TOKEN}" "${URL}" \
  | jq -r '.values[]? | select(length >= 4) | select(.[0] == "TRUE") | "\(.[3])\t\(.[1])"'
# .[0] = L (active checkbox), .[1] = M (fullName), .[2] = N (displayOrder), .[3] = O (stableId)
