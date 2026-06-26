#!/bin/bash

# Get video info without downloading
# Usage: ./info.sh <twitter-url> [options]

set -e

URL="$1"
PROXY="$2"

if [[ -z "$URL" ]]; then
  echo "❌ Error: Please provide a Twitter/X URL"
  echo "Usage: $0 <twitter-url> [--proxy <url>]"
  exit 1
fi

# Build proxy args
PROXY_ARGS=""
if [[ -n "$PROXY" && "$PROXY" == --proxy* ]]; then
  PROXY_ARGS="$PROXY"
fi

echo "🐦 Getting video information..."
echo ""

if ! yt-dlp \
  --dump-json \
  --no-download \
  $PROXY_ARGS \
  "$URL" 2>/dev/null | python3 -c "
import json
import sys

try:
    data = json.load(sys.stdin)
    print('📹 Title:', data.get('title', 'N/A'))
    print('👤 Author:', data.get('uploader', 'N/A'))
    print('⏱️  Duration:', f\"{data.get('duration', 0)//60}m {data.get('duration', 0)%60}s\")
    print('📊 Views:', data.get('view_count', 'N/A'))
    print('❤️  Likes:', data.get('like_count', 'N/A'))
    print('🔄 Retweets:', data.get('repost_count', 'N/A'))
    print('')
    print('📁 Available formats:')
    
    formats = data.get('formats', [])
    video_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('height')]
    
    # Group by height and show best quality for each
    heights = sorted(set(f.get('height', 0) for f in video_formats), reverse=True)
    
    for height in heights[:5]:  # Show top 5 qualities
        format_info = next((f for f in video_formats if f.get('height') == height), None)
        if format_info:
            ext = format_info.get('ext', 'mp4')
            print(f'   {height}p ({ext})')
    
    print('')
    print('💡 Download commands:')
    print('   download.sh \"$URL\"')
    print('   download.sh \"$URL\" -q 1080')
    
except Exception as e:
    print(f'Error: Unable to fetch video info', file=sys.stderr)
    print('If you are in a restricted network, try using a proxy:', file=sys.stderr)
    print('  info.sh \"$URL\" --proxy http://127.0.0.1:7890', file=sys.stderr)
    sys.exit(1)
"; then
  echo ""
  echo "❌ Failed to get video information!"
  echo ""
  echo "⚠️  If you are in a network-restricted country/region,"
  echo "   please use the --proxy option:"
  echo ""
  echo "   $0 \"$URL\" --proxy http://127.0.0.1:7890"
  exit 1
fi
