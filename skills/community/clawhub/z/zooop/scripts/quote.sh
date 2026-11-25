#!/usr/bin/env bash
# Quote a Zooop AI task without submitting. Prints the JSON response from
# POST /v1/quote — returns exact credits + ETA seconds with no side effects.
#
# Three modes:
#   quote.sh <interfaceId> <versionId> '<params-json>'
#   quote.sh --ai-tool  <slug>         '<params-json>'
#   quote.sh --template <slug>         '<params-json>'
#
# Examples:
#   quote.sh d2c0... pro '{"prompt":"a red panda eating noodles","aspect_ratio":"1:1"}'
#   quote.sh --ai-tool background-removal '{"image_url":"https://storage.zooop.ai/…"}'
#   quote.sh --template superhero-movie-poster '{"image_urls":["https://storage.zooop.ai/…"]}'
#
# Discover identifiers via:
#   GET /v1/models?type=<type>&subtype=<subType>     (raw path)
#   GET /v1/ai-tools[?type=image|video]              (curated tools)
#   GET /v1/templates[?type=image|video]             (gallery templates)
set -euo pipefail

: "${ZOOOP_API_KEY:?ZOOOP_API_KEY must be set — visit https://zooop.ai/user?tab=apiKeys to create one}"
HOST="${ZOOOP_API_HOST:-https://api.zooop.ai}"

if [[ ${1:-} == "--ai-tool" ]]; then
  if [[ $# -lt 3 ]]; then
    echo "usage: $0 --ai-tool <slug> <params-json>" >&2
    exit 64
  fi
  SLUG="$2"
  PARAMS="$3"
  BODY=$(printf '{"aiTool":"%s","params":%s}' "$SLUG" "$PARAMS")
elif [[ ${1:-} == "--template" ]]; then
  if [[ $# -lt 3 ]]; then
    echo "usage: $0 --template <slug> <params-json>" >&2
    exit 64
  fi
  SLUG="$2"
  PARAMS="$3"
  BODY=$(printf '{"template":"%s","params":%s}' "$SLUG" "$PARAMS")
else
  if [[ $# -lt 3 ]]; then
    echo "usage: $0 <interfaceId> <versionId> <params-json>" >&2
    echo "       $0 --ai-tool <slug> <params-json>" >&2
    echo "       $0 --template <slug> <params-json>" >&2
    exit 64
  fi
  INTERFACE_ID="$1"
  VERSION_ID="$2"
  PARAMS="$3"
  # Same body shape as submit.sh; the API enforces identical schema.
  BODY=$(printf '{"interfaceId":"%s","versionId":"%s","params":%s}' "$INTERFACE_ID" "$VERSION_ID" "$PARAMS")
fi

curl -fsS -X POST "$HOST/v1/quote" \
  -H "Authorization: Bearer $ZOOOP_API_KEY" \
  -H "Content-Type: application/json" \
  --data "$BODY"
