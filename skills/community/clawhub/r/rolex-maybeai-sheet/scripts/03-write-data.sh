#!/usr/bin/env bash
# MaybeAI Sheet — Writing & Editing Data
# Usage: export MAYBEAI_API_TOKEN=your_token_here
#        export DOC_ID=your_document_id_here
#        bash 03-write-data.sh

BASE_URL="https://play-be.omnimcp.ai"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"
DOC_ID="${DOC_ID:?Please set DOC_ID}"

# ── Update Range ──────────────────────────────────────────────────────────────
echo "=== Update Range ==="
curl -s -X POST "$BASE_URL/api/v1/excel/update_range" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"sheet\": \"Sheet1\",
    \"range\": \"A1:C3\",
    \"values\": [
      [\"Name\", \"Score\", \"Grade\"],
      [\"Alice\",  95,      \"A\"],
      [\"Bob\",    82,      \"B\"]
    ]
  }" \
  | jq .

# ── Update Range by Lookup ────────────────────────────────────────────────────
# Finds the row where lookup_column == lookup_value and updates the given fields
echo "=== Update Range by Lookup ==="
curl -s -X POST "$BASE_URL/api/v1/excel/update_range_by_lookup" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"sheet\": \"Sheet1\",
    \"lookup_column\": \"Name\",
    \"lookup_value\": \"Alice\",
    \"updates\": {\"Score\": 98, \"Grade\": \"A+\"}
  }" \
  | jq .

# ── Clear Range ───────────────────────────────────────────────────────────────
echo "=== Clear Range ==="
curl -s -X POST "$BASE_URL/api/v1/excel/clear_range" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\", \"range\": \"D1:F10\"}" \
  | jq .

# ── Append Rows ───────────────────────────────────────────────────────────────
echo "=== Append Rows ==="
curl -s -X POST "$BASE_URL/api/v1/excel/append_rows" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"sheet\": \"Sheet1\",
    \"rows\": [
      [\"Charlie\", 77, \"C\"],
      [\"Diana\",   91, \"A-\"]
    ]
  }" \
  | jq .

# ── Write New Sheet (full data at once) ───────────────────────────────────────
echo "=== Write New Sheet ==="
curl -s -X POST "$BASE_URL/api/v1/excel/write_new_sheet" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"sheet\": \"Summary\",
    \"data\": [
      [\"Category\", \"Total\"],
      [\"Sales\",    12000],
      [\"Returns\",  300]
    ]
  }" \
  | jq .

# ── Copy Range with Formulas ──────────────────────────────────────────────────
echo "=== Copy Range with Formulas ==="
curl -s -X POST "$BASE_URL/api/v1/excel/copy_range_with_formulas" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"sheet\": \"Sheet1\",
    \"src_range\": \"A1:D10\",
    \"dst_range\": \"F1\"
  }" \
  | jq .

# ── Copy Range by Lookup ──────────────────────────────────────────────────────
echo "=== Copy Range by Lookup ==="
curl -s -X POST "$BASE_URL/api/v1/excel/copy_range_by_lookup" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"sheet\": \"Sheet1\",
    \"lookup_column\": \"Status\",
    \"lookup_value\": \"Done\",
    \"dst_sheet\": \"Archive\"
  }" \
  | jq .
