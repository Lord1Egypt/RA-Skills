#!/usr/bin/env bash
# MaybeAI Sheet — End-to-End Workflow Examples
#
# This script demonstrates three complete workflows:
#   1. Upload → read → update → export
#   2. Build a report from scratch
#   3. Append new data and recalculate
#
# Usage:
#   export MAYBEAI_API_TOKEN=your_token_here
#   bash 09-end-to-end.sh

BASE_URL="https://play-be.omnimcp.ai"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"

echo "============================================================"
echo " Workflow 1: Upload → Read → Update → Export"
echo "============================================================"

# Step 1: Upload
echo "[1/4] Uploading sample.xlsx ..."
UPLOAD_RESP=$(curl -s -X POST "$BASE_URL/api/v1/excel/upload" \
  -F "file=@./sample.xlsx" \
  -F "user_id=demo")
echo "$UPLOAD_RESP" | jq .
DOC_ID=$(echo "$UPLOAD_RESP" | jq -r '.document_id // .uri')
echo "Document ID: $DOC_ID"

# Step 2: List worksheets
echo "[2/4] Listing worksheets ..."
curl -s -X POST "$BASE_URL/api/v1/excel/list_worksheets" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\"}" \
  | jq .

# Step 3: Read Sheet1
echo "[3/4] Reading Sheet1 ..."
curl -s -X POST "$BASE_URL/api/v1/excel/read_sheet" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\"}" \
  | jq .

# Step 4: Update a range and export
echo "[4/4] Updating A1:B2 and exporting ..."
curl -s -X POST "$BASE_URL/api/v1/excel/update_range" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"sheet\": \"Sheet1\",
    \"range\": \"A1:B2\",
    \"values\": [[\"Product\",\"Q1\"],[\"Widget\",5000]]
  }" | jq .

curl -s -o "./workflow1_output.xlsx" \
  "$BASE_URL/api/v1/excel/export/$DOC_ID"
echo "Exported to ./workflow1_output.xlsx"

echo ""
echo "============================================================"
echo " Workflow 2: Build a Report from Scratch"
echo "============================================================"

# Upload blank template (or use existing DOC_ID from step above)
echo "[1/5] Using document from Workflow 1 (DOC_ID=$DOC_ID)"

# Write summary sheet
echo "[2/5] Writing Summary worksheet ..."
curl -s -X POST "$BASE_URL/api/v1/excel/write_new_worksheet" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"sheet\": \"Summary\",
    \"data\": [
      [\"Month\",\"Revenue\",\"Cost\",\"Profit\"],
      [\"Jan\", 50000, 30000, \"=C2-D2\"],
      [\"Feb\", 62000, 35000, \"=C3-D3\"],
      [\"Mar\", 71000, 38000, \"=C4-D4\"]
    ]
  }" | jq .

# Freeze header row
echo "[3/5] Freezing header row ..."
curl -s -X POST "$BASE_URL/api/v1/excel/freeze_panes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"worksheet_name\": \"Summary\", \"freeze_rows\": 1, \"freeze_columns\": 0}" \
  | jq .

# Add auto filter
echo "[4/5] Adding auto filter ..."
curl -s -X POST "$BASE_URL/api/v1/excel/set_auto_filter" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"worksheet_name\": \"Summary\", \"auto_filter\": {\"ref\": \"A1:D4\"}}" \
  | jq .

# Add a bar chart
echo "[5/5] Adding revenue bar chart ..."
curl -s -X POST "$BASE_URL/api/v1/excel/add_chart" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"worksheet_name\": \"Summary\",
    \"cell\": \"F2\",
    \"chart\": {
      \"type\": \"bar\",
      \"series\": [{
        \"name\": \"Revenue\",
        \"categories\": \"Summary!\$A\$2:\$A\$4\",
        \"values\": \"Summary!\$B\$2:\$B\$4\"
      }],
      \"title\": {\"name\": \"Quarterly Revenue\"}
    }
  }" | jq .

echo ""
echo "============================================================"
echo " Workflow 3: Append New Data and Recalculate"
echo "============================================================"

echo "[1/3] Appending new rows to Sheet1 ..."
curl -s -X POST "$BASE_URL/api/v1/excel/append_rows" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"sheet\": \"Sheet1\",
    \"rows\": [
      [\"Apr\", 80000, 42000],
      [\"May\", 95000, 48000]
    ]
  }" | jq .

echo "[2/3] Recalculating all formulas ..."
curl -s -X POST "$BASE_URL/api/v1/excel/recalculate_formulas" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\"}" \
  | jq .

echo "[3/3] Reading updated sheet ..."
curl -s -X POST "$BASE_URL/api/v1/excel/read_sheet" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\"}" \
  | jq .

echo ""
echo "All workflows complete."
