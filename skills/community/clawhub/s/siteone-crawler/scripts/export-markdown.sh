#!/usr/bin/env bash
# SiteOne Crawler - Markdown Export Script
# Usage: ./export-markdown.sh <url> <output_dir> [--single] [--no-images] [--no-files]
# Examples:
#   ./export-markdown.sh https://example.com /tmp/md-export
#   ./export-markdown.sh https://example.com /tmp/md-export --single --no-images

set -euo pipefail

# Auto-detect binary
if [ -x "$HOME/.siteone-crawler/siteone-crawler" ]; then
  CRAWLER="$HOME/.siteone-crawler/siteone-crawler"
elif command -v siteone-crawler &>/dev/null; then
  CRAWLER="$(command -v siteone-crawler)"
else
  echo "❌ siteone-crawler not found. Run Setup in SKILL.md first." >&2; exit 1
fi
URL="${1:?Usage: export-markdown.sh <url> <output_dir> [--single] [--no-images] [--no-files]}"
OUTPUT_DIR="${2:?Usage: export-markdown.sh <url> <output_dir> [--single] [--no-images] [--no-files]}"
SINGLE=false
NO_IMAGES=false
NO_FILES=false

for arg in "${@:3}"; do
  case "$arg" in
    --single) SINGLE=true ;;
    --no-images) NO_IMAGES=true ;;
    --no-files) NO_FILES=true ;;
  esac
done

ARGS=(
  --url="$URL"
  --markdown-export-dir="$OUTPUT_DIR"
  --timezone="Asia/Shanghai"
  --no-color
)

if $SINGLE; then
  DOMAIN=$(echo "$URL" | sed 's|https\?://\([^/]*\).*|\1|' | tr ':' '_')
  SINGLE_FILE="$OUTPUT_DIR/${DOMAIN}_combined.md"
  ARGS+=(--markdown-export-single-file="$SINGLE_FILE")
fi

if $NO_IMAGES; then
  ARGS+=(--markdown-disable-images)
fi

if $NO_FILES; then
  ARGS+=(--markdown-disable-files)
fi

echo "📝 Exporting to markdown: $URL"
echo "📁 Output: $OUTPUT_DIR"

"$CRAWLER" "${ARGS[@]}"

echo ""
echo "✅ Export complete!"
if $SINGLE; then
  echo "📄 Single file: $SINGLE_FILE"
fi
