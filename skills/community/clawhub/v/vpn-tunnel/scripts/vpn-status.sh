#!/bin/bash
# VPN Tunnel Status - Show WireGuard + SOCKS5 proxy status
# Usage: vpn-status.sh

SOCKS_PORT=1080

echo "=== WireGuard ==="
echo "crscd" | sudo -S wg show 2>/dev/null || echo "  Not connected"

echo ""
echo "=== SOCKS5 Proxy ==="
if pgrep -f "ssh.*-D $SOCKS_PORT" > /dev/null; then
    echo "  Running on 127.0.0.1:$SOCKS_PORT ✓"
else
    echo "  Not running"
fi

echo ""
echo "=== Quick Test ==="
if pgrep -f "ssh.*-D $SOCKS_PORT" > /dev/null; then
    echo "  Google: $(curl -s --max-time 8 --proxy socks5h://127.0.0.1:$SOCKS_PORT -o /dev/null -w '%{http_code}' https://www.google.com 2>/dev/null || echo FAIL)"
    echo "  GitHub: $(curl -s --max-time 8 --proxy socks5h://127.0.0.1:$SOCKS_PORT -o /dev/null -w '%{http_code}' https://github.com 2>/dev/null || echo FAIL)"
else
    echo "  Proxy not running, skip"
fi
