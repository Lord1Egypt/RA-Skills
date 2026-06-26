#!/usr/bin/env bash
# timeline.sh — Personal event log for dated facts
# Usage: timeline.sh <command> [args]

set -euo pipefail

VAULT="${VAULT_PATH:-/Users/andrew/Documents/Vault v3}"
TIMELINE_FILE="$VAULT/Timeline.md"

# Ensure timeline file exists
init_timeline() {
    if [[ ! -f "$TIMELINE_FILE" ]]; then
        # Use unquoted EOF delimiter so that $(date +%Y-%m-%d) is expanded by
        # the shell and stored as a real ISO date, not the literal string.
        cat > "$TIMELINE_FILE" << EOF
---
created: $(date +%Y-%m-%d)
type: timeline
---

# Timeline

Personal event log. Not a calendar — a memory.

EOF
    fi
}

# Log an event
cmd_log() {
    local text=""
    local date_str=""
    local tags=""
    local time_str
    time_str=$(date +%H:%M)

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --date|-d)
                date_str="$2"
                shift 2
                ;;
            --tags|-t)
                tags="$2"
                shift 2
                ;;
            --time)
                time_str="$2"
                shift 2
                ;;
            *)
                if [[ -z "$text" ]]; then
                    text="$1"
                else
                    text="$text $1"
                fi
                shift
                ;;
        esac
    done

    if [[ -z "$text" ]]; then
        echo "Error: No event text provided" >&2
        echo "Usage: timeline log \"event text\" [--date YYYY-MM-DD] [--tags tag1,tag2]" >&2
        exit 1
    fi

    # Default to today
    if [[ -z "$date_str" ]]; then
        date_str=$(date +%Y-%m-%d)
    fi

    # Format tags as hashtags
    local tag_str=""
    if [[ -n "$tags" ]]; then
        tag_str=" #${tags//,/ #}"
    fi

    init_timeline

    # Check if date section exists
    local date_header="## $date_str"
    if ! grep -q "^$date_header$" "$TIMELINE_FILE" 2>/dev/null; then
        # Add new date section (insert after frontmatter/header)
        echo -e "\n$date_header\n" >> "$TIMELINE_FILE"
    fi

    # Append entry under the date
    local entry="- **$time_str** $text$tag_str"

    # Use sed to insert after the date header
    if [[ "$(uname)" == "Darwin" ]]; then
        sed -i '' "/^## $date_str$/a\\
$entry
" "$TIMELINE_FILE"
    else
        sed -i "/^## $date_str$/a $entry" "$TIMELINE_FILE"
    fi

    echo "✓ Logged: $text ($date_str)$tag_str"
}

# Search timeline
cmd_search() {
    local query=""
    local tag=""
    local from_date=""
    local to_date=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --tag|-t)
                tag="$2"
                shift 2
                ;;
            --from)
                from_date="$2"
                shift 2
                ;;
            --to)
                to_date="$2"
                shift 2
                ;;
            *)
                query="$1"
                shift
                ;;
        esac
    done

    if [[ ! -f "$TIMELINE_FILE" ]]; then
        echo "No timeline found."
        exit 0
    fi

    local pattern=""
    if [[ -n "$query" ]]; then
        pattern="$query"
    fi
    if [[ -n "$tag" ]]; then
        if [[ -n "$pattern" ]]; then
            pattern="$pattern.*#$tag\\|#$tag.*$pattern"
        else
            pattern="#$tag"
        fi
    fi

    if [[ -z "$pattern" ]]; then
        cat "$TIMELINE_FILE"
    else
        grep -i -E "$pattern|^## [0-9]{4}" "$TIMELINE_FILE" | head -50
    fi
}

# List recent entries
cmd_list() {
    local limit=10

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --limit|-n)
                limit="$2"
                shift 2
                ;;
            --tag|-t)
                cmd_search --tag "$2"
                return
                ;;
            *)
                shift
                ;;
        esac
    done

    if [[ ! -f "$TIMELINE_FILE" ]]; then
        echo "No timeline found."
        exit 0
    fi

    # Show recent entries (grep for entry lines, take last N)
    grep -E "^- \*\*[0-9]{2}:[0-9]{2}\*\*|^## [0-9]{4}" "$TIMELINE_FILE" | tail -$((limit + 10)) | head -$((limit + 5))
}

# Main
case "${1:-}" in
    log|add)
        shift
        cmd_log "$@"
        ;;
    search|find|query)
        shift
        cmd_search "$@"
        ;;
    list|recent|ls)
        shift
        cmd_list "$@"
        ;;
    help|--help|-h)
        echo "timeline — Personal event log"
        echo ""
        echo "Commands:"
        echo "  log \"text\" [--date YYYY-MM-DD] [--tags tag1,tag2]"
        echo "  search \"query\" [--tag TAG] [--from DATE] [--to DATE]"
        echo "  list [--limit N] [--tag TAG]"
        echo ""
        echo "Examples:"
        echo "  timeline log \"Colette had a fever\" --tags medical,family"
        echo "  timeline search fever"
        echo "  timeline list --limit 20"
        ;;
    *)
        echo "Usage: timeline <log|search|list> [args]"
        echo "Run 'timeline help' for details."
        exit 1
        ;;
esac
