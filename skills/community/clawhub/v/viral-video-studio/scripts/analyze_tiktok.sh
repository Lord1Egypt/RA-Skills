#!/bin/bash
# Analyze a TikTok video URL and extract key information
# Usage: ./analyze_tiktok.sh <tiktok_url>

URL="$1"
if [ -z "$URL" ]; then
  echo "Usage: $0 <tiktok_url>"
  exit 1
fi

echo "🎬 Downloading TikTok video..."
yt-dlp -o "/tmp/tiktok-ref.%(ext)s" --no-playlist "$URL" 2>&1 | tail -3

echo ""
echo "🖼️ Extracting thumbnail frames..."
ffmpeg -i /tmp/tiktok-ref.mp4 -vf "fps=1/5" /tmp/tiktok-frame-%03d.jpg -update 1 -y 2>/dev/null
echo "Frames saved to /tmp/tiktok-frame-*.jpg"

echo ""
echo "📝 Attempting subtitle extraction..."
yt-dlp --write-auto-sub --sub-lang "vi,en,zh" --skip-download \
  -o "/tmp/tiktok-sub" "$URL" 2>&1 | grep -E "Writing|ERROR|no subtitles"

echo ""
echo "📊 Video info:"
yt-dlp --dump-json --no-playlist "$URL" 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'Title: {d.get(\"title\", \"N/A\")}')
print(f'Duration: {d.get(\"duration\", 0)}s')
print(f'Views: {d.get(\"view_count\", \"N/A\")}')
print(f'Likes: {d.get(\"like_count\", \"N/A\")}')
print(f'Creator: @{d.get(\"uploader_id\", \"N/A\")}')
print(f'Description: {d.get(\"description\", \"N/A\")[:200]}')
" 2>/dev/null

echo ""
echo "✅ Done! Now analyze /tmp/tiktok-frame-001.jpg with the image tool."
