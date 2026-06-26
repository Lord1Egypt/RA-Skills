#!/bin/bash
# cursor_send.sh - Send additional instructions to running task
# SECURITY: Uses -l flag for literal mode (prevents shell injection in tmux)

set -e

SESSION_NAME="$1"
COMMAND="$2"

if [ -z "$SESSION_NAME" ] || [ -z "$COMMAND" ]; then
    echo "Usage: $0 <session-name> <command>"
    exit 1
fi

# Check if session exists
if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Session not found: $SESSION_NAME"
    exit 1
fi

# Send instruction using literal mode (-l)
# SECURITY: -l flag sends keys literally, preventing shell metacharacter interpretation
# This is safer than default mode where $, `, \, etc. could be interpreted
tmux send-keys -t "$SESSION_NAME" -l -- "$COMMAND" Enter

echo "Command sent to $SESSION_NAME: $COMMAND"
echo "Mode: literal (-l flag enabled for security)"
