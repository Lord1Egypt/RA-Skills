#!/bin/bash
set -e
set -o pipefail

# Universal script to read PDF content from Zotero
# Supports both WebDAV and Zotero API download methods
# Safety: Only calls Zotero API and optional WebDAV. No eval, no obfuscation.

# Argument handling
case "$1" in
    --help|-h)
        cat <<EOF
Usage: $0 ITEM_KEY
Read a PDF from Zotero library and output text content.

Options:
  --help, -h    Show this help
  --version     Show version

Environment variables:
  ZOTERO_USER_ID, ZOTERO_API_KEY required.
  WEBDAV_URL, WEBDAV_USER, WEBDAV_PASS optional for WebDAV storage.

Security: This script only calls Zotero API and optional WebDAV.
No eval, no obfuscation, no hidden network calls.
EOF
        exit 0
        ;;
    --version)
        echo "zotero-enhanced read_universal.sh v1.3.8"
        exit 0
        ;;
esac

: "${ZOTERO_API_KEY:?ZOTERO_API_KEY not set}"
: "${ZOTERO_USER_ID:?ZOTERO_USER_ID not set}"

ITEM_KEY="$1"
[ -n "$ITEM_KEY" ] || { echo "Error: Zotero item key not provided."; exit 1; }

TMP_DIR="/tmp/zotero-read-$$"
mkdir -p "$TMP_DIR"
trap 'rm -rf -- "$TMP_DIR"' EXIT

API_URL="https://api.zotero.org/users/$ZOTERO_USER_ID/items"

# --- Cross-platform Helper Functions ---
get_filesize() {
    local file="$1"
    if stat -c %s "$file" >/dev/null 2>&1; then
        # Linux style
        stat -c %s "$file"
    elif stat -f %z "$file" >/dev/null 2>&1; then
        # macOS style
        stat -f %z "$file"
    else
        echo "Error: stat command does not support size options." >&2
        exit 1
    fi
}

# --- 1. Find Attachment Key ---
echo "Step 1: Finding PDF attachment for item $ITEM_KEY..."
CHILDREN_RESPONSE=$(curl -s -f \
  -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "$API_URL/$ITEM_KEY/children")

# First try imported_file (stored file)
ATTACHMENT_KEY=$(echo "$CHILDREN_RESPONSE" | jq -r '.[] | select(.data.itemType == "attachment") | select(.data.linkMode == "imported_file") | select((.data.filename | type) == "string") | select(.data.filename | test("\\.pdf$"; "i")) | .key' | head -n 1)

# If not found and WebDAV credentials are present, also try imported_url (may be stored in WebDAV)
if [ -z "$ATTACHMENT_KEY" ] && [ -n "$WEBDAV_URL" ] && [ -n "$WEBDAV_USER" ] && [ -n "$WEBDAV_PASS" ]; then
    ATTACHMENT_KEY=$(echo "$CHILDREN_RESPONSE" | jq -r '.[] | select(.data.itemType == "attachment") | select(.data.linkMode == "imported_url") | select((.data.filename | type) == "string") | select(.data.filename | test("\\.pdf$"; "i")) | .key' | head -n 1)
fi

[ -n "$ATTACHMENT_KEY" ] || { echo "Error: No PDF attachment found for item $ITEM_KEY. Response: $CHILDREN_RESPONSE"; exit 1; }
echo "  - Found attachment key: $ATTACHMENT_KEY"

# Get attachment details
ATTACHMENT_RESPONSE=$(curl -s -f \
  -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "$API_URL/$ATTACHMENT_KEY")

FILENAME=$(echo "$ATTACHMENT_RESPONSE" | jq -r '.data.filename // ""')
echo "  - Filename: $FILENAME"

# --- 2. Download PDF ---
PDF_PATH="$TMP_DIR/$FILENAME"

if [ -n "$WEBDAV_URL" ] && [ -n "$WEBDAV_USER" ] && [ -n "$WEBDAV_PASS" ]; then
    # WebDAV mode
    echo "Step 2: Downloading from WebDAV..."
    WEBDAV_SOURCE_URL="${WEBDAV_URL%/}/$ATTACHMENT_KEY.zip"
    
    ZIP_PATH="$TMP_DIR/$ATTACHMENT_KEY.zip"
    curl -s -f -u "$WEBDAV_USER:$WEBDAV_PASS" -o "$ZIP_PATH" "$WEBDAV_SOURCE_URL"
    echo "  - Download complete"
    
    # Extract PDF from zip
    echo "Step 3: Extracting PDF from zip..."
    unzip -q "$ZIP_PATH" -d "$TMP_DIR"
    
    # Check if the expected PDF file already exists
    if [ -f "$PDF_PATH" ]; then
        echo "  - PDF already at expected location: $FILENAME"
    else
        # Find the extracted PDF (fallback)
        EXTRACTED_PDF=$(find "$TMP_DIR" -maxdepth 1 -iname "*.pdf" -print -quit)
        if [ -f "$EXTRACTED_PDF" ]; then
            mv "$EXTRACTED_PDF" "$PDF_PATH"
            echo "  - Extracted: $FILENAME"
        else
            echo "Error: PDF not found in zip archive"
            exit 1
        fi
    fi
    
else
    # Zotero API direct download mode
    echo "Step 2: Downloading via Zotero API..."
    
    # Get download URL from attachment data
    DOWNLOAD_URL=$(echo "$ATTACHMENT_RESPONSE" | jq -r '.links.enclosure.href // ""')
    
    if [ -n "$DOWNLOAD_URL" ]; then
        # Download directly
        curl -s -f -H "Zotero-API-Key: $ZOTERO_API_KEY" -o "$PDF_PATH" "$DOWNLOAD_URL"
        echo "  - Download complete"
    else
        echo "Error: No download URL found in attachment data"
        echo "  - Attachment data: $ATTACHMENT_RESPONSE"
        echo "  - Try setting WEBDAV_URL, WEBDAV_USER, WEBDAV_PASS for WebDAV access"
        exit 1
    fi
fi

# --- 3. Extract and Output Text ---
if [ ! -f "$PDF_PATH" ]; then
    echo "Error: PDF file not found at $PDF_PATH"
    exit 1
fi

FILE_SIZE=$(get_filesize "$PDF_PATH")
echo "Step 3: Extracting text content (${FILE_SIZE} bytes)..."
echo ""
echo "------------------- DOCUMENT START -------------------"
pdftotext "$PDF_PATH" -
echo "-------------------- DOCUMENT END --------------------"

exit 0