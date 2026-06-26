#!/usr/bin/env bash
# UniFi Integration API helper (X-API-KEY auth)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${UNIFI_CONFIG_FILE:-$HOME/.clawdbot/credentials/unifi/config.json}"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "Error: UniFi not configured. Create $CONFIG_FILE with {\"url\": \"https://...\", \"token\": \"...\", \"site\": \"default\"}" >&2
  exit 1
fi

UNIFI_URL=$(jq -r '.url // empty' "$CONFIG_FILE")
UNIFI_TOKEN=$(jq -r '.token // empty' "$CONFIG_FILE")
UNIFI_SITE=$(jq -r '.site // "default"' "$CONFIG_FILE")

if [ -z "$UNIFI_URL" ] || [ -z "$UNIFI_TOKEN" ]; then
  echo "Error: UniFi config must include url and token" >&2
  exit 1
fi

unifi_request() {
  local path="$1"
  curl -sk \
    -H "X-API-KEY: $UNIFI_TOKEN" \
    -H "Accept: application/json" \
    "$UNIFI_URL$path"
}

unifi_sites() {
  unifi_request "/proxy/network/integration/v1/sites"
}

unifi_site_id() {
  unifi_sites | jq -r --arg ref "$UNIFI_SITE" '
    (.data[] | select(.internalReference == $ref) | .id),
    .data[0].id
  ' | head -n1
}

unifi_get() {
  local endpoint="$1"
  local site_id
  site_id=$(unifi_site_id)

  case "$endpoint" in
    sites)
      unifi_sites
      ;;
    devices)
      unifi_request "/proxy/network/integration/v1/sites/$site_id/devices?limit=200"
      ;;
    clients)
      unifi_request "/proxy/network/integration/v1/sites/$site_id/clients?limit=${UNIFI_CLIENT_LIMIT:-200}"
      ;;
    dashboard|health)
      jq -n \
        --argjson sites "$(unifi_sites)" \
        --argjson devices "$(unifi_request "/proxy/network/integration/v1/sites/$site_id/devices?limit=200")" \
        --argjson clients "$(unifi_request "/proxy/network/integration/v1/sites/$site_id/clients?limit=${UNIFI_CLIENT_LIMIT:-200}")" \
        '{sites:$sites,devices:$devices,clients:$clients}'
      ;;
    /*)
      unifi_request "$endpoint"
      ;;
    *)
      echo "Error: Unsupported endpoint '$endpoint'" >&2
      return 1
      ;;
  esac
}

export -f unifi_request
export -f unifi_sites
export -f unifi_site_id
export -f unifi_get
export UNIFI_URL UNIFI_SITE UNIFI_TOKEN
