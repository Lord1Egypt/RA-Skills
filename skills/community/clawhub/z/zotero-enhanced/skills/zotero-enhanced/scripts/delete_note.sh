#!/bin/bash
set -e
set -o pipefail

# Zotero note deletion script
# Deletes notes with confirmation and optional backup
# Version: 1.3.6
# Safety: Only calls Zotero API. No eval, no obfuscation.

# Argument handling
DRY_RUN=false
NO_CONFIRM=false
BACKUP=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help|-h)
            cat <<EOF
Usage: $0 [OPTIONS] NOTE_KEY
Delete a note from Zotero.

Options:
  --help, -h        Show this help
  --version         Show version
  --dry-run         Show steps without deleting
  --no-confirm      Skip confirmation prompt
  --backup          Save note content to file before deleting

Environment variables:
  ZOTERO_USER_ID, ZOTERO_API_KEY required.

Examples:
  $0 ABC12
  $0 --no-confirm ABC12
  $0 --backup ABC12
  $0 --dry-run ABC12

Security: This script only calls Zotero API.
No eval, no obfuscation, no hidden network calls.
EOF
            exit 0
            ;;
        --version)
            echo "zotero-enhanced delete_note.sh v1.3.6"
            exit 0
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --no-confirm)
            NO_CONFIRM=true
            shift
            ;;
        --backup)
            BACKUP=true
            shift
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

API_URL="https://api.zotero.org/users/$ZOTERO_USER_ID/items/$NOTE_KEY"

# Fetch note to show what will be deleted
if [ "$DRY_RUN" = false ]; then
    CURRENT_RESPONSE=$(curl -s -f \
        -H "Zotero-API-Key: $ZOTERO_API_KEY" \
        "$API_URL")
    
    # Validate response
    if ! echo "$CURRENT_RESPONSE" | jq -e '.data' > /dev/null; then
        echo "Error: Note not found or invalid response from Zotero API." >&2
        exit 1
    fi
    
    # Check if it's a note
    ITEM_TYPE=$(echo "$CURRENT_RESPONSE" | jq -r '.data.itemType')
    if [ "$ITEM_TYPE" != "note" ]; then
        echo "Error: Item is not a note (type: $ITEM_TYPE)." >&2
        exit 1
    fi
    
    CURRENT_VERSION=$(echo "$CURRENT_RESPONSE" | jq -r '.version')
    NOTE_HTML=$(echo "$CURRENT_RESPONSE" | jq -r '.data.note')
    
    # Convert HTML to plain text for preview
    NOTE_PREVIEW=$(echo "$NOTE_HTML" | sed 's/<p>/\n/g; s/<\/p>/\n/g; s/<[^>]*>//g' | sed '/^$/d' | head -3)
else
    CURRENT_VERSION="1"
    NOTE_PREVIEW="This is a dry-run. Note content preview."
fi

echo "Note to delete: $NOTE_KEY"
echo "Preview:"
echo "$NOTE_PREVIEW"
echo "..."

# Confirmation prompt
if [ "$NO_CONFIRM" = false ] && [ "$DRY_RUN" = false ]; then
    read -p "Are you sure you want to delete this note? (yes/no): " CONFIRM
    if [ "$CONFIRM" != "yes" ]; then
        echo "Deletion cancelled."
        exit 0
    fi
fi

# Backup note content if requested
if [ "$BACKUP" = true ] && [ "$DRY_RUN" = false ]; then
    BACKUP_DIR="${HOME}/.zotero-backup"
    mkdir -p "$BACKUP_DIR"

    # Validate NOTE_KEY: Zotero keys are 8 alphanumeric chars; reject path traversal
    if ! echo "$NOTE_KEY" | grep -qE '^[A-Za-z0-9]{8}$'; then
        echo "Error: Invalid NOTE_KEY format (must be 8 alphanumeric characters)." >&2
        exit 1
    fi

    BACKUP_FILE="$BACKUP_DIR/note_${NOTE_KEY}_$(date +%Y%m%d_%H%M%S).txt"
    
    # Full HTML to plain text conversion for backup
    NOTE_FULL_TEXT=$(echo "$NOTE_HTML" | sed \
        -e 's/<ul>//gi' \
        -e 's/<\/ul>//gi' \
        -e 's/<ol>//gi' \
        -e 's/<\/ol>//gi' \
        -e 's/<li>/  - /gi' \
        -e 's/<\/li>//gi' \
        -e 's/<br[[:space:]]*\/>/ /gi' \
        -e 's/<p>[[:space:]]*<\/p>//gi' \
        -e 's/<p>/ /gi' \
        -e 's/<\/p>/ /gi' \
        -e 's/<strong>/**/gi' \
        -e 's/<\/strong>/**/gi' \
        -e 's/<b>/**/gi' \
        -e 's/<\/b>/**/gi' \
        -e 's/<[^>]*>//g' \
        -e 's/&amp;/\&/g' \
        -e 's/&lt;/</g' \
        -e 's/&gt;/>/g' \
        -e 's/&quot;/"/g' \
        -e 's/&nbsp;/ /g' \
        -e 's/&#39;/'"'"'/g' \
        -e 's/&#x27;/'"'"'/g' \
        -e 's/^[[:space:]]*//; s/[[:space:]]*$//')

    # Save both HTML and plain text
    echo "Note Key: $NOTE_KEY" > "$BACKUP_FILE"
    echo "Backup Date: $(date)" >> "$BACKUP_FILE"
    echo "========================================" >> "$BACKUP_FILE"
    echo "" >> "$BACKUP_FILE"
    echo "HTML Content:" >> "$BACKUP_FILE"
    echo "$NOTE_HTML" >> "$BACKUP_FILE"
    echo "" >> "$BACKUP_FILE"
    echo "========================================" >> "$BACKUP_FILE"
    echo "" >> "$BACKUP_FILE"
    echo "Plain Text:" >> "$BACKUP_FILE"
    echo "$NOTE_FULL_TEXT" >> "$BACKUP_FILE"
    
    echo "Backup saved to: $BACKUP_FILE"
fi

# Delete the note
if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "DRY-RUN MODE: Would delete note $NOTE_KEY"
else
    DELETE_RESPONSE=$(curl -s -f \
        -X DELETE \
        -H "Zotero-API-Key: $ZOTERO_API_KEY" \
        -H "If-Unmodified-Since-Version: $CURRENT_VERSION" \
        "$API_URL")
    
    # Check for conflicts
    if echo "$DELETE_RESPONSE" | jq -e '.conflicted' > /dev/null; then
        echo "Error: Delete conflict. Note was modified by another process." >&2
        echo "Please fetch the note again and retry." >&2
        exit 1
    fi
fi

echo ""
echo "Success! Note deleted."
echo "Note key: $NOTE_KEY"
