#!/usr/bin/env bash
# topology_export.sh — full site topology as markdown for docs/memory
# Args: [--out <file>]

source "$(dirname "$0")/lib.sh"
load_config

OUTFILE=""
[[ "${1}" == "--out" && -n "${2}" ]] && OUTFILE="${2}"

devices=$(cached_api "devices"      "/proxy/network/v2/api/site/${UNIFI_SITE}/device"         "${TTL_INVENTORY}")
networks=$(cached_api "networks"    "/proxy/network/api/s/${UNIFI_SITE}/rest/networkconf"      "${TTL_INVENTORY}")
wlans=$(cached_api "wlans"          "/proxy/network/api/s/${UNIFI_SITE}/rest/wlanconf"         "${TTL_INVENTORY}")
pf=$(cached_api "port_forwards"     "/proxy/network/api/s/${UNIFI_SITE}/rest/portforward"      "${TTL_INVENTORY}")
health=$(cached_api "health"        "/proxy/network/api/s/${UNIFI_SITE}/stat/health"           "${TTL_OPERATIONAL}")

{
  echo "# UniFi Site: ${UNIFI_SITE}"
  echo ""
  echo "*Generated: $(date '+%Y-%m-%d %H:%M:%S')*"
  echo ""

  echo "## WAN"
  echo "${health}" | jq -r '.data[] | select(.subsystem=="wan") | "- Status: \(.status)\n- WAN IP: \(.wan_ip // "unknown")"'
  echo ""

  echo "## Devices"
  echo ""
  echo "| Name | Model | IP | Firmware | Clients | Status |"
  echo "|------|-------|----|----------|---------|--------|"
  echo "${devices}" | jq -r '(.network_devices // .data)[] | "| \(.name // .mac) | \(.model) | \(.ip // "-") | \(.version // "?") | \(.num_sta // 0) | \(if .state==1 then "up" else "DOWN" end) |"'
  echo ""

  echo "## Networks / VLANs"
  echo ""
  echo "| Name | Purpose | VLAN | Subnet | DHCP |"
  echo "|------|---------|------|--------|------|"
  echo "${networks}" | jq -r '.data[] | select(.purpose != "wan") | "| \(.name) | \(.purpose) | \(.vlan // 1) | \(.ip_subnet // "-") | \(if .dhcpd_enabled then "yes" else "no" end) |"'
  echo ""

  echo "## Wireless Networks"
  echo ""
  echo "| SSID | Security | VLAN | Enabled |"
  echo "|------|----------|------|---------|"
  echo "${wlans}" | jq -r '.data[] | "| \(.name) | \(.security) | \(.vlanid // "untagged") | \(if .enabled then "yes" else "no" end) |"'
  echo ""

  echo "## Port Forwards"
  echo ""
  echo "| Name | Proto | External Port | Internal | Enabled |"
  echo "|------|-------|--------------|----------|---------|"
  echo "${pf}" | jq -r '.data[] | "| \(.name) | \(.proto) | \(.dst_port) | \(.fwd):\(.fwd_port) | \(if .enabled then "yes" else "no" end) |"'
  echo ""

  echo "---"
  echo "*Source: UniFi API — ${UNIFI_URL}*"
} | if [[ -n "${OUTFILE}" ]]; then
  tee "${OUTFILE}"
  echo "" >&2
  echo "Written to: ${OUTFILE}" >&2
else
  cat
fi
