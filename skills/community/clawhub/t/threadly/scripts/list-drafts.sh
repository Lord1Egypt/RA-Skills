#!/bin/sh
# Usage: list-drafts.sh [status] [limit] [offset]
# status defaults to pending_review, matching the API's own default.
set -eu
. "$(dirname "$0")/common.sh"

status="${1:-pending_review}"
limit="${2:-}"
offset="${3:-}"

query="status=${status}&"
[ -n "$limit" ] && query="${query}limit=${limit}&"
[ -n "$offset" ] && query="${query}offset=${offset}&"
query="${query%&}"

curl -s "$BASE/public/v1/drafts?${query}" -H "$AUTH_HEADER" | print_response
