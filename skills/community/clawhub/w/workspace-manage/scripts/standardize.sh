#!/usr/bin/env bash
# Workspace Standardize - Ensure standard directory structure exists
# Part of workspace-manager skill

set -euo pipefail

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"

echo "=========================================="
echo "      🏗️  Workspace Standardizer"
echo "=========================================="
echo "Date: $(date '+%Y-%m-%d %H:%M')"
echo "Path: $WORKSPACE"
echo ""

# Define all required directories
HUMAN_DIRS=(
    "$WORKSPACE/Workspace_Human/input"
    "$WORKSPACE/Workspace_Human/output/images"
    "$WORKSPACE/Workspace_Human/output/docs"
    "$WORKSPACE/Workspace_Human/output/data"
    "$WORKSPACE/Workspace_Human/backup"
    "$WORKSPACE/Workspace_Human/temp"
)

AGENT_DIRS=(
    "$WORKSPACE/Workspace_Agent/memory"
    "$WORKSPACE/Workspace_Agent/skills"
    "$WORKSPACE/Workspace_Agent/subagents"
    "$WORKSPACE/Workspace_Agent/shared_context"
    "$WORKSPACE/Workspace_Agent/artifacts"
    "$WORKSPACE/Workspace_Agent/cache"
    "$WORKSPACE/Workspace_Agent/logs"
    "$WORKSPACE/Workspace_Agent/skills_custom"
    "$WORKSPACE/Workspace_Agent/prompts"
    "$WORKSPACE/Workspace_Agent/kb"
)

SYSTEM_DIRS=(
    "$WORKSPACE/archive"
    "$WORKSPACE/scripts"
    "$WORKSPACE/secret"
)

ALL_DIRS=("${HUMAN_DIRS[@]}" "${AGENT_DIRS[@]}" "${SYSTEM_DIRS[@]}")

CREATED=0
EXISTING=0

for dir in "${ALL_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        EXISTING=$((EXISTING + 1))
    else
        mkdir -p "$dir"
        echo "   ✅ Created: ${dir#$WORKSPACE/}"
        CREATED=$((CREATED + 1))
    fi
done

echo ""
echo "📊 Summary:"
echo "   Existing: $EXISTING directories"
echo "   Created:  $CREATED directories"
echo ""

# Check for misplaced files in root
echo "📋 Checking root directory for misplaced files..."
ROOT_FILES=$(find "$WORKSPACE" -maxdepth 1 -type f 2>/dev/null | grep -v -E "^(MEMORY|SOUL|USER|AGENTS|HEARTBEAT|TOOLS|IDENTITY)" || true)

if [ -z "$ROOT_FILES" ]; then
    echo "   ✅ Root directory is clean."
else
    COUNT=$(echo "$ROOT_FILES" | wc -l)
    echo "   ⚠️  Found $COUNT misplaced file(s) in root:"
    echo "$ROOT_FILES" | while read -r f; do
        echo "   • $(basename "$f")"
    done
    echo ""
    echo "   💡 Run 'organize.sh' to move these to Workspace_Human/"
fi

echo ""
echo "✅ Standardization complete."
