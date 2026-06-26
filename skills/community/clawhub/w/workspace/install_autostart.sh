#!/bin/bash
# Install Jira Prompts Autostart

echo "🔧 Installing Jira Prompts Autostart..."
echo ""

# Check if we're in the right directory
if [[ ! -f "start_prompts.sh" ]]; then
    echo "❌ Error: Must run from the workspace directory"
    echo "   cd ~/.openclaw/workspace"
    exit 1
fi

# Copy LaunchAgent plist to user's LaunchAgents directory
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_SRC="com.user.jiraprompts.plist"
PLIST_DEST="$LAUNCH_AGENTS_DIR/com.user.jiraprompts.plist"

echo "📁 Installing LaunchAgent..."
mkdir -p "$LAUNCH_AGENTS_DIR"
cp "$PLIST_SRC" "$PLIST_DEST"

if [[ $? -eq 0 ]]; then
    echo "✅ LaunchAgent installed to: $PLIST_DEST"
else
    echo "❌ Failed to install LaunchAgent"
    exit 1
fi

# Load the LaunchAgent
echo ""
echo "🔄 Loading LaunchAgent..."
launchctl unload "$PLIST_DEST" 2>/dev/null
launchctl load "$PLIST_DEST"

if [[ $? -eq 0 ]]; then
    echo "✅ LaunchAgent loaded successfully"
else
    echo "❌ Failed to load LaunchAgent"
    echo "   You may need to load it manually:"
    echo "   launchctl load $PLIST_DEST"
fi

# Set permissions
chmod 644 "$PLIST_DEST"

echo ""
echo "🎉 Autostart installation complete!"
echo ""
echo "📋 What this does:"
echo "   • Starts automatically at 8:00 AM on weekdays"
echo "   • Runs even if terminal is closed"
echo "   • Logs to: launchagent.log and launchagent.error.log"
echo ""
echo "🔧 Manual controls:"
echo "   Start now: launchctl start com.user.jiraprompts"
echo "   Stop: launchctl stop com.user.jiraprompts"
echo "   Unload: launchctl unload $PLIST_DEST"
echo "   Check status: launchctl list | grep jiraprompts"
echo ""
echo "📊 To verify it's working tomorrow:"
echo "   ./start_prompts.sh status"
echo "   tail -f prompt_system.log"
echo ""
echo "⚠️  Note: The system will auto-start at 8:00 AM tomorrow."
echo "   If you want to test today, run: ./start_prompts.sh start"