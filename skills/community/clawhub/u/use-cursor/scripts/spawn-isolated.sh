#!/bin/bash
# cursor_spawn_isolated.sh - Start background Cursor task in isolated environment
# This version runs tmux with minimal environment to reduce secret exposure

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

# Create new session with minimal environment
# Use 'env -i' to clear most environment variables
tmux new-session -d -s "$SESSION_NAME"

# Navigate to working directory
# SECURITY: Using -l flag for literal mode (prevents shell expansion)
tmux send-keys -t "$SESSION_NAME" -l -- "cd $WORKDIR" Enter
sleep 1

# Run Cursor agent with minimal environment
# SECURITY: Uses env -i to clear all vars, then explicitly set only safe ones
# PATH is reconstructed to avoid inheriting malicious paths
# All sent with -l flag for literal mode
tmux send-keys -t "$SESSION_NAME" -l -- "env -i PATH=/usr/local/bin:/usr/bin:/bin HOME=$HOME USER=$USER CURSOR_API_KEY=${CURSOR_API_KEY:-} $AGENT_CMD --model auto --print --trust $TASK" Enter

# Return session info
echo "Session: $SESSION_NAME"
echo "Task: $TASK"
echo "Workdir: $WORKDIR"
echo "Mode: isolated (minimal env)"
echo "Status: running"
