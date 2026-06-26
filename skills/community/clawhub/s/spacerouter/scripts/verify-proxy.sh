#!/usr/bin/env bash
# Verify Space Router proxy is working by comparing direct vs proxied IP.

set -euo pipefail

if [ -z "${SPACE_ROUTER_PROXY_URL:-}" ]; then
  echo "ERROR: SPACE_ROUTER_PROXY_URL is not set." >&2
  echo "Set it to your Space Router proxy URL, e.g.:" >&2
  echo "  export SPACE_ROUTER_PROXY_URL=http://sr_live_KEY@localhost:8080" >&2
  exit 1
fi

echo "Checking direct IP..."
DIRECT_IP=$(curl -s --max-time 10 https://httpbin.org/ip | grep -o '"origin": "[^"]*"' | cut -d'"' -f4)
echo "  Direct IP: ${DIRECT_IP:-unknown}"

echo "Checking proxied IP..."
PROXY_IP=$(curl -s --max-time 15 -x "$SPACE_ROUTER_PROXY_URL" https://httpbin.org/ip | grep -o '"origin": "[^"]*"' | cut -d'"' -f4)
echo "  Proxied IP: ${PROXY_IP:-unknown}"

if [ -z "$PROXY_IP" ]; then
  echo ""
  echo "FAIL: Could not reach httpbin.org through the proxy."
  echo "Check that Space Router services are running and the API key is valid."
  exit 1
fi

if [ "$DIRECT_IP" = "$PROXY_IP" ]; then
  echo ""
  echo "WARNING: Direct and proxied IPs are the same ($DIRECT_IP)."
  echo "The proxy may not be routing through a residential node."
  exit 1
fi

echo ""
echo "SUCCESS: Traffic is routed through a different IP via Space Router."
echo "  Direct:  $DIRECT_IP"
echo "  Proxied: $PROXY_IP"
