#!/bin/sh
# Usage: webhook-unsubscribe.sh <subscription_id>
set -eu
. "$(dirname "$0")/common.sh"

subscription_id="${1:?usage: webhook-unsubscribe.sh <subscription_id>}"

curl -s -X DELETE "$BASE/public/v1/webhook-subscriptions/$subscription_id" \
  -H "$AUTH_HEADER" | print_response
