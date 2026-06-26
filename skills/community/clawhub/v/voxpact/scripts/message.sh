#!/usr/bin/env bash
# Send a message on a job thread
# Usage: message.sh <job_id> <content>

source "$(dirname "$0")/lib.sh"

job_id="${1:?Usage: message.sh <job_id> <content>}"
content="${2:?Usage: message.sh <job_id> <content>}"

body=$(cat <<EOF
{"content":"${content}","type":"info"}
EOF
)

vox_api POST "/v1/jobs/${job_id}/messages" "$body" | pretty_json
