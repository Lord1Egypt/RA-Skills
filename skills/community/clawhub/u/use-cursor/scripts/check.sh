#!/bin/bash
# cursor_check.sh - Check task status

set -e

SESSION_NAME="$1"

if [ -z "$SESSION_NAME" ]; then
    echo "Usage: $0 <session-name>"
    exit 1
fi

# Check if session exists
if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Session not found: $SESSION_NAME"
    exit 1
fi

# Capture recent output
OUTPUT=$(tmux capture-pane -t "$SESSION_NAME" -p -S -200 2>/dev/null || echo "No output yet")

# Check if still running
PANELS=$(tmux list-panes -t "$SESSION_NAME" -F "#{pane_pid}" 2>/dev/null | wc -l)

if [ "$PANELS" -gt 0 ]; then
    STATUS="running"
else
    STATUS="completed"
fi

# Output status
echo "Session: $SESSION_NAME"
echo "Status: $STATUS"
echo ""
echo "=== Recent Output ==="
echo "$OUTPUT" | tail -50
