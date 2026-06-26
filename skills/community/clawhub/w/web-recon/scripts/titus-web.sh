#!/bin/bash
# Titus web scanner - downloads website content and scans for secrets
# Usage: titus-web.sh <url> [--validate]

set -e

URL="$1"
VALIDATE=""
if [[ "$2" == "--validate" ]]; then
    VALIDATE="--validate"
fi

if [[ -z "$URL" ]]; then
    echo "Usage: titus-web.sh <url> [--validate]"
    echo ""
    echo "Examples:"
    echo "  titus-web.sh https://example.com"
    echo "  titus-web.sh https://example.com/app.js --validate"
    exit 1
fi

TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

echo "🔍 Scanning: $URL"

# Determine if single file or crawl
if [[ "$URL" =~ \.(js|json|txt|xml|html|css|md)$ ]]; then
    # Single file
    FILENAME=$(basename "$URL")
    curl -sL "$URL" -o "$TMPDIR/$FILENAME"
    echo "📄 Downloaded: $FILENAME"
else
    # Try to get main page + common JS files
    echo "📥 Fetching page content..."
    curl -sL "$URL" -o "$TMPDIR/index.html" 2>/dev/null || true
    
    # Extract JS URLs from page
    if [[ -f "$TMPDIR/index.html" ]]; then
        grep -oE 'src="[^"]+\.js"' "$TMPDIR/index.html" | sed 's/src="//;s/"$//' | while read jsfile; do
            if [[ "$jsfile" == /* ]]; then
                # Absolute path
                BASEURL=$(echo "$URL" | grep -oE 'https?://[^/]+')
                curl -sL "${BASEURL}${jsfile}" -o "$TMPDIR/$(basename $jsfile)" 2>/dev/null || true
            elif [[ "$jsfile" != http* ]]; then
                # Relative path
                curl -sL "${URL%/}/${jsfile}" -o "$TMPDIR/$(basename $jsfile)" 2>/dev/null || true
            else
                curl -sL "$jsfile" -o "$TMPDIR/$(basename $jsfile)" 2>/dev/null || true
            fi
        done
    fi
fi

echo "📂 Files to scan:"
ls -la "$TMPDIR"
echo ""

# Run titus
titus scan "$TMPDIR" --output :memory: $VALIDATE --format human
