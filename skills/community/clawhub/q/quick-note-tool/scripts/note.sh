#!/bin/bash
# Quick Note - Fast note-taking script
# Version: 1.0.0

NOTES_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
NOTES_FILE="$NOTES_DIR/notes/quick-notes.md"

# Ensure notes directory exists
mkdir -p "$NOTES_DIR/notes"

# Initialize file if not exists
if [ ! -f "$NOTES_FILE" ]; then
    echo "# Quick Notes" > "$NOTES_FILE"
    echo "" >> "$NOTES_FILE"
fi

# Generate note ID
generate_id() {
    local count=$(grep -c "^## \[" "$NOTES_FILE" 2>/dev/null || echo "0")
    printf "ID-%03d" $((count + 1))
}

# Get current timestamp
get_timestamp() {
    date "+%Y-%m-%d %H:%M"
}

# Add note
add_note() {
    local content="$1"
    local tags="$2"
    local id=$(generate_id)
    local timestamp=$(get_timestamp)
    
    {
        echo ""
        echo "## [$id] $timestamp"
        if [ -n "$tags" ]; then
            echo "**Tags:** $tags"
        fi
        echo "$content"
        echo ""
        echo "---"
        echo ""
    } >> "$NOTES_FILE"
    
    echo "✅ Note saved: $id"
    if [ -n "$tags" ]; then
        echo "   Tags: $tags"
    fi
}

# Search notes
search_notes() {
    local keyword="$1"
    echo "🔍 Searching for: $keyword"
    echo ""
    grep -A 3 -B 1 -i "$keyword" "$NOTES_FILE" | head -50
}

# List recent notes
list_notes() {
    local limit="${1:-10}"
    echo "📋 Recent Notes (last $limit):"
    echo ""
    grep "^## \[" "$NOTES_FILE" | tail -n "$limit"
}

# List by tag
list_by_tag() {
    local tag="$1"
    echo "🏷️  Notes tagged: $tag"
    echo ""
    grep -A 5 -B 1 "$tag" "$NOTES_FILE" | head -50
}

# Delete note (by ID)
delete_note() {
    local id="$1"
    if grep -q "\[$id\]" "$NOTES_FILE"; then
        # Create backup
        cp "$NOTES_FILE" "$NOTES_FILE.bak"
        # Remove note block (simplified - removes line with ID)
        sed -i.bak "/\[$id\]/,/---/d" "$NOTES_FILE"
        echo "✅ Note $id deleted (backup: quick-notes.md.bak)"
    else
        echo "❌ Note $id not found"
    fi
}

# Show help
show_help() {
    echo "Quick Note - Fast note-taking"
    echo ""
    echo "Usage:"
    echo "  note.sh add \"<content>\" [--tags tag1,tag2]"
    echo "  note.sh search \"<keyword>\""
    echo "  note.sh list [limit]"
    echo "  note.sh tag \"<tagname>\""
    echo "  note.sh delete \"<id>\""
    echo ""
}

# Main command handler
case "$1" in
    add)
        shift
        content=""
        tags=""
        while [ $# -gt 0 ]; do
            case "$1" in
                --tags)
                    tags="$2"
                    shift 2
                    ;;
                *)
                    content="$content $1"
                    shift
                    ;;
            esac
        done
        content=$(echo "$content" | sed 's/^ *//')
        add_note "$content" "$tags"
        ;;
    search)
        search_notes "$2"
        ;;
    list)
        list_notes "${2:-10}"
        ;;
    tag)
        list_by_tag "$2"
        ;;
    delete)
        delete_note "$2"
        ;;
    *)
        show_help
        ;;
esac
