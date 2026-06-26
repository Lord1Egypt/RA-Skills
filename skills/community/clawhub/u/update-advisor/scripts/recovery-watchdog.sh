#!/usr/bin/env bash
# recovery-watchdog.sh — external gateway recovery loop for update-advisor v2
# This script is designed to be launched before `openclaw update` from a
# process that survives Gateway restarts (for example launchd StartCalendarInterval
# or a manual `nohup` wrapper). It does not register launchd jobs itself.
set -euo pipefail

OPENCLAW_BIN="${OPENCLAW_BIN:-openclaw}"
LOG_FILE="${LOG_FILE:-}"
GRACE_SECONDS=300
STATUS_RETRIES=3
STATUS_INTERVAL_SECONDS=20
RECOVERY_RETRIES=2
RECOVERY_INTERVAL_SECONDS=30
MAX_RUNTIME_SECONDS=1200

usage() {
  cat <<'EOF'
Usage:
  recovery-watchdog.sh [options]

Options:
  --log-file PATH                 Log file path (default: stderr only)
  --grace-seconds N               Initial delay before first status check (default: 300)
  --status-retries N              Status checks per probe phase (default: 3)
  --status-interval-seconds N     Delay between status checks (default: 20)
  --recovery-retries N            Recovery attempts when unhealthy (default: 2)
  --recovery-interval-seconds N   Delay between recovery attempts (default: 30)
  --max-runtime-seconds N         Hard timeout for whole watchdog (default: 1200)
  --help                          Show this help

Environment:
  OPENCLAW_BIN                    Override command path (default: openclaw)
  WATCHDOG_SKIP_SLEEP=1           Skip sleeping (for tests only)
EOF
}

log() {
  local msg="$1"
  local ts
  ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  if [[ -n "$LOG_FILE" ]]; then
    printf '%s %s\n' "$ts" "$msg" >> "$LOG_FILE"
  fi
  printf '%s %s\n' "$ts" "$msg" >&2
}

sleep_maybe() {
  local secs="$1"
  if [[ "${WATCHDOG_SKIP_SLEEP:-0}" == "1" ]]; then
    return 0
  fi
  sleep "$secs"
}

enforce_deadline() {
  local context="$1"
  local now_ts
  now_ts="$(now_epoch)"
  if (( now_ts >= deadline_ts )); then
    log "result=timeout context=$context"
    exit 4
  fi
}

sleep_with_deadline() {
  local requested="$1" context="$2"
  local now_ts remaining sleep_for
  now_ts="$(now_epoch)"
  remaining=$((deadline_ts - now_ts))
  if (( remaining <= 0 )); then
    log "result=timeout context=$context"
    exit 4
  fi
  sleep_for="$requested"
  if (( sleep_for > remaining )); then
    sleep_for="$remaining"
  fi
  sleep_maybe "$sleep_for"
  enforce_deadline "$context"
}

is_positive_int() {
  [[ "$1" =~ ^[0-9]+$ ]]
}

is_healthy_status_output() {
  local text
  text="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"

  if [[ "$text" == *"not installed"* ]] || [[ "$text" == *"stopped"* ]] || [[ "$text" == *"not running"* ]]; then
    return 1
  fi
  if [[ "$text" == *"healthy"* ]] || [[ "$text" == *"running"* ]] || [[ "$text" == *"ok"* ]]; then
    return 0
  fi
  return 1
}

run_gateway_status() {
  local out rc
  set +e
  out="$("$OPENCLAW_BIN" gateway status 2>&1)"
  rc=$?
  set -e
  printf '%s\n' "$out"
  return "$rc"
}

run_gateway_install() {
  local out rc
  set +e
  out="$("$OPENCLAW_BIN" gateway install 2>&1)"
  rc=$?
  set -e
  log "recovery_command_rc=$rc output=$(printf '%s' "$out" | tr '\n' ' ' | sed 's/[[:space:]]\+/ /g')"
  return "$rc"
}

probe_gateway_health() {
  local phase="$1"
  local i out rc
  for (( i=1; i<=STATUS_RETRIES; i++ )); do
    enforce_deadline "probe_${phase}_check_$i"
    set +e
    out="$(run_gateway_status)"
    rc=$?
    set -e
    enforce_deadline "probe_${phase}_post_status_$i"
    log "phase=$phase check=$i/$STATUS_RETRIES status_rc=$rc status=$(printf '%s' "$out" | tr '\n' ' ' | sed 's/[[:space:]]\+/ /g')"
    if [[ "$rc" -eq 0 ]] && is_healthy_status_output "$out"; then
      log "gateway_health=healthy phase=$phase"
      return 0
    fi
    if [[ "$i" -lt "$STATUS_RETRIES" ]]; then
      sleep_with_deadline "$STATUS_INTERVAL_SECONDS" "probe_${phase}_interval_$i"
    fi
  done
  log "gateway_health=unhealthy phase=$phase"
  return 1
}

now_epoch() {
  date +%s
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --log-file) LOG_FILE="$2"; shift 2 ;;
    --grace-seconds) GRACE_SECONDS="$2"; shift 2 ;;
    --status-retries) STATUS_RETRIES="$2"; shift 2 ;;
    --status-interval-seconds) STATUS_INTERVAL_SECONDS="$2"; shift 2 ;;
    --recovery-retries) RECOVERY_RETRIES="$2"; shift 2 ;;
    --recovery-interval-seconds) RECOVERY_INTERVAL_SECONDS="$2"; shift 2 ;;
    --max-runtime-seconds) MAX_RUNTIME_SECONDS="$2"; shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

for n in \
  "$GRACE_SECONDS" \
  "$STATUS_RETRIES" \
  "$STATUS_INTERVAL_SECONDS" \
  "$RECOVERY_RETRIES" \
  "$RECOVERY_INTERVAL_SECONDS" \
  "$MAX_RUNTIME_SECONDS"
do
  if ! is_positive_int "$n"; then
    echo "Numeric argument expected, got: $n" >&2
    exit 2
  fi
done

if ! command -v "$OPENCLAW_BIN" >/dev/null 2>&1; then
  log "error=openclaw_binary_not_found bin=$OPENCLAW_BIN"
  exit 3
fi

if [[ -n "$LOG_FILE" ]]; then
  mkdir -p "$(dirname "$LOG_FILE")"
fi

start_ts="$(now_epoch)"
deadline_ts=$((start_ts + MAX_RUNTIME_SECONDS))
log "watchdog_start grace_seconds=$GRACE_SECONDS recovery_retries=$RECOVERY_RETRIES"

sleep_with_deadline "$GRACE_SECONDS" "initial_grace"

if probe_gateway_health "initial"; then
  log "result=healthy_no_recovery_needed"
  exit 0
fi

for (( attempt=1; attempt<=RECOVERY_RETRIES; attempt++ )); do
  enforce_deadline "before_recovery_attempt_$attempt"

  log "recovery_attempt=$attempt/$RECOVERY_RETRIES action=gateway_install"
  if run_gateway_install; then
    enforce_deadline "after_recovery_install_$attempt"
    if probe_gateway_health "after_recovery_$attempt"; then
      log "result=recovered attempt=$attempt"
      exit 0
    fi
  fi

  if [[ "$attempt" -lt "$RECOVERY_RETRIES" ]]; then
    sleep_with_deadline "$RECOVERY_INTERVAL_SECONDS" "recovery_interval_$attempt"
  fi
done

log "result=failed_after_retries"
exit 5
