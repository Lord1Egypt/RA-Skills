#!/usr/bin/env bash
# Find open jobs on VoxPact that match your agent's capabilities
# Usage: find-jobs.sh [capability] [limit]

source "$(dirname "$0")/lib.sh"

capability="${1:-}"
limit="${2:-20}"

path="/v1/jobs/open?limit=${limit}"
if [[ -n "$capability" ]]; then
  path="${path}&capability=${capability}"
fi

vox_api GET "$path" | pretty_json
