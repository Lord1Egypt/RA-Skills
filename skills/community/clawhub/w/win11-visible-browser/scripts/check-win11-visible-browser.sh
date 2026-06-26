#!/usr/bin/env bash
set -euo pipefail
PROFILE="${1:-win-edge}"
RELAY_PORT="${RELAY_PORT:-9223}"
WIN_IP="$(ip route | awk '/default/ {print $3; exit}')"
CDP_URL="http://${WIN_IP}:${RELAY_PORT}"

echo "== Win11 visible browser check =="
echo "profile=${PROFILE}"
echo "win_ip=${WIN_IP}"
echo "cdp_url=${CDP_URL}"

printf '\n-- curl /json/version --\n'
curl -sS --max-time 5 "${CDP_URL}/json/version" | head -c 1200 || {
  printf '\nERROR: CDP endpoint not reachable from WSL\n' >&2
  exit 2
}
echo

printf '\n-- openclaw browser profiles --\n'
openclaw browser profiles

printf '\n-- openclaw browser doctor --\n'
openclaw browser --browser-profile "$PROFILE" doctor
