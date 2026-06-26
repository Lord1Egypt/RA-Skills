#!/bin/bash
# cursor_spawn.sh - Start background Cursor task

set -e

SESSION_NAME="${1:-cursor-$(date +%s)}"
TASK="${2:-}"
WORKDIR="${3:-$(pwd)}"

if [ -z "$TASK" ]; then
    echo "Usage: $0 <session-name> <task> [workdir]"
    exit 1
fi

# Check dependencies
if ! command -v tmux &> /dev/null; then
    echo "ERROR: tmux not installed"
    exit 1
fi

if ! command -v agent &> /dev/null && ! command -v cursor-agent &> /dev/null; then
    echo "ERROR: Cursor CLI not installed (agent or cursor-agent)"
    exit 1
fi

# Determine agent command
AGENT_CMD="agent"
if ! command -v agent &> /dev/null; then
    AGENT_CMD="cursor-agent"
fi

# Clean up old session (if exists)
tmux kill-session -t "$SESSION_NAME" 2>/dev/null || true

# Create new session
tmux new-session -d -s "$SESSION_NAME"

# Navigate to working directory
# SECURITY: Using -l flag for literal mode (prevents shell expansion)
tmux send-keys -t "$SESSION_NAME" -l -- "cd $WORKDIR" Enter
sleep 1

# Run Cursor agent (non-interactive mode + auto model + trust workspace)
# SECURITY: Using -l flag for literal mode, entire command sent as single string
# TASK is passed as $2 (already escaped by JS layer with single-quote method)
tmux send-keys -t "$SESSION_NAME" -l -- "$AGENT_CMD --model auto --print --trust $TASK" Enter

# Return session info
echo "Session: $SESSION_NAME"
echo "Task: $TASK"
echo "Workdir: $WORKDIR"
echo "Status: running"
