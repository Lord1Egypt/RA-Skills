#!/bin/bash

# Batch download Twitter videos
# Usage: ./batch-download.sh [options] <url1> <url2> ...

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROXY_ARGS=""
URLS=()

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --proxy|-p)
      PROXY_ARGS="--proxy $2"
      shift 2
      ;;
    --help|-h)
      echo "Usage: $0 [options] <url1> [<url2>] [<url3>] ..."
      echo ""
      echo "Options:"
      echo "  -p, --proxy <url>    Proxy URL (e.g., http://127.0.0.1:7890)"
      echo "  -h, --help          Show this help"
      exit 0
      ;;
    *)
      URLS+=("$1")
      shift
      ;;
  esac
done

if [[ ${#URLS[@]} -eq 0 ]]; then
  echo "❌ Error: Please provide at least one Twitter/X URL"
  echo "Usage: $0 [options] <url1> [<url2>] ..."
  exit 1
fi

echo "🐦 Twitter Batch Video Downloader"
echo "📊 Total URLs: ${#URLS[@]}"
if [[ -n "$PROXY_ARGS" ]]; then
  echo "🌐 Proxy: enabled"
fi
echo ""

SUCCESS=0
FAILED=0

for url in "${URLS[@]}"; do
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  
  if "$SCRIPT_DIR/download.sh" "$url" $PROXY_ARGS; then
    ((SUCCESS++))
  else
    ((FAILED++))
    echo "❌ Failed to download: $url"
  fi
  
  echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎉 Batch download complete!"
echo "✅ Successful: $SUCCESS"
echo "❌ Failed: $FAILED"

if [[ $FAILED -gt 0 ]]; then
  echo ""
  echo "⚠️  If downloads failed, you may need to use a proxy:"
  echo "   $0 --proxy http://127.0.0.1:7890 <url1> <url2> ..."
fi
