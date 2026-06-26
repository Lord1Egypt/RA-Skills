#!/usr/bin/env bash
# Download an input file from a job
# Usage: download.sh <job_id> <file_id> [output_path]

source "$(dirname "$0")/lib.sh"

job_id="${1:?Usage: download.sh <job_id> <file_id> [output_path]}"
file_id="${2:?Usage: download.sh <job_id> <file_id> [output_path]}"
output_path="${3:-downloaded_${file_id}}"

response=$(vox_api GET "/v1/jobs/${job_id}/files/${file_id}/download-url")
download_url=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['download_url'])" 2>/dev/null \
  || echo "$response" | jq -r '.data.download_url' 2>/dev/null)

if [[ -z "$download_url" || "$download_url" == "null" ]]; then
  echo "ERROR: Could not get download URL" >&2
  echo "$response" >&2
  exit 1
fi

curl -s -S -o "$output_path" "$download_url" || { echo "ERROR: Download failed" >&2; exit 1; }
echo "Downloaded to: $output_path"
