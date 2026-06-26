#!/usr/bin/env bash
# health.sh — subsystem health summary
# Args: [--json] [--raw]

source "$(dirname "$0")/lib.sh"
load_config

MODE="${1:-}"

data=$(cached_api "health" "/proxy/network/api/s/${UNIFI_SITE}/stat/health" "${TTL_OPERATIONAL}")

case "${MODE}" in
  --raw)  echo "${data}" ;;
  --json) echo "${data}" | jq '.data' ;;
  *)
    echo "# Health (cache: $(cache_age health))"
    echo "${data}" | jq -r '
      .data[] |
      "\(.subsystem) | \(.status) | \(
        [to_entries[] | select(.key | startswith("num_")) | "\(.key|ltrimstr("num_")):\(.value)"] | join(" ")
      )"
    '
    ;;
esac
