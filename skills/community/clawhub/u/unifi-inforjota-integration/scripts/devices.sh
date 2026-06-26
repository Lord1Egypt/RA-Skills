#!/usr/bin/env bash
# List UniFi devices via Integration API
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/unifi-api.sh"

FORMAT="${1:-table}"

SITE_ID=$(curl -sk \
  -H "X-API-KEY: $UNIFI_TOKEN" \
  -H "Accept: application/json" \
  "$UNIFI_URL/proxy/network/integration/v1/sites" | jq -r '.data[0].id')

data=$(curl -sk \
  -H "X-API-KEY: $UNIFI_TOKEN" \
  -H "Accept: application/json" \
  "$UNIFI_URL/proxy/network/integration/v1/sites/$SITE_ID/devices?limit=200")

if [ "$FORMAT" = "json" ]; then
  echo "$data"
else
  echo "$data" | jq -r '
    ["NAME", "MODEL", "IP", "STATE", "VERSION", "FEATURES"],
    ["----", "-----", "--", "-----", "-------", "--------"],
    (.data[] | [
      (.name // .macAddress // "N/A"),
      (.model // "N/A"),
      (.ipAddress // "N/A"),
      (.state // "UNKNOWN"),
      (.firmwareVersion // "N/A"),
      ((.features // [] | join(",")) // "N/A")
    ]) | @tsv
  ' | column -t -s $'\t'
fi
