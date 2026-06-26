#!/usr/bin/env bash
# MaybeAI Sheet — Formatting (Freeze, Filters, Conditional Formats)
# Usage: export MAYBEAI_API_TOKEN=your_token_here
#        export DOC_ID=your_document_id_here
#        bash 08-formatting.sh

BASE_URL="https://play-be.omnimcp.ai"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"
DOC_ID="${DOC_ID:?Please set DOC_ID}"

# ── Freeze Panes ──────────────────────────────────────────────────────────────
# freeze_rows=1 locks the header row; freeze_columns=0 means no column freeze
echo "=== Freeze Header Row ==="
curl -s -X POST "$BASE_URL/api/v1/excel/freeze_panes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"worksheet_name\": \"Sheet1\",
    \"freeze_rows\": 1,
    \"freeze_columns\": 0
  }" \
  | jq .

# Freeze both first row and first column
echo "=== Freeze Row + Column ==="
curl -s -X POST "$BASE_URL/api/v1/excel/freeze_panes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"worksheet_name\": \"Sheet1\",
    \"freeze_rows\": 1,
    \"freeze_columns\": 1
  }" \
  | jq .

# ── Set Auto Filter ───────────────────────────────────────────────────────────
echo "=== Set Auto Filter ==="
curl -s -X POST "$BASE_URL/api/v1/excel/set_auto_filter" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"worksheet_name\": \"Sheet1\",
    \"auto_filter\": {
      \"ref\": \"A1:F100\",
      \"filter_columns\": []
    }
  }" \
  | jq .

# ── Remove Auto Filter ────────────────────────────────────────────────────────
echo "=== Remove Auto Filter ==="
curl -s -X POST "$BASE_URL/api/v1/excel/remove_auto_filter" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"worksheet_name\": \"Sheet1\"}" \
  | jq .

# ── Set Conditional Formats ───────────────────────────────────────────────────
# Highlights cells in B2:B100 red when value > 90
echo "=== Set Conditional Formats (highlight high scores) ==="
curl -s -X POST "$BASE_URL/api/v1/excel/set_conditional_formats" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"worksheet_name\": \"Sheet1\",
    \"formats\": [
      {
        \"sqref\": \"B2:B100\",
        \"type\": \"cell\",
        \"criteria\": \">\",
        \"value\": \"90\",
        \"format\": {
          \"font\": {\"color\": \"FF0000\", \"bold\": true},
          \"fill\": {\"type\": \"pattern\", \"color\": \"FFEB9C\"}
        }
      }
    ]
  }" \
  | jq .

# Highlight cells below threshold in red (e.g. flag low scores)
echo "=== Set Conditional Formats (flag low scores) ==="
curl -s -X POST "$BASE_URL/api/v1/excel/set_conditional_formats" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"worksheet_name\": \"Sheet1\",
    \"formats\": [
      {
        \"sqref\": \"B2:B100\",
        \"type\": \"cell\",
        \"criteria\": \"<\",
        \"value\": \"60\",
        \"format\": {
          \"font\": {\"color\": \"FFFFFF\"},
          \"fill\": {\"type\": \"pattern\", \"color\": \"FF0000\"}
        }
      }
    ]
  }" \
  | jq .
