#!/bin/sh
# Usage: list-replies.sh [limit] [offset]
set -eu
. "$(dirname "$0")/common.sh"

limit="${1:-}"
offset="${2:-}"

query=""
[ -n "$limit" ] && query="${query}limit=${limit}&"
[ -n "$offset" ] && query="${query}offset=${offset}&"
query="${query%&}"

url="$BASE/public/v1/replies"
[ -n "$query" ] && url="${url}?${query}"

curl -s "$url" -H "$AUTH_HEADER" | print_response
