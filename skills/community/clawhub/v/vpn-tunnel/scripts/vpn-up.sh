#!/bin/bash
# VPN Tunnel Up - Start WireGuard and SOCKS5 proxy via cloud VPS
# Usage: vpn-up.sh [--test]

set -e

CLOUD_SSH_HOST="47.85.45.122"
CLOUD_SSH_USER="smile"
CLOUD_SSH_PASS="thXBwViKf+uSUL0LIZTZ3AeV"
SOCKS_PORT=1080

# === Start WireGuard ===
echo "[1/3] Starting WireGuard..."
echo "crscd" | sudo -S wg-quick up wg0 2>/dev/null || {
    echo "  WireGuard already up or failed to start"
}

# Wait for handshake
echo "[2/3] Waiting for handshake..."
for i in $(seq 1 10); do
    if echo "crscd" | sudo -S wg show 2>/dev/null | grep -q "handshake"; then
        echo "  Handshake established ✓"
        break
    fi
    sleep 2
done

# === Start SOCKS5 proxy ===
echo "[3/3] Starting SOCKS5 proxy on port $SOCKS_PORT..."
# Kill any existing proxy
pkill -f "ssh.*-D $SOCKS_PORT.*$CLOUD_SSH_HOST" 2>/dev/null || true
sleep 1

sshpass -p "$CLOUD_SSH_PASS" ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -f -N -D $SOCKS_PORT "$CLOUD_SSH_USER@$CLOUD_SSH_HOST" 2>/dev/null

sleep 2
if pgrep -f "ssh.*-D $SOCKS_PORT" > /dev/null; then
    echo "  SOCKS5 proxy running on 127.0.0.1:$SOCKS_PORT ✓"
else
    echo "  ERROR: SOCKS5 proxy failed to start"
    exit 1
fi

echo ""
echo "=== VPN Tunnel Ready ==="
echo "SOCKS5: 127.0.0.1:$SOCKS_PORT"
echo "Usage: curl --proxy socks5h://127.0.0.1:$SOCKS_PORT <url>"

# Run test if requested
if [ "$1" = "--test" ]; then
    echo ""
    echo "=== Testing ==="
    echo "Google: $(curl -s --max-time 10 --proxy socks5h://127.0.0.1:$SOCKS_PORT -o /dev/null -w '%{http_code}' https://www.google.com 2>/dev/null || echo FAIL)"
    echo "GitHub: $(curl -s --max-time 10 --proxy socks5h://127.0.0.1:$SOCKS_PORT -o /dev/null -w '%{http_code}' https://github.com 2>/dev/null || echo FAIL)"
    echo "Docker Hub: $(curl -s --max-time 10 --proxy socks5h://127.0.0.1:$SOCKS_PORT -o /dev/null -w '%{http_code}' https://hub.docker.com 2>/dev/null || echo FAIL)"
    echo "PyPI: $(curl -s --max-time 10 --proxy socks5h://127.0.0.1:$SOCKS_PORT -o /dev/null -w '%{http_code}' https://pypi.org 2>/dev/null || echo FAIL)"
    echo "IP (via proxy): $(curl -s --max-time 10 --proxy socks5h://127.0.0.1:$SOCKS_PORT https://ifconfig.me 2>/dev/null || echo FAIL)"
fi
