#!/usr/bin/env bash
# SiteOne Crawler - Quick Audit Script
# Usage: ./audit.sh <url> [output_dir] [--json] [--upload]
# Examples:
#   ./audit.sh https://example.com
#   ./audit.sh https://example.com /tmp/reports --json --upload

set -euo pipefail

# Auto-detect binary
if [ -x "$HOME/.siteone-crawler/siteone-crawler" ]; then
  CRAWLER="$HOME/.siteone-crawler/siteone-crawler"
elif command -v siteone-crawler &>/dev/null; then
  CRAWLER="$(command -v siteone-crawler)"
else
  echo "❌ siteone-crawler not found. Run Setup in SKILL.md first." >&2; exit 1
fi
URL="${1:?Usage: audit.sh <url> [output_dir] [--json] [--upload]}"
OUTPUT_DIR="${2:-/tmp/siteone-audit}"
DO_JSON=false
DO_UPLOAD=false

for arg in "${@:3}"; do
  case "$arg" in
    --json) DO_JSON=true ;;
    --upload) DO_UPLOAD=true ;;
  esac
done

mkdir -p "$OUTPUT_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DOMAIN=$(echo "$URL" | sed 's|https\?://\([^/]*\).*|\1|' | tr ':' '_')
HTML_REPORT="$OUTPUT_DIR/report_${DOMAIN}_${TIMESTAMP}.html"

ARGS=(
  --url="$URL"
  --output-html-report="$HTML_REPORT"
  --timezone="Asia/Shanghai"
  --no-color
)

if $DO_JSON; then
  JSON_FILE="$OUTPUT_DIR/result_${DOMAIN}_${TIMESTAMP}.json"
  ARGS+=(--output-json-file="$JSON_FILE")
fi

if $DO_UPLOAD; then
  ARGS+=(--upload --upload-retention="7d")
fi

echo "🔍 Auditing: $URL"
echo "📊 Report: $HTML_REPORT"

"$CRAWLER" "${ARGS[@]}"

echo ""
echo "✅ Audit complete!"
echo "📄 HTML Report: $HTML_REPORT"
if $DO_JSON; then
  echo "📋 JSON Result: $JSON_FILE"
fi
