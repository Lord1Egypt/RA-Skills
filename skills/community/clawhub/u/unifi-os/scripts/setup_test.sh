#!/usr/bin/env bash
# setup_test.sh — validate config, connectivity, and API endpoint compatibility
# Run this once after install to confirm everything works

source "$(dirname "$0")/lib.sh"
load_config

PASS=0
FAIL=0

check() {
  local label="$1" result="$2" expect="$3"
  if echo "${result}" | grep -q "${expect}"; then
    echo "  ✓ ${label}"
    (( PASS++ ))
  else
    echo "  ✗ ${label}"
    echo "    → ${result:0:120}"
    (( FAIL++ ))
  fi
}

echo "=== UniFi OS Setup Test ==="
echo "URL  : ${UNIFI_URL}"
echo "Site : ${UNIFI_SITE}"
echo ""

echo "[ Connectivity ]"
http_code=$(curl -so /dev/null -w "%{http_code}" -H "X-API-Key: ${UNIFI_API_KEY}" "${UNIFI_URL}/proxy/network/api/s/${UNIFI_SITE}/stat/health")
check "HTTPS reachable" "${http_code}" "200\|401\|403"
check "Auth accepted (200)" "${http_code}" "200"

echo ""
echo "[ API Endpoints ]"

r=$(api_get "/proxy/network/api/s/${UNIFI_SITE}/stat/health")
check "health (legacy)" "${r}" '"ok"\|"warning"\|"error"'

r=$(api_get "/proxy/network/v2/api/site/${UNIFI_SITE}/device")
check "devices (v2)" "${r}" '"network_devices"\|"data"'

r=$(api_get "/proxy/network/api/s/${UNIFI_SITE}/rest/networkconf")
check "networks" "${r}" '"data"'

r=$(api_get "/proxy/network/api/s/${UNIFI_SITE}/rest/wlanconf")
check "wlans" "${r}" '"data"'

r=$(api_get "/proxy/network/api/s/${UNIFI_SITE}/rest/portconf")
check "port_profiles" "${r}" '"data"'

r=$(api_get "/proxy/network/api/s/${UNIFI_SITE}/rest/portforward")
check "port_forwards" "${r}" '"data"'

r=$(api_get "/proxy/network/api/s/${UNIFI_SITE}/stat/sta")
check "clients (active)" "${r}" '"data"'

r=$(api_get "/proxy/network/api/s/${UNIFI_SITE}/stat/alluser?within=1")
check "client_history" "${r}" '"data"'

r=$(api_get "/proxy/network/api/s/${UNIFI_SITE}/stat/sitedpi")
check "dpi" "${r}" '"data"'

r=$(api_get "/proxy/network/api/s/${UNIFI_SITE}/stat/alarm?archived=false")
check "alerts" "${r}" '"data"'

echo ""
echo "[ Dependencies ]"
for bin in curl jq; do
  if command -v "${bin}" &>/dev/null; then
    echo "  ✓ ${bin} ($(${bin} --version 2>&1 | head -1))"
    (( PASS++ ))
  else
    echo "  ✗ ${bin} not found"
    (( FAIL++ ))
  fi
done

echo ""
echo "=== Result: ${PASS} passed, ${FAIL} failed ==="
[[ "${FAIL}" -eq 0 ]] && exit 0 || exit 1
