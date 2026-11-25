#!/usr/bin/env bash
# List Zooop AI tools (admin-curated recipes), or fetch one tool's full
# param schema by slug.
#
# Usage:
#   ai-tools.sh                       # all tools
#   ai-tools.sh image                 # filter by mediaType
#   ai-tools.sh video                 # filter by mediaType
#   ai-tools.sh -s <slug>             # one tool's detail (full param schema)
#
# Examples:
#   ai-tools.sh
#   ai-tools.sh image
#   ai-tools.sh -s background-removal
set -euo pipefail

: "${ZOOOP_API_KEY:?ZOOOP_API_KEY must be set — visit https://zooop.ai/user?tab=apiKeys to create one}"
HOST="${ZOOOP_API_HOST:-https://api.zooop.ai}"

if [[ ${1:-} == "-s" ]]; then
  if [[ $# -lt 2 ]]; then
    echo "usage: $0 -s <slug>" >&2
    exit 64
  fi
  SLUG="$2"
  curl -fsS "$HOST/v1/ai-tools/$SLUG" \
    -H "Authorization: Bearer $ZOOOP_API_KEY"
elif [[ $# -gt 0 ]]; then
  TYPE="$1"
  if [[ "$TYPE" != "image" && "$TYPE" != "video" ]]; then
    echo "type must be 'image' or 'video' (got: $TYPE)" >&2
    exit 64
  fi
  curl -fsS "$HOST/v1/ai-tools?type=$TYPE" \
    -H "Authorization: Bearer $ZOOOP_API_KEY"
else
  curl -fsS "$HOST/v1/ai-tools" \
    -H "Authorization: Bearer $ZOOOP_API_KEY"
fi
