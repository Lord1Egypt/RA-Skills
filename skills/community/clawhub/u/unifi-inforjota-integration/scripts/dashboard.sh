#!/usr/bin/env bash
# UniFi Network Dashboard via Integration API + classic read-only endpoints
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/unifi-api.sh"

OUTPUT_JSON="${1:-}"
CLIENT_LIMIT="${UNIFI_CLIENT_LIMIT:-200}"

SITE_JSON=$(unifi_sites)
SITE_ID=$(echo "$SITE_JSON" | jq -r '.data[0].id')
SITE_NAME=$(echo "$SITE_JSON" | jq -r '.data[0].name')
SITE_REF=$(echo "$SITE_JSON" | jq -r '.data[0].internalReference')
DEVICES=$(unifi_request "/proxy/network/integration/v1/sites/$SITE_ID/devices?limit=200")
CLIENTS=$(unifi_request "/proxy/network/integration/v1/sites/$SITE_ID/clients?limit=$CLIENT_LIMIT")
HEALTH=$(unifi_request "/proxy/network/api/s/$UNIFI_SITE/stat/health")
SYSINFO=$(unifi_request "/proxy/network/api/s/$UNIFI_SITE/stat/sysinfo")
NETWORKS=$(unifi_request "/proxy/network/api/s/$UNIFI_SITE/rest/networkconf")
WLANS=$(unifi_request "/proxy/network/api/s/$UNIFI_SITE/rest/wlanconf")
ALARMS=$(unifi_request "/proxy/network/api/s/$UNIFI_SITE/stat/alarm?limit=10")

if [ "$OUTPUT_JSON" = "json" ]; then
  jq -n \
    --arg siteId "$SITE_ID" \
    --arg siteName "$SITE_NAME" \
    --arg siteRef "$SITE_REF" \
    --argjson devices "$DEVICES" \
    --argjson clients "$CLIENTS" \
    --argjson health "$HEALTH" \
    --argjson sysinfo "$SYSINFO" \
    --argjson networks "$NETWORKS" \
    --argjson wlans "$WLANS" \
    --argjson alarms "$ALARMS" \
    '{siteId:$siteId,siteName:$siteName,siteRef:$siteRef,devices:$devices,clients:$clients,health:$health,sysinfo:$sysinfo,networks:$networks,wlans:$wlans,alarms:$alarms}'
  exit 0
fi

DEVICE_TOTAL=$(echo "$DEVICES" | jq '.totalCount // (.data | length)')
DEVICE_ONLINE=$(echo "$DEVICES" | jq '[.data[] | select(.state == "ONLINE")] | length')
DEVICE_OFFLINE=$(echo "$DEVICES" | jq '[.data[] | select(.state != "ONLINE")] | length')
APS=$(echo "$DEVICES" | jq '[.data[] | select((.features // []) | index("accessPoint"))] | length')
SWITCHES=$(echo "$DEVICES" | jq '[.data[] | select((.features // []) | index("switching"))] | length')
CLIENT_TOTAL=$(echo "$CLIENTS" | jq '.totalCount // (.data | length)')
WIRED=$(echo "$CLIENTS" | jq '[.data[] | select(.type == "WIRED")] | length')
WIRELESS=$(echo "$CLIENTS" | jq '[.data[] | select(.type == "WIRELESS")] | length')
NETWORK_COUNT=$(echo "$NETWORKS" | jq '.data | length')
WLAN_COUNT=$(echo "$WLANS" | jq '.data | length')
ALARM_COUNT=$(echo "$ALARMS" | jq '.data | length')
UNIFI_VER=$(echo "$SYSINFO" | jq -r '.data[0].server_version // .data[0].version // "N/A"')
HOSTNAME=$(echo "$SYSINFO" | jq -r '.data[0].hostname // "N/A"')

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                      UNIFI NETWORK DASHBOARD                     ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo
echo "Site: $SITE_NAME ($SITE_REF)"
echo "Site ID: $SITE_ID"
echo "Console: $HOSTNAME"
echo "UniFi version: $UNIFI_VER"
echo
echo "Overview"
echo "- Devices: $DEVICE_TOTAL total / $DEVICE_ONLINE online / $DEVICE_OFFLINE offline"
echo "- Roles: $APS AP(s), $SWITCHES switching device(s)"
echo "- Clients: $CLIENT_TOTAL total / $WIRED wired / $WIRELESS wireless"
echo "- Networks: $NETWORK_COUNT"
echo "- WLANs: $WLAN_COUNT"
echo "- Recent alarms: $ALARM_COUNT"
echo
echo "Health"
echo "$HEALTH" | jq -r '
  .data[] | "- \(.subsystem // "unknown"): \(.status // "unknown")"
'
echo
echo "Devices"
echo "$DEVICES" | jq -r '
  .data[] | "- \(.name // "N/A") | \(.model // "N/A") | \(.ipAddress // "N/A") | \(.state // "UNKNOWN") | fw \(.firmwareVersion // "N/A")"
'
echo
echo "Networks"
echo "$NETWORKS" | jq -r '
  .data[] | "- \(.name // "N/A") | purpose \(.purpose // "N/A")"
'
echo
echo "WLANs"
echo "$WLANS" | jq -r '
  .data[] | "- \(.name // "N/A") | enabled \(.enabled // false)"
'
echo
echo "Top clients (first 15)"
echo "$CLIENTS" | jq -r '
  .data[0:15][] | "- \(.name // "Unknown") | \(.type // "N/A") | \(.ipAddress // "N/A") | \(.macAddress // "N/A")"
'
echo
echo "Alarms"
if [ "$ALARM_COUNT" -eq 0 ]; then
  echo "- No recent UniFi alarms"
else
  echo "$ALARMS" | jq -r '
    .data[0:10][] | "- \(.datetime // "N/A") | \(.key // "N/A") | \(.msg // "N/A")"
  '
fi

echo
echo "Generated at: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
