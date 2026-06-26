#!/usr/bin/env bash
# client_locate.sh — find a client and everything about its location
# Composite: clients + devices + networks — all from cache
# Args: <hostname|ip|mac> [--json] [--include-history]

source "$(dirname "$0")/lib.sh"
load_config

QUERY=""
MODE=""
INCLUDE_HISTORY=false

for arg in "$@"; do
  case "${arg}" in
    --json)            MODE="json" ;;
    --include-history) INCLUDE_HISTORY=true ;;
    -*)                ;;
    *)                 [[ -z "${QUERY}" ]] && QUERY="${arg}" ;;
  esac
done

[[ -z "${QUERY}" ]] && { echo "Usage: client_locate.sh <hostname|ip|mac> [--json] [--include-history]" >&2; exit 1; }

clients=$(cached_api "clients" "/proxy/network/api/s/${UNIFI_SITE}/stat/sta" "${TTL_OPERATIONAL}")
devices=$(cached_api "devices" "/proxy/network/v2/api/site/${UNIFI_SITE}/device" "${TTL_INVENTORY}")
networks=$(cached_api "networks" "/proxy/network/api/s/${UNIFI_SITE}/rest/networkconf" "${TTL_INVENTORY}")

# Find client
client=$(echo "${clients}" | jq --arg q "${QUERY}" '
  .data[] | select(
    (.hostname // "" | ascii_downcase | contains($q | ascii_downcase)) or
    (.ip // "") == $q or
    (.mac // "" | ascii_downcase) == ($q | ascii_downcase)
  )
' | jq -s '.[0]')

# Try history if not found active
if [[ "${client}" == "null" || -z "${client}" ]]; then
  if "${INCLUDE_HISTORY}"; then
    history=$(cached_api "client_history_24" "/proxy/network/api/s/${UNIFI_SITE}/stat/alluser?within=24" "${TTL_OPERATIONAL}")
    client=$(echo "${history}" | jq --arg q "${QUERY}" '
      .data[] | select(
        (.hostname // "" | ascii_downcase | contains($q | ascii_downcase)) or
        (.ip // "") == $q or
        (.mac // "" | ascii_downcase) == ($q | ascii_downcase)
      )
    ' | jq -s '.[0]')
    HISTORICAL=true
  fi
fi

[[ "${client}" == "null" || -z "${client}" ]] && { echo "Client not found: ${QUERY}. Try --include-history"; exit 1; }

# Resolve connected device (AP or switch)
connected_mac=$(echo "${client}" | jq -r '.ap_mac // .sw_mac // ""')
connected_device=$(echo "${devices}" | jq --arg mac "${connected_mac}" '(.network_devices // .data)[] | select((.mac | ascii_downcase) == ($mac | ascii_downcase))' | jq -s '.[0]')

# Resolve network name from VLAN ID
vlan_id=$(echo "${client}" | jq -r '.vlan // 1')
network_name=$(echo "${networks}" | jq -r --argjson v "${vlan_id}" '.data[] | select((.vlan // 1) == $v) | .name' | head -1)

if [[ "${MODE}" == "--json" ]]; then
  jq -n \
    --argjson client "${client}" \
    --argjson device "${connected_device}" \
    --arg network "${network_name}" \
    '{client: $client, connected_to: $device, network: $network}'
  exit 0
fi

STATUS="${HISTORICAL:+HISTORICAL (not currently active)}"
STATUS="${STATUS:-ACTIVE}"

echo "# Client: $(echo "${client}" | jq -r '.hostname // .mac') [${STATUS}]"
echo "IP      : $(echo "${client}" | jq -r '.ip // "?"')"
echo "MAC     : $(echo "${client}" | jq -r '.mac')"
echo "VLAN    : ${vlan_id} (${network_name:-unknown})"

is_wired=$(echo "${client}" | jq -r '.is_wired')
if [[ "${is_wired}" == "true" ]]; then
  echo "Connect : wired"
  echo "Switch  : $(echo "${connected_device}" | jq -r '.name // .mac // "unknown"') ($(echo "${client}" | jq -r '.sw_mac // "?"'))"
  echo "Port    : $(echo "${client}" | jq -r '.sw_port // "?"')"
else
  echo "Connect : wifi"
  echo "AP      : $(echo "${connected_device}" | jq -r '.name // .mac // "unknown"') ($(echo "${client}" | jq -r '.ap_mac // "?"'))"
  echo "Signal  : $(echo "${client}" | jq -r '.signal // "?")dBm"
  echo "SSID    : $(echo "${client}" | jq -r '.essid // "?"')"
fi

echo "Last seen: $(echo "${client}" | jq -r '.last_seen | todate')"
