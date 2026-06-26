#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/unraid_common.sh"

json_mode=0
if [[ "${1:-}" == "--json" ]]; then
  json_mode=1
fi

require_command "jq" "required to read snapshot data"
snapshot_file="$(latest_snapshot_path)"

if [[ ! -f "$snapshot_file" ]]; then
  echo "FAIL: Snapshot file not found at ${snapshot_file}. Run ./scripts/unraid_snapshot.sh first."
  exit 8
fi

if [[ $json_mode -eq 1 ]]; then
  jq '{
    timestamp: (.timestamp // null),
    docker: {
      enabled: (.data.docker.enabled // false),
      total: ((.data.docker.containers // []) | length),
      running: ((.data.docker.containers // []) | map(select((.state // "") | ascii_downcase == "running")) | length),
      stopped: ((.data.docker.containers // []) | map(select((.state // "") | ascii_downcase != "running")) | length),
      containers: (.data.docker.containers // [])
    }
  }' "$snapshot_file"
  exit 0
fi

enabled="$(jq -r '.data.docker.enabled // false' "$snapshot_file")"
total="$(jq -r '(.data.docker.containers // []) | length' "$snapshot_file")"
running="$(jq -r '(.data.docker.containers // []) | map(select((.state // "") | ascii_downcase == "running")) | length' "$snapshot_file")"
stopped="$(jq -r '(.data.docker.containers // []) | map(select((.state // "") | ascii_downcase != "running")) | length' "$snapshot_file")"

echo "Docker:"
echo "- Enabled: ${enabled}"
echo "- Total: ${total}"
echo "- Running: ${running}"
echo "- Stopped: ${stopped}"

if [[ "$stopped" -gt 0 ]]; then
  echo "- Stopped Containers:"
  jq -r '(.data.docker.containers // []) | map(select((.state // "") | ascii_downcase != "running")) | .[] | "  - \(.name // "unknown"): \(.status // "unknown")"' "$snapshot_file"
fi

exit 0