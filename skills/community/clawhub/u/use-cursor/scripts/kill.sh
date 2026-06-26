#!/bin/bash
# cursor_kill.sh - End task

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

# End session
tmux kill-session -t "$SESSION_NAME"

echo "Session killed: $SESSION_NAME"
