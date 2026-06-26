#!/bin/bash
# dashboard/platform-breakdown — 各平台播放量
# Usage: bash platform-breakdown.sh
# Requires: X2C_API_KEY env var

set -euo pipefail

API_URL="https://eumfmgwxwjyagsvqloac.supabase.co/functions/v1/open-api"
API_KEY="${X2C_API_KEY:-}"

if [ -z "$API_KEY" ]; then
  echo '{"success":false,"error":"X2C_API_KEY is not set"}' >&2
  exit 1
fi

curl -sS -X POST "$API_URL" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"action":"dashboard/platform-breakdown"}'
