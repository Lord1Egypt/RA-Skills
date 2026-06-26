#!/usr/bin/env bash
# Workspace Organizer - Move files to proper locations
# Part of workspace-manager skill

set -euo pipefail

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
HUMAN="$WORKSPACE/Workspace_Human"
AGENT="$WORKSPACE/Workspace_Agent"
ARTIFACTS="$AGENT/artifacts"

echo "=========================================="
echo "      📂 Workspace Organizer"
echo "=========================================="
echo "Date: $(date '+%Y-%m-%d %H:%M')"
echo ""

# Ensure directories exist
mkdir -p "$HUMAN/input"
mkdir -p "$HUMAN/output/images"
mkdir -p "$HUMAN/output/docs"
mkdir -p "$HUMAN/output/data"
mkdir -p "$HUMAN/backup"
mkdir -p "$HUMAN/temp"
mkdir -p "$AGENT/memory"
mkdir -p "$AGENT/skills"
mkdir -p "$AGENT/subagents"
mkdir -p "$AGENT/shared_context"
mkdir -p "$AGENT/artifacts"
mkdir -p "$AGENT/cache"
mkdir -p "$AGENT/logs"
mkdir -p "$AGENT/skills_custom"
mkdir -p "$AGENT/prompts"
mkdir -p "$AGENT/kb"

echo "✅ Directory structure verified"
echo ""

# Organize artifacts
echo "📦 Organizing artifacts..."
MOVED=0

# Images from artifacts -> Workspace_Human/output/images
find "$ARTIFACTS" -maxdepth 1 -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.webp" \) 2>/dev/null | while read -r file; do
    mv "$file" "$HUMAN/output/images/"
    echo "   📷 $(basename "$file") -> output/images/"
    MOVED=$((MOVED + 1))
done

# Docs from artifacts -> Workspace_Human/output/docs
find "$ARTIFACTS" -maxdepth 1 -type f \( -name "*.pdf" -o -name "*.docx" -o -name "*.doc" \) 2>/dev/null | while read -r file; do
    mv "$file" "$HUMAN/output/docs/"
    echo "   📄 $(basename "$file") -> output/docs/"
    MOVED=$((MOVED + 1))
done

# Data files from artifacts -> Workspace_Human/output/data
find "$ARTIFACTS" -maxdepth 1 -type f \( -name "*.json" -o -name "*.csv" -o -name "*.xml" \) 2>/dev/null | while read -r file; do
    mv "$file" "$HUMAN/output/data/"
    echo "   📊 $(basename "$file") -> output/data/"
    MOVED=$((MOVED + 1))
done

# Temp files -> Workspace_Human/temp
find "$ARTIFACTS" -maxdepth 1 -type f \( -name "*screenshot*" -o -name "cdp_tmp_*" -o -name "*.tmp" \) 2>/dev/null | while read -r file; do
    mv "$file" "$HUMAN/temp/"
    echo "   🕐 $(basename "$file") -> temp/"
    MOVED=$((MOVED + 1))
done

# Files in workspace root -> artifacts
find "$WORKSPACE" -maxdepth 1 -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.pdf" -o -name "*.json" -o -name "*.csv" \) 2>/dev/null | grep -v -E "^(MEMORY|SOUL|USER|AGENTS|HEARTBEAT|TOOLS)" | while read -r file; do
    mv "$file" "$ARTIFACTS/"
    echo "   📦 $(basename "$file") -> artifacts/"
    MOVED=$((MOVED + 1))
done

echo ""
if [ $MOVED -eq 0 ]; then
    echo "✅ No files to organize."
else
    echo "✅ Organized $MOVED files."
fi
