#!/usr/bin/env bash
# Cancel a job (refunds the buyer)
# Usage: cancel.sh <job_id>

source "$(dirname "$0")/lib.sh"

job_id="${1:?Usage: cancel.sh <job_id>}"

vox_api POST "/v1/jobs/${job_id}/cancel" | pretty_json
