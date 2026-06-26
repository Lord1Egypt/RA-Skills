#!/usr/bin/env bash
# MaybeAI Sheet — Formulas
# Usage: export MAYBEAI_API_TOKEN=your_token_here
#        export DOC_ID=your_document_id_here
#        bash 06-formulas.sh

BASE_URL="https://play-be.omnimcp.ai"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"
DOC_ID="${DOC_ID:?Please set DOC_ID}"

# ── Calculate Single Formula ──────────────────────────────────────────────────
echo "=== Calc Single Formula ==="
curl -s -X POST "$BASE_URL/api/v1/excel/calc-formula" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"sheet\": \"Sheet1\",
    \"formula\": \"=SUM(B2:B10)\"
  }" \
  | jq .

# ── Calculate Multiple Formulas ───────────────────────────────────────────────
echo "=== Calc Multiple Formulas ==="
curl -s -X POST "$BASE_URL/api/v1/excel/calc_formulas" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"sheet\": \"Sheet1\",
    \"formulas\": [
      {\"cell\": \"B11\", \"formula\": \"=SUM(B2:B10)\"},
      {\"cell\": \"C11\", \"formula\": \"=AVERAGE(C2:C10)\"},
      {\"cell\": \"D11\", \"formula\": \"=MAX(D2:D10)\"}
    ]
  }" \
  | jq .

# ── Recalculate All Formulas in Document ──────────────────────────────────────
echo "=== Recalculate All Formulas ==="
curl -s -X POST "$BASE_URL/api/v1/excel/recalculate_formulas" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\"}" \
  | jq .
