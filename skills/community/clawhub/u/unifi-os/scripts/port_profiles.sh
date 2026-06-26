#!/usr/bin/env bash
# port_profiles.sh — switch port profiles
# Args: [--json] [--raw]

source "$(dirname "$0")/lib.sh"
load_config

MODE="${1:-}"

data=$(cached_api "port_profiles" "/proxy/network/api/s/${UNIFI_SITE}/rest/portconf" "${TTL_INVENTORY}")

case "${MODE}" in
  --raw)  echo "${data}" ;;
  --json) echo "${data}" | jq '[.data[] | {name,native_networkconf_id,tagged_vlan_mgmt,poe_mode,speed,duplex}]' ;;
  *)
    echo "# Port Profiles (cache: $(cache_age port_profiles))"
    echo "${data}" | jq -r '
      .data[] |
      "\(.name) | native_vlan:\(.native_networkconf_id // "default") | poe:\(.poe_mode // "off") | speed:\(.speed // "auto")"
    '
    ;;
esac
