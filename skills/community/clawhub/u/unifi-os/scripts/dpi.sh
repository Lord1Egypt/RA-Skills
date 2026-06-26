#!/usr/bin/env bash
# dpi.sh — top applications by bandwidth
# Args: [N (default 10)] [--json]

source "$(dirname "$0")/lib.sh"
load_config

N=10
MODE=""

for arg in "$@"; do
  case "${arg}" in
    --json) MODE="json" ;;
    [0-9]*) N="${arg}" ;;
  esac
done

data=$(cached_api "dpi" "/proxy/network/api/s/${UNIFI_SITE}/stat/sitedpi" "${TTL_OPERATIONAL}")

case "${MODE}" in
  json) echo "${data}" | jq "[.data[:${N}][]]" ;;
  *)
    echo "# Top ${N} apps by bandwidth (cache: $(cache_age dpi))"
    echo "${data}" | jq -r "
      [.data[] | {cat,app,rx_bytes,tx_bytes,total:(.rx_bytes+.tx_bytes)}] |
      sort_by(-.total) | .[:${N}][] |
      \"\(.app // .cat) | rx:\(.rx_bytes/1073741824|.*10|round/10)GB tx:\(.tx_bytes/1073741824|.*10|round/10)GB\"
    "
    ;;
esac
