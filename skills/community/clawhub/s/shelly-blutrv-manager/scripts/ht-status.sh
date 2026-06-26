#!/usr/bin/env bash
# Read Shelly H&T sensor status via Shelly Cloud API.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/shelly-config.sh"
load_shelly_skill_env

DEFAULT_CACHE_TTL=15
CLOUD_CACHE_FILE="/tmp/shelly-cloud-all-status.json"
CLOUD_CACHE_LOCK="/tmp/shelly-cloud-all-status.lock"

usage() {
  cat <<'EOF'
Usage:
  ht-status.sh <ht-alias>
  ht-status.sh <device_id>

Examples:
  ht-status.sh schlafzimmer
  ht-status.sh bedroom
  ht-status.sh decafbadf00d

Behavior:
  - Reads H&T sensor data from Shelly Cloud (WiFi devices, no local RPC)
  - Returns normalized JSON with temperature_C, humidity_percent, battery_percent, rssi
  - Uses cached device list (15s TTL) to avoid rate limiting

Output fields:
  - alias: resolved alias or device_id
  - device_id: Shelly device ID
  - temperature_C: room temperature
  - humidity_percent: relative humidity
  - battery_percent: battery level
  - rssi: WiFi signal strength
EOF
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

if [[ $# -lt 1 ]]; then
  usage >&2
  exit 2
fi

input="$1"

# Try to resolve as alias first, otherwise treat as device_id
device_id=""
resolved_alias=""

if resolved_record="$(shelly_ht_record_for_alias "$input" 2>/dev/null)"; then
  IFS='|' read -r resolved_alias device_id <<<"$resolved_record"
else
  # Treat input as device_id
  device_id="$input"
  resolved_alias="$input"
fi

command -v jq >/dev/null 2>&1 || {
  echo "jq not installed" >&2
  exit 1
}

refresh_cloud_cache

if ! jq -e --arg device_id "$device_id" '.data.devices_status[$device_id]' "$CLOUD_CACHE_FILE" >/dev/null 2>&1; then
  echo "H&T sensor not found in Shelly Cloud: $device_id" >&2
  exit 1
fi

jq \
  --arg alias "$resolved_alias" \
  --arg device_id "$device_id" \
  '
    .data.devices_status[$device_id] as $sensor
    | {
        alias: $alias,
        device_id: $device_id,
        temperature_C: ($sensor["temperature:0"].tC // null),
        humidity_percent: ($sensor["humidity:0"].rh // null),
        battery_percent: ($sensor["devicepower:0"].battery.percent // null),
        rssi: ($sensor.wifi.rssi // null),
        updated_at: ($sensor._updated // null)
      }
  ' "$CLOUD_CACHE_FILE"