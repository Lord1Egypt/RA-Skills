#!/usr/bin/env bash
# snapshot.sh — compact site overview for agent orientation
# Call this first. Use output to decide if deeper queries are needed.
# Cache: blends inventory + operational TTLs (uses shortest = 5min)

source "$(dirname "$0")/lib.sh"
load_config

MODE="${1:-}" # --json or blank

health=$(cached_api "health" "/proxy/network/api/s/${UNIFI_SITE}/stat/health" "${TTL_OPERATIONAL}")
devices=$(cached_api "devices" "/proxy/network/v2/api/site/${UNIFI_SITE}/device" "${TTL_INVENTORY}")
clients=$(cached_api "clients" "/proxy/network/api/s/${UNIFI_SITE}/stat/sta" "${TTL_OPERATIONAL}")
networks=$(cached_api "networks" "/proxy/network/api/s/${UNIFI_SITE}/rest/networkconf" "${TTL_INVENTORY}")
alerts=$(cached_api "alerts_false" "/proxy/network/api/s/${UNIFI_SITE}/stat/alarm?archived=false" "${TTL_ALERTS}")

# UniFi OS API returns network_devices + unmanaged_devices arrays (not .data)
device_count=$(echo "${devices}" | jq '[.network_devices // [], .unmanaged_devices // [] | length] | add // 0')
managed_count=$(echo "${devices}" | jq '.network_devices | length // 0')

if [[ "${MODE}" == "--json" ]]; then
  jq -n \
    --argjson h "${health}" \
    --argjson dc "${device_count}" \
    --argjson mc "${managed_count}" \
    --argjson c "${clients}" \
    --argjson n "${networks}" \
    --argjson a "${alerts}" \
    '{health:$h.data, managed_device_count:$mc, total_device_count:$dc, client_count:($c.data|length), network_count:($n.data|length), alert_count:($a.data|length)}'
  exit 0
fi

echo "=== UniFi Site: ${UNIFI_SITE} | $(date '+%Y-%m-%d %H:%M') ==="
echo ""

# WAN status
echo "WAN:"
wan_info=$(echo "${health}" | jq -r '.data[] | select(.subsystem=="wan") | "  \(.status) | ip:\(.wan_ip // "?") | up:\(.latency // "?")ms latency"' 2>/dev/null)
[[ -n "${wan_info}" ]] && echo "${wan_info}" || echo "  unknown (gateway may be offline)"

echo ""
echo "Counts:"
echo "  Devices : ${managed_count} adopted / ${device_count} total (incl. unmanaged)"
echo "  Clients : $(echo "${clients}" | jq '.data | length') active"
echo "  Networks: $(echo "${networks}" | jq '.data | length') configured"
echo "  Alerts  : $(echo "${alerts}" | jq '.data[:5] | length') open"

echo ""
echo "Device health:"
echo "${devices}" | jq -r '
  .network_devices[] |
  "  \(.name // .mac) | \(.model) | \(if .state == 1 then "up" elif .state == 0 then "DOWN" else "other" end) | \(.num_sta // 0)c"
'

echo ""
echo "Networks/VLANs:"
echo "${networks}" | jq -r '.data[] | select(.purpose != "wan") | "  \(.name) | vlan:\(.vlan // "1") | \(.ip_subnet // "-")"'

echo ""
echo "Open alerts:"
alert_lines=$(echo "${alerts}" | jq -r '.data[:5][] | "  [\(.datetime // "?")] \(.msg // .key)"' 2>/dev/null)
[[ -n "${alert_lines}" ]] && echo "${alert_lines}" || echo "  none"

echo ""
echo "Cache: devices=$(cache_age devices) clients=$(cache_age clients) alerts=$(cache_age alerts)"
