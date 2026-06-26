#!/usr/bin/env bash
# MaybeAI Sheet — Worksheet Management
# Usage: export MAYBEAI_API_TOKEN=your_token_here
#        export DOC_ID=your_document_id_here
#        bash 05-worksheets.sh

BASE_URL="https://play-be.omnimcp.ai"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"
DOC_ID="${DOC_ID:?Please set DOC_ID}"

# ── Write New Worksheet (with data) ──────────────────────────────────────────
echo "=== Write New Worksheet ==="
curl -s -X POST "$BASE_URL/api/v1/excel/write_new_worksheet" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_ID\",
    \"sheet\": \"Q1 Report\",
    \"data\": [
      [\"Month\", \"Revenue\", \"Cost\"],
      [\"Jan\",   50000,      30000],
      [\"Feb\",   62000,      35000],
      [\"Mar\",   71000,      38000]
    ]
  }" \
  | jq .

# ── Rename Worksheet ──────────────────────────────────────────────────────────
echo "=== Rename Worksheet ==="
curl -s -X POST "$BASE_URL/api/v1/excel/rename_worksheet" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sheet1\", \"new_name\": \"Sales Data\"}" \
  | jq .

# ── Move Worksheet ────────────────────────────────────────────────────────────
# position is 0-indexed (0 = first tab)
echo "=== Move Worksheet ==="
curl -s -X POST "$BASE_URL/api/v1/excel/move_worksheet" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Summary\", \"position\": 0}" \
  | jq .

# ── Duplicate Worksheet ───────────────────────────────────────────────────────
echo "=== Duplicate Worksheet ==="
curl -s -X POST "$BASE_URL/api/v1/excel/copy_worksheet" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sales Data\", \"new_name\": \"Sales Data (copy)\"}" \
  | jq .

# ── Delete Worksheet ──────────────────────────────────────────────────────────
echo "=== Delete Worksheet ==="
curl -s -X POST "$BASE_URL/api/v1/excel/delete_worksheet" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"sheet\": \"Sales Data (copy)\"}" \
  | jq .
