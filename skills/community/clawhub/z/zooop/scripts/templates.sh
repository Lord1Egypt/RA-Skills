#!/usr/bin/env bash
# List Zooop templates (the one-click presets published at /templates), or
# fetch one template's full param schema by slug.
#
# Usage:
#   templates.sh                       # all templates
#   templates.sh image                 # filter by mediaType
#   templates.sh video                 # filter by mediaType
#   templates.sh -s <slug>             # one template's detail (full param schema)
#
# Examples:
#   templates.sh image
#   templates.sh -s superhero-movie-poster
#
# Every approved, live template is listed — official and community alike.
# Run one with: submit.sh --template <slug> '<params-json>'
set -euo pipefail

: "${ZOOOP_API_KEY:?ZOOOP_API_KEY must be set — visit https://zooop.ai/user?tab=apiKeys to create one}"
HOST="${ZOOOP_API_HOST:-https://api.zooop.ai}"

if [[ ${1:-} == "-s" ]]; then
  if [[ $# -lt 2 ]]; then
    echo "usage: $0 -s <slug>" >&2
    exit 64
  fi
  SLUG="$2"
  curl -fsS "$HOST/v1/templates/$SLUG" \
    -H "Authorization: Bearer $ZOOOP_API_KEY"
elif [[ $# -gt 0 ]]; then
  TYPE="$1"
  if [[ "$TYPE" != "image" && "$TYPE" != "video" ]]; then
    echo "type must be 'image' or 'video' (got: $TYPE)" >&2
    exit 64
  fi
  curl -fsS "$HOST/v1/templates?type=$TYPE" \
    -H "Authorization: Bearer $ZOOOP_API_KEY"
else
  curl -fsS "$HOST/v1/templates" \
    -H "Authorization: Bearer $ZOOOP_API_KEY"
fi
