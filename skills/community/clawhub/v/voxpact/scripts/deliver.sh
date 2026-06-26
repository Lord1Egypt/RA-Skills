#!/usr/bin/env bash
# Deliver work for a job (worker action — triggers payment release flow)
# Usage: deliver.sh <job_id> <file_path>

source "$(dirname "$0")/lib.sh"

job_id="${1:?Usage: deliver.sh <job_id> <file_path>}"
file_path="${2:?Usage: deliver.sh <job_id> <file_path>}"

if [[ ! -f "$file_path" ]]; then
  echo "ERROR: File not found: $file_path" >&2
  exit 1
fi

content_type=$(get_content_type "$file_path")
file_size=$(wc -c < "$file_path" | tr -d ' ')

echo "Delivering ${file_size} bytes as ${content_type}..."

vox_api_raw POST "/v1/jobs/${job_id}/deliver" "$content_type" "$file_path" | pretty_json
