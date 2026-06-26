#!/usr/bin/env bash
# Read Shelly BluTRV status via local RPC and fall back to Shelly Cloud.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/shelly-config.sh"
load_shelly_skill_env

DEFAULT_CONNECT_TIMEOUT=2
DEFAULT_MAX_TIME=8
DEFAULT_RETRIES=1
DEFAULT_CACHE_TTL=15
CLOUD_CACHE_FILE="/tmp/shelly-cloud-all-status.json"
CLOUD_CACHE_LOCK="/tmp/shelly-cloud-all-status.lock"
LAST_LOCAL_ERROR=""

usage() {
  cat <<'EOF'
Usage:
  blutrv-status.sh <target-alias> [--retries N]
  blutrv-status.sh <gateway_ip> <trv_id> [--retries N] [--gateway-device-id ID]

Examples:
  blutrv-status.sh schlafzimmer
  blutrv-status.sh office-radiator
  blutrv-status.sh 192.168.0.101 200
  blutrv-status.sh 192.168.0.102 202 --retries 2
  blutrv-status.sh 192.168.0.102 200 --gateway-device-id e5f17c9204ab

Behavior:
  - Tries local RPC first with strict timeouts
  - Falls back to Shelly Cloud device status when local RPC fails
  - Returns normalized JSON with source=local or source=cloud
  - Retries the local RPC once by default because BluTRV/Bluetooth can be sleepy
EOF
}

is_ipv4() {
  [[ "${1:-}" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]]
}

if [[ $# -lt 1 ]]; then
  usage >&2
  exit 2
fi

gateway_ip=""
trv_id=""
target_alias=""
target_device_id=""
gateway_key=""

if is_ipv4 "$1"; then
  [[ $# -ge 2 ]] || { usage >&2; exit 2; }
  gateway_ip="$1"
  trv_id="$2"
  shift 2
else
  target_alias="$1"
  read -r _resolved_aliases gateway_key gateway_ip trv_id target_device_id <<<"$(shelly_resolve_target_alias "$target_alias")" || {
    echo "Unknown target alias: $target_alias" >&2
    usage >&2
    exit 2
  }
  shift 1
fi

retries="$DEFAULT_RETRIES"
gateway_device_id=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --retries)
      [[ $# -ge 2 ]] || { echo "Missing value for --retries" >&2; exit 2; }
      retries="$2"
      shift 2
      ;;
    --gateway-device-id)
      [[ $# -ge 2 ]] || { echo "Missing value for --gateway-device-id" >&2; exit 2; }
      gateway_device_id="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if ! [[ "$trv_id" =~ ^[0-9]+$ ]]; then
  echo "TRV id must be numeric: $trv_id" >&2
  exit 2
fi

if ! [[ "$retries" =~ ^[0-9]+$ ]]; then
  echo "Retries must be numeric: $retries" >&2
  exit 2
fi

if [[ -z "$gateway_device_id" ]]; then
  gateway_device_id="$(shelly_gateway_device_id_for_ip "$gateway_ip" || true)"
fi

payload=$(printf '{"method":"BluTrv.GetRemoteStatus","params":{"id":%s}}' "$trv_id")
url="http://${gateway_ip}/rpc"

json_out() {
  if command -v jq >/dev/null 2>&1; then
    jq .
  else
    cat
  fi
}

local_status() {
  local attempt=0
  local response=""
  local stderr_file=""

  while :; do
    attempt=$((attempt + 1))
    stderr_file=$(mktemp)
    if response=$(
      curl \
        --silent \
        --show-error \
        --fail \
        --connect-timeout "$DEFAULT_CONNECT_TIMEOUT" \
        --max-time "$DEFAULT_MAX_TIME" \
        --header "Content-Type: application/json" \
        --request POST \
        --data "$payload" \
        "$url" \
        2>"$stderr_file"
    ); then
      rm -f "$stderr_file"
      if command -v jq >/dev/null 2>&1; then
        jq \
          --arg gateway_ip "$gateway_ip" \
          --arg gateway_device_id "$gateway_device_id" \
          --argjson trv_id "$trv_id" \
          '{
            source: "local",
            gateway_ip: $gateway_ip,
            gateway_device_id: (if $gateway_device_id == "" then null else $gateway_device_id end),
            trv_id: $trv_id,
            room_temperature_C: (.result.status["temperature:0"].tC // null),
            current_C: (.result.status["trv:0"].current_C // null),
            target_C: (.result.status["trv:0"].target_C // null),
            battery_percent: null,
            connected: true
          }' <<<"$response"
      else
        printf '%s\n' "$response"
      fi
      return 0
    fi

    LAST_LOCAL_ERROR="$(cat "$stderr_file" 2>/dev/null || true)"
    rm -f "$stderr_file"

    if (( attempt > retries )); then
      return 1
    fi

    sleep 2
  done
}

cloud_cache_fresh() {
  [[ -f "$CLOUD_CACHE_FILE" ]] || return 1
  local now mtime age
  now=$(date +%s)
  mtime=$(stat -c %Y "$CLOUD_CACHE_FILE" 2>/dev/null || echo 0)
  age=$((now - mtime))
  (( age <= DEFAULT_CACHE_TTL ))
}

refresh_cloud_cache() {
  mkdir -p "$(dirname "$CLOUD_CACHE_FILE")"

  if command -v flock >/dev/null 2>&1; then
    exec 9>"$CLOUD_CACHE_LOCK"
    flock 9
    if ! cloud_cache_fresh; then
      "${SCRIPT_DIR}/shelly-cloud.sh" list >"$CLOUD_CACHE_FILE.tmp"
      mv "$CLOUD_CACHE_FILE.tmp" "$CLOUD_CACHE_FILE"
    fi
    flock -u 9
    exec 9>&-
    return 0
  fi

  if ! cloud_cache_fresh; then
    "${SCRIPT_DIR}/shelly-cloud.sh" list >"$CLOUD_CACHE_FILE.tmp"
    mv "$CLOUD_CACHE_FILE.tmp" "$CLOUD_CACHE_FILE"
  fi
}

cloud_status() {
  [[ -n "$gateway_device_id" ]] || {
    echo "Cloud fallback unavailable: no gateway device id for ${gateway_ip}" >&2
    return 1
  }

  command -v jq >/dev/null 2>&1 || {
    echo "Cloud fallback unavailable: jq not installed" >&2
    return 1
  }

  refresh_cloud_cache

  jq \
    --arg gateway_ip "$gateway_ip" \
    --arg gateway_device_id "$gateway_device_id" \
    --argjson trv_id "$trv_id" \
    '
      .data.devices_status[$gateway_device_id] as $gw
      | if $gw == null then
          error("Gateway not present in Shelly Cloud list: " + $gateway_device_id)
        else
          {
            source: "cloud",
            gateway_ip: $gateway_ip,
            gateway_device_id: $gateway_device_id,
            trv_id: $trv_id,
            trv_device_id: ($gw["blutrv_rinfo:\($trv_id)"].device_info.id // null),
            room_temperature_C: ($gw["blutrv_rstatus:\($trv_id)"].status["temperature:0"].tC // null),
            current_C: (
              $gw["blutrv_rstatus:\($trv_id)"].status["trv:0"].current_C
              // $gw["blutrv:\($trv_id)"].current_C
              // null
            ),
            target_C: (
              $gw["blutrv_rstatus:\($trv_id)"].status["trv:0"].target_C
              // $gw["blutrv:\($trv_id)"].target_C
              // null
            ),
            battery_percent: ($gw["blutrv:\($trv_id)"].battery // null),
            connected: ($gw["blutrv:\($trv_id)"].connected // null),
            rssi: ($gw["blutrv:\($trv_id)"].rssi // null),
            updated_at: ($gw._updated // null)
          }
        end
    ' "$CLOUD_CACHE_FILE"
}

if local_status; then
  exit 0
fi

cloud_error=""
if cloud_output=$(cloud_status 2>&1); then
  printf '%s\n' "$cloud_output" | json_out
  exit 0
fi
cloud_error="$cloud_output"

echo "BluTRV status request failed after local timeout and cloud fallback failure: gateway=${gateway_ip} trv_id=${trv_id}" >&2
if [[ -n "$LAST_LOCAL_ERROR" ]]; then
  printf '%s\n' "$LAST_LOCAL_ERROR" >&2
fi
if [[ -n "$cloud_error" ]]; then
  printf '%s\n' "$cloud_error" >&2
fi
exit 1
