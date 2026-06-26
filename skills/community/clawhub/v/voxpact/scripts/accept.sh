#!/usr/bin/env bash
# Accept a direct job assigned to your agent
# Usage: accept.sh <job_id>

source "$(dirname "$0")/lib.sh"

job_id="${1:?Usage: accept.sh <job_id>}"

vox_api POST "/v1/jobs/${job_id}/accept" | pretty_json
