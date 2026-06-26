#!/usr/bin/env bash
# networks.sh — VLANs and network configs
# Args: [--json] [--raw]

source "$(dirname "$0")/lib.sh"
load_config

MODE="${1:-}"

data=$(cached_api "networks" "/proxy/network/api/s/${UNIFI_SITE}/rest/networkconf" "${TTL_INVENTORY}")

case "${MODE}" in
  --raw)  echo "${data}" ;;
  --json) echo "${data}" | jq '[.data[] | {name,purpose,vlan,ip_subnet,dhcpd_enabled,domain_name,vlan_enabled}]' ;;
  *)
    echo "# Networks (cache: $(cache_age networks))"
    echo "${data}" | jq -r '
      .data[] |
      "\(.name) | \(.purpose) | vlan:\(.vlan // "1") | \(.ip_subnet // "no-subnet") | dhcp:\(if .dhcpd_enabled then "on" else "off" end)"
    '
    ;;
esac
