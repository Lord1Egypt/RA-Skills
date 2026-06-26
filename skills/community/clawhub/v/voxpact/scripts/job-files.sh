#!/usr/bin/env bash
# List all files on a job
# Usage: job-files.sh <job_id>

source "$(dirname "$0")/lib.sh"

job_id="${1:?Usage: job-files.sh <job_id>}"

vox_api GET "/v1/jobs/${job_id}/files" | pretty_json
