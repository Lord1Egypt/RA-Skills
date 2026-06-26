#!/usr/bin/env bash
# port_forwards.sh — NAT/port forward rules
# Args: [--json] [--raw]

source "$(dirname "$0")/lib.sh"
load_config

MODE="${1:-}"

data=$(cached_api "port_forwards" "/proxy/network/api/s/${UNIFI_SITE}/rest/portforward" "${TTL_INVENTORY}")

case "${MODE}" in
  --raw)  echo "${data}" ;;
  --json) echo "${data}" | jq '[.data[] | {name,proto,dst_port,fwd,fwd_port,enabled,src}]' ;;
  *)
    echo "# Port Forwards (cache: $(cache_age port_forwards))"
    echo "${data}" | jq -r '
      .data[] |
      "\(.name) | \(.proto) :\(.dst_port) → \(.fwd):\(.fwd_port) | src:\(.src // "any") | \(if .enabled then "on" else "off" end)"
    '
    ;;
esac
