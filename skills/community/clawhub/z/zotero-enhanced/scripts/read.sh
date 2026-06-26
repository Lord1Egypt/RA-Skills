#!/bin/bash
set -e
set -o pipefail

# A script to download, extract, and read a PDF from a Zotero WebDAV library.
# Safety: Only calls Zotero API and WebDAV. No eval, no obfuscation.

# --- Argument handling ---
case "$1" in
    --help|-h)
        cat <<EOF
Usage: $0 ITEM_KEY
Download and read a PDF attachment from a Zotero item via WebDAV.

Environment variables:
  ZOTERO_USER_ID, ZOTERO_API_KEY required.
  WEBDAV_URL, WEBDAV_USER, WEBDAV_PASS required (WebDAV storage).

Version: zotero-enhanced read.sh v1.3.8
EOF
        exit 0
        ;;
    --version)
        echo "zotero-enhanced read.sh v1.3.8"
        exit 0
        ;;
esac

# --- Configuration ---
: "${ZOTERO_API_KEY:?ZOTERO_API_KEY not set}"
: "${ZOTERO_USER_ID:?ZOTERO_USER_ID not set}"
: "${WEBDAV_URL:?WEBDAV_URL not set}"
: "${WEBDAV_USER:?WEBDAV_USER not set}"
: "${WEBDAV_PASS:?WEBDAV_PASS not set}"

ITEM_KEY="$1"
[ -n "$ITEM_KEY" ] || { echo "Error: Zotero item key not provided."; exit 1; }

TMP_DIR="/tmp/zotero-read-$$"
mkdir -p "$TMP_DIR"
trap 'rm -rf -- "$TMP_DIR"' EXIT

API_URL="https://api.zotero.org/users/$ZOTERO_USER_ID/items"

# --- 1. Find Attachment Key ---
echo "Step 1: Finding PDF attachment for item $ITEM_KEY..."
CHILDREN_RESPONSE=$(curl -s -f \
  -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "$API_URL/$ITEM_KEY/children")

ATTACHMENT_KEY=$(echo "$CHILDREN_RESPONSE" | jq -r '.[] | select(.data.itemType == "attachment") | select(.data.linkMode == "imported_file") | select((.data.filename | type) == "string") | select(.data.filename | test("\\.pdf$"; "i")) | .key' | head -n 1)

[ -n "$ATTACHMENT_KEY" ] || { echo "Error: No PDF attachment found for item $ITEM_KEY. Response: $CHILDREN_RESPONSE"; exit 1; }
echo "  - Found attachment key: $ATTACHMENT_KEY"

# --- 2. Download from WebDAV ---
ZIP_FILE="$ATTACHMENT_KEY.zip"
WEBDAV_SOURCE_URL="${WEBDAV_URL%/}/$ZIP_FILE"
LOCAL_ZIP_PATH="$TMP_DIR/$ZIP_FILE"

echo "Step 2: Downloading $ZIP_FILE from WebDAV..."
curl -s -f -u "$WEBDAV_USER:$WEBDAV_PASS" -o "$LOCAL_ZIP_PATH" "$WEBDAV_SOURCE_URL"
echo "  - Download complete."

# --- 3. Unzip and Find PDF ---
echo "Step 3: Extracting PDF..."
unzip -q "$LOCAL_ZIP_PATH" -d "$TMP_DIR"
PDF_FILE=$(find "$TMP_DIR" -maxdepth 1 -iname "*.pdf" -print -quit)
[ -f "$PDF_FILE" ] || { echo "Error: PDF file not found in zip archive."; exit 1; }
echo "  - Extracted to $PDF_FILE"

# --- 4. Extract and Output Text ---
echo "Step 4: Extracting text content..."
echo ""
echo "------------------- DOCUMENT START -------------------"
pdftotext "$PDF_FILE" -
echo "-------------------- DOCUMENT END --------------------"

# The trap will handle cleanup of TMP_DIR
exit 0
