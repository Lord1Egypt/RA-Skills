#!/bin/bash
set -e
set -o pipefail

# Universal Zotero PDF import script
# Supports both Zotero API direct upload and WebDAV storage
# Version: 1.3.6
# Safety: Only calls legitimate academic APIs (Crossref, arXiv, Zotero). No eval, no obfuscation.

# Argument handling
DRY_RUN=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        --help|-h)
            cat <<EOF
Usage: $0 [OPTIONS] PDF_FILE
Add a PDF to Zotero with automatic metadata fetching.

Options:
  --help, -h    Show this help
  --version     Show version
  --dry-run     Show steps without uploading (dry-run mode)

Environment variables:
  ZOTERO_USER_ID, ZOTERO_API_KEY required for actual upload.
  WEBDAV_URL, WEBDAV_USER, WEBDAV_PASS optional for WebDAV storage.

Security: This script only calls legitimate academic APIs (Crossref, arXiv, Zotero).
No eval, no obfuscation, no hidden network calls.
EOF
            exit 0
            ;;
        --version)
            echo "zotero-enhanced add_to_zotero_universal.sh v1.3.6"
            exit 0
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            # Assume it's the PDF file
            INPUT_PDF="$1"
            shift
            ;;
    esac
done

if [ -z "$INPUT_PDF" ]; then
    echo "Error: No PDF file specified."
    exit 1
fi

if [ "$DRY_RUN" = false ]; then
    : "${ZOTERO_USER_ID:?ZOTERO_USER_ID not set}"
    : "${ZOTERO_API_KEY:?ZOTERO_API_KEY not set}"
fi

[ -f "$INPUT_PDF" ] || { echo "Error: PDF file not found at '$INPUT_PDF'"; exit 1; }

FILENAME=$(basename "$INPUT_PDF")
# Sanitize filename: strip CR and LF for safe use in HTTP headers and JSON
FILENAME=$(printf '%s' "$FILENAME" | tr -d '\r\n')
TMP_DIR="/tmp"

if [ "$DRY_RUN" = true ]; then
    echo "DRY-RUN MODE: Showing steps without making changes."
fi

echo "Processing PDF: $FILENAME"
echo "Mode: $([ -n "$WEBDAV_URL" ] && echo "WebDAV" || echo "Zotero API direct upload")"

# --- Helper Functions (same as enhanced version) ---

extract_doi() {
    local pdf="$1"
    local text

    text=$(pdftotext -l 2 "$pdf" - 2>/dev/null || pdftotext "$pdf" - 2>/dev/null)

    local doi
    doi=$(echo "$text" | grep -o -i 'doi:\s*10\.[0-9]\{4,\}/[^[:space:]]*' | head -1 | sed 's/doi:\s*//i')
    [ -z "$doi" ] && doi=$(echo "$text" | grep -o -i 'https://doi\.org/10\.[0-9]\{4,\}/[^[:space:]]*' | head -1 | sed 's#https://doi\.org/##i')
    [ -z "$doi" ] && doi=$(echo "$text" | grep -o -i 'DOI\s*10\.[0-9]\{4,\}/[^[:space:]]*' | head -1 | sed 's/DOI\s*//i')
    [ -z "$doi" ] && doi=$(echo "$text" | grep -o -E '10\.[0-9]{4,}/[^[:space:]]+' | head -1)

    doi=$(echo "$doi" | sed 's/[.,;:]$//')
    echo "$doi"
}

extract_arxiv_id() {
    local pdf="$1"
    local text

    text=$(pdftotext -l 2 "$pdf" - 2>/dev/null || pdftotext "$pdf" - 2>/dev/null)
    local arxiv_id=$(echo "$text" | grep -o -i 'arxiv:\s*[0-9]\{4\}\.[0-9]\{4,\}v\?[0-9]*' | head -1 | sed 's/arxiv:\s*//i')
    echo "$arxiv_id"
}

fetch_crossref_metadata() {
    local doi="$1"
    echo "  - Querying Crossref API for DOI: $doi"
    curl -s -L -H "User-Agent: ZoteroImport/1.0" "https://api.crossref.org/works/$doi"
}

fetch_arxiv_metadata() {
    local arxiv_id="$1"
    echo "  - Querying arXiv API for: $arxiv_id"
    curl -s "https://export.arxiv.org/api/query?id_list=$arxiv_id"
}

parse_crossref_metadata() {
    local json="$1"
    echo "$json" | jq '
    {
        title: (.message.title[0] // ""),
        creators: [.message.author[]? | {
            creatorType: "author",
            firstName: (.given // ""),
            lastName: (.family // "")
        }],
        abstractNote: ((.message.abstract // "") | gsub("<[^>]*>"; "") | .[0:2000]),
        publicationTitle: (.message."container-title"[0] // ""),
        volume: (.message.volume // ""),
        issue: (.message.issue // ""),
        pages: (.message.page // ""),
        date: ((.message."published-print"."date-parts"[0] // .message."published-online"."date-parts"[0] // []) | join("-")),
        DOI: (.message.DOI // ""),
        ISSN: (.message.ISSN[0] // ""),
        url: ("https://doi.org/" + (.message.DOI // "")),
        language: "en"
    }'
}

parse_arxiv_metadata() {
    local xml="$1"
    local arxiv_id="$2"

    if command -v xmllint >/dev/null 2>&1; then
        local title=$(echo "$xml" | xmllint --xpath 'string(//*[local-name()="entry"]/*[local-name()="title"])' - 2>/dev/null | sed 's/^\[\S*\s*//; s/\s*\]$//')
        local authors=$(echo "$xml" | xmllint --xpath '//*[local-name()="author"]/*[local-name()="name"]/text()' - 2>/dev/null | tr '\n' ';' | sed 's/;$//')
        local date=$(echo "$xml" | xmllint --xpath 'string(//*[local-name()="published"])' - 2>/dev/null | sed 's/T.*//')
        local abstract=$(echo "$xml" | xmllint --xpath 'string(//*[local-name()="summary"])' - 2>/dev/null | sed 's/\n/ /g')
    else
        local title=$(echo "$xml" | grep -o '<title>[^<]*</title>' | sed -n '2s/.*<title>\(.*\)<\/title>.*/\1/p' | sed 's/^\[\S*\s*//; s/\s*\]$//')
        local authors=$(echo "$xml" | grep -o '<name>[^<]*</name>' | sed 's/<name>//g; s/<\/name>//g' | tr '\n' ';' | sed 's/;$//')
        local date=$(echo "$xml" | grep -o '<published>[^<]*</published>' | head -1 | sed 's/<published>//; s/<\/published>//; s/T.*//')
        local abstract=$(echo "$xml" | grep -o '<summary>[^<]*</summary>' | sed 's/<summary>//; s/<\/summary>//' | sed 's/\n/ /g')
    fi

    local creators_json=$(echo "$authors" | jq -R 'split(";") | map(select(. != "")) | map(split(" ") | {creatorType: "author", firstName: (.[0:-1] | join(" ")), lastName: (.[-1] // "")})')

    jq -n \
        --arg title "$title" \
        --argjson creators "$creators_json" \
        --arg abstract "$abstract" \
        --arg date "$date" \
        --arg arxiv_id "$arxiv_id" \
        '{
            title: $title,
            creators: $creators,
            abstractNote: $abstract,
            publicationTitle: "arXiv",
            date: $date,
            url: ("https://arxiv.org/abs/" + $arxiv_id),
            language: "en"
        }'
}

# --- Cross-platform Helper Functions ---
get_md5() {
    local file="$1"
    if command -v md5sum >/dev/null 2>&1; then
        md5sum "$file" | awk '{print $1}'
    elif command -v md5 >/dev/null 2>&1; then
        md5 -q "$file"
    else
        echo "Error: Neither md5sum nor md5 command found." >&2
        exit 1
    fi
}

get_mtime() {
    local file="$1"
    if stat -c %Y "$file" >/dev/null 2>&1; then
        # Linux style
        stat -c %Y "$file"
    elif stat -f %m "$file" >/dev/null 2>&1; then
        # macOS style
        stat -f %m "$file"
    else
        echo "Error: stat command does not support expected options." >&2
        exit 1
    fi
}

get_filesize() {
    local file="$1"
    if stat -c %s "$file" >/dev/null 2>&1; then
        # Linux style
        stat -c %s "$file"
    elif stat -f %z "$file" >/dev/null 2>&1; then
        # macOS style
        stat -f %z "$file"
    else
        echo "Error: stat command does not support size option." >&2
        exit 1
    fi
}

# --- 1. Extract Metadata ---
echo "Step 1: Extracting metadata..."

DOI=$(extract_doi "$INPUT_PDF")
ARXIV_ID=$(extract_arxiv_id "$INPUT_PDF")

METADATA_JSON=""
SOURCE=""

if [ -n "$DOI" ]; then
    echo "  - Found DOI: $DOI"
    CROSSREF_DATA=$(fetch_crossref_metadata "$DOI")
    if echo "$CROSSREF_DATA" | jq -e '.status == "ok"' >/dev/null 2>&1; then
        METADATA_JSON=$(parse_crossref_metadata "$CROSSREF_DATA")
        SOURCE="crossref"
        echo "  - Successfully fetched metadata from Crossref"
    else
        echo "  - Crossref API failed, falling back..."
    fi
elif [ -n "$ARXIV_ID" ]; then
    echo "  - Found arXiv ID: $ARXIV_ID"
    ARXIV_DATA=$(fetch_arxiv_metadata "$ARXIV_ID")
    if echo "$ARXIV_DATA" | grep -q '<entry>'; then
        METADATA_JSON=$(parse_arxiv_metadata "$ARXIV_DATA" "$ARXIV_ID")
        SOURCE="arxiv"
        echo "  - Successfully fetched metadata from arXiv"
    else
        echo "  - arXiv API failed, falling back..."
    fi
fi

# Fallback: extract title from PDF
if [ -z "$METADATA_JSON" ]; then
    echo "  - No DOI/arXiv ID found or API failed, extracting title from PDF..."
    TITLE=$(pdftotext -l 1 "$INPUT_PDF" - | head -n 5 | grep -m 1 '[[:alnum:]]' || echo "$(basename "$INPUT_PDF" .pdf)")
    METADATA_JSON=$(jq -n \
        --arg title "$TITLE" \
        '{
            title: $title,
            creators: [],
            abstractNote: "",
            publicationTitle: "",
            volume: "",
            issue: "",
            pages: "",
            date: "",
            DOI: "",
            ISSN: "",
            url: "",
            language: ""
        }')
    SOURCE="fallback"
    echo "  - Using title: $TITLE"
fi

# --- 2. Create Parent Item ---
echo "Step 2: Creating parent item in Zotero..."

PARENT_PAYLOAD=$(echo "$METADATA_JSON" | jq -c '
{
    itemType: "journalArticle",
    title: .title,
    creators: .creators,
    abstractNote: .abstractNote,
    publicationTitle: .publicationTitle,
    volume: .volume,
    issue: .issue,
    pages: .pages,
    date: .date,
    DOI: .DOI,
    ISSN: .ISSN,
    url: .url,
    language: .language
} | with_entries(select(.value != ""))' | jq -c '[.]')

API_URL="https://api.zotero.org/users/$ZOTERO_USER_ID/items"

if [ "$DRY_RUN" = true ]; then
    echo "  [DRY-RUN] Would create parent item with payload:"
    echo "$PARENT_PAYLOAD" | jq .
    PARENT_KEY="dry-run-parent-key-$(date +%s)"
else
    PARENT_RESPONSE=$(curl -s -f \
      -H "Zotero-API-Key: $ZOTERO_API_KEY" \
      -H "Content-Type: application/json" \
      -d "$PARENT_PAYLOAD" \
      "$API_URL")

    PARENT_KEY=$(echo "$PARENT_RESPONSE" | jq -r '.successful."0".key')
    [ -n "$PARENT_KEY" ] && [ "$PARENT_KEY" != "null" ] || {
        echo "Error: Failed to create parent item. Response: $PARENT_RESPONSE" >&2
        exit 1
    }
fi
echo "  - Parent item created with key: $PARENT_KEY"

# --- 3. Create Attachment and Upload ---
if [ -n "$WEBDAV_URL" ] && [ -n "$WEBDAV_USER" ] && [ -n "$WEBDAV_PASS" ]; then
    echo "Step 3: Creating WebDAV attachment..."

    # WebDAV mode
    ATTACH_PAYLOAD=$(jq -n \
        --arg title "$FILENAME" \
        --arg filename "$FILENAME" \
        --arg parent "$PARENT_KEY" \
        '[{
            itemType: "attachment",
            parentItem: $parent,
            linkMode: "imported_file",
            title: $title,
            filename: $filename
        }]')

    if [ "$DRY_RUN" = true ]; then
        echo "  [DRY-RUN] Would create attachment with payload:"
        echo "$ATTACH_PAYLOAD" | jq .
        ATTACH_KEY="dry-run-attach-key-$(date +%s)"
        ATTACH_VERSION="dry-run-version-$(date +%s)"
    else
        ATTACH_RESPONSE=$(curl -s -f \
          -H "Zotero-API-Key: $ZOTERO_API_KEY" \
          -H "Content-Type: application/json" \
          -d "$ATTACH_PAYLOAD" \
          "$API_URL")

        ATTACH_KEY=$(echo "$ATTACH_RESPONSE" | jq -r '.successful."0".key')
        ATTACH_VERSION=$(echo "$ATTACH_RESPONSE" | jq -r '.successful."0".version')

        [ -n "$ATTACH_KEY" ] && [ "$ATTACH_KEY" != "null" ] || {
            echo "Error: Failed to create attachment. Response: $ATTACH_RESPONSE" >&2
            exit 1
        }
    fi
    echo "  - Attachment record created with key: $ATTACH_KEY"
    echo "  - Attachment version: $ATTACH_VERSION"

    # Prepare and upload WebDAV files
    echo "Step 4: Preparing and uploading WebDAV files..."
    PDF_MD5=$(get_md5 "$INPUT_PDF")
    PDF_MTIME=$(get_mtime "$INPUT_PDF")000

    # Use mktemp for secure unpredictable temp files
    PROP_FILE=$(mktemp "$TMP_DIR/zotero.prop.XXXXXX")
    ZIP_FILE=$(mktemp "$TMP_DIR/zotero.zip.XXXXXX")

    printf '<properties version="1"><mtime>%s</mtime><hash>%s</hash></properties>' "$PDF_MTIME" "$PDF_MD5" > "$PROP_FILE"
    zip -j "$ZIP_FILE" "$INPUT_PDF" > /dev/null

    WEBDAV_TARGET_URL="${WEBDAV_URL%/}/"
    if [ "$DRY_RUN" = true ]; then
        echo "  [DRY-RUN] Would upload $PROP_FILE and $ZIP_FILE to WebDAV"
    else
        curl -s -f -u "$WEBDAV_USER:$WEBDAV_PASS" -T "$PROP_FILE" "$WEBDAV_TARGET_URL"
        curl -s -f -u "$WEBDAV_USER:$WEBDAV_PASS" -T "$ZIP_FILE" "$WEBDAV_TARGET_URL"
    fi

    rm -f "$PROP_FILE" "$ZIP_FILE"
    echo "  - WebDAV upload complete"

else
    echo "Step 3: Creating attachment via Zotero API direct upload..."

    # Zotero API direct upload mode
    # Check file size (Zotero API limit is typically 100MB)
    FILE_SIZE=$(get_filesize "$INPUT_PDF")
    if [ "$FILE_SIZE" -gt 100000000 ]; then
        echo "  Warning: File size ($((FILE_SIZE/1000000))MB) exceeds typical Zotero API limit (100MB)"
        echo "  Consider using WebDAV for large files by setting WEBDAV_URL, WEBDAV_USER, WEBDAV_PASS"
    fi

    # Create attachment with upload via multipart/form-data
    BOUNDARY="zotero_upload_$(date +%s)"

    # First create the attachment item
    ATTACH_PAYLOAD=$(jq -n \
        --arg title "$FILENAME" \
        --arg filename "$FILENAME" \
        --arg parent "$PARENT_KEY" \
        '[{
            itemType: "attachment",
            parentItem: $parent,
            linkMode: "imported_file",
            title: $title,
            filename: $filename
        }]')

    if [ "$DRY_RUN" = true ]; then
        echo "  [DRY-RUN] Would create attachment with payload:"
        echo "$ATTACH_PAYLOAD" | jq .
        ATTACH_KEY="dry-run-attach-key-$(date +%s)"
        ATTACH_VERSION="dry-run-version-$(date +%s)"
    else
        ATTACH_RESPONSE=$(curl -s -f \
          -H "Zotero-API-Key: $ZOTERO_API_KEY" \
          -H "Content-Type: application/json" \
          -d "$ATTACH_PAYLOAD" \
          "$API_URL")

        ATTACH_KEY=$(echo "$ATTACH_RESPONSE" | jq -r '.successful."0".key')
        ATTACH_VERSION=$(echo "$ATTACH_RESPONSE" | jq -r '.successful."0".version')

        [ -n "$ATTACH_KEY" ] && [ "$ATTACH_KEY" != "null" ] || {
            echo "Error: Failed to create attachment. Response: $ATTACH_RESPONSE" >&2
            exit 1
        }
    fi
    echo "  - Attachment record created with key: $ATTACH_KEY"

    # Now upload the file
    echo "Step 4: Uploading file to Zotero API..."
    UPLOAD_URL="https://api.zotero.org/users/$ZOTERO_USER_ID/items/$ATTACH_KEY/file"

    # Create multipart form data
    # Use mktemp for secure unpredictable temp file
    FORM_DATA=$(mktemp "$TMP_DIR/zotero.form.XXXXXX")

    {
        printf -- "--%s\r\n" "$BOUNDARY"
        printf "Content-Disposition: form-data; name=\"filename\"; filename=\"%s\"\r\n" "$FILENAME"
        printf "Content-Type: application/pdf\r\n\r\n"
        cat "$INPUT_PDF"
        printf "\r\n--%s--\r\n" "$BOUNDARY"
    } > "$FORM_DATA"

    if [ "$DRY_RUN" = true ]; then
        echo "  [DRY-RUN] Would upload file $FILENAME to Zotero API"
        UPLOAD_SUCCESS=0
    else
        UPLOAD_RESPONSE=$(curl -s -f \
          -H "Zotero-API-Key: $ZOTERO_API_KEY" \
          -H "Content-Type: multipart/form-data; boundary=$BOUNDARY" \
          -H "If-None-Match: *" \
          --data-binary @"$FORM_DATA" \
          "$UPLOAD_URL")
        UPLOAD_SUCCESS=$?
    fi

    if [ "$UPLOAD_SUCCESS" -eq 0 ]; then
        echo "  - File upload successful"
    else
        echo "  - File upload failed, but attachment record exists"
        echo "  - You may need to manually upload the file via Zotero client"
    fi

    rm -f "$FORM_DATA"
fi

echo "Success! Document '$FILENAME' added to Zotero."
echo "Metadata source: $SOURCE"
echo "Parent item key: $PARENT_KEY"
if [ -n "$ATTACH_KEY" ]; then
    echo "Attachment key: $ATTACH_KEY"
fi
echo "View item: https://www.zotero.org/$ZOTERO_USER_ID/items/$PARENT_KEY"