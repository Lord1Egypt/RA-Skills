#!/bin/sh
# Usage: list-conversations.sh [tag] [limit] [offset]
set -eu
. "$(dirname "$0")/common.sh"

tag="${1:-}"
limit="${2:-}"
offset="${3:-}"

query=""
[ -n "$tag" ] && query="${query}tag=${tag}&"
[ -n "$limit" ] && query="${query}limit=${limit}&"
[ -n "$offset" ] && query="${query}offset=${offset}&"
query="${query%&}"

url="$BASE/public/v1/conversations"
[ -n "$query" ] && url="${url}?${query}"

curl -s "$url" -H "$AUTH_HEADER" | print_response
