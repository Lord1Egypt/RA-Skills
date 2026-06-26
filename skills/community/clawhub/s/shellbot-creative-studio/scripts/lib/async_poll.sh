#!/usr/bin/env bash
# shellbot-creative-studio — async task polling
# Generic polling loop that works across Freepik and fal.ai.

# Poll an async task until completion or timeout
# Usage: poll_task <provider> <task_id> [<endpoint>] [--max-wait 300] [--interval 3]
# Returns: JSON result to stdout
poll_task() {
  local provider="$1"
  local task_id="$2"
  local endpoint="${3:-}"
  shift 3 2>/dev/null || true

  local max_wait=300
  local interval=3

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --max-wait) max_wait="$2"; shift 2 ;;
      --interval) interval="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  local elapsed=0
  local status_url=""
  local auth_header=""

  case "$provider" in
    freepik)
      # Freepik polls at the same endpoint as submission + /{task_id}
      # The caller MUST pass the submission endpoint as $3
      if [[ -n "$endpoint" ]]; then
        status_url="${endpoint}/${task_id}"
      else
        status_url="https://api.freepik.com/v1/ai/generation/${task_id}"
      fi
      auth_header="x-freepik-api-key: ${FREEPIK_API_KEY}"
      ;;
    fal)
      # fal uses the original endpoint + /requests/<task_id>/status
      if [[ -n "$endpoint" ]]; then
        status_url="${endpoint}/requests/${task_id}/status"
      else
        status_url="https://queue.fal.run/fal-ai/flux-2/requests/${task_id}/status"
      fi
      auth_header="Authorization: Key ${FAL_API_KEY}"
      ;;
    *)
      log_error "Polling not supported for provider: ${provider}"
      return 1
      ;;
  esac

  log_info "Polling ${provider} task ${task_id}..."

  while [[ $elapsed -lt $max_wait ]]; do
    local response
    response=$(curl -sf -H "$auth_header" "$status_url" 2>/dev/null) || true

    if [[ -z "$response" ]]; then
      sleep "$interval"
      elapsed=$((elapsed + interval))
      continue
    fi

    local status
    case "$provider" in
      freepik)
        status=$(echo "$response" | jq -r '.data.status // .status // "unknown"' 2>/dev/null)
        ;;
      fal)
        status=$(echo "$response" | jq -r '.status // "unknown"' 2>/dev/null)
        ;;
    esac

    case "$status" in
      COMPLETED|completed|succeeded|SUCCEEDED)
        log_ok "Task completed"
        # For fal, fetch the actual result
        if [[ "$provider" == "fal" ]]; then
          local result_url="${endpoint}/requests/${task_id}"
          response=$(curl -sf -H "$auth_header" "$result_url" 2>/dev/null)
        fi
        echo "$response"
        return 0
        ;;
      FAILED|failed|error|ERROR)
        log_error "Task failed"
        echo "$response"
        return 1
        ;;
      *)
        local pct
        pct=$(echo "$response" | jq -r '.progress // .data.progress // ""' 2>/dev/null)
        if [[ -n "$pct" && "$pct" != "null" ]]; then
          log_info "Status: ${status} (${pct}%) — ${elapsed}s elapsed"
        else
          log_info "Status: ${status} — ${elapsed}s elapsed"
        fi
        ;;
    esac

    sleep "$interval"
    elapsed=$((elapsed + interval))
  done

  log_error "Timed out after ${max_wait}s"
  json_error "Task ${task_id} timed out after ${max_wait}s"
}
