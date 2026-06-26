#!/bin/bash
# Smart Image Finder - Image Verification Script
# Usage: ./verify.sh <image_file_or_url>

TARGET="$1"

if [ -z "$TARGET" ]; then
    echo "Usage: $0 <image_file_or_url>"
    exit 1
fi

# If URL, check HTTP status first
if [[ "$TARGET" == http* ]]; then
    echo "Checking URL: $TARGET"
    echo ""
    
    # HTTP status
    STATUS=$(curl -sI --max-time 10 "$TARGET" | head -1)
    echo "HTTP Status: $STATUS"
    
    # Content-Type
    CTYPE=$(curl -sI --max-time 10 "$TARGET" | grep -i "content-type" | head -1)
    echo "Content-Type: $CTYPE"
    
    # Content-Length
    CLEN=$(curl -sI --max-time 10 "$TARGET" | grep -i "content-length" | head -1)
    echo "Content-Length: $CLEN"
    
    # Result
    echo ""
    if echo "$STATUS" | grep -q "200"; then
        if echo "$CTYPE" | grep -qi "image"; then
            echo "✅ URL is accessible and returns an image"
        else
            echo "⚠️ URL is accessible but not an image type"
        fi
    else
        echo "❌ URL is not accessible"
    fi
else
    # Local file
    echo "Checking file: $TARGET"
    echo ""
    
    if [ ! -f "$TARGET" ]; then
        echo "❌ File does not exist"
        exit 1
    fi
    
    # File type
    TYPE=$(file "$TARGET")
    echo "File type: $TYPE"
    
    # File size
    SIZE=$(ls -lh "$TARGET" | awk '{print $5}')
    echo "File size: $SIZE"
    
    # Image dimensions
    if command -v identify &> /dev/null; then
        DIMS=$(identify -format '%wx%h' "$TARGET" 2>/dev/null || echo "unable to identify")
        echo "Dimensions: $DIMS"
    fi
    
    # Result
    echo ""
    if echo "$TYPE" | grep -qiE "JPEG|PNG|WEBP|GIF"; then
        echo "✅ Valid image file"
    else
        echo "❌ Not an image file"
    fi
fi
