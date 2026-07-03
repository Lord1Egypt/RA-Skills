#!/bin/bash
#===========================================================
# Save Sol State - Backup everything
#===========================================================
# Usage: bash save-sol.sh

BACKUP_DIR="${HOME}/SolCal-Backups/$(date +%Y%m%d_%H%M%S)"
CONFIG_FILE="~/.openclaw/openclaw.json"
SESSIONS_DIR="~/.openclaw/agents/main/sessions"

echo "💾 Saving Sol state..."
echo "Backup location: $BACKUP_DIR"

mkdir -p "$BACKUP_DIR"

# Save config
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "$BACKUP_DIR/openclaw.json"
    echo "✓ Config saved"
fi

# Save sessions
if [ -d "$SESSIONS_DIR" ]; then
    cp -r "$SESSIONS_DIR" "$BACKUP_DIR/sessions"
    echo "✓ Sessions saved"
fi

# Save skills
if [ -d ~/.openclaw/workspace/skills ]; then
    mkdir -p "$BACKUP_DIR/skills"
    cp -r ~/.openclaw/workspace/skills/* "$BACKUP_DIR/skills/" 2>/dev/null || true
    echo "✓ Skills saved"
fi

# Save secrets (token only)
if [ -f ~/.openclaw/workspace/secrets/github-token.txt ]; then
    mkdir -p "$BACKUP_DIR/secrets"
    cp ~/.openclaw/workspace/secrets/github-token.txt "$BACKUP_DIR/secrets/" 2>/dev/null || true
    echo "✓ GitHub token saved"
fi

echo ""
echo "✅ Backup complete: $BACKUP_DIR"
echo "To restore: bash restore-sol.sh $BACKUP_DIR"