#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/unraid_common.sh"

ensure_state_dirs

severity="${1:-INFO}"
message="${2:-Unraid notification event}"
host_label="${UNRAID_NOTIFY_HOST_LABEL:-$(hostname)}"
log_file="${LOG_DIR}/notify.log"
timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

echo "${timestamp} severity=${severity} host=${host_label} message=${message}" >> "$log_file"
echo "PASS: Notification written to local log (${log_file})."
exit 0