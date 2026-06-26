#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://skills.easytoken.cc/api}"
ENDPOINT="${1:-stats}"
QUERY="${2:-}"

if [[ -n "$QUERY" ]]; then
  URL="$BASE_URL/$ENDPOINT?$QUERY"
else
  URL="$BASE_URL/$ENDPOINT"
fi

echo "[request] $URL" >&2
curl --fail-with-body -sS "$URL"
