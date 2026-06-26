#!/bin/bash
# check_session_state.sh - Check if SESSION-STATE.md has been modified since last check
# 
# Usage: 
#   ./scripts/check_session_state.sh          # Check and report if changed
#   ./scripts/check_session_state.sh --update  # Update tracker without reporting
#   ./scripts/check_session_state.sh --force   # Force re-read and report
#   ./scripts/check_session_state.sh --watch   # Real-time inotify watch (optional, requires inotify-tools)

set -euo pipefail

WORKSPACE="/root/.openclaw/workspace"
SESSION_STATE="$WORKSPACE/SESSION-STATE.md"
TRACKER="$WORKSPACE/data/.session_state_tracker.json"
MAX_LINES=2000
KEEP_LINES=1000

# --- Helper: truncate SESSION-STATE.md if too large ---
truncate_if_needed() {
    local line_count
    line_count=$(wc -l < "$SESSION_STATE" 2>/dev/null || echo "0")
    
    if [ "$line_count" -gt "$MAX_LINES" ]; then
        echo "⚠️  SESSION-STATE.md has $line_count lines (>$MAX_LINES), truncating to last $KEEP_LINES lines..."
        
        local truncated_count=$((line_count - KEEP_LINES))
        echo "  (Truncating $truncated_count lines of history)"
        
        tail -"$KEEP_LINES" "$SESSION_STATE" > "${SESSION_STATE}.tmp"
        
        {
            echo "---"
            echo "## 📋 历史截断通知"
            echo ""
            echo "**时间**: $(date -Iseconds)"
            echo "**原因**: 文件超过 ${MAX_LINES} 行（当前 ${line_count} 行）"
            echo "**操作**: 保留最近 ${KEEP_LINES} 行，截断 ${truncated_count} 行历史"
            echo "**建议**: 重要内容已归档至 SESSION-STATE-history.md"
            echo ""
            echo "---"
            echo ""
            cat "${SESSION_STATE}.tmp"
        } > "$SESSION_STATE"
        
        rm -f "${SESSION_STATE}.tmp"
        echo "✅ Truncation complete. New size: $(wc -l < "$SESSION_STATE") lines"
    fi
}

# --- Helper: update tracker with current mtime ---
update_tracker() {
    local mtime="$1"
    local mtime_human="$2"
    local session_start
    session_start=$(python3 -c '
import json, sys
try:
    with open(sys.argv[1]) as f:
        d = json.load(f)
    print(d.get("session_start_mtime", 0))
except Exception:
    print(0)
' "$TRACKER" 2>/dev/null || echo "0")
    
    # Ensure all values are integers
    mtime=$((mtime + 0))
    session_start=$((session_start + 0))
    
    cat > "$TRACKER" << EOF
{
  "last_known_mtime": $mtime,
  "last_known_mtime_human": "$mtime_human",
  "last_check_time": "$(date -Iseconds)",
  "session_start_mtime": $session_start
}
EOF
}

# --- Ensure tracker exists ---
if [ ! -f "$TRACKER" ]; then
    echo "{}" > "$TRACKER"
fi

# --- Watch mode (inotify, optional) ---
if [ "${1:-}" = "--watch" ]; then
    if ! command -v inotifywait &>/dev/null; then
        echo "❌ inotifywait not found. Install: apt install inotify-tools"
        exit 1
    fi
    
    echo "🔍 Watching $SESSION_STATE for changes (inotify mode)..."
    echo "   Press Ctrl+C to stop."
    
    # Daemon mode?
    if [ "${2:-}" = "--daemon" ]; then
        echo "   (daemon mode: log to /tmp/session-state-watch.log)"
        exec >> /tmp/session-state-watch.log 2>&1
    fi
    
    while inotifywait -q -e close_write "$SESSION_STATE" 2>/dev/null; do
        echo ""
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Change detected!"
        # Trigger the normal check (without --watch arg)
        "$0"
    done
    exit 0
fi

# --- Stop daemon ---
if [ "${1:-}" = "--stop-daemon" ]; then
    echo "Stopping session-state-watch daemon..."
    pkill -f "check_session_state.sh --watch" || echo "No daemon running"
    exit 0
fi

# --- Get current mtime ---
CURRENT_MTIME=$(stat -c %Y "$SESSION_STATE" 2>/dev/null || echo "0")
CURRENT_MTIME_HUMAN=$(stat -c %y "$SESSION_STATE" 2>/dev/null || echo "unknown")

# --- Get last known mtime ---
LAST_KNOWN_MTIME=$(python3 -c '
import json, sys
try:
    with open(sys.argv[1]) as f:
        d = json.load(f)
    print(d.get("last_known_mtime", 0))
except Exception:
    print(0)
' "$TRACKER" 2>/dev/null || echo "0")
LAST_KNOWN_MTIME=$((LAST_KNOWN_MTIME + 0))

# --- Force re-read ---
if [ "${1:-}" = "--force" ]; then
    echo "--- SESSION-STATE.md (force read) ---"
    head -50 "$SESSION_STATE"
    echo "..."
    echo "--- End ---"
    update_tracker "$CURRENT_MTIME" "$CURRENT_MTIME_HUMAN"
    exit 0
fi

# --- Update tracker only ---
if [ "${1:-}" = "--update" ]; then
    update_tracker "$CURRENT_MTIME" "$CURRENT_MTIME_HUMAN"
    exit 0
fi

# --- Check if changed ---
if [ "$CURRENT_MTIME" -gt "$LAST_KNOWN_MTIME" ] 2>/dev/null; then
    echo "🔄 SESSION-STATE.md has been UPDATED since last check!"
    echo "  Last known: $(date -d @$LAST_KNOWN_MTIME '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo 'never')"
    echo "  Current:     $CURRENT_MTIME_HUMAN"
    echo ""
    echo "--- Recent additions (last 30 lines) ---"
    echo "(Full content available in $SESSION_STATE)"
    echo ""
    tail -30 "$SESSION_STATE"
    echo ""
    echo "--- End of recent additions ---"
    
    # Update tracker
    update_tracker "$CURRENT_MTIME" "$CURRENT_MTIME_HUMAN"
    
    # Truncate if needed (after reading, before next check)
    truncate_if_needed
    
    echo ""
    echo "✅ Tracker updated. Next check will use current state as baseline."
else
    echo "✓ SESSION-STATE.md unchanged since last check."
fi
