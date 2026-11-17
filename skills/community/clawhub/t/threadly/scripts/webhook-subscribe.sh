#!/bin/sh
# Usage: webhook-subscribe.sh <target_url> [event_types_csv]
#
# target_url must be https:// and publicly reachable (not localhost/a private IP) — see
# SKILL.md's "Webhook subscriptions" section before using this. If you don't have a stable
# public endpoint, poll list-conversations.sh instead.
set -eu
. "$(dirname "$0")/common.sh"

target_url="${1:?usage: webhook-subscribe.sh <target_url> [event_types_csv]}"
event_types_csv="${2:-conversation.discovered}"

# Turn "a,b,c" into a JSON array ["a","b","c"] without depending on jq being installed.
event_types_json=$(printf '%s' "$event_types_csv" | awk -F, '{
  out = "["
  for (i = 1; i <= NF; i++) {
    if (i > 1) out = out ","
    out = out "\"" $i "\""
  }
  print out "]"
}')

curl -s -X POST "$BASE/public/v1/webhook-subscriptions" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d "{\"target_url\": \"$target_url\", \"event_types\": $event_types_json}" | print_response
