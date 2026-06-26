#!/usr/bin/env bash
# WordPress REST API wrapper with draft-only safety
# Usage: wp.sh <METHOD> <endpoint> [json_body]
# Env: WP_URL, WP_USER, WP_APP_PASSWORD (reads from .env if present)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Load .env from workspace root (walk up from skill dir)
ENV_FILE=""
d="$SKILL_DIR"
for _ in 1 2 3 4 5; do
  if [[ -f "$d/.env" ]]; then ENV_FILE="$d/.env"; break; fi
  d="$(dirname "$d")"
done
if [[ -n "$ENV_FILE" ]]; then
  while IFS='=' read -r key value; do
    [[ -z "$key" || "$key" =~ ^# ]] && continue
    key=$(echo "$key" | xargs)
    [[ -z "$key" ]] && continue
    export "$key"="$value"
  done < "$ENV_FILE"
fi

# Validate required vars
: "${WP_URL:?Set WP_URL in .env}"
: "${WP_USER:?Set WP_USER in .env}"
: "${WP_APP_PASSWORD:?Set WP_APP_PASSWORD in .env}"

METHOD="${1:?Usage: wp.sh <GET|POST|PUT|DELETE> <endpoint> [json_body]}"
ENDPOINT="${2:?Missing endpoint}"
BODY="${3:-}"

# Normalize
METHOD=$(echo "$METHOD" | tr '[:lower:]' '[:upper:]')
URL="${WP_URL}/wp-json/wp/v2/${ENDPOINT}"

# SAFETY: Force draft on new posts/pages unless explicitly overridden
if [[ "$METHOD" == "POST" && ("$ENDPOINT" == "posts" || "$ENDPOINT" == "pages") ]]; then
  if [[ -n "$BODY" ]]; then
    # Check if status is explicitly set to publish
    HAS_PUBLISH=$(echo "$BODY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('status',''))" 2>/dev/null || echo "")
    if [[ "$HAS_PUBLISH" != "publish" ]]; then
      # Force draft
      BODY=$(echo "$BODY" | python3 -c "import json,sys; d=json.load(sys.stdin); d['status']='draft'; print(json.dumps(d))")
    else
      echo "⚠️  WARNING: Creating with status=publish. Content will be live immediately." >&2
    fi
  else
    BODY='{"status":"draft"}'
  fi
fi

# SAFETY: Block DELETE — use trash instead
if [[ "$METHOD" == "DELETE" ]]; then
  echo "❌ DELETE blocked by safety policy. Use PUT with {\"status\":\"trash\"} instead." >&2
  exit 1
fi

# Build curl command
CURL_ARGS=(
  -s
  -X "$METHOD"
  -u "${WP_USER}:${WP_APP_PASSWORD}"
  -H "Content-Type: application/json"
)

if [[ -n "$BODY" && "$METHOD" != "GET" ]]; then
  CURL_ARGS+=(-d "$BODY")
fi

# Execute
RESPONSE=$(curl "${CURL_ARGS[@]}" "$URL")

# Pretty print if python3 available
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
