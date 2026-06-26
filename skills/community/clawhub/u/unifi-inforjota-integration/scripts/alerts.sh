#!/usr/bin/env bash
# Recent UniFi alarms via classic API with X-API-KEY auth
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/unifi-api.sh"

LIMIT="${1:-20}"

data=$(unifi_request "/proxy/network/api/s/$UNIFI_SITE/stat/alarm?limit=$LIMIT")
count=$(echo "$data" | jq '.data | length')

if [ "$count" -eq 0 ]; then
  echo "No recent UniFi alarms."
  exit 0
fi

echo "$data" | jq -r --argjson limit "$LIMIT" '
  ["TIME", "KEY", "MESSAGE", "DEVICE"],
  ["----", "---", "-------", "------"],
  (.data[:$limit][] | [
    (.datetime // "N/A"),
    (.key // "N/A"),
    (.msg // "N/A"),
    (.ap_name // .gw_name // .sw_name // .dev_name // "N/A")
  ]) | @tsv
' | column -t -s $'\t'
