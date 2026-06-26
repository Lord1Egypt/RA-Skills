#!/usr/bin/env bash
# Approve a delivered job and release payment
# Usage: approve.sh <job_id>

source "$(dirname "$0")/lib.sh"

job_id="${1:?Usage: approve.sh <job_id>}"

vox_api POST "/v1/jobs/${job_id}/approve" | pretty_json
