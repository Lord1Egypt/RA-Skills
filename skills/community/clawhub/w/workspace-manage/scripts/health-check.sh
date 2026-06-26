#!/usr/bin/env bash
# Workspace Health Check - Audit workspace health and entropy
# Part of workspace-manager skill

set -euo pipefail

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
SCORE=100
ISSUES=()

echo "=========================================="
echo "      🏥 Workspace Health Check"
echo "=========================================="
echo "Date: $(date '+%Y-%m-%d %H:%M')"
echo "Path: $WORKSPACE"
echo ""

# 1. Broken symlinks
echo "1. Checking for broken symlinks..."
BROKEN=$(find "$WORKSPACE" -type l ! -exec test -e {} \; -print 2>/dev/null || true)
if [ -n "$BROKEN" ]; then
    SCORE=$((SCORE - 10 * $(echo "$BROKEN" | wc -l)))
    ISSUES+=("🔴 Broken symlinks found:")
    while IFS= read -r link; do
        ISSUES+=("   • $link")
    done <<< "$BROKEN"
    echo "   ⚠️  Found $(echo "$BROKEN" | wc -l) broken symlinks"
else
    echo "   ✅ No broken symlinks"
fi
echo ""

# 2. Empty directories
echo "2. Checking for empty directories..."
EMPTY=$(find "$WORKSPACE" -mindepth 1 -type d -empty 2>/dev/null | grep -v -E "(node_modules|\.git|memory|Workspace_Human|Workspace_Agent)" || true)
if [ -n "$EMPTY" ]; then
    COUNT=$(echo "$EMPTY" | wc -l)
    SCORE=$((SCORE - 2 * COUNT))
    ISSUES+=("🟡 Empty directories: $COUNT")
    echo "   ⚠️  Found $COUNT empty directories"
else
    echo "   ✅ No empty directories"
fi
echo ""

# 3. Large files
echo "3. Checking for large files (>10MB)..."
LARGE=$(find "$WORKSPACE" -mindepth 1 -type f -size +10M 2>/dev/null | head -10 || true)
if [ -n "$LARGE" ]; then
    COUNT=$(echo "$LARGE" | wc -l)
    SCORE=$((SCORE - 5 * COUNT))
    ISSUES+=("🟠 Large files found: $COUNT")
    echo "   ⚠️  Found large files:"
    while IFS= read -r file; do
        SIZE=$(du -h "$file" 2>/dev/null | cut -f1)
        echo "   • $SIZE - $(basename "$file")"
    done <<< "$LARGE"
else
    echo "   ✅ No large files"
fi
echo ""

# 4. Malformed names (spaces, special chars)
echo "4. Checking for malformed names..."
MALFORMED=$(find "$WORKSPACE" -mindepth 1 \( -name "*[ ]*" -o -name "*[(){}[\]]*" -o -name "*[>&<|]*" \) 2>/dev/null | grep -v -E "(Workspace_Human|Workspace_Agent)" | head -10 || true)
if [ -n "$MALFORMED" ]; then
    COUNT=$(echo "$MALFORMED" | wc -l)
    SCORE=$((SCORE - 3 * COUNT))
    ISSUES+=("🟡 Malformed names: $COUNT")
    echo "   ⚠️  Found $COUNT problematic names:"
    while IFS= read -r file; do
        echo "   • $(basename "$file")"
    done <<< "$MALFORMED"
else
    echo "   ✅ No malformed names"
fi
echo ""

# 5. Disk usage by top-level directory
echo "5. Disk usage by directory:"
du -sh "$WORKSPACE"/* 2>/dev/null | sort -hr | head -10 | while IFS= read -r line; do
    echo "   $line"
done
echo ""

# 6. File counts
echo "6. File statistics:"
TOTAL_FILES=$(find "$WORKSPACE" -type f 2>/dev/null | wc -l)
TOTAL_DIRS=$(find "$WORKSPACE" -type d 2>/dev/null | wc -l)
echo "   📁 Total files: $TOTAL_FILES"
echo "   📂 Total directories: $TOTAL_DIRS"
echo ""

# 7. Recent changes (last 24h)
echo "7. Recently modified (last 24h):"
RECENT=$(find "$WORKSPACE" -type f -mtime -1 2>/dev/null | grep -v -E "(\.git|node_modules)" | head -10 || true)
if [ -n "$RECENT" ]; then
    echo "   Recent activity:"
    while IFS= read -r file; do
        echo "   • $(basename "$file")"
    done <<< "$RECENT"
else
    echo "   ℹ️  No recent changes"
fi
echo ""

# Final score
echo "=========================================="
if [ $SCORE -ge 90 ]; then
    STATUS="🟢 Healthy"
elif [ $SCORE -ge 70 ]; then
    STATUS="🟡 Fair"
elif [ $SCORE -ge 50 ]; then
    STATUS="🟠 Degraded"
else
    STATUS="🔴 Critical"
fi
echo "Health Score: $SCORE/100 - $STATUS"
echo "=========================================="
echo ""

# Recommendations
if [ ${#ISSUES[@]} -gt 0 ]; then
    echo "📋 Recommendations:"
    for issue in "${ISSUES[@]}"; do
        echo "   $issue"
    done
    echo ""
    echo "💡 Run cleanup: python3 {{SKILL_DIR}}/scripts/cleanup.py --execute"
fi
