#!/usr/bin/env zsh
set -euo pipefail

state_file=""
timeout_seconds="8"
reason="manual_stop"

print_help() {
  cat <<'EOF'
Usage: ros1_stop_target.sh --state-file <path> [options]

Stop a previously started ROS1 target using its pid/pgid metadata.

Options:
  --state-file <path>     State file created by ros1_start_target.sh
  --timeout-seconds <n>   Wait time before SIGKILL, default: 8
  --reason <text>         Reason recorded in the state file
  --help                  Show this help
EOF
}

append_or_replace_state() {
  local key="$1"
  local value="$2"
  if grep -q "^${key}=" "$state_file"; then
    sed -i "s|^${key}=.*|${key}=${(q)value}|" "$state_file"
  else
    print -r -- "${key}=${(q)value}" >> "$state_file"
  fi
}

related_pids_for_ros_home() {
  local ros_home="$1"
  [[ -n "$ros_home" ]] || return 0
  ps -eo pid=,args= | awk -v needle="$ros_home" 'index($0, needle) {print $1}'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --state-file)
      state_file="${2:-}"
      [[ -n "$state_file" ]] || { echo "[ERROR] missing value for --state-file" >&2; exit 2; }
      shift 2
      ;;
    --timeout-seconds)
      timeout_seconds="${2:-}"
      [[ -n "$timeout_seconds" ]] || { echo "[ERROR] missing value for --timeout-seconds" >&2; exit 2; }
      shift 2
      ;;
    --reason)
      reason="${2:-}"
      [[ -n "$reason" ]] || { echo "[ERROR] missing value for --reason" >&2; exit 2; }
      shift 2
      ;;
    --help|-h)
      print_help
      exit 0
      ;;
    *)
      echo "[ERROR] unknown argument: $1" >&2
      print_help >&2
      exit 2
      ;;
  esac
done

[[ -n "$state_file" ]] || { echo "[ERROR] --state-file is required" >&2; exit 2; }
state_file="${state_file:A}"
[[ -f "$state_file" ]] || { echo "[ERROR] state file not found: $state_file" >&2; exit 1; }

# shellcheck disable=SC1090
source "$state_file"
pid="${PID:-}"
pgid="${PGID:-}"
ros_home="${ROS_HOME:-}"

append_or_replace_state "STOP_REQUESTED_AT" "$(date -Iseconds)"
append_or_replace_state "STOP_REASON" "$reason"

if [[ -z "$pid" ]]; then
  append_or_replace_state "STATUS" "stopped"
  echo "[ros1-stop] status=already_stopped"
  exit 0
fi

if ! kill -0 "$pid" 2>/dev/null; then
  related_pids=("${(@f)$(related_pids_for_ros_home "$ros_home")}")
  if (( ${#related_pids[@]} == 0 )); then
    append_or_replace_state "STATUS" "stopped"
    echo "[ros1-stop] status=already_stopped"
    exit 0
  fi
  for child_pid in "${related_pids[@]}"; do
    kill -TERM "$child_pid" 2>/dev/null || true
  done
  sleep 2
  remaining=("${(@f)$(related_pids_for_ros_home "$ros_home")}")
  if (( ${#remaining[@]} > 0 )); then
    for child_pid in "${remaining[@]}"; do
      kill -KILL "$child_pid" 2>/dev/null || true
    done
    append_or_replace_state "STOP_SIGNAL" "SIGKILL"
    append_or_replace_state "STATUS" "stopped"
    append_or_replace_state "STOPPED_AT" "$(date -Iseconds)"
    echo "[ros1-stop] status=forced_stop"
    exit 0
  fi
  append_or_replace_state "STOP_SIGNAL" "SIGTERM"
  append_or_replace_state "STATUS" "stopped"
  append_or_replace_state "STOPPED_AT" "$(date -Iseconds)"
  echo "[ros1-stop] status=stopped"
  exit 0
fi

target="-$pgid"
if [[ -z "$pgid" ]]; then
  target="$pid"
fi

kill -TERM "$target" 2>/dev/null || kill -TERM "$pid" 2>/dev/null || true

deadline=$((SECONDS + timeout_seconds))
while kill -0 "$pid" 2>/dev/null; do
  if (( SECONDS >= deadline )); then
    kill -KILL "$target" 2>/dev/null || kill -KILL "$pid" 2>/dev/null || true
    append_or_replace_state "STOP_SIGNAL" "SIGKILL"
    append_or_replace_state "STATUS" "stopped"
    append_or_replace_state "STOPPED_AT" "$(date -Iseconds)"
    echo "[ros1-stop] status=forced_stop"
    exit 0
  fi
  sleep 1
done

append_or_replace_state "STOP_SIGNAL" "SIGTERM"
append_or_replace_state "STATUS" "stopped"
append_or_replace_state "STOPPED_AT" "$(date -Iseconds)"
echo "[ros1-stop] status=stopped"
