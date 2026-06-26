#!/bin/bash

# X Media Parser - Extract media URLs from X/Twitter posts

if [ -z "$1" ]; then
  echo "Usage: x-media-parser \"<X/Twitter URL>\""
  exit 1
fi

URL="$1"

# Extract tweet ID
TWEET_ID=$(echo "$URL" | grep -oE 'status/[0-9]+' | grep -oE '[0-9]+')

if [ -z "$TWEET_ID" ]; then
  echo '{"success": false, "error": "无法提取推文 ID"}'
  exit 1
fi

# Call vxtwitter API, then parse with Python to handle special characters
curl -s "https://api.vxtwitter.com/Twitter/status/${TWEET_ID}" | python3 -c "
import sys, json, re

try:
    data = json.load(sys.stdin)
except:
    print(json.dumps({'success': False, 'error': 'API 请求失败'}))
    sys.exit(0)

if not data.get('hasMedia'):
    print(json.dumps({'success': False, 'error': '该推文没有媒体内容'}))
    sys.exit(0)

# Clean text - remove newlines and non-ASCII
text = (data.get('text') or '').replace('\n', ' ').replace('\r', '')
text = re.sub(r'[^\x00-\x7F]+', '', text)

title = f\"{data.get('user_name', '')}: {text[:50]}\" if data.get('user_name') else f\"@{data.get('user_screen_name', '')} 的推文\"

media = data.get('media_extended', [])
videos = [m for m in media if m.get('type') in ('video', 'gif')]
images = [m for m in media if m.get('type') == 'image']

# Build video URLs
video_urls = [v['url'] for v in videos if v.get('url')]

# Build image URLs with high quality
image_urls = []
for img in images:
    u = img.get('url', '')
    if u and 'pbs.twimg.com/media/' in u:
        # Extract filename and add large format
        image_urls.append(u.split('?')[0] + '?format=jpg&name=large')
    elif u:
        image_urls.append(u)

# Determine type
if videos and images:
    typ = 'mixed'
elif len(videos) > 1:
    typ = 'videos'
elif videos:
    typ = 'video'
elif len(images) > 1:
    typ = 'images'
elif images:
    typ = 'image'
else:
    typ = 'unknown'

first = videos[0] if videos else images[0] if images else {}

result = {
    'success': True,
    'media': {
        'type': typ,
        'title': title[:100],
        'url': '$URL',
        'directUrl': (video_urls or image_urls)[0] if (video_urls or image_urls) else '',
        'videoUrls': video_urls if video_urls else None,
        'imageUrls': image_urls if image_urls else None,
        'thumbnails': [v['thumbnail_url'] for v in videos if v.get('thumbnail_url')],
        'thumbnail': first.get('thumbnail_url'),
        'duration': int(first.get('duration_millis', 0) / 1000) if first.get('duration_millis') else None,
        'resolution': f\"{first['size']['width']}x{first['size']['height']}\" if first.get('size') else None
    }
}
print(json.dumps(result, ensure_ascii=False))
"
