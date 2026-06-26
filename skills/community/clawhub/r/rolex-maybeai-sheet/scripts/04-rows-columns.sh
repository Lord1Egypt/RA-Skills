#!/usr/bin/env bash
# MaybeAI Sheet — Row & Column Operations
# Usage: export MAYBEAI_API_TOKEN=your_token_here
#        export DOC_ID=your_document_id_here
#        bash 04-rows-columns.sh

BASE_URL="https://play-be.omnimcp.ai"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"
DOC_ID="${DOC_ID:?Please set DOC_ID}"

# ── Insert Rows ───────────────────────────────────────────────────────────────
# Inserts 2 blank rows starting at row 3 (1-indexed)
echo "=== Insert Rows ==="
curl -s -X POST "$BASE_URL/api/v1/excel/insert_rows" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\", \"row\": 3, \"count\": 2}" \
  | jq .

# ── Delete Rows ───────────────────────────────────────────────────────────────
echo "=== Delete Rows ==="
curl -s -X POST "$BASE_URL/api/v1/excel/delete_rows" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\", \"row\": 5, \"count\": 2}" \
  | jq .

# ── Move Row ──────────────────────────────────────────────────────────────────
echo "=== Move Row ==="
curl -s -X POST "$BASE_URL/api/v1/excel/move_row" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\", \"from_row\": 8, \"to_row\": 2}" \
  | jq .

# ── Move Rows (batch) ─────────────────────────────────────────────────────────
echo "=== Move Rows (batch) ==="
curl -s -X POST "$BASE_URL/api/v1/excel/move_rows" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\", \"rows\": [5, 6, 7], \"to_row\": 2}" \
  | jq .

# ── Undo Delete Rows ──────────────────────────────────────────────────────────
echo "=== Undo Delete Rows ==="
curl -s -X POST "$BASE_URL/api/v1/excel/undo_delete_rows" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\"}" \
  | jq .

# ── Insert Columns ────────────────────────────────────────────────────────────
echo "=== Insert Columns ==="
curl -s -X POST "$BASE_URL/api/v1/excel/insert_columns" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\", \"column\": \"C\", \"count\": 1}" \
  | jq .

# ── Delete Columns ────────────────────────────────────────────────────────────
echo "=== Delete Columns ==="
curl -s -X POST "$BASE_URL/api/v1/excel/delete_columns" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\", \"column\": \"D\", \"count\": 1}" \
  | jq .

# ── Move Column ───────────────────────────────────────────────────────────────
echo "=== Move Column ==="
curl -s -X POST "$BASE_URL/api/v1/excel/move_column" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\", \"from_column\": \"E\", \"to_column\": \"B\"}" \
  | jq .

# ── Move Columns (batch) ──────────────────────────────────────────────────────
echo "=== Move Columns (batch) ==="
curl -s -X POST "$BASE_URL/api/v1/excel/move_columns" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\", \"columns\": [\"E\", \"F\"], \"to_column\": \"B\"}" \
  | jq .

# ── Undo Delete Columns ───────────────────────────────────────────────────────
echo "=== Undo Delete Columns ==="
curl -s -X POST "$BASE_URL/api/v1/excel/undo_delete_columns" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\"}" \
  | jq .

# ── Add Header Columns ────────────────────────────────────────────────────────
echo "=== Add Header Columns ==="
curl -s -X POST "$BASE_URL/api/v1/excel/add_header_columns" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\", \"columns\": [\"Region\", \"Quarter\"]}" \
  | jq .

# ── Set Columns Width ─────────────────────────────────────────────────────────
echo "=== Set Columns Width ==="
curl -s -X POST "$BASE_URL/api/v1/excel/set_columns_width" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"sheet\": \"Sheet1\",
    \"columns\": [
      {\"column\": \"A\", \"width\": 25},
      {\"column\": \"B\", \"width\": 15}
    ]
  }" \
  | jq .

# ── Set Rows Height ───────────────────────────────────────────────────────────
echo "=== Set Rows Height ==="
curl -s -X POST "$BASE_URL/api/v1/excel/set_rows_height" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"sheet\": \"Sheet1\",
    \"rows\": [
      {\"row\": 1, \"height\": 30},
      {\"row\": 2, \"height\": 20}
    ]
  }" \
  | jq .
