#!/usr/bin/env bash
# Shelly Cloud API wrapper using the managed OpenClaw skills environment.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/shelly-config.sh"
load_shelly_skill_env

require_env() {
  local name="$1"
  if [[ -z "${!name:-}" ]]; then
    echo "Missing required env var: ${name}" >&2
    exit 1
  fi
}

require_env "SHELLY_CLOUD_SERVER_URI"
require_env "SHELLY_CLOUD_TOKEN"

json_out() {
  if command -v jq >/dev/null 2>&1; then
    jq .
  else
    cat
  fi
}

api_get() {
  local endpoint="$1"
  shift

  local args=(
    --silent
    --show-error
    --fail
    --get
    --data-urlencode "auth_key=${SHELLY_CLOUD_TOKEN}"
  )
  local kv
  for kv in "$@"; do
    args+=(--data-urlencode "$kv")
  done

  curl "${args[@]}" "${SHELLY_CLOUD_SERVER_URI}${endpoint}" | json_out
}

api_post() {
  local endpoint="$1"
  shift

  local args=(
    --silent
    --show-error
    --fail
    --request POST
    --data-urlencode "auth_key=${SHELLY_CLOUD_TOKEN}"
  )
  local kv
  for kv in "$@"; do
    args+=(--data-urlencode "$kv")
  done

  curl "${args[@]}" "${SHELLY_CLOUD_SERVER_URI}${endpoint}" | json_out
}

usage() {
  cat <<EOF
Usage:
  $(basename "$0") list
  $(basename "$0") status <device_id>
  $(basename "$0") relay <device_id> <on|off|toggle> [channel]
  $(basename "$0") thermostat <device_id> <channel> <temperature>
  $(basename "$0") raw <endpoint> [key=value ...]

Commands:
  list
    Read all device statuses via /device/all_status.

  status <device_id>
    Read one device via /device/status?id=<device_id>.

  relay <device_id> <on|off|toggle> [channel]
    Control a relay via /device/relay/control.
    Example: $(basename "$0") relay abc123 on 0

  thermostat <device_id> <channel> <temperature>
    Set target temperature for a BluTRV thermostat.
    Example: $(basename "$0") thermostat e5f17c9204ab 200 20.0

  raw <endpoint> [key=value ...]
    Perform a raw GET request against the configured Shelly cloud server.
    Example: $(basename "$0") raw /device/status id=abc123

Environment sources:
  ${ENV_FILES[0]}

Server:
  ${SHELLY_CLOUD_SERVER_URI}
EOF
}

cmd="${1:-}"
case "$cmd" in
  list)
    shift
    [[ $# -eq 0 ]] || { usage >&2; exit 2; }
    api_get "/device/all_status"
    ;;
  status)
    shift
    [[ $# -eq 1 ]] || { usage >&2; exit 2; }
    api_get "/device/status" "id=$1"
    ;;
  relay)
    shift
    [[ $# -ge 2 && $# -le 3 ]] || { usage >&2; exit 2; }
    case "$2" in
      on|off|toggle) ;;
      *) echo "Invalid relay action: $2" >&2; exit 2 ;;
    esac
    api_get "/device/relay/control" "id=$1" "turn=$2" "channel=${3:-0}"
    ;;
  thermostat)
    shift
    [[ $# -eq 3 ]] || { usage >&2; exit 2; }
    api_post "/device/thermostat/control" "id=$1" "channel=$2" "target_temp_c=$3"
    ;;
  raw)
    shift
    [[ $# -ge 1 ]] || { usage >&2; exit 2; }
    endpoint="$1"
    shift
    api_get "$endpoint" "$@"
    ;;
  help|-h|--help|"")
    usage
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    usage >&2
    exit 2
    ;;
esac
