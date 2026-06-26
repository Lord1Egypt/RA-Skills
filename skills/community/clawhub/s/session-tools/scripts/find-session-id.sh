#!/usr/bin/env bash
# find-session-id.sh - Find current session ID by searching for a unique marker
#
# Usage:
#   find-session-id.sh <marker> [project_dir]
#
# Arguments:
#   marker       - Unique string to search for in session files
#   project_dir  - (Optional) Override project directory. If omitted, derived from CWD.
#
# The marker must already exist in the session JSONL file (e.g., printed by Claude
# in the conversation, which gets recorded in the JSONL).

set -euo pipefail

CLAUDE_PROJECTS_DIR="$HOME/.claude/projects"

# Convert CWD to Claude Code project name
# Matches @claude-sessions/core pathToFolderName:
#   absolutePath.replace(/[^a-zA-Z0-9]/g, '-')
cwd_to_project_name() {
    local cwd="$1"
    cwd="${cwd%/}"
    # Replace all non-alphanumeric characters with '-'
    echo "$cwd" | sed 's/[^a-zA-Z0-9]/-/g'
}

MARKER="${1:-}"
if [[ -z "$MARKER" ]]; then
    echo "Usage: $0 <marker> [project_dir]" >&2
    exit 1
fi

# Determine project directory
if [[ -n "${2:-}" ]]; then
    PROJECT_DIR="$2"
else
    PROJECT_NAME=$(cwd_to_project_name "$(pwd)")
    PROJECT_DIR="$CLAUDE_PROJECTS_DIR/$PROJECT_NAME"
fi

if [[ ! -d "$PROJECT_DIR" ]]; then
    echo "ERROR: Project directory not found: $PROJECT_DIR" >&2
    exit 1
fi

# Search for the marker in session files (exclude sync-conflict files)
RESULT=$(grep -rl "$MARKER" "$PROJECT_DIR"/*.jsonl 2>/dev/null | grep -v 'sync-conflict' | head -1 || true)

if [[ -z "$RESULT" ]]; then
    echo "ERROR: No session file found containing marker: $MARKER" >&2
    exit 1
fi

# Extract session ID (UUID) from filename
SESSION_ID=$(basename "$RESULT" .jsonl)
echo "$SESSION_ID"
