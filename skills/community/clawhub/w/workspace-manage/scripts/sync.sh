#!/usr/bin/env bash
# Workspace Sync - Backup workspace to Google Drive via gog
# Part of workspace-manager skill
# ⚠️ This is an OPTIONAL extension. Requires 'gog' CLI to be installed and authenticated.
#    If gog is not available, skip gracefully without blocking other pipeline steps.

set -euo pipefail

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
HUMAN="$WORKSPACE/Workspace_Human"
AGENT="$WORKSPACE/Workspace_Agent"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Load optional config
CONFIG_FILE="$SKILL_DIR/config/sync-config.json"
if [ -f "$CONFIG_FILE" ]; then
    source <(jq -r 'to_entries | .[] | "SYNC_\(.key|ascii_upcase)=\(.value)"' "$CONFIG_FILE" 2>/dev/null || true)
fi

# Sync config (all optional, defaults to false to be conservative)
SYNC_HUMAN="${SYNC_HUMAN:-true}"
SYNC_AGENT="${SYNC_AGENT:-false}"
SYNC_BACKUP="${SYNC_BACKUP:-true}"
OUTPUT_FOLDER="${OUTPUT_FOLDER:-AI_Workspace}"
BACKUP_FOLDER="${BACKUP_FOLDER:-AI_Workspace_Backup}"

echo "=========================================="
echo "      ☁️  Workspace Sync (Optional)"
echo "=========================================="
echo "Date: $(date '+%Y-%m-%d %H:%M')"
echo ""

# Check if gog is available
if ! command -v gog &>/dev/null; then
    echo "ℹ️  gog CLI not found. Sync skipped."
    echo "   To enable: go install github.com/cilaboratory/gog@latest"
    echo "   Then run: gog auth login"
    exit 0
fi

# Check if gog is authenticated
if ! gog whoami &>/dev/null; then
    echo "ℹ️  gog not authenticated. Sync skipped."
    echo "   Run 'gog auth login' to enable sync."
    exit 0
fi

SYNCED=0
FAILED=0

# Sync Workspace_Human/ (all contents)
if [ "$SYNC_HUMAN" = "true" ] && [ -d "$HUMAN" ]; then
    echo "📁 Syncing Workspace_Human/..."
    echo "   → $OUTPUT_FOLDER/Workspace_Human/"
    
    FILE_COUNT=$(find "$HUMAN" -type f 2>/dev/null | wc -l || echo 0)
    echo "   Files: $FILE_COUNT"
    
    if [ "$FILE_COUNT" -eq 0 ]; then
        echo "   ℹ️  Nothing to sync"
    elif gog drive sync upload "$HUMAN/" --folder "$OUTPUT_FOLDER" 2>/dev/null; then
        echo "   ✅ Workspace_Human synced"
        SYNCED=$((SYNCED + 1))
    else
        echo "   ❌ Failed"
        FAILED=$((FAILED + 1))
    fi
    echo ""
fi

# Sync Workspace_Agent/ (all contents)
if [ "$SYNC_AGENT" = "true" ] && [ -d "$AGENT" ]; then
    echo "🧠 Syncing Workspace_Agent/..."
    echo "   → $OUTPUT_FOLDER/Workspace_Agent/"
    
    FILE_COUNT=$(find "$AGENT" -type f 2>/dev/null | wc -l || echo 0)
    echo "   Files: $FILE_COUNT"
    
    if [ "$FILE_COUNT" -eq 0 ]; then
        echo "   ℹ️  Nothing to sync"
    elif gog drive sync upload "$AGENT/" --folder "$OUTPUT_FOLDER" 2>/dev/null; then
        echo "   ✅ Workspace_Agent synced"
        SYNCED=$((SYNCED + 1))
    else
        echo "   ❌ Failed"
        FAILED=$((FAILED + 1))
    fi
    echo ""
fi

# Backup core config files
if [ "$SYNC_BACKUP" = "true" ]; then
    echo "💾 Backing up core configuration files..."
    echo "   → $BACKUP_FOLDER"
    
    CORE_FILES=("MEMORY.md" "SOUL.md" "USER.md" "AGENTS.md" "IDENTITY.md")
    BACKED_UP=0
    
    for file in "${CORE_FILES[@]}"; do
        if [ -f "$WORKSPACE/$file" ]; then
            if gog drive sync upload "$WORKSPACE/$file" --folder "$BACKUP_FOLDER" 2>/dev/null; then
                BACKED_UP=$((BACKED_UP + 1))
            fi
        fi
    done
    
    echo "   ✅ Backed up $BACKED_UP core file(s)"
    [ $BACKED_UP -gt 0 ] && SYNCED=$((SYNCED + 1))
    echo ""
fi

echo "=========================================="
echo "📊 Sync Summary:"
echo "   ✅ Successful: $SYNCED"
echo "   ❌ Failed: $FAILED"
echo "=========================================="

[ $FAILED -gt 0 ] && exit 1 || exit 0
