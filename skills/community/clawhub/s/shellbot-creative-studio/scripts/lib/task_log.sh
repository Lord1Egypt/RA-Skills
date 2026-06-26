#!/usr/bin/env bash
# shellbot-creative-studio — JSONL task tracking
# Appends task entries to a per-project log file for pipeline orchestration.

# Append a task entry to the log
# Usage: log_task <task_id> <provider> <command> <status> [output_file]
log_task() {
  local task_id="$1"
  local provider="$2"
  local command="$3"
  local status="$4"
  local output_file="${5:-}"
  local log_dir="${CREATIVE_OUTPUT_DIR:-$DEFAULT_OUTPUT_DIR}"
  local log_file="${log_dir}/${TASK_LOG_FILE}"

  mkdir -p "$log_dir"
  printf '{"task_id":"%s","provider":"%s","command":"%s","status":"%s","output_file":"%s","timestamp":"%s"}\n' \
    "$task_id" "$provider" "$command" "$status" "$output_file" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    >> "$log_file"
}

# Look up a task by ID
# Usage: get_task <task_id>
get_task() {
  local task_id="$1"
  local log_dir="${CREATIVE_OUTPUT_DIR:-$DEFAULT_OUTPUT_DIR}"
  local log_file="${log_dir}/${TASK_LOG_FILE}"

  if [[ ! -f "$log_file" ]]; then
    echo "{}"
    return
  fi

  # Return the most recent entry for this task_id
  grep "\"task_id\":\"${task_id}\"" "$log_file" | tail -1
}

# List all tasks, optionally filtered by status
# Usage: list_tasks [--status pending|completed|failed] [--command image|video|...]
list_tasks() {
  local filter_status=""
  local filter_command=""
  local log_dir="${CREATIVE_OUTPUT_DIR:-$DEFAULT_OUTPUT_DIR}"
  local log_file="${log_dir}/${TASK_LOG_FILE}"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --status) filter_status="$2"; shift 2 ;;
      --command) filter_command="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  if [[ ! -f "$log_file" ]]; then
    echo "[]"
    return
  fi

  local jq_filter="."
  if [[ -n "$filter_status" ]]; then
    jq_filter="${jq_filter} | select(.status == \"${filter_status}\")"
  fi
  if [[ -n "$filter_command" ]]; then
    jq_filter="${jq_filter} | select(.command == \"${filter_command}\")"
  fi

  jq -s "[.[] | ${jq_filter}]" "$log_file"
}
