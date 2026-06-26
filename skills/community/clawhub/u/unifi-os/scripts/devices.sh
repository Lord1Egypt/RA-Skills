#!/usr/bin/env bash
# devices.sh — all adopted devices, stripped output
# Args: [--json] [--raw]

source "$(dirname "$0")/lib.sh"
load_config

MODE="${1:-}"

data=$(cached_api "devices" "/proxy/network/v2/api/site/${UNIFI_SITE}/device" "${TTL_INVENTORY}")

# UniFi OS API: data is in .network_devices array, not .data
DEVICES_JSON=$(echo "${data}" | jq '.network_devices // []')

case "${MODE}" in
  --raw)  echo "${data}" ;;
 --json) echo "${DEVICES_JSON}" | jq '[.[] | {name,model,ip,mac,version,state,uptime,num_sta,type}]' ;;
  *)
    echo "# Devices (cache: $(cache_age devices))"
    echo "${DEVICES_JSON}" | jq -r '
      .[] |
      "\(.name // .mac) | \(.model) | \(.ip // "no-ip") | \(if .state==1 then "up" elif .state==0 then "DOWN" else "other" end) | \(.num_sta // 0)c | fw:\(.version // "?")"
    '
    ;;
esac
