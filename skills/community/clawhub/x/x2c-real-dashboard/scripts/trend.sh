#!/bin/bash
# dashboard/trend — 收益趋势
# Usage: bash trend.sh [DAYS]
# DAYS: 1–90, default 7
# Requires: X2C_API_KEY env var

set -euo pipefail

API_URL="https://eumfmgwxwjyagsvqloac.supabase.co/functions/v1/open-api"
API_KEY="${X2C_API_KEY:-}"
DAYS="${1:-7}"

if [ -z "$API_KEY" ]; then
  echo '{"success":false,"error":"X2C_API_KEY is not set"}' >&2
  exit 1
fi

if ! [[ "$DAYS" =~ ^[0-9]+$ ]] || [ "$DAYS" -lt 1 ] || [ "$DAYS" -gt 90 ]; then
  echo '{"success":false,"error":"DAYS must be between 1 and 90"}' >&2
  exit 1
fi

curl -sS -X POST "$API_URL" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"action\":\"dashboard/trend\",\"days\":$DAYS}"
