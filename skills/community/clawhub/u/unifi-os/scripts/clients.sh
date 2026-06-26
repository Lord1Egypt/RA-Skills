#!/usr/bin/env bash
# clients.sh — active connected clients
# Args: [--json] [--raw] [--wifi|--wired]

source "$(dirname "$0")/lib.sh"
load_config

MODE=""
FILTER=""

for arg in "$@"; do
  case "${arg}" in
    --json)  MODE="json" ;;
    --raw)   MODE="raw" ;;
    --wifi)  FILTER="wifi" ;;
    --wired) FILTER="wired" ;;
  esac
done

data=$(cached_api "clients" "/proxy/network/api/s/${UNIFI_SITE}/stat/sta" "${TTL_OPERATIONAL}")

# Apply filter
filtered="${data}"
if [[ "${FILTER}" == "wifi" ]]; then
  filtered=$(echo "${data}" | jq '{data:[.data[] | select(.is_wired == false)]}')
elif [[ "${FILTER}" == "wired" ]]; then
  filtered=$(echo "${data}" | jq '{data:[.data[] | select(.is_wired == true)]}')
fi

case "${MODE}" in
  raw)  echo "${filtered}" ;;
  json) echo "${filtered}" | jq '[.data[] | {hostname,ip,mac,vlan,ap_mac,sw_mac,sw_port,is_wired,signal,rx_bytes,tx_bytes}]' ;;
  *)
    echo "# Clients ($(echo "${filtered}" | jq '.data|length') active, cache: $(cache_age clients))"
    echo "${filtered}" | jq -r '
      .data[] |
      "\(.hostname // .mac) | \(.ip // "no-ip") | vlan:\(.vlan // "1") | \(if .is_wired then "wired sw:\(.sw_mac // "?") p:\(.sw_port // "?") " else "wifi ap:\(.ap_mac // "?") sig:\(.signal // "?")dBm" end)"
    '
    ;;
esac
