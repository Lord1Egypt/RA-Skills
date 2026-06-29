#!/bin/bash
# Session Renamer - assign a custom title to a Claude Code session
#
# Usage:
#   rename-session.sh <session_id> "<title>"          # Assign title to a specific session
#   rename-session.sh "<title>"                        # Assign title to the latest session in current project
#   rename-session.sh --show <session_id>              # Show current title
#   rename-session.sh --list                           # List titled sessions in current project
#
# Mechanism:
#   Claude Code stores custom titles by appending a {"type":"custom-title","customTitle":"...","sessionId":"..."} record
#   to the session JSONL file.

set -e

CLAUDE_DIR="$HOME/.claude"
PROJECTS_DIR="$CLAUDE_DIR/projects"

# Compute current project directory
CURRENT_DIR="$(pwd)"
if [[ "$OSTYPE" == msys* || "$OSTYPE" == mingw* || "$OSTYPE" == cygwin* ]]; then
  # Windows: /c/Users/... -> C--Users-... (drive letter uppercase, C: + \ = double dash)
  PROJECT_FOLDER=$(echo "$CURRENT_DIR" | sed -E 's|^/([a-zA-Z])/|\U\1--|; s|/|-|g; s|\.|-|g')
else
  # Unix: /Users/... -> -Users-...
  PROJECT_FOLDER=$(echo "$CURRENT_DIR" | sed 's|/|-|g; s|\.|-|g')
fi
SESSION_DIR="$PROJECTS_DIR/$PROJECT_FOLDER"

# -- Helper functions --------------------------------------------------

find_session_file() {
    local session_id="$1"
    local file="$SESSION_DIR/${session_id}.jsonl"
    if [ ! -f "$file" ]; then
        # Search across all projects
        file=$(find "$PROJECTS_DIR" -name "${session_id}.jsonl" 2>/dev/null | head -1)
    fi
    echo "$file"
}

get_current_title() {
    local session_file="$1"
    # Extract customTitle value from the last custom-title record in the JSONL
    grep '"type":"custom-title"' "$session_file" 2>/dev/null | tail -1 | \
        sed 's/.*"customTitle":"\([^"]*\)".*/\1/' || echo ""
}

set_title() {
    local session_file="$1"
    local session_id="$2"
    local title="$3"

    local current
    current=$(get_current_title "$session_file")
    if [ -n "$current" ]; then
        echo "Current title: $current"
        echo "New title:     $title"
    fi

    # Append custom-title + agent-name records (Claude Code format)
    jq -nc --arg title "$title" --arg sid "$session_id" \
        '{"type":"custom-title","customTitle":$title,"sessionId":$sid}' >> "$session_file"
    jq -nc --arg title "$title" --arg sid "$session_id" \
        '{"type":"agent-name","agentName":$title,"sessionId":$sid}' >> "$session_file"

    echo "Title set: $title"
    echo "Session: $session_id"
}

show_title() {
    local session_id="$1"
    local session_file
    session_file=$(find_session_file "$session_id")

    if [ -z "$session_file" ] || [ ! -f "$session_file" ]; then
        echo "Session file not found: $session_id"
        exit 1
    fi

    local title
    title=$(get_current_title "$session_file")
    if [ -n "$title" ]; then
        echo "Title: $title"
    else
        echo "(no title)"
    fi
}

list_sessions() {
    if [ ! -d "$SESSION_DIR" ]; then
        echo "Project session directory not found: $SESSION_DIR"
        exit 1
    fi

    echo "=== Titled sessions ==="
    local found=0
    for f in "$SESSION_DIR"/*.jsonl; do
        [ -f "$f" ] || continue
        local title
        title=$(get_current_title "$f")
        if [ -n "$title" ]; then
            local id
            id=$(basename "$f" .jsonl)
            printf "%-36s  %s\n" "$id" "$title"
            found=$((found + 1))
        fi
    done

    if [ $found -eq 0 ]; then
        echo "(no titled sessions)"
    fi
}

# -- main --------------------------------------------------------------

case "$1" in
    --show)
        show_title "$2"
        ;;
    --list)
        list_sessions
        ;;
    *)
        # Handle based on argument count
        if [ $# -eq 2 ]; then
            # rename-session.sh <session_id> "<title>"
            SESSION_ID="$1"
            TITLE="$2"
            SESSION_FILE=$(find_session_file "$SESSION_ID")
            if [ -z "$SESSION_FILE" ] || [ ! -f "$SESSION_FILE" ]; then
                echo "Session file not found: $SESSION_ID"
                exit 1
            fi
            set_title "$SESSION_FILE" "$SESSION_ID" "$TITLE"

        elif [ $# -eq 1 ]; then
            # rename-session.sh "<title>" -- latest session in current project
            TITLE="$1"
            if [ ! -d "$SESSION_DIR" ]; then
                echo "Project session directory not found: $SESSION_DIR"
                exit 1
            fi
            LATEST=$(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -1)
            if [ -z "$LATEST" ]; then
                echo "No session files found."
                exit 1
            fi
            SESSION_ID=$(basename "$LATEST" .jsonl)
            echo "Selected latest session: $SESSION_ID"
            set_title "$LATEST" "$SESSION_ID" "$TITLE"

        else
            echo "Usage:"
            echo "  $(basename "$0") <session_id> \"<title>\"    # Assign title to a specific session"
            echo "  $(basename "$0") \"<title>\"                  # Assign title to latest session in current project"
            echo "  $(basename "$0") --show <session_id>         # Show current title"
            echo "  $(basename "$0") --list                       # List titled sessions"
            exit 1
        fi
        ;;
esac
