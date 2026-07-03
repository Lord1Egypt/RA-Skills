#!/bin/bash
#===========================================================
# Start Sol - Quick one-liner
#===========================================================
# Usage: bash start-sol.sh

echo "🚀 Starting Sol..."

# Start gateway if not running
if ! openclaw gateway status 2>/dev/null | grep -q "running"; then
    openclaw gateway start
    sleep 2
fi

# Check status
if openclaw gateway status 2>/dev/null | grep -q "running"; then
    echo "✅ Sol is online!"
    echo ""
    openclaw gateway status | grep -E "Runtime|Dashboard"
else
    echo "❌ Sol failed to start"
    echo "Run: bash SolCal-Recovery.sh diagnose"
fi