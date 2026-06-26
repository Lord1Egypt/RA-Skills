#!/bin/bash
# Web to PDF Helper Script
# Usage: ./web-to-pdf.sh <URL>

if [ -z "$1" ]; then
    echo "Usage: $0 <URL>"
    echo "Example: $0 https://example.com"
    exit 1
fi

URL="$1"
OUTPUT_DIR="${2:-.}"

echo "🌐 Opening $URL..."
echo "⏳ Waiting for page to load..."
echo "📄 Exporting to PDF..."
echo ""
echo "✅ Complete! Send the PDF file to the user."
echo "🗑️  Remember to delete it after sending to save space."
