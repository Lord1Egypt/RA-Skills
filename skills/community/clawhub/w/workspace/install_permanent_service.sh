#!/bin/bash
# Install Permanent Jira Auto Tracker Service

echo "🔧 Installing Permanent Jira Auto Tracker Service"
echo "=================================================="
echo ""

# Check prerequisites
echo "🧪 Checking prerequisites..."
if [[ ! -f "start_auto_tracker.sh" ]]; then
    echo "❌ Error: Must run from the workspace directory"
    echo "   cd ~/.openclaw/workspace"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found"
    exit 1
fi

# Test Jira connection
echo "Testing Jira connection..."
python3 -c "
try:
    from jira_tools import JiraClient
    jira = JiraClient()
    if jira.test_connection():
        print('✅ Jira connection successful')
    else:
        print('❌ Jira connection failed')
        exit(1)
except Exception as e:
    print(f'❌ Error: {e}')
    exit(1)
"

if [[ $? -ne 0 ]]; then
    exit 1
fi

# Install LaunchAgent
echo ""
echo "📁 Installing LaunchAgent..."
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_SRC="com.user.jiraautotracker.plist"
PLIST_DEST="$LAUNCH_AGENTS_DIR/com.user.jiraautotracker.plist"

mkdir -p "$LAUNCH_AGENTS_DIR"
cp "$PLIST_SRC" "$PLIST_DEST"

if [[ $? -eq 0 ]]; then
    echo "✅ LaunchAgent installed to: $PLIST_DEST"
else
    echo "❌ Failed to install LaunchAgent"
    exit 1
fi

# Set permissions
chmod 644 "$PLIST_DEST"

# Load the LaunchAgent
echo ""
echo "🔄 Loading LaunchAgent..."
launchctl unload "$PLIST_DEST" 2>/dev/null
launchctl load "$PLIST_DEST"

if [[ $? -eq 0 ]]; then
    echo "✅ LaunchAgent loaded successfully"
else
    echo "⚠️  Failed to load LaunchAgent (may need manual load)"
fi

# Start the service now
echo ""
echo "🚀 Starting Auto Tracker now..."
./start_auto_tracker.sh start

sleep 3

echo ""
echo "🎉 PERMANENT SERVICE INSTALLED!"
echo "=================================================="
echo ""
echo "📋 What this does:"
echo "   • Starts automatically on system login/reboot"
echo "   • Runs 24/7 in background"
echo "   • Auto-restarts if crashes"
echo "   • Low priority (minimal resource usage)"
echo ""
echo "⏰ Daily Schedule:"
echo "   08:00-08:30  Creates daily work log automatically"
echo "   09:30        Morning reminder"
echo "   12:00        Mid-day check"
echo "   15:30        Afternoon check"
echo "   17:00        End of day approaching"
echo "   18:30        Final reminder"
echo "   + Random reminders during work hours"
echo ""
echo "🔧 Manual Controls:"
echo "   Check status: ./start_auto_tracker.sh status"
echo "   Stop service: ./start_auto_tracker.sh stop"
echo "   View logs: ./start_auto_tracker.sh logs"
echo "   Restart: ./start_auto_tracker.sh restart"
echo ""
echo "📊 System Info:"
echo "   Service PID: cat .auto_tracker.pid"
echo "   Main logs: tail -f jira_tracker.log"
echo "   Service logs: tail -f autotracker_service.log"
echo ""
echo "🔒 To uninstall:"
echo "   ./start_auto_tracker.sh stop"
echo "   launchctl unload $PLIST_DEST"
echo "   rm $PLIST_DEST"
echo ""
echo "=================================================="
echo "✅ Installation complete! The service is now running."
echo "   It will continue running even after reboot."
echo "   You can close this terminal."
echo "=================================================="