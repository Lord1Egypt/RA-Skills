#!/usr/bin/env bash
# Show the connected Muse accounts, or read one account's plan and weekly allowance live from Muse.
# Usage: account.sh [email]     (default: USEAPI_EMAIL. With neither, lists every account as last read.)
# quota.percentUsed is the share of the week used, in whole percent. quota.resetsAt is when it starts over.
# On the free plan a video used 2 to 3 percent and an image 0 to 1 percent in useapi.net's tests.
# videoLimitUntil shows only while Muse's video limit for the last 24 hours holds the account.
# videoRegionBlocked shows when Meta switched off video for the account in its country or region.
# Docs: https://useapi.net/docs/api-muse-v1/get-muse-accounts-email
source "$(dirname "$0")/_common.sh"
EMAIL="${1:-${USEAPI_EMAIL:-}}"
FIELDS='{email, health, maxJobs, session, videoLimitUntil, videoRegionBlocked, quota: ((.quota // {}) | {tier, percentUsed, resetsAt, quotaStatus, topupLabel})} | with_entries(select(.value != null))'
if [ -n "$EMAIL" ]; then
  api_poll GET "accounts/$(enc "$EMAIL")" | jq "$FIELDS"
else
  api_poll GET accounts | jq "[.[] | $FIELDS]"
fi
