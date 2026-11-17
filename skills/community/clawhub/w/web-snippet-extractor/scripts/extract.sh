#!/usr/bin/env bash
# extract.sh - Quick snippet extractor for CLI use
# Usage: ./extract.sh <url> [max-chars]
# Requires: curl, pandoc (optional for markdown conversion)

set -euo pipefail

URL="${1:?Usage: extract.sh <url> [max-chars]}"
MAX_CHARS="${2:-20000}"

if ! command -v curl &>/dev/null; then
  echo "Error: curl is required" >&2
  exit 1
fi

echo "# Snippets from: $URL"
echo ""

# Fetch and extract code blocks using grep if no pandoc
html=$(curl -sL --max-time 30 "$URL")

if command -v pandoc &>/dev/null; then
  # pandoc converts HTML to markdown preserving fenced code blocks
  echo "$html" | pandoc -f html -t markdown --wrap=none 2>/dev/null | head -c "$MAX_CHARS"
else
  # Fallback: extract <code> and <pre> blocks with grep
  echo "(pandoc not found, showing raw code blocks)" >&2
  echo "$html" | grep -oP '(?<=<code[^>]*>)(.*?)(?=</code>)' | head -50 || true
fi
