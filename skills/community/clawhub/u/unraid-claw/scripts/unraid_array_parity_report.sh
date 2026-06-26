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
    array: {
      state: (.data.array.state // "unknown"),
      sync_action: (.data.array.syncAction // "none"),
      sync_progress: (.data.array.syncProgress // "0"),
      errors: (.data.array.errors // 0),
      parity: (.data.array.parity // {}),
      disks: (.data.array.disks // [])
    }
  }' "$snapshot_file"
  exit 0
fi

array_state="$(jq -r '.data.array.state // "unknown"' "$snapshot_file")"
sync_action="$(jq -r '.data.array.syncAction // "none"' "$snapshot_file")"
sync_progress="$(jq -r '.data.array.syncProgress // "0"' "$snapshot_file")"
array_errors="$(jq -r '.data.array.errors // 0' "$snapshot_file")"
parity_status="$(jq -r '.data.array.parity.status // "unknown"' "$snapshot_file")"
parity_last_check="$(jq -r '.data.array.parity.lastCheck // "unknown"' "$snapshot_file")"
parity_errors="$(jq -r '.data.array.parity.errors // 0' "$snapshot_file")"

echo "Array:"
echo "- State: ${array_state}"
echo "- Sync: ${sync_action} ${sync_progress}"
echo "- Errors: ${array_errors}"
echo
echo "Parity:"
echo "- Status: ${parity_status}"
echo "- Last Check: ${parity_last_check}"
echo "- Errors: ${parity_errors}"
echo
echo "Disks:"
jq -r '
  (.data.array.disks // [])
  | if length == 0 then
      "- None"
    else
      .[] | "- \(.name // "unknown"): status=\(.status // "unknown"), smart=\(.smartStatus // "unknown"), temp=\(.temperature // "unknown")"
    end
' "$snapshot_file"

exit 0