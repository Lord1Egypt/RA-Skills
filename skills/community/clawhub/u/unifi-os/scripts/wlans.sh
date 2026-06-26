#!/usr/bin/env bash
# wlans.sh — wireless network configs
# Args: [--json] [--raw]

source "$(dirname "$0")/lib.sh"
load_config

MODE="${1:-}"

data=$(cached_api "wlans" "/proxy/network/api/s/${UNIFI_SITE}/rest/wlanconf" "${TTL_INVENTORY}")

case "${MODE}" in
  --raw)  echo "${data}" ;;
  --json) echo "${data}" | jq '[.data[] | {name,security,vlanid,enabled,band,hide_ssid,wpa_mode}]' ;;
  *)
    echo "# WLANs (cache: $(cache_age wlans))"
    echo "${data}" | jq -r '
      .data[] |
      "\(.name) | \(.security) | vlan:\(.vlanid // "untagged") | \(if .enabled then "enabled" else "disabled" end) | hidden:\(if .hide_ssid then "yes" else "no" end)"
    '
    ;;
esac
