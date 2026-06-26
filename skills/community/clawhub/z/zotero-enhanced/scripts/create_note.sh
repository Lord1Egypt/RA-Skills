#!/bin/bash
set -e
set -o pipefail

# Zotero note creation script
# Creates a new note with plain text converted to HTML
# Version: 1.3.6
# Safety: Only calls Zotero API. No eval, no obfuscation.

# Argument handling
DRY_RUN=false
PARENT_KEY=""
TAGS=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help|-h)
            cat <<EOF
Usage: $0 [OPTIONS] NOTE_TEXT
Create a new note in Zotero.

Options:
  --help, -h        Show this help
  --version         Show version
  --dry-run         Show steps without creating note
  --parent KEY      Attach note to parent item (document key)
  --tag TAG         Add tag (can be used multiple times)

Environment variables:
  ZOTERO_USER_ID, ZOTERO_API_KEY required.

Examples:
  $0 "My important research notes"
  $0 --parent ABC12 --tag research "Meeting notes"
  $0 --tag to-read --tag important "Follow up on this paper"

Security: This script only calls Zotero API.
No eval, no obfuscation, no hidden network calls.
EOF
            exit 0
            ;;
        --version)
            echo "zotero-enhanced create_note.sh v1.3.8"
            exit 0
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --parent)
            PARENT_KEY="$2"
            shift 2
            ;;
        --tag)
            TAGS="$TAGS$2,"
            shift 2
            ;;
        *)
            # Assume it's the note text
            NOTE_TEXT="$1"
            shift
            ;;
    esac
done

if [ -z "$NOTE_TEXT" ]; then
    echo "Error: Note text not provided."
    exit 1
fi

if [ "$DRY_RUN" = false ]; then
    : "${ZOTERO_USER_ID:?ZOTERO_USER_ID not set}"
    : "${ZOTERO_API_KEY:?ZOTERO_API_KEY not set}"
fi

echo "Creating note in Zotero..."
echo "Note: $(echo "$NOTE_TEXT" | head -c 50)..."
[ -n "$PARENT_KEY" ] && echo "Parent item: $PARENT_KEY"
[ -n "$TAGS" ] && echo "Tags: ${TAGS%,}"

# Convert plain text to HTML (paragraphs, line breaks, bold, lists)
convert_text_to_html() {
    local text="$1"
    local html=""

    # Escape HTML special characters first
    text=$(echo "$text" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g; s/"/\&quot;/g')

    # Convert **bold** to <strong>
    text=$(echo "$text" | sed 's/\*\*\([^\*]*\)\*\*/<strong>\1<\/strong>/g')

    # Process line by line
    local in_ul=false
    local line_html=""

    while IFS= read -r line || [ -n "$line" ]; do
        # Blank line = paragraph separator (skip for now, handled below)
        if [ -z "$(echo "$line" | tr -d '[:space:]')" ]; then
            # Close open ul
            if [ "$in_ul" = true ]; then
                html="${html}</ul>"
                in_ul=false
            fi
            continue
        fi

        # Check for list items (- or * or numbered)
        if echo "$line" | grep -qE '^[[:space:]]*[-*][[:space:]]'; then
            if [ "$in_ul" = false ]; then
                html="${html}<ul>"
                in_ul=true
            fi
            local item=$(echo "$line" | sed 's/^[[:space:]]*[-*][[:space:]]//')
            html="${html}<li>${item}</li>"
        elif echo "$line" | grep -qE '^[[:space:]]*[0-9]+\.[[:space:]]'; then
            if [ "$in_ul" = false ]; then
                html="${html}<ul>"
                in_ul=true
            fi
            local item=$(echo "$line" | sed 's/^[[:space:]]*[0-9]\+\.[[:space:]]//')
            html="${html}<li>${item}</li>"
        else
            # Close open ul before paragraph
            if [ "$in_ul" = true ]; then
                html="${html}</ul>"
                in_ul=false
            fi
            # Single newline within paragraph → <br>
            html="${html}<p>${line}</p>"
        fi
    done <<< "$text"

    # Close any open ul
    if [ "$in_ul" = true ]; then
        html="${html}</ul>"
    fi

    echo "$html"
}

NOTE_HTML=$(convert_text_to_html "$NOTE_TEXT")

# Build JSON payload
# Start with base item
PAYLOAD=$(jq -n \
    --arg html "$NOTE_HTML" \
    '{
        itemType: "note",
        note: $html
    }')

# Add parent if specified
if [ -n "$PARENT_KEY" ]; then
    PAYLOAD=$(echo "$PAYLOAD" | jq --arg parent "$PARENT_KEY" '. + {parentItem: $parent}')
fi

# Add tags if specified
if [ -n "$TAGS" ]; then
    # Remove trailing comma and split by comma
    TAGS_ARRAY=$(echo "${TAGS%,}" | jq -R 'split(",") | map(select(length > 0)) | map({tag: .})')
    PAYLOAD=$(echo "$PAYLOAD" | jq --argjson tags "$TAGS_ARRAY" '. + {tags: $tags}')
fi

# Wrap in array for API
PAYLOAD_ARRAY=$(echo "$PAYLOAD" | jq -c '[.]')

API_URL="https://api.zotero.org/users/$ZOTERO_USER_ID/items"

if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "DRY-RUN MODE: Would create note with payload:"
    echo "$PAYLOAD" | jq .
    NOTE_KEY="dry-run-note-key-$(date +%s)"
else
    RESPONSE=$(curl -s -f \
        -H "Zotero-API-Key: $ZOTERO_API_KEY" \
        -H "Content-Type: application/json" \
        -d "$PAYLOAD_ARRAY" \
        "$API_URL")
    
    NOTE_KEY=$(echo "$RESPONSE" | jq -r '.successful."0".key')
    
    [ -n "$NOTE_KEY" ] && [ "$NOTE_KEY" != "null" ] || { 
        echo "Error: Failed to create note. Response: $RESPONSE" >&2
        exit 1
    }
fi

echo ""
echo "Success! Note created."
echo "Note key: $NOTE_KEY"
echo "View note: https://www.zotero.org/$ZOTERO_USER_ID/items/$NOTE_KEY"
