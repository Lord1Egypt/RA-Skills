#!/bin/bash
set -euo pipefail

echo "=== record2note Uninstall ==="

# Unload launchd agent
PLIST="$HOME/Library/LaunchAgents/com.user.record2note.plist"
if [ -f "$PLIST" ]; then
    if launchctl unload "$PLIST" 2>/dev/null; then
        rm "$PLIST"
        echo "launchd agent removed."
    else
        echo "Warning: could not unload launchd agent." >&2
    fi
fi

echo ""
echo "Uninstall complete."
echo "Note: config, recordings, and notes were NOT deleted."
echo "  Config: <skill_folder>/config.json"
echo "  Recordings: your configured directories"
echo "  Notes: kept in your Obsidian vault"
echo "To remove these manually, delete the directories above."
