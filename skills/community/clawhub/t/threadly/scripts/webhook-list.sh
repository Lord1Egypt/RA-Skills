#!/bin/sh
# Usage: webhook-list.sh
set -eu
. "$(dirname "$0")/common.sh"

curl -s "$BASE/public/v1/webhook-subscriptions" -H "$AUTH_HEADER" | print_response
