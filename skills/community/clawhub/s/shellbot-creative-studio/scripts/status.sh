#!/usr/bin/env bash
# shellbot-creative-studio — async task status checker
# Usage: status [--task-id <id>] [--provider freepik|fal] [--all]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/config.sh"
source "${SCRIPT_DIR}/lib/output.sh"
source "${SCRIPT_DIR}/lib/provider_router.sh"
source "${SCRIPT_DIR}/lib/task_log.sh"

TASK_ID=""
PROVIDER=""
SHOW_ALL=false

usage() {
  cat >&2 <<'EOF'
Usage: status [options]

Options:
  --task-id   Specific task ID to check
  --provider  Provider for the task: freepik, fal
  --all       Show all tracked tasks from the task log
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --task-id)  TASK_ID="$2"; shift 2 ;;
    --provider) PROVIDER="$2"; shift 2 ;;
    --all)      SHOW_ALL=true; shift ;;
    -h|--help)  usage; exit 0 ;;
    *)          log_error "Unknown option: $1"; usage; exit 1 ;;
  esac
done

# Show all tracked tasks
if [[ "$SHOW_ALL" == "true" ]]; then
  log_info "All tracked tasks:"
  list_tasks
  exit 0
fi

# Check specific task
if [[ -z "$TASK_ID" ]]; then
  log_error "Specify --task-id or --all"
  usage
  exit 1
fi

# Try to find provider from task log if not specified
if [[ -z "$PROVIDER" ]]; then
  local_entry=$(get_task "$TASK_ID")
  if [[ -n "$local_entry" && "$local_entry" != "{}" ]]; then
    PROVIDER=$(echo "$local_entry" | jq -r '.provider // empty')
  fi
fi

if [[ -z "$PROVIDER" ]]; then
  log_error "Cannot determine provider. Use --provider to specify."
  exit 1
fi

log_info "Checking ${PROVIDER} task ${TASK_ID}..."

case "$PROVIDER" in
  freepik)
    require_provider_key freepik
    local api_key
    api_key=$(get_provider_key freepik)
    response=$(curl -sf "https://api.freepik.com/v1/ai/generation/${TASK_ID}" \
      -H "x-freepik-api-key: ${api_key}" 2>/dev/null) || true
    ;;
  fal)
    require_provider_key fal
    local api_key
    api_key=$(get_provider_key fal)
    response=$(curl -sf "https://queue.fal.run/fal-ai/flux-2/requests/${TASK_ID}/status?logs=1" \
      -H "Authorization: Key ${api_key}" 2>/dev/null) || true
    ;;
  *)
    json_error "Cannot check status for provider: ${PROVIDER}"
    ;;
esac

if [[ -z "${response:-}" ]]; then
  json_error "No response from ${PROVIDER} for task ${TASK_ID}"
fi

echo "$response" | jq .
