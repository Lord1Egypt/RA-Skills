#!/usr/bin/env bash
# memory_health.sh — Generate a memory system health report.
# Shows stats, orphans, staleness, and token cost estimate.

set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
MEMORY_DIR="$WORKSPACE/memory"

echo "=== Memory Health Report ==="
echo "Generated: $(date -u '+%Y-%m-%d %H:%M UTC')"
echo ""

# 1. MEMORY.md stats
echo "--- MEMORY.md ---"
if [ -f "$MEMORY_FILE" ]; then
    LINES=$(wc -l < "$MEMORY_FILE")
    CHARS=$(wc -c < "$MEMORY_FILE")
    # Rough token estimate: 1 token ≈ 4 chars for English, ≈ 2 chars for CJK
    TOKENS_EST=$((CHARS / 3))
    SECTIONS=$(grep -c '^## ' "$MEMORY_FILE" || echo 0)

    echo "  Lines: $LINES"
    echo "  Characters: $CHARS"
    echo "  Estimated tokens: ~$TOKENS_EST"
    echo "  Sections: $SECTIONS"

    # Count by type
    echo "  Entries by type:"
    for TYPE in PREF PROJ TECH LESSON PEOPLE TEMP; do
        COUNT=$(grep -ci "\[$TYPE\]" "$MEMORY_FILE" 2>/dev/null | tail -1 || echo 0)
        COUNT=$(echo "$COUNT" | tr -d '[:space:]')
        if [ -n "$COUNT" ] && [ "$COUNT" -gt 0 ] 2>/dev/null; then
            echo "    [$TYPE]: $COUNT"
        fi
    done

    # Untagged entries
    UNTAGGED=$(grep -c '^  - ' "$MEMORY_FILE" 2>/dev/null | tail -1 || echo 0)
    UNTAGGED=$(echo "$UNTAGGED" | tr -d '[:space:]')
    TAGGED=$(grep -c '\[PREF\]\|\[PROJ\]\|\[TECH\]\|\[LESSON\]\|\[PEOPLE\]' "$MEMORY_FILE" 2>/dev/null | tail -1 || echo 0)
    TAGGED=$(echo "$TAGGED" | tr -d '[:space:]')
    ORPHANS=$((UNTAGGED - TAGGED))
    if [ "$ORPHANS" -lt 0 ]; then ORPHANS=0; fi
    echo "  Untagged entries: ~$ORPHANS"

    # Health warnings
    if [ "$LINES" -gt 200 ]; then
        echo "  ⚠️  MEMORY.md exceeds 200 lines — consider decay/archival"
    fi
    if [ "$TOKENS_EST" -gt 5000 ]; then
        echo "  ⚠️  Estimated token cost is high (~$TOKENS_EST) — run memory_decay.py"
    fi
else
    echo "  MEMORY.md not found!"
fi
echo ""

# 2. Daily memory files
echo "--- Daily Notes (memory/*.md) ---"
if [ -d "$MEMORY_DIR" ]; then
    FILE_COUNT=$(find "$MEMORY_DIR" -maxdepth 1 -name "*.md" -type f | wc -l)
    TOTAL_SIZE=$(find "$MEMORY_DIR" -maxdepth 1 -name "*.md" -type f -exec cat {} + 2>/dev/null | wc -c)
    echo "  Files: $FILE_COUNT"
    echo "  Total size: $((TOTAL_SIZE / 1024))KB"

    # Oldest file
    OLDEST=$(find "$MEMORY_DIR" -maxdepth 1 -name "*.md" -type f -printf '%T+ %p\n' 2>/dev/null | sort | head -1)
    if [ -n "$OLDEST" ]; then
        OLDEST_DATE=$(echo "$OLDEST" | cut -d' ' -f1 | cut -d'T' -f1)
        echo "  Oldest file: $OLDEST_DATE"
    fi

    # Archive status
    ARCHIVE_DIR="$MEMORY_DIR/archive"
    if [ -d "$ARCHIVE_DIR" ]; then
        ARCHIVE_COUNT=$(find "$ARCHIVE_DIR" -name "*.md" -type f | wc -l)
        echo "  Archived files: $ARCHIVE_COUNT"
    else
        echo "  Archive: not initialized"
    fi
else
    echo "  memory/ directory not found!"
fi
echo ""

# 3. Session cache
echo "--- Session Cache ---"
CACHE_COUNT=$(ls /tmp/openclaw-session-cache-*.json 2>/dev/null | wc -l | tr -d '[:space:]' || echo 0)
CACHE_COUNT=${CACHE_COUNT:-0}
if [ "$CACHE_COUNT" -gt 0 ]; then
    echo "  Active caches: $CACHE_COUNT"
    for cache in /tmp/openclaw-session-cache-*.json; do
        KEYS=$(python3 -c "import json; print(len(json.load(open('$cache'))))" 2>/dev/null || echo 0)
        echo "    $(basename "$cache"): $KEYS entries"
    done
else
    echo "  No active session caches."
fi
echo ""

# 4. Actionable suggestions
echo "--- Suggestions ---"
python3 "$(dirname "$0")/memory_decay.py" --promote-only --dry-run 2>/dev/null | grep -E "Found|promote" | head -3 || echo "  No lessons to promote."

# Check if classify would find anything
UNTAGGED=$(python3 "$(dirname "$0")/classify_memory.py" --summary 2>/dev/null | grep "Total:" | head -1 || echo "")
if [ -n "$UNTAGGED" ]; then
    echo "  $UNTAGGED — run classify_memory.py --apply to fix"
fi

# Check archive candidates
ARCHIVE_CANDIDATES=$(python3 "$(dirname "$0")/memory_decay.py" --dry-run 2>/dev/null | grep "Archived" | head -1 || echo "")
if [ -n "$ARCHIVE_CANDIDATES" ]; then
    echo "  $ARCHIVE_CANDIDATES — run memory_decay.py to archive"
fi

echo ""
echo "=== End Report ==="
