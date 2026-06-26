#!/usr/bin/env bash
# UniFi summary via Integration API
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/unifi-api.sh"

FORMAT="${1:-table}"
CLIENT_LIMIT="${UNIFI_CLIENT_LIMIT:-500}"

SITE_JSON=$(curl -sk -H "X-API-KEY: $UNIFI_TOKEN" -H "Accept: application/json" "$UNIFI_URL/proxy/network/integration/v1/sites")
SITE_ID=$(echo "$SITE_JSON" | jq -r '.data[0].id')
SITE_NAME=$(echo "$SITE_JSON" | jq -r '.data[0].name')
DEVICES=$(curl -sk -H "X-API-KEY: $UNIFI_TOKEN" -H "Accept: application/json" "$UNIFI_URL/proxy/network/integration/v1/sites/$SITE_ID/devices?limit=200")
CLIENTS=$(curl -sk -H "X-API-KEY: $UNIFI_TOKEN" -H "Accept: application/json" "$UNIFI_URL/proxy/network/integration/v1/sites/$SITE_ID/clients?limit=$CLIENT_LIMIT")

if [ "$FORMAT" = "json" ]; then
  jq -n \
    --arg siteId "$SITE_ID" \
    --arg siteName "$SITE_NAME" \
    --argjson devices "$DEVICES" \
    --argjson clients "$CLIENTS" \
    '{siteId:$siteId,siteName:$siteName,devices:$devices,clients:$clients}'
else
  DEVICE_TOTAL=$(echo "$DEVICES" | jq '.totalCount // (.data | length)')
  DEVICE_ONLINE=$(echo "$DEVICES" | jq '[.data[] | select(.state == "ONLINE")] | length')
  DEVICE_OFFLINE=$(echo "$DEVICES" | jq '[.data[] | select(.state != "ONLINE")] | length')
  APS=$(echo "$DEVICES" | jq '[.data[] | select((.features // []) | index("accessPoint"))] | length')
  SWITCHES=$(echo "$DEVICES" | jq '[.data[] | select((.features // []) | index("switching"))] | length')
  CLIENT_TOTAL=$(echo "$CLIENTS" | jq '.totalCount // (.data | length)')
  WIRED=$(echo "$CLIENTS" | jq '[.data[] | select(.type == "WIRED")] | length')
  WIRELESS=$(echo "$CLIENTS" | jq '[.data[] | select(.type == "WIRELESS")] | length')

  printf "%-12s %-36s %-8s %-6s %-7s %-3s %-8s %-7s %-10s\n" "SITE" "SITE ID" "DEVICES" "ONLINE" "OFFLINE" "APs" "SWITCHES" "CLIENTS" "WIRELESS"
  printf "%-12s %-36s %-8s %-6s %-7s %-3s %-8s %-7s %-10s\n" "----" "-------" "-------" "------" "-------" "---" "--------" "-------" "--------"
  printf "%-12s %-36s %-8s %-6s %-7s %-3s %-8s %-7s %-10s\n" "$SITE_NAME" "$SITE_ID" "$DEVICE_TOTAL" "$DEVICE_ONLINE" "$DEVICE_OFFLINE" "$APS" "$SWITCHES" "$CLIENT_TOTAL" "$WIRELESS"
  echo
  echo "Wired clients: $WIRED"
fi
