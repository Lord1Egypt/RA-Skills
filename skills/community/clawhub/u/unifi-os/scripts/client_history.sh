#!/usr/bin/env bash
# client_history.sh — clients seen in last N hours (including disconnected)
# Args: [hours (default 24)] [--json]

source "$(dirname "$0")/lib.sh"
load_config

HOURS=24
MODE=""

for arg in "$@"; do
  case "${arg}" in
    --json)  MODE="json" ;;
    [0-9]*)  HOURS="${arg}" ;;
  esac
done

data=$(cached_api "client_history_${HOURS}" "/proxy/network/api/s/${UNIFI_SITE}/stat/alluser?within=${HOURS}" "${TTL_OPERATIONAL}")

case "${MODE}" in
  json) echo "${data}" | jq '[.data[] | {hostname,ip,mac,last_seen,is_wired,ap_mac,sw_mac,sw_port}]' ;;
  *)
    echo "# Client history (last ${HOURS}h, cache: $(cache_age client_history_${HOURS}))"
    echo "${data}" | jq -r '
      .data[] |
      "\(.hostname // .mac) | \(.ip // "?") | last:\(.last_seen | todate) | \(if .is_wired then "wired" else "wifi" end)"
    '
    ;;
esac
