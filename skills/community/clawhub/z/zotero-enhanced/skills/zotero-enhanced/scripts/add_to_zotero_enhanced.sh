#!/bin/bash
set -e
set -o pipefail

# Enhanced script to add a PDF to Zotero with automatic metadata fetching
# Supports Crossref API (via DOI) and arXiv API for preprints
# Safety: Only calls legitimate academic APIs (Crossref, arXiv, Zotero). No eval, no obfuscation.

# --- Argument handling ---
case "$1" in
    --help|-h)
        cat <<EOF
Usage: $0 PDF_FILE
Add a PDF to Zotero with automatic metadata fetching (DOI/arXiv).

Environment variables:
  ZOTERO_USER_ID, ZOTERO_API_KEY required.
  WEBDAV_URL, WEBDAV_USER, WEBDAV_PASS optional for WebDAV storage.

Version: zotero-enhanced add_to_zotero_enhanced.sh v1.3.6
EOF
        exit 0
        ;;
    --version)
        echo "zotero-enhanced add_to_zotero_enhanced.sh v1.3.6"
        exit 0
        ;;
esac

# --- Configuration ---
: "${ZOTERO_API_KEY:?ZOTERO_API_KEY not set}"
: "${ZOTERO_USER_ID:?ZOTERO_USER_ID not set}"

# WebDAV is optional for enhanced script - will use cloud storage if not provided
: "${WEBDAV_URL:=}"
: "${WEBDAV_USER:=}"
: "${WEBDAV_PASS:=}"

INPUT_PDF="$1"
[ -f "$INPUT_PDF" ] || { echo "Error: PDF file not found at '$INPUT_PDF'"; exit 1; }

FILENAME=$(basename "$INPUT_PDF")
FILENAME=$(printf "%s" "$FILENAME" | tr -d "\r\n")
TMP_DIR="/tmp"

echo "Processing PDF: $FILENAME"

# --- Helper Functions ---

extract_doi() {
    local pdf="$1"
    local text
    
    # Extract text from first 2 pages (most PDFs have metadata on first page)
    text=$(pdftotext -l 2 "$pdf" - 2>/dev/null || pdftotext "$pdf" - 2>/dev/null)
    
    # Try various DOI patterns
    local doi
    
    # Pattern 1: doi:10.xxxx/xxxx
    doi=$(echo "$text" | grep -o -i 'doi:\s*10\.[0-9]\{4,\}/[^[:space:]]*' | head -1 | sed 's/doi:\s*//i')
    
    # Pattern 2: https://doi.org/10.xxxx/xxxx
    [ -z "$doi" ] && doi=$(echo "$text" | grep -o -i 'https://doi\.org/10\.[0-9]\{4,\}/[^[:space:]]*' | head -1 | sed 's#https://doi\.org/##i')
    
    # Pattern 3: DOI 10.xxxx/xxxx
    [ -z "$doi" ] && doi=$(echo "$text" | grep -o -i 'DOI\s*10\.[0-9]\{4,\}/[^[:space:]]*' | head -1 | sed 's/DOI\s*//i')
    
    # Pattern 4: Just 10.xxxx/xxxx
    [ -z "$doi" ] && doi=$(echo "$text" | grep -o -E '10\.[0-9]{4,}/[^[:space:]]+' | head -1)
    
    # Normalize DOI (remove trailing punctuation)
    doi=$(echo "$doi" | sed 's/[.,;:]$//')
    
    echo "$doi"
}

extract_arxiv_id() {
    local pdf="$1"
    local text
    
    text=$(pdftotext -l 2 "$pdf" - 2>/dev/null || pdftotext "$pdf" - 2>/dev/null)
    
    # Look for arXiv identifiers
    local arxiv_id
    
    # Pattern: arXiv:xxxx.xxxxx or arXiv:xxxx.xxxxxvN
    arxiv_id=$(echo "$text" | grep -o -i 'arxiv:\s*[0-9]\{4\}\.[0-9]\{4,\}v\?[0-9]*' | head -1 | sed 's/arxiv:\s*//i')
    
    echo "$arxiv_id"
}

fetch_crossref_metadata() {
    local doi="$1"
    local response
    
    echo "  - Querying Crossref API for DOI: $doi"
    response=$(curl -s -L -H "User-Agent: ZoteroImport/1.0" "https://api.crossref.org/works/$doi")
    
    if echo "$response" | jq -e '.status == "ok"' >/dev/null 2>&1; then
        echo "$response"
    else
        echo "  - Crossref API error for DOI: $doi" >&2
        return 1
    fi
}

fetch_arxiv_metadata() {
    local arxiv_id="$1"
    local response
    
    echo "  - Querying arXiv API for: $arxiv_id"
    response=$(curl -s "https://export.arxiv.org/api/query?id_list=$arxiv_id")
    
    if echo "$response" | grep -q '<entry>'; then
        echo "$response"
    else
        echo "  - arXiv API error for ID: $arxiv_id" >&2
        return 1
    fi
}

parse_crossref_metadata() {
    local json="$1"
    
    # Build metadata using jq directly
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
    
    # Try to use xmllint if available for proper XML parsing
    if command -v xmllint >/dev/null 2>&1; then
        # Use xmllint for robust parsing
        local title=$(echo "$xml" | xmllint --xpath 'string(//*[local-name()="entry"]/*[local-name()="title"])' - 2>/dev/null | sed 's/^\[\S*\s*//; s/\s*\]$//')
        local authors=$(echo "$xml" | xmllint --xpath '//*[local-name()="author"]/*[local-name()="name"]/text()' - 2>/dev/null | tr '\n' ';' | sed 's/;$//')
        local date=$(echo "$xml" | xmllint --xpath 'string(//*[local-name()="published"])' - 2>/dev/null | sed 's/T.*//')
        local abstract=$(echo "$xml" | xmllint --xpath 'string(//*[local-name()="summary"])' - 2>/dev/null | sed 's/\n/ /g')
    else
        # Fallback to grep/sed
        local title=$(echo "$xml" | grep -o '<title>[^<]*</title>' | sed -n '2s/.*<title>\(.*\)<\/title>.*/\1/p' | sed 's/^\[\S*\s*//; s/\s*\]$//')
        local authors=$(echo "$xml" | grep -o '<name>[^<]*</name>' | sed 's/<name>//g; s/<\/name>//g' | tr '\n' ';' | sed 's/;$//')
        local date=$(echo "$xml" | grep -o '<published>[^<]*</published>' | head -1 | sed 's/<published>//; s/<\/published>//; s/T.*//')
        local abstract=$(echo "$xml" | grep -o '<summary>[^<]*</summary>' | sed 's/<summary>//; s/<\/summary>//' | sed 's/\n/ /g')
    fi
    
    # Build creators array with jq for proper JSON
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
        echo "Error: stat command does not support size options." >&2
        exit 1
    fi
}

# --- 1. Extract Metadata ---
echo "Step 1: Extracting metadata..."

# Try to extract DOI first
DOI=$(extract_doi "$INPUT_PDF")
ARXIV_ID=$(extract_arxiv_id "$INPUT_PDF")

METADATA_JSON=""
SOURCE=""

if [ -n "$DOI" ]; then
    echo "  - Found DOI: $DOI"
    CROSSREF_DATA=$(fetch_crossref_metadata "$DOI")
    if [ $? -eq 0 ]; then
        METADATA_JSON=$(parse_crossref_metadata "$CROSSREF_DATA")
        SOURCE="crossref"
        echo "  - Successfully fetched metadata from Crossref"
    fi
elif [ -n "$ARXIV_ID" ]; then
    echo "  - Found arXiv ID: $ARXIV_ID"
    ARXIV_DATA=$(fetch_arxiv_metadata "$ARXIV_ID")
    if [ $? -eq 0 ]; then
        METADATA_JSON=$(parse_arxiv_metadata "$ARXIV_DATA" "$ARXIV_ID")
        SOURCE="arxiv"
        echo "  - Successfully fetched metadata from arXiv"
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

# Build the parent item payload using jq
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

PARENT_RESPONSE=$(curl -s -f \
  -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PARENT_PAYLOAD" \
  "$API_URL")

PARENT_KEY=$(echo "$PARENT_RESPONSE" | jq -r '.successful."0".key')
[ -n "$PARENT_KEY" ] && [ "$PARENT_KEY" != "null" ] || { 
    echo "Error: Failed to create parent item. Response: $PARENT_RESPONSE" >&2
    echo "Payload sent: $PARENT_PAYLOAD" >&2
    exit 1
}
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

[ -n "$ATTACH_KEY" ] && [ "$ATTACH_KEY" != "null" ] || { 
    echo "Error: Failed to create attachment. Response: $ATTACH_RESPONSE" >&2
    exit 1
}
echo "  - Attachment record created with key: $ATTACH_KEY"
echo "  - Attachment version: $ATTACH_VERSION"

# --- 4. Prepare Files ---
echo "Step 4: Preparing .zip and .prop files..."
PDF_MD5=$(get_md5 "$INPUT_PDF")
PDF_MTIME=$(get_mtime "$INPUT_PDF")000 # mtime in milliseconds

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
rm -f "$PROP_FILE" "$ZIP_FILE"
echo "  - Removed temp files"

echo "Success! Document '$FILENAME' added to Zotero."
echo "Metadata source: $SOURCE"
echo "Parent item key: $PARENT_KEY"
echo "Attachment key: $ATTACH_KEY"