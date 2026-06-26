#!/usr/bin/env bash
# Top applications by traffic via classic API with X-API-KEY auth
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/unifi-api.sh"

LIMIT="${1:-10}"

data=$(unifi_request "/proxy/network/api/s/$UNIFI_SITE/stat/sitedpi")
app_count=$(echo "$data" | jq '(.data[0].by_app // []) | length')

if [ "$app_count" -eq 0 ]; then
  echo "No DPI/top application data available right now."
  exit 0
fi

echo "$data" | jq -r --argjson limit "$LIMIT" '
  ["APP", "CATEGORY", "RX (GB)", "TX (GB)", "TOTAL (GB)"],
  ["---", "--------", "-------", "-------", "----------"],
  ((.data[0].by_app // [])
   | sort_by(-((.tx_bytes // 0) + (.rx_bytes // 0)))
   | .[:$limit][]
   | [
      (.app // "N/A"),
      (.cat // "N/A"),
      (((.rx_bytes // 0) / 1073741824 * 100 | floor) / 100 | tostring),
      (((.tx_bytes // 0) / 1073741824 * 100 | floor) / 100 | tostring),
      ((((.rx_bytes // 0) + (.tx_bytes // 0)) / 1073741824 * 100 | floor) / 100 | tostring)
    ]) | @tsv
' | column -t -s $'\t'
