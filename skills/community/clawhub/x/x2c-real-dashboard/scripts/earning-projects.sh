#!/bin/bash
# dashboard/earning-projects — 赚钱作品列表
# Usage: bash earning-projects.sh [PAGE] [PAGE_SIZE]
# PAGE default 1, PAGE_SIZE default 10 (max 50)
# Requires: X2C_API_KEY env var

set -euo pipefail

API_URL="https://eumfmgwxwjyagsvqloac.supabase.co/functions/v1/open-api"
API_KEY="${X2C_API_KEY:-}"
PAGE="${1:-1}"
PAGE_SIZE="${2:-10}"

if [ -z "$API_KEY" ]; then
  echo '{"success":false,"error":"X2C_API_KEY is not set"}' >&2
  exit 1
fi

if ! [[ "$PAGE" =~ ^[0-9]+$ ]] || [ "$PAGE" -lt 1 ]; then
  echo '{"success":false,"error":"PAGE must be >= 1"}' >&2
  exit 1
fi

if ! [[ "$PAGE_SIZE" =~ ^[0-9]+$ ]] || [ "$PAGE_SIZE" -lt 1 ] || [ "$PAGE_SIZE" -gt 50 ]; then
  echo '{"success":false,"error":"PAGE_SIZE must be between 1 and 50"}' >&2
  exit 1
fi

curl -sS -X POST "$API_URL" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"action\":\"dashboard/earning-projects\",\"page\":$PAGE,\"page_size\":$PAGE_SIZE}"
