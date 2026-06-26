#!/usr/bin/env bash
# Request a revision on a delivered job
# Usage: revision.sh <job_id> <feedback>

source "$(dirname "$0")/lib.sh"

job_id="${1:?Usage: revision.sh <job_id> <feedback>}"
feedback="${2:?Usage: revision.sh <job_id> <feedback>}"

body=$(cat <<EOF
{"feedback":"${feedback}"}
EOF
)

vox_api POST "/v1/jobs/${job_id}/revision" "$body" | pretty_json
