#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/../.env"

if [ -f "$ENV_FILE" ]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

if [ $# -lt 1 ]; then
  echo "Usage: $0 \"directive text\"" >&2
  exit 1
fi

HA_URL="${HA_URL:-}"
HA_TOKEN="${HA_TOKEN:-}"
ENTITY_ID="${XIAOAI_EXECUTE_TEXT_ENTITY_ID:-}"
TEXT="$*"

if [ -z "$HA_URL" ]; then
  echo "ERROR: HA_URL is not set" >&2
  echo "Checked env file: $ENV_FILE" >&2
  exit 2
fi

if [ -z "$HA_TOKEN" ]; then
  echo "ERROR: HA_TOKEN is not set" >&2
  echo "Checked env file: $ENV_FILE" >&2
  exit 2
fi

if [ -z "$ENTITY_ID" ]; then
  echo "ERROR: XIAOAI_EXECUTE_TEXT_ENTITY_ID is not set" >&2
  echo "Checked env file: $ENV_FILE" >&2
  exit 2
fi

ESCAPED_TEXT=$(printf '%s' "$TEXT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')

curl -sS --noproxy '*' -X POST \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  "${HA_URL}/api/services/text/set_value" \
  -d "{\"entity_id\":\"${ENTITY_ID}\",\"value\":${ESCAPED_TEXT}}"

echo "Sent to XiaoAI execute_text_directive (${ENTITY_ID}): ${TEXT}" >&2
