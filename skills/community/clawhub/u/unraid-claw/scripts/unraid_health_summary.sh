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

health_json="$(compute_health_status_from_snapshot "$snapshot_file")"

if [[ $json_mode -eq 1 ]]; then
  jq -n \
    --slurpfile snapshot "$snapshot_file" \
    --argjson health "$health_json" '
    {
      overall: $health.overall,
      timestamp: ($snapshot[0].timestamp // null),
      health: $health,
      system: {
        uptime: ($snapshot[0].data.info.os.uptime // "unknown"),
        cpu_usage_percent: ($snapshot[0].data.info.cpu.usage // "unknown"),
        cpu_temperature: ($snapshot[0].data.info.cpu.temperature // "unknown"),
        memory_usage_percent: ($snapshot[0].data.info.memory.usage // "unknown")
      },
      array: {
        state: ($snapshot[0].data.array.state // "unknown"),
        sync_action: ($snapshot[0].data.array.syncAction // "none"),
        sync_progress: ($snapshot[0].data.array.syncProgress // "0"),
        parity_status: ($snapshot[0].data.array.parity.status // "unknown")
      },
      docker: {
        enabled: ($snapshot[0].data.docker.enabled // false),
        total: (($snapshot[0].data.docker.containers // []) | length),
        running: (($snapshot[0].data.docker.containers // []) | map(select((.state // "") | ascii_downcase == "running")) | length),
        stopped: (($snapshot[0].data.docker.containers // []) | map(select((.state // "") | ascii_downcase != "running")) | length)
      }
    }
  '
  exit 0
fi

overall="$(jq -r '.overall' <<< "$health_json")"
check_time="$(jq -r '.timestamp // "unknown"' "$snapshot_file")"
uptime="$(jq -r '.data.info.os.uptime // "unknown"' "$snapshot_file")"
cpu_usage="$(jq -r '.data.info.cpu.usage // "unknown"' "$snapshot_file")"
cpu_temp="$(jq -r '.data.info.cpu.temperature // "unknown"' "$snapshot_file")"
mem_usage="$(jq -r '.data.info.memory.usage // "unknown"' "$snapshot_file")"
array_state="$(jq -r '.data.array.state // "unknown"' "$snapshot_file")"
sync_action="$(jq -r '.data.array.syncAction // "none"' "$snapshot_file")"
sync_progress="$(jq -r '.data.array.syncProgress // "0"' "$snapshot_file")"
parity_status="$(jq -r '.data.array.parity.status // "unknown"' "$snapshot_file")"
total_containers="$(jq -r '(.data.docker.containers // []) | length' "$snapshot_file")"
running_containers="$(jq -r '(.data.docker.containers // []) | map(select((.state // "") | ascii_downcase == "running")) | length' "$snapshot_file")"
stopped_containers="$(jq -r '(.data.docker.containers // []) | map(select((.state // "") | ascii_downcase != "running")) | length' "$snapshot_file")"

echo "Overall: ${overall}"
echo "Time: ${check_time}"
echo
echo "System:"
echo "- Uptime: ${uptime}"
echo "- CPU: ${cpu_usage}% (${cpu_temp})"
echo "- Memory: ${mem_usage}%"
echo
echo "Array:"
echo "- State: ${array_state}"
echo "- Sync: ${sync_action} ${sync_progress}"
echo "- Parity: ${parity_status}"
echo
echo "Docker:"
echo "- Total: ${total_containers}"
echo "- Running: ${running_containers}"
echo "- Stopped: ${stopped_containers}"
echo
echo "Alerts:"
jq -r '.alerts[]?' <<< "$health_json" | sed 's/^/- /'

if [[ "$(jq -r '.alerts | length' <<< "$health_json")" == "0" ]]; then
  echo "- None"
fi

exit 0