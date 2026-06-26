#!/usr/bin/env bash
# Restart OpenClaw service after model updates
# Part of updating-openrouter-free-models skill for OpenClaw

set -e

echo "🔄 Restarting OpenClaw..."

# Check if OpenClaw is running via launchctl
LAUNCHCTL_SVC=$(launchctl list | grep "ai.openclaw.gateway" || true)

if [[ -n "$LAUNCHCTL_SVC" ]]; then
    echo "Found OpenClaw launchctl service, restarting..."
    # Try gui/501/ai.openclaw.gateway format
    launchctl kickstart -k "gui/501/ai.openclaw.gateway" 2>/dev/null || \
    launchctl kickstart -k "ai.openclaw.gateway" 2>/dev/null || \
    echo "Warning: Could not restart via launchctl (service not found or permission denied)"
    sleep 2
fi

# Kill any existing gateway processes
if pgrep -f "openclaw.*gateway" > /dev/null; then
    echo "Stopping existing OpenClaw gateway processes..."
    pkill -f "openclaw.*gateway"
    sleep 2
fi

# Start OpenClaw gateway
echo "Starting OpenClaw gateway..."
if command -v openclaw &> /dev/null; then
    # Run in background with log redirection
    nohup openclaw gateway > /tmp/openclaw-gateway.log 2>&1 &
    OPENCLAW_PID=$!
    echo "Started OpenClaw gateway (PID: $OPENCLAW_PID)"

    # Wait and verify
    sleep 3
    if ps -p $OPENCLAW_PID > /dev/null; then
        echo "✅ OpenClaw gateway started successfully"
        echo "📝 Logs: tail -f /tmp/openclaw-gateway.log"
        echo "🛑 Stop: kill $OPENCLAW_PID"
    else
        echo "⚠️  Process exited unexpectedly, check log:"
        tail -20 /tmp/openclaw-gateway.log 2>/dev/null || echo "No log file"
        exit 1
    fi
else
    echo "⚠️  'openclaw' command not found in PATH"
    echo "Ensure OpenClaw is installed: npm install -g openclaw"
    exit 1
fi
