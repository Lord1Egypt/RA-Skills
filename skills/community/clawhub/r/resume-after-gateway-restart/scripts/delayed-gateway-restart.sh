#!/usr/bin/env bash
set -euo pipefail

# Schedule a gateway restart after a short delay using systemd-run.
# This avoids killing the current agent before its "about to restart" message is delivered.
#
# Usage:
#   delayed-gateway-restart.sh 8

DELAY_SEC=${1:-15}
UNIT="openclaw-gateway-restart-$(date +%s)"

# Run systemctl restart in a separate transient user unit.
systemd-run --user --quiet --unit "$UNIT" --on-active="${DELAY_SEC}s" /usr/bin/systemctl --user restart openclaw-gateway.service

echo "Scheduled gateway restart in ${DELAY_SEC}s (unit=$UNIT)"