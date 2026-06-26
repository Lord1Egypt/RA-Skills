#!/bin/bash
# Quick status check of all VPS
# EDIT THIS: Add your VPS IPs, names, username, and password

VPS_LIST=(
    "YOUR_INTERNAL_IP:Internal"
    "YOUR_VPS1_IP:VPS1"
    "YOUR_VPS2_IP:VPS2"
)

USER="YOUR_USERNAME"
PASS="YOUR_PASSWORD"

echo "=== VPS Health Check ==="
echo ""

for VPS_INFO in "${VPS_LIST[@]}"; do
    VPS=$(echo "$VPS_INFO" | cut -d: -f1)
    NAME=$(echo "$VPS_INFO" | cut -d: -f2)
    
    echo -n "$NAME ($VPS): "
    
    # Check if local
    if [ "$VPS" = "127.0.0.1" ] || [ "$VPS" = "$(hostname -I | awk '{print $1}')" ]; then
        echo "✅ Local"
        UPTIME=$(uptime -p)
        LOAD=$(cat /proc/loadavg | cut -d' ' -f1-3)
        PROVIDERS=$(docker ps --filter name=urnetwork --format '{{.Names}}' 2>/dev/null | wc -l)
        echo "  Uptime: $UPTIME"
        echo "  Load: $LOAD"
        echo "  Providers: $PROVIDERS"
    elif sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$USER@$VPS" "echo OK" 2>/dev/null | grep -q "OK"; then
        echo "✅ Online"
        
        # Get basic stats
        UPTIME=$(sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$USER@$VPS" "uptime -p" 2>/dev/null)
        LOAD=$(sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$USER@$VPS" "cat /proc/loadavg | cut -d' ' -f1-3" 2>/dev/null)
        PROVIDERS=$(sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$USER@$VPS" "docker ps --filter name=urnetwork --format '{{.Names}}' 2>/dev/null | wc -l" 2>/dev/null)
        
        echo "  Uptime: $UPTIME"
        echo "  Load: $LOAD"
        echo "  Providers: $PROVIDERS"
    else
        echo "❌ Offline"
    fi
    echo ""
done