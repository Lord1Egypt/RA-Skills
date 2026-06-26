#!/usr/bin/env bash
# MaybeAI Sheet — File Management
# Usage: export MAYBEAI_API_TOKEN=your_token_here
#        export BASE_URL=https://play-be.omnimcp.ai   (or your self-hosted URL)
#        bash 01-file-management.sh

BASE_URL="https://play-be.omnimcp.ai"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"

# ── Upload Excel File ────────────────────────────────────────────────────────
# Returns: { "document_id": "...", "uri": "...", ... }
# Save the document_id — it is used as "uri" in all subsequent calls.
echo "=== Upload Excel File ==="
curl -s -X POST "$BASE_URL/api/v1/excel/upload" \
  -F "file=@./sample.xlsx" \
  -F "user_id=demo-user" \
  | jq .

# ── Import File by URL ───────────────────────────────────────────────────────
echo "=== Import File by URL ==="
curl -s -X POST "$BASE_URL/api/v1/excel/import_by_url" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/data.xlsx"}' \
  | jq .

# ── List Files ───────────────────────────────────────────────────────────────
echo "=== List Files ==="
curl -s -X POST "$BASE_URL/api/v1/excel/list_files" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}' \
  | jq .

# ── Search Files ─────────────────────────────────────────────────────────────
echo "=== Search Files ==="
curl -s -X POST "$BASE_URL/api/v1/excel/search_files" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "sales"}' \
  | jq .

# ── Rename File ──────────────────────────────────────────────────────────────
DOC_ID="your_document_id_here"
echo "=== Rename File ==="
curl -s -X POST "$BASE_URL/api/v1/excel/rename_file" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\", \"name\": \"renamed_sales_report.xlsx\"}" \
  | jq .

# ── Delete File ──────────────────────────────────────────────────────────────
echo "=== Delete File ==="
curl -s -X POST "$BASE_URL/api/v1/excel/delete_file" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\"}" \
  | jq .

# ── Export (Download) File ───────────────────────────────────────────────────
echo "=== Export File ==="
curl -s -o "./exported.xlsx" \
  "$BASE_URL/api/v1/excel/export/$DOC_ID"
echo "Saved to ./exported.xlsx"

# ── Copy Excel Document ──────────────────────────────────────────────────────
echo "=== Copy Excel ==="
curl -s -X POST "$BASE_URL/api/v1/excel/copy_excel" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_ID\"}" \
  | jq .
