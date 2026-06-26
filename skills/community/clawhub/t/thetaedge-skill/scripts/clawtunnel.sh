#!/usr/bin/env bash
#
# clawtunnel.sh — SSH tunnels between host and OpenClaw VM
#
# Usage: ./clawtunnel.sh
#   -L: Forward VM's OpenClaw dashboard to host at http://localhost:18789
#   -R: Expose host's ThetaEdge API to VM at localhost:3200
#   Press Ctrl+C to close the tunnel.

set -euo pipefail

VM_PORT=2222
VM_USER=openclaw
VM_HOST=localhost
DASHBOARD_PORT=18789
API_PORT=3200

echo "Opening tunnels to OpenClaw VM..."
echo "  Dashboard (local):  http://localhost:$DASHBOARD_PORT"
echo "  ThetaEdge API (remote): localhost:$API_PORT → host:$API_PORT"
echo "  Press Ctrl+C to close."
echo ""

ssh -N \
  -L "$DASHBOARD_PORT:127.0.0.1:$DASHBOARD_PORT" \
  -R "$API_PORT:127.0.0.1:$API_PORT" \
  -p "$VM_PORT" "$VM_USER@$VM_HOST"
