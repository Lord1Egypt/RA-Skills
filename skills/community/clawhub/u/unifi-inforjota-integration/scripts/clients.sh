#!/usr/bin/env bash
# List active UniFi clients via Integration API
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/unifi-api.sh"

FORMAT="${1:-table}"
LIMIT="${UNIFI_CLIENT_LIMIT:-200}"

SITE_ID=$(curl -sk \
  -H "X-API-KEY: $UNIFI_TOKEN" \
  -H "Accept: application/json" \
  "$UNIFI_URL/proxy/network/integration/v1/sites" | jq -r '.data[0].id')

data=$(curl -sk \
  -H "X-API-KEY: $UNIFI_TOKEN" \
  -H "Accept: application/json" \
  "$UNIFI_URL/proxy/network/integration/v1/sites/$SITE_ID/clients?limit=$LIMIT")

if [ "$FORMAT" = "json" ]; then
  echo "$data"
else
  echo "$data" | jq -r '
    ["NAME", "TYPE", "IP", "MAC", "CONNECTED AT", "UPLINK DEVICE ID"],
    ["----", "----", "--", "---", "------------", "----------------"],
    (.data[] | [
      (.name // "Unknown"),
      (.type // "N/A"),
      (.ipAddress // "N/A"),
      (.macAddress // "N/A"),
      (.connectedAt // "N/A"),
      (.uplinkDeviceId // "N/A")
    ]) | @tsv
  ' | column -t -s $'\t'
fi
