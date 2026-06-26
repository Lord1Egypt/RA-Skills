#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/../.env"

if [ -f "$ENV_FILE" ]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

if [ $# -lt 1 ]; then
  echo "Usage: $0 \"media url\" [media_content_type]" >&2
  exit 1
fi

HA_URL="${HA_URL:-}"
HA_TOKEN="${HA_TOKEN:-}"
ENTITY_ID="${XIAOAI_MEDIA_PLAYER_ENTITY_ID:-}"
MEDIA_URL="$1"
MEDIA_TYPE="${2:-music}"

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
  echo "ERROR: XIAOAI_MEDIA_PLAYER_ENTITY_ID is not set" >&2
  echo "Checked env file: $ENV_FILE" >&2
  exit 2
fi

ESCAPED_URL=$(printf '%s' "$MEDIA_URL" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')
ESCAPED_TYPE=$(printf '%s' "$MEDIA_TYPE" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')

curl -sS --noproxy '*' -X POST \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  "${HA_URL}/api/services/media_player/play_media" \
  -d "{\"entity_id\":\"${ENTITY_ID}\",\"media_content_id\":${ESCAPED_URL},\"media_content_type\":${ESCAPED_TYPE}}"

echo "Sent to XiaoAI media_player (${ENTITY_ID}): ${MEDIA_URL} [${MEDIA_TYPE}]" >&2
