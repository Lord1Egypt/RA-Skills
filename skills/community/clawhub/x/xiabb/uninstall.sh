#!/bin/bash
echo "Uninstalling XiaBB..."

# Stop if running
pkill -f "XiaBB.app/Contents/MacOS/XiaBB" 2>/dev/null

# Remove auto-start
launchctl unload ~/Library/LaunchAgents/com.xiabb.plist 2>/dev/null
rm -f ~/Library/LaunchAgents/com.xiabb.plist

# Remove app
rm -rf "/Applications/XiaBB.app"

# Remove log
rm -f ~/Library/Logs/XiaBB.log

echo "Uninstalled."
echo "   Config and API key at ~/Tools/xiabb/ left intact."
echo "   To fully remove: rm -rf ~/Tools/xiabb/"
