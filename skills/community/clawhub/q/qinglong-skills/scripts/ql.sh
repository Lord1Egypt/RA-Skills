#!/usr/bin/env bash
# ============================================================
# QingLong Panel CLI Wrapper
# Usage: ql.sh <resource> <action> [options...]
# ============================================================
set -euo pipefail

# ── Environment Variables ────────────────────────────────────
QL_URL="${QINGLONG_URL:-}"
QL_CLIENT_ID="${QINGLONG_CLIENT_ID:-}"
QL_CLIENT_SECRET="${QINGLONG_CLIENT_SECRET:-}"
TOKEN_CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/qinglong"
TOKEN_CACHE_FILE="$TOKEN_CACHE_DIR/token"

# ── Colors ───────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# ── Helpers ──────────────────────────────────────────────────
die() { echo -e "${RED}Error: $*${NC}" >&2; exit 1; }
info() { echo -e "${CYAN}$*${NC}"; }
success() { echo -e "${GREEN}$*${NC}"; }

check_deps() {
  for cmd in curl jq; do
    command -v "$cmd" &>/dev/null || die "Required command '$cmd' not found"
  done
}

check_env() {
  [[ -z "$QL_URL" ]] && die "QINGLONG_URL is not set"
  [[ -z "$QL_CLIENT_ID" ]] && die "QINGLONG_CLIENT_ID is not set"
  [[ -z "$QL_CLIENT_SECRET" ]] && die "QINGLONG_CLIENT_SECRET is not set"
  # Remove trailing slash
  QL_URL="${QL_URL%/}"
}

# ── Token Management ────────────────────────────────────────
get_cached_token() {
  if [[ -f "$TOKEN_CACHE_FILE" ]]; then
    local cached_expiration
    cached_expiration=$(jq -r '.expiration // 0' "$TOKEN_CACHE_FILE" 2>/dev/null || echo 0)
    local now
    now=$(date +%s)
    # Refresh if expired or expiring within 60 seconds
    if (( cached_expiration > now + 60 )); then
      jq -r '.token' "$TOKEN_CACHE_FILE" 2>/dev/null
      return 0
    fi
  fi
  return 1
}

fetch_new_token() {
  mkdir -p "$TOKEN_CACHE_DIR"
  local response
  response=$(curl -sf "${QL_URL}/open/auth/token?client_id=${QL_CLIENT_ID}&client_secret=${QL_CLIENT_SECRET}" 2>&1) || \
    die "Failed to connect to QingLong at ${QL_URL}"

  local code
  code=$(echo "$response" | jq -r '.code // 0' 2>/dev/null)
  if [[ "$code" != "200" ]]; then
    local msg
    msg=$(echo "$response" | jq -r '.message // "Unknown error"' 2>/dev/null)
    die "Auth failed (code ${code}): ${msg}"
  fi

  local token expiration
  token=$(echo "$response" | jq -r '.data.token')
  expiration=$(echo "$response" | jq -r '.data.expiration')

  echo "{\"token\":\"${token}\",\"expiration\":${expiration}}" > "$TOKEN_CACHE_FILE"
  echo "$token"
}

get_token() {
  local token
  token=$(get_cached_token 2>/dev/null) || token=$(fetch_new_token)
  echo "$token"
}

# ── API Call ─────────────────────────────────────────────────
api() {
  local method="$1" path="$2"
  shift 2
  local data="" query=""

  # Parse remaining arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --data) data="$2"; shift 2 ;;
      --query) query="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  local token
  token=$(get_token)

  local url="${QL_URL}/open${path}"
  [[ -n "$query" ]] && url="${url}?${query}"

  local args=(-sf -X "$method" -H "Authorization: Bearer $token" -H "Content-Type: application/json")
  [[ -n "$data" ]] && args+=(-d "$data")

  local response http_code
  response=$(curl "${args[@]}" -w "\n%{http_code}" "$url" 2>&1) || \
    die "Request failed: ${url}"

  http_code=$(echo "$response" | tail -1)
  local body
  body=$(echo "$response" | sed '$d')

  if [[ "$http_code" -ge 400 ]]; then
    echo "$body" | jq . 2>/dev/null || echo "$body"
    return 1
  fi

  echo "$body" | jq . 2>/dev/null || echo "$body"
}

# ── Resource Handlers ────────────────────────────────────────

# ── Cron Jobs ────────────────────────────────────────────────
handle_cron() {
  local action="${1:-list}"; shift 2>/dev/null || true

  case "$action" in
    list)
      api GET "/crons"
      ;;
    get)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh cron get <id>"
      api GET "/crons/detail" --query "id=$1"
      ;;
    create)
      local command="" schedule="" name="" labels=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --command) command="$2"; shift 2 ;;
          --schedule) schedule="$2"; shift 2 ;;
          --name) name="$2"; shift 2 ;;
          --labels) labels="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      [[ -z "$command" ]] && die "Usage: ql.sh cron create --command <cmd> --schedule <cron_expr> [--name <name>]"
      [[ -z "$schedule" ]] && die "--schedule is required"
      local payload="{\"command\":\"$(echo "$command" | sed 's/"/\\"/g')\",\"schedule\":\"${schedule}\"}"
      [[ -n "$name" ]] && payload=$(echo "$payload" | jq --arg n "$name" '. + {name: $n}')
      [[ -n "$labels" ]] && payload=$(echo "$payload" | jq --arg l "$labels" '. + {labels: ($l | split(","))}')
      api POST "/crons" --data "$payload"
      ;;
    update)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh cron update <id> [--command <cmd>] [--schedule <expr>] [--name <name>]"
      local id="$1"; shift
      local payload="{\"id\":${id}}"
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --command) payload=$(echo "$payload" | jq --arg c "$2" '. + {command: $c}'); shift 2 ;;
          --schedule) payload=$(echo "$payload" | jq --arg s "$2" '. + {schedule: $s}'); shift 2 ;;
          --name) payload=$(echo "$payload" | jq --arg n "$2" '. + {name: $n}'); shift 2 ;;
          *) shift ;;
        esac
      done
      api PUT "/crons" --data "$payload"
      ;;
    delete)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh cron delete <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api DELETE "/crons" --data "$ids"
      ;;
    run)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh cron run <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api PUT "/crons/run" --data "$ids"
      ;;
    stop)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh cron stop <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api PUT "/crons/stop" --data "$ids"
      ;;
    enable)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh cron enable <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api PUT "/crons/enable" --data "$ids"
      ;;
    disable)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh cron disable <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api PUT "/crons/disable" --data "$ids"
      ;;
    pin)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh cron pin <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api PUT "/crons/pin" --data "$ids"
      ;;
    unpin)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh cron unpin <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api PUT "/crons/unpin" --data "$ids"
      ;;
    log)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh cron log <id>"
      api GET "/crons/$1/log"
      ;;
    logs)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh cron logs <id>"
      api GET "/crons/$1/logs"
      ;;
    *)
      die "Unknown cron action: $action (available: list|get|create|update|delete|run|stop|enable|disable|pin|unpin|log|logs)"
      ;;
  esac
}

# ── Environment Variables ────────────────────────────────────
handle_env() {
  local action="${1:-list}"; shift 2>/dev/null || true

  case "$action" in
    list)
      local search="${1:-}"
      if [[ -n "$search" ]]; then
        api GET "/envs" --query "searchValue=${search}"
      else
        api GET "/envs"
      fi
      ;;
    get)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh env get <id>"
      api GET "/envs/$1"
      ;;
    create)
      local name="" value="" remarks=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --name) name="$2"; shift 2 ;;
          --value) value="$2"; shift 2 ;;
          --remarks) remarks="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      [[ -z "$name" ]] && die "--name is required"
      [[ -z "$value" ]] && die "--value is required"
      local payload="[{\"name\":\"${name}\",\"value\":\"$(echo "$value" | sed 's/"/\\"/g')\""
      [[ -n "$remarks" ]] && payload+=",\"remarks\":\"${remarks}\""
      payload+="}]"
      api POST "/envs" --data "$payload"
      ;;
    update)
      local id="" name="" value="" remarks=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --id) id="$2"; shift 2 ;;
          --name) name="$2"; shift 2 ;;
          --value) value="$2"; shift 2 ;;
          --remarks) remarks="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      [[ -z "$id" ]] && die "--id is required"
      [[ -z "$name" ]] && die "--name is required"
      [[ -z "$value" ]] && die "--value is required"
      local payload="{\"id\":${id},\"name\":\"${name}\",\"value\":\"$(echo "$value" | sed 's/"/\\"/g')\""
      [[ -n "$remarks" ]] && payload+=",\"remarks\":\"${remarks}\""
      payload+="}"
      api PUT "/envs" --data "$payload"
      ;;
    delete)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh env delete <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api DELETE "/envs" --data "$ids"
      ;;
    enable)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh env enable <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api PUT "/envs/enable" --data "$ids"
      ;;
    disable)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh env disable <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api PUT "/envs/disable" --data "$ids"
      ;;
    *)
      die "Unknown env action: $action (available: list|get|create|update|delete|enable|disable)"
      ;;
  esac
}

# ── Scripts ──────────────────────────────────────────────────
handle_script() {
  local action="${1:-list}"; shift 2>/dev/null || true

  case "$action" in
    list)
      local path="${1:-}"
      if [[ -n "$path" ]]; then
        api GET "/scripts" --query "path=${path}"
      else
        api GET "/scripts"
      fi
      ;;
    get)
      local file="" path=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --file) file="$2"; shift 2 ;;
          --path) path="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      [[ -z "$file" ]] && die "--file is required"
      local query="file=${file}"
      [[ -n "$path" ]] && query+="&path=${path}"
      api GET "/scripts/detail" --query "$query"
      ;;
    save)
      local file="" content="" path=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --file) file="$2"; shift 2 ;;
          --content) content="$2"; shift 2 ;;
          --path) path="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      [[ -z "$file" ]] && die "--file is required"
      [[ -z "$content" ]] && die "--content is required"
      local payload="{\"filename\":\"${file}\",\"content\":\"$(echo "$content" | sed 's/"/\\"/g' | sed 's/\n/\\n/g')\"}"
      [[ -n "$path" ]] && payload=$(echo "$payload" | jq --arg p "$path" '. + {path: $p}')
      api PUT "/scripts" --data "$payload"
      ;;
    run)
      local file="" content="" path=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --file) file="$2"; shift 2 ;;
          --content) content="$2"; shift 2 ;;
          --path) path="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      [[ -z "$file" ]] && die "--file is required"
      local payload="{\"filename\":\"${file}\"}"
      [[ -n "$content" ]] && payload=$(echo "$payload" | jq --arg c "$(echo "$content" | sed 's/"/\\"/g')" '. + {content: $c}')
      [[ -n "$path" ]] && payload=$(echo "$payload" | jq --arg p "$path" '. + {path: $p}')
      api PUT "/scripts/run" --data "$payload"
      ;;
    stop)
      local file="" path=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --file) file="$2"; shift 2 ;;
          --path) path="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      [[ -z "$file" ]] && die "--file is required"
      local payload="{\"filename\":\"${file}\"}"
      [[ -n "$path" ]] && payload=$(echo "$payload" | jq --arg p "$path" '. + {path: $p}')
      api PUT "/scripts/stop" --data "$payload"
      ;;
    delete)
      local file="" path=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --file) file="$2"; shift 2 ;;
          --path) path="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      [[ -z "$file" ]] && die "--file is required"
      local payload="{\"filename\":\"${file}\"}"
      [[ -n "$path" ]] && payload=$(echo "$payload" | jq --arg p "$path" '. + {path: $p}')
      api DELETE "/scripts" --data "$payload"
      ;;
    *)
      die "Unknown script action: $action (available: list|get|save|run|stop|delete)"
      ;;
  esac
}

# ── Dependencies ─────────────────────────────────────────────
handle_dep() {
  local action="${1:-list}"; shift 2>/dev/null || true

  case "$action" in
    list)
      local search="" type="" status=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --search) search="$2"; shift 2 ;;
          --type) type="$2"; shift 2 ;;
          --status) status="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      local query_parts=()
      [[ -n "$search" ]] && query_parts+=("searchValue=${search}")
      [[ -n "$type" ]] && query_parts+=("type=${type}")
      [[ -n "$status" ]] && query_parts+=("status=${status}")
      local query=""
      [[ ${#query_parts[@]} -gt 0 ]] && query=$(IFS='&'; echo "${query_parts[*]}")
      if [[ -n "$query" ]]; then
        api GET "/dependencies" --query "$query"
      else
        api GET "/dependencies"
      fi
      ;;
    get)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh dep get <id>"
      api GET "/dependencies/$1"
      ;;
    install)
      local name="" type="" remark=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --name) name="$2"; shift 2 ;;
          --type) type="$2"; shift 2 ;;
          --remark) remark="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      [[ -z "$name" ]] && die "--name is required"
      [[ -z "$type" ]] && die "--type is required (0=node, 1=linux, 2=python3)"
      local payload="[{\"name\":\"${name}\",\"type\":${type}"
      [[ -n "$remark" ]] && payload+=",\"remark\":\"${remark}\""
      payload+="}]"
      api POST "/dependencies" --data "$payload"
      ;;
    reinstall)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh dep reinstall <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api PUT "/dependencies/reinstall" --data "$ids"
      ;;
    cancel)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh dep cancel <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api PUT "/dependencies/cancel" --data "$ids"
      ;;
    delete)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh dep delete <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api DELETE "/dependencies" --data "$ids"
      ;;
    *)
      die "Unknown dep action: $action (available: list|get|install|reinstall|cancel|delete)"
      ;;
  esac
}

# ── Subscriptions ────────────────────────────────────────────
handle_sub() {
  local action="${1:-list}"; shift 2>/dev/null || true

  case "$action" in
    list)
      api GET "/subscriptions"
      ;;
    get)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh sub get <id>"
      api GET "/subscriptions/$1"
      ;;
    run)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh sub run <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api PUT "/subscriptions/run" --data "$ids"
      ;;
    stop)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh sub stop <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api PUT "/subscriptions/stop" --data "$ids"
      ;;
    enable)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh sub enable <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api PUT "/subscriptions/enable" --data "$ids"
      ;;
    disable)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh sub disable <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api PUT "/subscriptions/disable" --data "$ids"
      ;;
    delete)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh sub delete <id> [id...]"
      local ids
      ids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
      api DELETE "/subscriptions" --data "$ids"
      ;;
    log)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh sub log <id>"
      api GET "/subscriptions/$1/log"
      ;;
    *)
      die "Unknown sub action: $action (available: list|get|run|stop|enable|disable|delete|log)"
      ;;
  esac
}

# ── Logs ─────────────────────────────────────────────────────
handle_log() {
  local action="${1:-list}"; shift 2>/dev/null || true

  case "$action" in
    list)
      api GET "/logs"
      ;;
    get)
      local file="" path=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --file) file="$2"; shift 2 ;;
          --path) path="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      [[ -z "$file" ]] && die "--file is required"
      local query=""
      [[ -n "$path" ]] && query="path=${path}"
      if [[ -n "$query" ]]; then
        api GET "/logs/${file}" --query "$query"
      else
        api GET "/logs/${file}"
      fi
      ;;
    detail)
      local file="" path=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --file) file="$2"; shift 2 ;;
          --path) path="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      [[ -z "$file" ]] && die "--file is required"
      local query="file=${file}"
      [[ -n "$path" ]] && query+="&path=${path}"
      api GET "/logs/detail" --query "$query"
      ;;
    delete)
      local file="" path=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --file) file="$2"; shift 2 ;;
          --path) path="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      [[ -z "$file" ]] && die "--file is required"
      local payload="{\"filename\":\"${file}\"}"
      [[ -n "$path" ]] && payload=$(echo "$payload" | jq --arg p "$path" '. + {path: $p}')
      api DELETE "/logs" --data "$payload"
      ;;
    *)
      die "Unknown log action: $action (available: list|get|detail|delete)"
      ;;
  esac
}

# ── System ───────────────────────────────────────────────────
handle_system() {
  local action="${1:-info}"; shift 2>/dev/null || true

  case "$action" in
    info)
      api GET "/system"
      ;;
    config)
      api GET "/system/config"
      ;;
    check-update)
      api PUT "/system/update-check"
      ;;
    update)
      api PUT "/system/update"
      ;;
    reload)
      local type="${1:-}"
      if [[ -n "$type" ]]; then
        api PUT "/system/reload" --data "{\"type\":\"${type}\"}"
      else
        api PUT "/system/reload"
      fi
      ;;
    command-run)
      local command=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --command) command="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      [[ -z "$command" ]] && die "--command is required"
      api PUT "/system/command-run" --data "{\"command\":\"$(echo "$command" | sed 's/"/\\"/g')\"}"
      ;;
    command-stop)
      local command="" pid=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --command) command="$2"; shift 2 ;;
          --pid) pid="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      local payload="{"
      [[ -n "$command" ]] && payload+="\"command\":\"${command}\""
      [[ -n "$pid" ]] && [[ -n "$command" ]] && payload+=","
      [[ -n "$pid" ]] && payload+="\"pid\":${pid}"
      payload+="}"
      api PUT "/system/command-stop" --data "$payload"
      ;;
    auth-reset)
      local username="" password=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --username) username="$2"; shift 2 ;;
          --password) password="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      local payload="{"
      [[ -n "$username" ]] && payload+="\"username\":\"${username}\""
      [[ -n "$password" ]] && [[ -n "$username" ]] && payload+=","
      [[ -n "$password" ]] && payload+="\"password\":\"${password}\""
      payload+="}"
      api PUT "/system/auth/reset" --data "$payload"
      ;;
    *)
      die "Unknown system action: $action (available: info|config|check-update|update|reload|command-run|command-stop|auth-reset)"
      ;;
  esac
}

# ── Config Files ─────────────────────────────────────────────
handle_config() {
  local action="${1:-list}"; shift 2>/dev/null || true

  case "$action" in
    files|list)
      api GET "/configs/files"
      ;;
    get)
      [[ -z "${1:-}" ]] && die "Usage: ql.sh config get <filename>"
      api GET "/configs/$1"
      ;;
    save)
      local name="" content=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --name) name="$2"; shift 2 ;;
          --content) content="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      [[ -z "$name" ]] && die "--name is required"
      [[ -z "$content" ]] && die "--content is required"
      api POST "/configs/save" --data "{\"name\":\"${name}\",\"content\":\"$(echo "$content" | sed 's/"/\\"/g' | sed 's/\n/\\n/g')\"}"
      ;;
    sample)
      api GET "/configs/sample"
      ;;
    *)
      die "Unknown config action: $action (available: list|files|get|save|sample)"
      ;;
  esac
}

# ── Token (debug) ────────────────────────────────────────────
handle_token() {
  local action="${1:-get}"; shift 2>/dev/null || true

  case "$action" in
    get|refresh)
      rm -f "$TOKEN_CACHE_FILE"
      local token
      token=$(fetch_new_token)
      success "Token refreshed: ${token:0:16}..."
      ;;
    show)
      if [[ -f "$TOKEN_CACHE_FILE" ]]; then
        cat "$TOKEN_CACHE_FILE" | jq .
      else
        info "No cached token"
      fi
      ;;
    clear)
      rm -f "$TOKEN_CACHE_FILE"
      success "Token cache cleared"
      ;;
    *)
      die "Unknown token action: $action (available: get|refresh|show|clear)"
      ;;
  esac
}

# ── Main ─────────────────────────────────────────────────────
main() {
  check_deps
  check_env

  local resource="${1:-help}"; shift 2>/dev/null || true

  case "$resource" in
    cron)   handle_cron "$@" ;;
    env)    handle_env "$@" ;;
    script) handle_script "$@" ;;
    dep)    handle_dep "$@" ;;
    sub)    handle_sub "$@" ;;
    log)    handle_log "$@" ;;
    system) handle_system "$@" ;;
    config) handle_config "$@" ;;
    token)  handle_token "$@" ;;
    help|--help|-h)
      cat <<'EOF'
🐉 QingLong Panel CLI

Usage: ql.sh <resource> <action> [options...]

Resources:
  cron      Cron jobs (list|get|create|update|delete|run|stop|enable|disable|pin|unpin|log|logs)
  env       Environment variables (list|get|create|update|delete|enable|disable)
  script    Scripts (list|get|save|run|stop|delete)
  dep       Dependencies (list|get|install|reinstall|cancel|delete)
  sub       Subscriptions (list|get|run|stop|enable|disable|delete|log)
  log       Logs (list|get|detail|delete)
  system    System info and operations (info|config|check-update|update|reload|command-run|command-stop|auth-reset)
  config    Config files (list|get|save|sample)
  token     Token management (get|refresh|show|clear)

Environment Variables:
  QINGLONG_URL          Panel address (e.g. http://192.168.1.100:5700)
  QINGLONG_CLIENT_ID    Open API Client ID
  QINGLONG_CLIENT_SECRET Open API Client Secret

Examples:
  ql.sh cron list
  ql.sh cron create --command "task test.js" --schedule "0 0 * * *" --name "Daily Task"
  ql.sh env create --name "JD_COOKIE" --value "pt_key=xxx"
  ql.sh script run --file "test.js"
  ql.sh system info
EOF
      ;;
    *)
      die "Unknown resource: $resource (use 'ql.sh help' for usage)"
      ;;
  esac
}

main "$@"
