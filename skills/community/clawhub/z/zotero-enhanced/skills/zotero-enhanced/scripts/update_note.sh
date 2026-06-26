#!/bin/bash
set -e
set -o pipefail

# Zotero note update script
# Updates existing notes with new content and/or tags
# Version: 1.3.6
# Safety: Only calls Zotero API. No eval, no obfuscation.

# Argument handling
DRY_RUN=false
MODE="replace"  # Options: replace, append
TAGS=""
ADD_TAGS=false
REMOVE_TAGS=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help|-h)
            cat <<EOF
Usage: $0 [OPTIONS] NOTE_KEY
Update an existing note in Zotero.

Options:
  --help, -h        Show this help
  --version         Show version
  --dry-run         Show steps without updating
  --replace         Replace note content (default)
  --append          Append to existing note content
  --tag TAG         Add tag (can be used multiple times)
  --remove-tag TAG  Remove tag (can be used multiple times)

Environment variables:
  ZOTERO_USER_ID, ZOTERO_API_KEY required.

Examples:
  echo "New content" | $0 --replace ABC12
  echo "Additional notes" | $0 --append ABC12
  $0 --tag important --tag to-read ABC12
  $0 --remove-tag obsolete ABC12

Security: This script only calls Zotero API.
No eval, no obfuscation, no hidden network calls.
EOF
            exit 0
            ;;
        --version)
            echo "zotero-enhanced update_note.sh v1.3.6"
            exit 0
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --replace)
            MODE="replace"
            shift
            ;;
        --append)
            MODE="append"
            shift
            ;;
        --tag)
            [ -z "$TAGS" ] && TAGS="$2" || TAGS="$TAGS,$2"
            ADD_TAGS=true
            shift 2
            ;;
        --remove-tag)
            [ -z "$TAGS" ] && TAGS="$2" || TAGS="$TAGS,$2"
            REMOVE_TAGS=true
            shift 2
            ;;
        *)
            # Assume it's the note key
            NOTE_KEY="$1"
            shift
            ;;
    esac
done

if [ -z "$NOTE_KEY" ]; then
    echo "Error: Note key not provided."
    exit 1
fi

if [ "$DRY_RUN" = false ]; then
    : "${ZOTERO_USER_ID:?ZOTERO_USER_ID not set}"
    : "${ZOTERO_API_KEY:?ZOTERO_API_KEY not set}"
fi

# Read new content from stdin
NEW_CONTENT=""
if [ ! -t 0 ]; then
    NEW_CONTENT=$(cat)
fi

# Validate tag options
if [ "$ADD_TAGS" = true ] && [ "$REMOVE_TAGS" = true ]; then
    echo "Error: Cannot use --tag and --remove-tag together." >&2
    exit 1
fi

echo "Updating note: $NOTE_KEY"
[ -n "$NEW_CONTENT" ] && echo "Mode: $MODE content"
[ "$ADD_TAGS" = true ] && echo "Adding tags: ${TAGS}"
[ "$REMOVE_TAGS" = true ] && echo "Removing tags: ${TAGS}"

# Fetch current note to get version
API_URL="https://api.zotero.org/users/$ZOTERO_USER_ID/items/$NOTE_KEY"

if [ "$DRY_RUN" = false ]; then
    CURRENT_RESPONSE=$(curl -s -f \
        -H "Zotero-API-Key: $ZOTERO_API_KEY" \
        "$API_URL")
    
    # Validate response
    if ! echo "$CURRENT_RESPONSE" | jq -e '.data' > /dev/null; then
        echo "Error: Invalid response from Zotero API." >&2
        exit 1
    fi
    
    # Check if it's a note
    ITEM_TYPE=$(echo "$CURRENT_RESPONSE" | jq -r '.data.itemType')
    if [ "$ITEM_TYPE" != "note" ]; then
        echo "Error: Item is not a note (type: $ITEM_TYPE)." >&2
        exit 1
    fi
    
    CURRENT_VERSION=$(echo "$CURRENT_RESPONSE" | jq -r '.version')
    CURRENT_HTML=$(echo "$CURRENT_RESPONSE" | jq -r '.data.note')
    CURRENT_TAGS=$(echo "$CURRENT_RESPONSE" | jq -r '.data.tags')
else
    CURRENT_VERSION="1"
    CURRENT_HTML="<p>Current note content</p>"
    CURRENT_TAGS='[]'
fi

# Build update payload
PAYLOAD='{}'

# Handle content updates
if [ -n "$NEW_CONTENT" ]; then
    # Convert plain text to HTML with bold and list support
    convert_text_to_html() {
        local text="$1"
        local html=""

        # Escape HTML special characters first
        text=$(echo "$text" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g; s/"/\&quot;/g')

        # Convert **bold** to <strong>
        text=$(echo "$text" | sed 's/\*\*\([^\*]*\)\*\*/<strong>\1<\/strong>/g')

        # Process line by line with while/read
        local in_ul=false
        local line_html=""

        while IFS= read -r line || [ -n "$line" ]; do
            # Skip blank lines (paragraph separators)
            if [ -z "$(echo "$line" | tr -d '[:space:]')" ]; then
                # Close any open ul
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
                html="${html}<p>${line}</p>"
            fi
        done <<< "$text"

        # Close any open ul
        if [ "$in_ul" = true ]; then
            html="${html}</ul>"
        fi

        echo "$html"
    }

    NEW_HTML=$(convert_text_to_html "$NEW_CONTENT")

    if [ "$MODE" = "append" ]; then
        # Append to existing HTML
        UPDATED_HTML="${CURRENT_HTML}${NEW_HTML}"
    else
        # Replace content
        UPDATED_HTML="$NEW_HTML"
    fi

    PAYLOAD=$(echo "$PAYLOAD" | jq --arg html "$UPDATED_HTML" '. + {note: $html}')
fi

# Handle tag updates
if [ "$ADD_TAGS" = true ]; then
    # Add new tags to existing
    NEW_TAGS_ARRAY=$(echo "$TAGS" | jq -R 'split(",") | map(select(length > 0)) | map({tag: .})')
    UPDATED_TAGS=$(echo "$CURRENT_TAGS" "$NEW_TAGS_ARRAY" | jq -s 'add | unique')
    PAYLOAD=$(echo "$PAYLOAD" | jq --argjson tags "$UPDATED_TAGS" '. + {tags: $tags}')
elif [ "$REMOVE_TAGS" = true ]; then
    # Remove specified tags
    TAGS_TO_REMOVE=$(echo "$TAGS" | jq -R 'split(",") | map(select(length > 0))')
    UPDATED_TAGS=$(echo "$CURRENT_TAGS" | jq --argjson remove "$TAGS_TO_REMOVE" 'map(select(.tag as $t | $remove | index($t) | not))')
    PAYLOAD=$(echo "$PAYLOAD" | jq --argjson tags "$UPDATED_TAGS" '. + {tags: $tags}')
fi

# Check if there's anything to update
if [ "$PAYLOAD" = "{}" ]; then
    echo "Error: No changes specified. Use --replace, --append, --tag, or --remove-tag." >&2
    exit 1
fi

# Build final update payload with version
UPDATE_PAYLOAD=$(echo "$PAYLOAD" | jq -c \
    --arg version "$CURRENT_VERSION" \
    --arg key "$NOTE_KEY" \
    '{
        key: $key,
        version: ($version | tonumber),
        data: .
    } | [.]')

if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "DRY-RUN MODE: Would update note with payload:"
    echo "$UPDATE_PAYLOAD" | jq .
else
    UPDATE_RESPONSE=$(curl -s -f \
        -X PATCH \
        -H "Zotero-API-Key: $ZOTERO_API_KEY" \
        -H "Content-Type: application/json" \
        -H "If-Unmodified-Since-Version: $CURRENT_VERSION" \
        -d "$UPDATE_PAYLOAD" \
        "$API_URL")
    
    # Check for conflicts
    if echo "$UPDATE_RESPONSE" | jq -e '.conflicted' > /dev/null; then
        echo "Error: Update conflict. Note was modified by another process." >&2
        echo "Please fetch the note again and retry." >&2
        exit 1
    fi
    
    UPDATED_VERSION=$(echo "$UPDATE_RESPONSE" | jq -r '.successful."0".version')
fi

echo ""
echo "Success! Note updated."
echo "Note key: $NOTE_KEY"
[ "$DRY_RUN" = false ] && echo "New version: $UPDATED_VERSION"
echo "View note: https://www.zotero.org/$ZOTERO_USER_ID/items/$NOTE_KEY"
