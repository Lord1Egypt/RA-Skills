#!/usr/bin/env bash
# firmware.sh — devices with pending firmware updates
# Args: [--json] [--all]

source "$(dirname "$0")/lib.sh"
load_config

MODE="${1:-}"

data=$(cached_api "devices" "/proxy/network/v2/api/site/${UNIFI_SITE}/device" "${TTL_INVENTORY}")

# UniFi OS v2 API: devices are in .network_devices + .unmanaged_devices
# UniFi OS v2 API: devices are in .network_devices + .unmanaged_devices (not .data)

# Determine which key to use
DEV_KEY=$(echo "${data}" | jq -r 'if .network_devices then "network_devices" elif .data then "data" else empty end' 2>/dev/null)

case "${MODE}" in
  --json)
    echo "${data}" | jq --arg k "${DEV_KEY}" '[.${k}[] | select(.upgrade_to_firmware != null and .upgrade_to_firmware != "") | {name,model,version,upgrade_to_firmware}]'
    ;;
  --all)
    echo "# All device firmware (cache: $(cache_age devices))"
    echo "${data}" | jq -r --arg k "${DEV_KEY}" '.[$k][] | "\(.name // .mac) | \(.model) | current:\(.version // "?") | \(if (.upgrade_to_firmware // "") != "" then "update→\(.upgrade_to_firmware)" else "up-to-date" end)"'
    ;;
  *)
    echo "# Firmware updates available (cache: $(cache_age devices))"
    result=$(echo "${data}" | jq -r --arg k "${DEV_KEY}" '.[$k][] | select((.upgrade_to_firmware // "") != "") | "\(.name // .mac) | \(.model) | \(.version) → \(.upgrade_to_firmware)"')
    [[ -z "${result}" ]] && echo "All devices up-to-date" || echo "${result}"
    ;;
esac
