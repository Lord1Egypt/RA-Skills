#!/bin/bash
# VPN Tunnel Down - Stop SOCKS5 proxy and WireGuard
# Usage: vpn-down.sh

set -e

CLOUD_SSH_HOST="47.85.45.122"
SOCKS_PORT=1080

echo "[1/2] Stopping SOCKS5 proxy..."
if pkill -f "ssh.*-D $SOCKS_PORT.*$CLOUD_SSH_HOST" 2>/dev/null; then
    echo "  SOCKS5 proxy stopped ✓"
else
    echo "  No SOCKS5 proxy running"
fi

echo "[2/2] Stopping WireGuard..."
echo "crscd" | sudo -S wg-quick down wg0 2>/dev/null || {
    echo "  WireGuard already down"
}

echo "VPN Tunnel closed ✓"
