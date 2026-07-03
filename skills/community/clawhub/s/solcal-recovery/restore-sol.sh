#!/bin/bash
#===========================================================
# Restore Sol State
#===========================================================
# Usage: bash restore-sol.sh [backup-folder]

BACKUP_DIR="${1:-$(ls -td ~/SolCal-Backups/*/ 2>/dev/null | head -1)}"

if [ -z "$BACKUP_DIR" ] || [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ No backup found!"
    echo "Usage: bash restore-sol.sh ~/SolCal-Backups/20260403_120000"
    exit 1
fi

echo "📂 Restoring from: $BACKUP_DIR"

# Stop gateway first
openclaw gateway stop 2>/dev/null

# Restore config
if [ -f "$BACKUP_DIR/openclaw.json" ]; then
    cp "$BACKUP_DIR/openclaw.json" ~/.openclaw/openclaw.json
    echo "✓ Config restored"
fi

# Restore sessions
if [ -d "$BACKUP_DIR/sessions" ]; then
    rm -rf ~/.openclaw/agents/main/sessions 2>/dev/null
    cp -r "$BACKUP_DIR/sessions" ~/.openclaw/agents/main/
    echo "✓ Sessions restored"
fi

# Start gateway
openclaw gateway start

echo ""
echo "✅ Restore complete!"
echo "Run: bash start-sol.sh"