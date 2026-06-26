#!/usr/bin/env bash
set -euo pipefail

METHOD="${1:-GET}"
PATH_PART="${2:-/health}"
BODY="${3:-}"

BASE_URL="${SSH_AGENTD_URL:-http://127.0.0.1:18081}"
TOKEN="${SSH_AGENTD_TOKEN:-}"

CURL=(env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u all_proxy \
  curl --noproxy '*' -sS -X "$METHOD" "$BASE_URL$PATH_PART" \
  -H 'Content-Type: application/json')

if [[ -n "$TOKEN" ]]; then
  CURL+=( -H "Authorization: Bearer $TOKEN" )
fi

if [[ "$METHOD" == "POST" || "$METHOD" == "PUT" || "$METHOD" == "PATCH" ]]; then
  CURL+=( -d "$BODY" )
fi

"${CURL[@]}"
