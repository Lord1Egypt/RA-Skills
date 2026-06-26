#!/usr/bin/env bash
# alerts.sh — open alarms and recent events
# Args: [--json] [N (default 20)] [--archived]

source "$(dirname "$0")/lib.sh"
load_config

N=20
MODE=""
ARCHIVED="false"

for arg in "$@"; do
  case "${arg}" in
    --json)     MODE="json" ;;
    --archived) ARCHIVED="true" ;;
    [0-9]*)     N="${arg}" ;;
  esac
done

data=$(cached_api "alerts_${ARCHIVED}" "/proxy/network/api/s/${UNIFI_SITE}/stat/alarm?archived=${ARCHIVED}" "${TTL_ALERTS}")

case "${MODE}" in
  json) echo "${data}" | jq "[.data[:${N}][]]" ;;
  *)
    echo "# Alerts (archived:${ARCHIVED}, cache: $(cache_age alerts_${ARCHIVED}))"
    echo "${data}" | jq -r "
      .data[:${N}][] |
      \"[\(.datetime // \"?\")] \(.subsystem // \"-\") | \(.msg // .key)\"
    "
    ;;
esac
