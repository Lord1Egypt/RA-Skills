#!/usr/bin/env bash
# Stops the bridge + tunnel started by setup_byob_bridge.sh and flips MC
# back to platform-managed. Reads JWT + PIDs from the state file.
#
# Usage:
#   bash teardown_byob_bridge.sh --duck-id <SPACEDUCK_ID>
set -euo pipefail

SD=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --duck-id) SD="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 1;;
  esac
done
[[ -z "$SD" ]] && { echo "--duck-id required" >&2; exit 1; }

STATE_FILE="/tmp/spaceduck-bridge-$SD.state"
[[ -f "$STATE_FILE" ]] || { echo "no state file at $STATE_FILE — nothing to stop?" >&2; exit 1; }
# shellcheck disable=SC1090
source "$STATE_FILE"

ok() { echo "✓ $*"; }

# Kill processes (best-effort; PIDs may already be dead)
for p in "${BRIDGE_PID:-}" "${TUNNEL_PID:-}"; do
  if [[ -n "$p" ]] && kill -0 "$p" 2>/dev/null; then
    kill "$p" 2>/dev/null && ok "killed pid $p" || true
  fi
done

# Flip MC back to platform-managed
if [[ -n "${JWT:-}" && -n "${MC_API:-}" ]]; then
  HTTP=$(curl -s -o /tmp/teardown-flip-resp -w '%{http_code}' \
    -X POST "$MC_API/beak/me/duck/$SD/workspace-url" \
    -H "Authorization: Bearer $JWT" -H 'Content-Type: application/json' \
    -d '{}')
  if [[ "$HTTP" == "200" ]]; then
    ok "MC flipped back to platform-managed"
  else
    echo "✗ flip HTTP $HTTP — manual: curl -X POST $MC_API/beak/me/duck/$SD/workspace-url -H 'Authorization: Bearer <JWT>' -d '{}'" >&2
  fi
fi

# Clean up state files (keep logs for debugging)
rm -f "$STATE_FILE" "/tmp/spaceduck-flip-$SD.json"
ok "state files removed (logs at /tmp/spaceduck-{bridge,tunnel,selftest}-$SD.log)"
