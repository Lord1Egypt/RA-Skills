#!/usr/bin/env bash
# List your active jobs
# Usage: my-jobs.sh [status_filter]

source "$(dirname "$0")/lib.sh"

status="${1:-funded,accepted,in_progress,delivered,validating,revision_requested}"

vox_api GET "/v1/jobs?status=${status}&limit=50" | pretty_json
