#!/usr/bin/env bash
# MaybeAI Sheet — Charts & Pictures
# Usage: export MAYBEAI_API_TOKEN=your_token_here
#        export DOC_ID=your_document_id_here
#        bash 07-charts-pictures.sh

BASE_URL="https://play-be.omnimcp.ai"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"
DOC_ID="${DOC_ID:?Please set DOC_ID}"

# ── Add Chart ─────────────────────────────────────────────────────────────────
# Supported types: line, bar, col, pie, scatter, area, doughnut, radar
echo "=== Add Bar Chart ==="
curl -s -X POST "$BASE_URL/api/v1/excel/add_chart" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"worksheet_name\": \"Sheet1\",
    \"cell\": \"E2\",
    \"chart\": {
      \"type\": \"bar\",
      \"series\": [
        {
          \"name\": \"Revenue\",
          \"categories\": \"Sheet1!\$A\$2:\$A\$10\",
          \"values\": \"Sheet1!\$B\$2:\$B\$10\"
        }
      ],
      \"title\": {\"name\": \"Monthly Revenue\"},
      \"legend\": {\"position\": \"bottom\"}
    }
  }" \
  | jq .

# ── Add Line Chart ────────────────────────────────────────────────────────────
echo "=== Add Line Chart ==="
curl -s -X POST "$BASE_URL/api/v1/excel/add_chart" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"worksheet_name\": \"Sheet1\",
    \"cell\": \"E20\",
    \"chart\": {
      \"type\": \"line\",
      \"series\": [
        {
          \"name\": \"Sales\",
          \"categories\": \"Sheet1!\$A\$2:\$A\$12\",
          \"values\": \"Sheet1!\$C\$2:\$C\$12\"
        }
      ],
      \"title\": {\"name\": \"Sales Trend\"}
    }
  }" \
  | jq .

# ── Edit Chart ────────────────────────────────────────────────────────────────
echo "=== Edit Chart ==="
curl -s -X POST "$BASE_URL/api/v1/excel/set_chart" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"worksheet_name\": \"Sheet1\",
    \"chart_id\": 1,
    \"chart\": {
      \"title\": {\"name\": \"Updated Title\"}
    }
  }" \
  | jq .

# ── Delete Chart ──────────────────────────────────────────────────────────────
echo "=== Delete Chart ==="
curl -s -X POST "$BASE_URL/api/v1/excel/delete_chart" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"worksheet_name\": \"Sheet1\", \"chart_id\": 1}" \
  | jq .

# ── Add Picture ───────────────────────────────────────────────────────────────
echo "=== Add Picture ==="
curl -s -X POST "$BASE_URL/api/v1/excel/add_picture" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"sheet\": \"Sheet1\",
    \"cell\": \"H2\",
    \"picture_url\": \"https://example.com/logo.png\"
  }" \
  | jq .

# ── Read Pictures ─────────────────────────────────────────────────────────────
echo "=== Read Pictures ==="
curl -s -X POST "$BASE_URL/api/v1/excel/read_picture" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\"}" \
  | jq .

# ── Delete Picture ────────────────────────────────────────────────────────────
echo "=== Delete Picture ==="
curl -s -X POST "$BASE_URL/api/v1/excel/delete_picture" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\", \"picture_id\": 1}" \
  | jq .
