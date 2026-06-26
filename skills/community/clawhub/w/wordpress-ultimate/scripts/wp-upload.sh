#!/usr/bin/env bash
# WordPress media upload wrapper
# Usage: wp-upload.sh <file_path> [alt_text]
# Returns: JSON with media ID and URL
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Load .env
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

: "${WP_URL:?Set WP_URL in .env}"
: "${WP_USER:?Set WP_USER in .env}"
: "${WP_APP_PASSWORD:?Set WP_APP_PASSWORD in .env}"

FILE_PATH="${1:?Usage: wp-upload.sh <file_path> [alt_text]}"
ALT_TEXT="${2:-}"

if [[ ! -f "$FILE_PATH" ]]; then
  echo "❌ File not found: $FILE_PATH" >&2
  exit 1
fi

FILENAME=$(basename "$FILE_PATH")

# Detect MIME type
MIME=$(file --mime-type -b "$FILE_PATH")

RESPONSE=$(curl -s \
  -u "${WP_USER}:${WP_APP_PASSWORD}" \
  -H "Content-Disposition: attachment; filename=\"${FILENAME}\"" \
  -H "Content-Type: ${MIME}" \
  --data-binary "@${FILE_PATH}" \
  "${WP_URL}/wp-json/wp/v2/media")

MEDIA_ID=$(echo "$RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin).get('id','ERROR'))" 2>/dev/null || echo "ERROR")

if [[ "$MEDIA_ID" == "ERROR" ]]; then
  echo "❌ Upload failed:" >&2
  echo "$RESPONSE" >&2
  exit 1
fi

# Set alt text if provided
if [[ -n "$ALT_TEXT" ]]; then
  curl -s \
    -X PUT \
    -u "${WP_USER}:${WP_APP_PASSWORD}" \
    -H "Content-Type: application/json" \
    -d "{\"alt_text\": \"${ALT_TEXT}\"}" \
    "${WP_URL}/wp-json/wp/v2/media/${MEDIA_ID}" > /dev/null
fi

echo "$RESPONSE" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(json.dumps({
    'id': d['id'],
    'url': d.get('source_url', ''),
    'title': d.get('title', {}).get('rendered', ''),
    'mime': d.get('mime_type', '')
}, indent=2))
"
