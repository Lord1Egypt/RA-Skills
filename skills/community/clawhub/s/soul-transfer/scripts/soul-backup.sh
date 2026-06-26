#!/bin/bash
# soul-backup.sh — Quick backup of OpenClaw workspace to git
# Usage: bash soul-backup.sh [commit message]
#
# Set WORKSPACE env var or it defaults to ~/.openclaw/workspace

set -e

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
cd "$WORKSPACE"

# Check git is initialized
if [ ! -d .git ]; then
  echo "❌ No git repo in workspace. Run: git init && git remote add origin <url>"
  exit 1
fi

# Check remote exists
if ! git remote get-url origin &>/dev/null; then
  echo "❌ No git remote configured. Run: git remote add origin <url>"
  exit 1
fi

# Export current OpenClaw config for future restore
# This captures channel tokens, API keys, etc.
CONFIG_BACKUP="openclaw-config-backup.json"
if command -v openclaw &>/dev/null; then
  echo "📋 Exporting OpenClaw config..."
  openclaw config get --json 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    parsed = data.get('result', {}).get('parsed', data)
    with open('$CONFIG_BACKUP', 'w') as f:
        json.dump(parsed, f, indent=2)
    print('  ✅ Config exported to $CONFIG_BACKUP')
except Exception as e:
    print(f'  ⚠️ Config export failed: {e}')
" 2>/dev/null || echo "  ⚠️ Config export skipped (openclaw not available)"
fi

# Stage all changes
git add -A

# Check if there are changes
if git diff --cached --quiet; then
  echo "✅ No changes to backup"
  exit 0
fi

# Commit
MSG="${1:-backup: $(date +%Y-%m-%d_%H%M)}"
git commit -m "$MSG"

# Push
echo "📤 Pushing to remote..."
git push origin master 2>&1 || git push origin main 2>&1

echo "✅ Backup complete: $(git log --oneline -1)"
