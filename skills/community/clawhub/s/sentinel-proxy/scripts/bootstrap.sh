#!/usr/bin/env bash
# agent:bootstrap — verify Sentinel credentials before the agent starts.
set -euo pipefail

SENTINEL_API_URL="${SENTINEL_API_URL:-https://sentinel.ircnet.us}"
SENTINEL_KEY="${SENTINEL_KEY:-}"

if [[ -z "$SENTINEL_KEY" ]]; then
  echo "[sentinel] WARNING: SENTINEL_KEY is not set. Scrubbing is disabled." >&2
  echo "[sentinel] Get a free key at https://sentinel-proxy.skyblue-soft.com" >&2
  exit 0
fi

response=$(curl -sf -w "\n%{http_code}" \
  -X POST "${SENTINEL_API_URL}/v1/scrub" \
  -H "X-Sentinel-Key: ${SENTINEL_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"content":"bootstrap-check"}' 2>/dev/null) || true

http_code=$(echo "$response" | tail -n1)

case "$http_code" in
  200) echo "[sentinel] Connected — AI Firewall active (inbound + outbound scanning)." >&2 ;;
  401|403) echo "[sentinel] ERROR: Invalid SENTINEL_KEY. Check your key at sentinel-proxy.skyblue-soft.com" >&2 ;;
  *) echo "[sentinel] WARNING: Could not reach Sentinel (HTTP ${http_code:-unreachable}). Scrubbing disabled for this session." >&2 ;;
esac

exit 0  # never block agent startup
