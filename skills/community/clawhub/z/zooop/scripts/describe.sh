#!/usr/bin/env bash
# Describe a reference image — returns a structured prompt (subject,
# composition, style, lighting, palette, mood, camera + flowing
# overallDescription paragraph). Costs 1 credit per call.
#
# Usage:  describe.sh <zooop-cdn-image-url> [language]
#   language  optional locale code (zh / zh-TW / ja / fr / es / de / …) that
#             sets the OUTPUT language of every field. Omitted → English.
# Example:
#   describe.sh https://storage.zooop.ai/<userId>/<projectId>/<uuid>.png zh
#
# Input MUST be a ZOOOP CDN URL. Pipe local files through upload.sh first.
set -euo pipefail

: "${ZOOOP_API_KEY:?ZOOOP_API_KEY must be set — visit https://zooop.ai/user?tab=apiKeys to create one}"
HOST="${ZOOOP_API_HOST:-https://api.zooop.ai}"

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <zooop-cdn-image-url> [language]" >&2
  exit 64
fi

URL="$1"
LANG_CODE="${2:-}"
if [[ -n "$LANG_CODE" ]]; then
  BODY=$(printf '{"imageUrl":"%s","language":"%s"}' "$URL" "$LANG_CODE")
else
  BODY=$(printf '{"imageUrl":"%s"}' "$URL")
fi

curl -fsS -X POST "$HOST/v1/describe-image" \
  -H "Authorization: Bearer $ZOOOP_API_KEY" \
  -H "Content-Type: application/json" \
  --data "$BODY"
