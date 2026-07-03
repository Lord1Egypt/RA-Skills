#!/bin/bash
#===========================================================
# Emergency Repair - Fix everything
#===========================================================
# Usage: bash emergency-repair.sh

echo "🆘 EMERGENCY REPAIR"
echo "This will reset and restart Sol..."
echo ""

# 1. Stop everything
echo "[1/6] Stopping Gateway..."
openclaw gateway stop 2>/dev/null
pkill -f openclaw 2>/dev/null
sleep 1

# 2. Clear logs
echo "[2/6] Clearing logs..."
rm -f /tmp/openclaw/*.log 2>/dev/null

# 3. Reinstall if needed
echo "[3/6] Checking OpenClaw..."
if ! command -v openclaw &> /dev/null; then
    echo "Installing OpenClaw..."
    brew install openclaw 2>/dev/null || npm install -g openclaw
fi

# 4. Start fresh
echo "[4/6] Starting fresh..."
openclaw gateway start
sleep 3

# 5. Check status
echo "[5/6] Verifying..."
if openclaw gateway status | grep -q "running"; then
    echo "✅ SOL IS BACK ONLINE!"
    openclaw gateway status | grep -E "Runtime|Dashboard"
else
    echo "❌ Still not working"
    echo "Run: bash SolCal-Recovery.sh diagnose"
fi

echo "[6/6] Done."