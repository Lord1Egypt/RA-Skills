#!/usr/bin/env zsh
set -euo pipefail

script_dir="${0:A:h}"
state_file=""
workspace_path=""
expected_nodes=()
expected_topics=()
expected_services=()
tail_lines="30"

print_help() {
  cat <<'EOF'
Usage: ros1_runtime_health_check.sh --state-file <path> [options]

Check whether a previously started ROS1 target is still alive and whether the ROS graph
contains the expected nodes, topics, and services.

Options:
  --state-file <path>       State file created by ros1_start_target.sh
  --workspace <path>        Optional workspace path when no state file is available
  --expect-node <name>      Expected node (repeatable)
  --expect-topic <name>     Expected topic (repeatable)
  --expect-service <name>   Expected service (repeatable)
  --tail-lines <n>          Number of log lines to show on failure, default: 30
  --help                    Show this help
EOF
}

require_state_var() {
  local name="$1"
  if [[ -z "${(P)name:-}" ]]; then
    echo "[ERROR] missing $name in state file" >&2
    exit 2
  fi
}

append_or_replace_state() {
  local key="$1"
  local value="$2"
  if [[ -f "$state_file" ]] && grep -q "^${key}=" "$state_file"; then
    sed -i "s|^${key}=.*|${key}=${(q)value}|" "$state_file"
  else
    print -r -- "${key}=${(q)value}" >> "$state_file"
  fi
}

classify_log_tail() {
  local log_file="$1"
  [[ -f "$log_file" ]] || { print -r -- "no_log_available"; return; }
  if tail -n "$tail_lines" "$log_file" | grep -Eqi 'RLException|Resource not found|cannot launch'; then
    print -r -- "launch_configuration_error"
  elif tail -n "$tail_lines" "$log_file" | grep -Eqi 'ImportError|ModuleNotFoundError|No module named'; then
    print -r -- "python_dependency_error"
  elif tail -n "$tail_lines" "$log_file" | grep -Eqi 'Traceback|FATAL|Segmentation fault|core dumped'; then
    print -r -- "runtime_crash"
  elif tail -n "$tail_lines" "$log_file" | grep -Eqi 'Address already in use'; then
    print -r -- "port_conflict"
  else
    print -r -- "unknown_runtime_failure"
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
    --workspace|--path)
      workspace_path="${2:-}"
      [[ -n "$workspace_path" ]] || { echo "[ERROR] missing value for $1" >&2; exit 2; }
      shift 2
      ;;
    --expect-node)
      expected_nodes+=("${2:-}")
      [[ -n "${expected_nodes[-1]}" ]] || { echo "[ERROR] missing value for --expect-node" >&2; exit 2; }
      shift 2
      ;;
    --expect-topic)
      expected_topics+=("${2:-}")
      [[ -n "${expected_topics[-1]}" ]] || { echo "[ERROR] missing value for --expect-topic" >&2; exit 2; }
      shift 2
      ;;
    --expect-service)
      expected_services+=("${2:-}")
      [[ -n "${expected_services[-1]}" ]] || { echo "[ERROR] missing value for --expect-service" >&2; exit 2; }
      shift 2
      ;;
    --tail-lines)
      tail_lines="${2:-}"
      [[ -n "$tail_lines" ]] || { echo "[ERROR] missing value for --tail-lines" >&2; exit 2; }
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
require_state_var "WORKSPACE_ROOT"
require_state_var "ROS_SETUP"
require_state_var "LOG_FILE"

workspace_root="$WORKSPACE_ROOT"
ros_setup="$ROS_SETUP"
workspace_setup="${WORKSPACE_SETUP:-}"
log_file="$LOG_FILE"
pid="${PID:-}"
prior_status="${STATUS:-unknown}"
ros_home="${ROS_HOME:-}"

if [[ -n "$workspace_path" ]]; then
  workspace_root="${workspace_path:A}"
fi

if [[ -n "$pid" ]]; then
  if ! kill -0 "$pid" 2>/dev/null; then
    related_pids=("${(@f)$(related_pids_for_ros_home "$ros_home")}")
    if (( ${#related_pids[@]} == 0 )); then
      failure_class="$(classify_log_tail "$log_file")"
      append_or_replace_state "STATUS" "stopped"
      append_or_replace_state "LAST_HEALTH" "dead"
      append_or_replace_state "FAILURE_CLASS" "$failure_class"
      append_or_replace_state "LAST_CHECKED_AT" "$(date -Iseconds)"
      echo "[ros1-health] status=dead"
      echo "[ros1-health] failure_class=$failure_class"
      echo "[ros1-health] state_file=$state_file"
      echo "[ros1-health] log_tail:"
      tail -n "$tail_lines" "$log_file" || true
      exit 1
    fi
    append_or_replace_state "ACTIVE_PIDS" "${related_pids[*]}"
  fi
fi

# shellcheck disable=SC1090
source "$ros_setup"
if [[ -n "$workspace_setup" && -f "$workspace_setup" ]]; then
  # shellcheck disable=SC1090
  source "$workspace_setup"
fi

missing=()

if ! rosnode list >/dev/null 2>&1; then
  append_or_replace_state "LAST_HEALTH" "ros_master_unreachable"
  append_or_replace_state "LAST_CHECKED_AT" "$(date -Iseconds)"
  echo "[ros1-health] status=unreachable"
  echo "[ros1-health] failure_class=ros_master_unreachable"
  exit 1
fi

for node in "${expected_nodes[@]}"; do
  rosnode list | grep -Fx -- "$node" >/dev/null 2>&1 || missing+=("node:$node")
done

for topic in "${expected_topics[@]}"; do
  rostopic list | grep -Fx -- "$topic" >/dev/null 2>&1 || missing+=("topic:$topic")
done

for service in "${expected_services[@]}"; do
  rosservice list | grep -Fx -- "$service" >/dev/null 2>&1 || missing+=("service:$service")
done

append_or_replace_state "LAST_CHECKED_AT" "$(date -Iseconds)"

if (( ${#missing[@]} > 0 )); then
  append_or_replace_state "LAST_HEALTH" "degraded"
  append_or_replace_state "FAILURE_CLASS" "graph_expectation_missing"
  append_or_replace_state "MISSING" "${missing[*]}"
  echo "[ros1-health] status=degraded"
  echo "[ros1-health] failure_class=graph_expectation_missing"
  for item in "${missing[@]}"; do
    echo "[ros1-health] missing=$item"
  done
  if [[ -f "$log_file" ]]; then
    echo "[ros1-health] recent_log_tail:"
    tail -n "$tail_lines" "$log_file" || true
  fi
  exit 1
fi

append_or_replace_state "LAST_HEALTH" "healthy"
append_or_replace_state "FAILURE_CLASS" ""
append_or_replace_state "MISSING" ""
echo "[ros1-health] status=healthy"
echo "[ros1-health] pid=${pid:-unknown}"
if [[ -n "$ros_home" ]]; then
  active_pids=("${(@f)$(related_pids_for_ros_home "$ros_home")}")
  if (( ${#active_pids[@]} > 0 )); then
    append_or_replace_state "ACTIVE_PIDS" "${active_pids[*]}"
    echo "[ros1-health] active_pids=${active_pids[*]}"
  fi
fi
echo "[ros1-health] prior_status=$prior_status"
if (( ${#expected_nodes[@]} > 0 || ${#expected_topics[@]} > 0 || ${#expected_services[@]} > 0 )); then
  echo "[ros1-health] expectations_met=true"
fi
