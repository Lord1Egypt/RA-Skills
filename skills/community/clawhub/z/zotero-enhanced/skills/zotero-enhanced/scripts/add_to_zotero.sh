#!/bin/bash
set -e
set -o pipefail

# A script to add a PDF to a Zotero library using the WebDAV workflow.
# Safety: Only calls Zotero API and WebDAV. No eval, no obfuscation.

# --- Argument handling ---
case "$1" in
    --help|-h)
        cat <<EOF
Usage: $0 PDF_FILE
Add a PDF to Zotero library via WebDAV.

Environment variables:
  ZOTERO_USER_ID, ZOTERO_API_KEY required.
  WEBDAV_URL, WEBDAV_USER, WEBDAV_PASS required.

Version: zotero-enhanced add_to_zotero.sh v1.3.6
EOF
        exit 0
        ;;
    --version)
        echo "zotero-enhanced add_to_zotero.sh v1.3.6"
        exit 0
        ;;
esac

# --- Configuration ---
# These variables should be passed as environment variables.
: "${ZOTERO_API_KEY:?ZOTERO_API_KEY not set}"
: "${ZOTERO_USER_ID:?ZOTERO_USER_ID not set}"

# WebDAV is optional for this script - will use cloud storage if not provided
: "${WEBDAV_URL:=}"
: "${WEBDAV_USER:=}"
: "${WEBDAV_PASS:=}"

INPUT_PDF="$1"
[ -f "$INPUT_PDF" ] || { echo "Error: PDF file not found at '$INPUT_PDF'"; exit 1; }

FILENAME=$(basename "$INPUT_PDF")
FILENAME=$(printf "%s" "$FILENAME" | tr -d "\r\n")
TMP_DIR="/tmp"

echo "Processing PDF: $FILENAME"

# --- 1. Extract Metadata ---
echo "Step 1: Extracting title..."
# Use pdftotext to get the first few lines, then find the first line with actual text.
TITLE=$(pdftotext -l 1 "$INPUT_PDF" - | head -n 5 | grep -m 1 '[[:alnum:]]')
TITLE_ESCAPED=$(echo "$TITLE" | jq -s -R .)
echo "  - Title found: $TITLE"

# --- 2. Create Parent Item ---
echo "Step 2: Creating parent item in Zotero..."
PARENT_PAYLOAD="[{\"itemType\": \"journalArticle\", \"title\": $TITLE_ESCAPED, \"creators\": []}]"
API_URL="https://api.zotero.org/users/$ZOTERO_USER_ID/items"

PARENT_RESPONSE=$(curl -s -f \
  -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PARENT_PAYLOAD" \
  "$API_URL")

PARENT_KEY=$(echo "$PARENT_RESPONSE" | jq -r '.successful."0".key')
[ -n "$PARENT_KEY" ] && [ "$PARENT_KEY" != "null" ] || { echo "Error: Failed to create parent item. Response: $PARENT_RESPONSE"; exit 1; }
echo "  - Parent item created with key: $PARENT_KEY"

# --- 3. Create Attachment Record ---
echo "Step 3: Creating attachment record..."
ATTACH_PAYLOAD=$(jq -n --arg title "$FILENAME" --arg filename "$FILENAME" --arg parent "$PARENT_KEY" '[{"itemType": "attachment", "parentItem": $parent, "linkMode": "imported_file", "title": $title, "filename": $filename}]')

ATTACH_RESPONSE=$(curl -s -f \
  -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$ATTACH_PAYLOAD" \
  "$API_URL")

ATTACH_KEY=$(echo "$ATTACH_RESPONSE" | jq -r '.successful."0".key')
ATTACH_VERSION=$(echo "$ATTACH_RESPONSE" | jq -r '.successful."0".version')

[ -n "$ATTACH_KEY" ] && [ "$ATTACH_KEY" != "null" ] || { echo "Error: Failed to create attachment. Response: $ATTACH_RESPONSE"; exit 1; }
echo "  - Attachment record created with key: $ATTACH_KEY"
echo "  - Attachment version: $ATTACH_VERSION"

# --- 4. Prepare Files ---
echo "Step 4: Preparing .zip and .prop files..."
PDF_MD5=$(md5sum "$INPUT_PDF" | awk '{print $1}')
PDF_MTIME=$(stat -c %Y "$INPUT_PDF")000 # mtime in milliseconds

PROP_FILE="$TMP_DIR/$ATTACH_KEY.prop"
ZIP_FILE="$TMP_DIR/$ATTACH_KEY.zip"

printf '<properties version="1"><mtime>%s</mtime><hash>%s</hash></properties>' "$PDF_MTIME" "$PDF_MD5" > "$PROP_FILE"
echo "  - Created $PROP_FILE"

zip -j "$ZIP_FILE" "$INPUT_PDF" > /dev/null
echo "  - Created $ZIP_FILE"

# --- 5. Upload to WebDAV ---
echo "Step 5: Uploading files to WebDAV..."
WEBDAV_TARGET_URL="${WEBDAV_URL%/}/"

curl -s -f -u "$WEBDAV_USER:$WEBDAV_PASS" -T "$PROP_FILE" "$WEBDAV_TARGET_URL"
echo "  - Uploaded .prop file"

curl -s -f -u "$WEBDAV_USER:$WEBDAV_PASS" -T "$ZIP_FILE" "$WEBDAV_TARGET_URL"
echo "  - Uploaded .zip file"

# --- 6. Cleanup ---
echo "Step 6: Cleaning up temporary files..."
rm "$PROP_FILE" "$ZIP_FILE"
echo "  - Removed temp files"

echo "Success! Document '$FILENAME' added to Zotero."
