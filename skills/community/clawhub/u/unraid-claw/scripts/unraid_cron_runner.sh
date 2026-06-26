#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/unraid_common.sh"

ensure_state_dirs
run_ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
run_log="${LOG_DIR}/runner_$(date -u +"%Y%m%d").log"

log() {
  local line="$1"
  echo "${line}"
  echo "${run_ts} ${line}" >> "$run_log"
}

log "INFO: Starting Unraid cron runner."

"${SCRIPT_DIR}/unraid_preflight.sh" >> "$run_log" 2>&1
preflight_status=$?
if [[ $preflight_status -ne 0 ]]; then
  log "FAIL: Preflight failed with exit ${preflight_status}."
  "${SCRIPT_DIR}/unraid_notify.sh" "CRITICAL" "Unraid preflight failed with exit ${preflight_status}." >> "$run_log" 2>&1 || true
  exit $preflight_status
fi

"${SCRIPT_DIR}/unraid_snapshot.sh" >> "$run_log" 2>&1
snapshot_status=$?
if [[ $snapshot_status -ne 0 ]]; then
  log "FAIL: Snapshot failed with exit ${snapshot_status}."
  "${SCRIPT_DIR}/unraid_notify.sh" "CRITICAL" "Unraid snapshot failed with exit ${snapshot_status}." >> "$run_log" 2>&1 || true
  exit $snapshot_status
fi

summary_text="$("${SCRIPT_DIR}/unraid_health_summary.sh" 2>>"$run_log")"
summary_status=$?
echo "$summary_text" >> "$run_log"
if [[ $summary_status -ne 0 ]]; then
  log "FAIL: Health summary failed with exit ${summary_status}."
  "${SCRIPT_DIR}/unraid_notify.sh" "WARNING" "Unraid summary generation failed with exit ${summary_status}." >> "$run_log" 2>&1 || true
  exit $summary_status
fi

"${SCRIPT_DIR}/unraid_alerts.sh" >> "$run_log" 2>&1
alerts_status=$?

if [[ $alerts_status -eq 0 ]]; then
  log "PASS: Unraid status healthy."
  exit 0
fi

if [[ $alerts_status -eq 10 ]]; then
  log "WARN: Unraid status warning."
  "${SCRIPT_DIR}/unraid_notify.sh" "WARNING" "Unraid status warning. Review latest summary and alerts." >> "$run_log" 2>&1 || true
  exit 10
fi

if [[ $alerts_status -eq 20 ]]; then
  log "CRITICAL: Unraid status critical."
  "${SCRIPT_DIR}/unraid_notify.sh" "CRITICAL" "Unraid status critical. Immediate operator review required." >> "$run_log" 2>&1 || true
  exit 20
fi

log "FAIL: Alerts script returned unexpected exit ${alerts_status}."
"${SCRIPT_DIR}/unraid_notify.sh" "CRITICAL" "Unraid alerts script returned unexpected exit ${alerts_status}." >> "$run_log" 2>&1 || true
exit $alerts_status