#!/usr/bin/env bash
# device_detail.sh — full detail on one device (ports, RF, errors)
# Args: <name|ip|mac> [--json]
# Not cached — always fresh for troubleshooting

source "$(dirname "$0")/lib.sh"
load_config

QUERY="${1:-}"
MODE="${2:-}"

[[ -z "${QUERY}" ]] && { echo "Usage: device_detail.sh <name|ip|mac> [--json]" >&2; exit 1; }

# Pull from devices cache if fresh, otherwise live
data=$(cached_api "devices" "/proxy/network/v2/api/site/${UNIFI_SITE}/device" "${TTL_INVENTORY}")

# Match by name, IP, or MAC (case-insensitive)
# UniFi OS v2 API: devices are in .network_devices + .unmanaged_devices
device=$(echo "${data}" | jq --arg q "${QUERY}" '
  (.network_devices // .data)[] | select(
    (.name // "" | ascii_downcase) == ($q | ascii_downcase) or
    (.ip // "") == $q or
    (.mac // "" | ascii_downcase) == ($q | ascii_downcase)
  )
' | jq -s '.[0]')

[[ "${device}" == "null" || -z "${device}" ]] && { echo "No device found matching: ${QUERY}" >&2; exit 1; }

if [[ "${MODE}" == "--json" ]]; then
  echo "${device}"
  exit 0
fi

echo "# Device: $(echo "${device}" | jq -r '.name // .mac')"
echo "Model    : $(echo "${device}" | jq -r '.model')"
echo "IP       : $(echo "${device}" | jq -r '.ip // "none"')"
echo "MAC      : $(echo "${device}" | jq -r '.mac')"
echo "Firmware : $(echo "${device}" | jq -r '.version // "?"')"
echo "Uptime   : $(echo "${device}" | jq -r '(.uptime // 0) / 86400 | floor | "\(.)d"')"
echo "State    : $(echo "${device}" | jq -r 'if .state==1 then "up" else "DOWN" end')"
echo "Clients  : $(echo "${device}" | jq -r '.num_sta // 0')"

# Switch ports if present
port_count=$(echo "${device}" | jq '.port_table | length')
if (( port_count > 0 )); then
  echo ""
  echo "Ports:"
  echo "${device}" | jq -r '
    .port_table[] |
    "  p\(.port_idx) \(.name // "") | \(if .up then "up" else "down" end) | \(.speed // 0)Mbps | poe:\(.poe_mode // "off") \(.poe_power // 0)W | rx_err:\(.rx_errors // 0) tx_err:\(.tx_errors // 0)"
  '
fi

# Radio table (APs)
radio_count=$(echo "${device}" | jq '.radio_table | length')
if (( radio_count > 0 )); then
  echo ""
  echo "Radios:"
  echo "${device}" | jq -r '
    .radio_table[] |
    "  \(.radio) | ch:\(.channel) | \(.ht)MHz | tx:\(.tx_power // "auto")dBm"
  '
fi

echo ""
echo "Update available: $(echo "${device}" | jq -r 'if ((.upgrade_to_firmware // "") != "") then .upgrade_to_firmware else "none" end')"
