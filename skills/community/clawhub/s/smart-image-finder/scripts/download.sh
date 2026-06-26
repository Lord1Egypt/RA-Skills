#!/bin/bash
# Smart Image Finder - Batch Download Script
# Usage: ./download.sh <URL> [output_filename]

set -e

URL="$1"
OUTPUT="${2:-downloaded_$(date +%s).jpg}"

if [ -z "$URL" ]; then
    echo "Usage: $0 <image_url> [output_filename]"
    echo ""
    echo "Examples:"
    echo "  $0 'https://www.reuters.com/resizer/v2/xxx.jpg?width=1920' photo.jpg"
    exit 1
fi

echo "Downloading: $URL"
curl -sL --max-time 30 -o "$OUTPUT" "$URL"

# Verify
TYPE=$(file "$OUTPUT" | grep -oE "JPEG|PNG|WEBP|GIF" | head -1)

if [ -n "$TYPE" ]; then
    SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
    echo "✅ Success: $OUTPUT ($TYPE, $SIZE)"
    
    # Show dimensions if identify command available
    if command -v identify &> /dev/null; then
        DIMS=$(identify -format '%wx%h' "$OUTPUT" 2>/dev/null || echo "unknown")
        echo "   Dimensions: $DIMS"
    fi
else
    echo "❌ Failed: Response is not an image file"
    echo "   File type: $(file "$OUTPUT")"
    rm -f "$OUTPUT"
    exit 1
fi
