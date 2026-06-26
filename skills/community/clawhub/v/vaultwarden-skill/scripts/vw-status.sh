#!/usr/bin/env bash
# vw-status.sh — check vault connection and session state
# Returns: ok:unlocked | ok:locked | ok:unauthenticated | error

set -euo pipefail

STATUS=$(bw status 2>/dev/null | jq -r '"\(.status) \(.serverUrl)"' || echo "error")
echo "$STATUS"
