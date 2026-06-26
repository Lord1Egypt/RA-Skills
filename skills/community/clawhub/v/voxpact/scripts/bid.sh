#!/usr/bin/env bash
# Bid on an open job
# Usage: bid.sh <job_id> <price_eur> [message]

source "$(dirname "$0")/lib.sh"

job_id="${1:?Usage: bid.sh <job_id> <price_eur> [message]}"
price="${2:?Usage: bid.sh <job_id> <price_eur> [message]}"
message="${3:-I can complete this job.}"

body=$(cat <<EOF
{"proposed_price":${price},"message":"${message}"}
EOF
)

vox_api POST "/v1/jobs/${job_id}/bids" "$body" | pretty_json
