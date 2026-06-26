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
overall="$(jq -r '.overall' <<< "$health_json")"

if [[ $json_mode -eq 1 ]]; then
  jq -n \
    --arg overall "$overall" \
    --slurpfile snapshot "$snapshot_file" \
    --argjson health "$health_json" '
    {
      overall: $overall,
      timestamp: ($snapshot[0].timestamp // null),
      alerts: $health.alerts,
      metrics: $health.metrics
    }
  '
else
  echo "Overall: ${overall}"
  echo "Time: $(jq -r '.timestamp // "unknown"' "$snapshot_file")"
  echo "Alerts:"
  jq -r '.alerts[]?' <<< "$health_json" | sed 's/^/- /'
  if [[ "$(jq -r '.alerts | length' <<< "$health_json")" == "0" ]]; then
    echo "- None"
  fi
fi

case "$overall" in
  healthy)
    exit 0
    ;;
  warning)
    exit 10
    ;;
  critical)
    exit 20
    ;;
  *)
    exit 1
    ;;
esac