#!/bin/bash
# dashboard/recent-activity — 最近动态
# Usage: bash recent-activity.sh [LIMIT]
# LIMIT: 1–50, default 5
# Requires: X2C_API_KEY env var

set -euo pipefail

API_URL="https://eumfmgwxwjyagsvqloac.supabase.co/functions/v1/open-api"
API_KEY="${X2C_API_KEY:-}"
LIMIT="${1:-5}"

if [ -z "$API_KEY" ]; then
  echo '{"success":false,"error":"X2C_API_KEY is not set"}' >&2
  exit 1
fi

if ! [[ "$LIMIT" =~ ^[0-9]+$ ]] || [ "$LIMIT" -lt 1 ] || [ "$LIMIT" -gt 50 ]; then
  echo '{"success":false,"error":"LIMIT must be between 1 and 50"}' >&2
  exit 1
fi

curl -sS -X POST "$API_URL" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"action\":\"dashboard/recent-activity\",\"limit\":$LIMIT}"
