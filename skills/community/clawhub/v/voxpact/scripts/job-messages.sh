#!/usr/bin/env bash
# Read messages on a job
# Usage: job-messages.sh <job_id>

source "$(dirname "$0")/lib.sh"

job_id="${1:?Usage: job-messages.sh <job_id>}"

vox_api GET "/v1/jobs/${job_id}/messages?limit=100" | pretty_json
