#!/bin/bash

# X Media Parser + Aria2 Download

URL="$1"

RPC_URL="${ARIA2_RPC_URL:-http://localhost:6800/jsonrpc}"
SECRET="${ARIA2_SECRET:-}"
DIR="${ARIA2_DIR:-/mnt/sda1/download/X}"

TWEET_ID=$(echo "$URL" | grep -oE 'status/[0-9]+' | grep -oE '[0-9]+')

if [ -z "$TWEET_ID" ]; then
  echo "Error: Cannot extract tweet ID"
  exit 1
fi

curl -s "https://api.vxtwitter.com/Twitter/status/${TWEET_ID}" -o /tmp/tweet.json

if [ ! -s /tmp/tweet.json ]; then
  echo "Error: API request failed"
  exit 1
fi

python3 << 'PYEOF'
import json, re, subprocess, sys

with open('/tmp/tweet.json') as f:
    data = json.load(f)

if not data.get('hasMedia'):
    print("Error: No media in this tweet")
    sys.exit(0)

# Use nickname (user_name) instead of username (user_screen_name)
nickname = data.get('user_name', '')
if nickname:
    nickname = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '', nickname)  # Keep alphanumeric and Chinese
    nickname = nickname[:15] if len(nickname) >= 15 else nickname  # Limit to 15 chars
else:
    nickname = data.get('user_screen_name', 'unknown')
    nickname = re.sub(r'[^a-zA-Z0-9]', '', nickname)

text = data.get('text', '')
if text:
    text = re.sub(r'[\s\n\r]+', '', text)
    text_clean = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '', text)
    if text_clean:
        text = text_clean[:10]
    else:
        text = text[:10]
else:
    text = ''

prefix = f"{nickname}_{text}" if text else nickname

media = data.get('media_extended', [])
videos = [m for m in media if m.get('type') in ('video', 'gif')]
images = [m for m in media if m.get('type') == 'image']

video_urls = [v['url'] for v in videos if v.get('url')]
image_urls = []
for img in images:
    u = img.get('url', '')
    if u and 'pbs.twimg.com/media/' in u:
        image_urls.append(u.split('?')[0] + '?format=jpg&name=large')
    elif u:
        image_urls.append(u)

typ = 'mixed' if (videos and images) else ('videos' if len(videos) > 1 else ('video' if videos else ('images' if len(images) > 1 else ('image' if images else 'unknown'))))

print("="*50)
print("【解析完成】")
print("="*50)
print(f"昵称: {nickname}")
print(f"贴文: {text}")
print(f"类型: {typ}")
print(f"文件数: {len(video_urls) + len(image_urls)}")
print("="*50)

all_urls = video_urls + image_urls
rpc_url = 'http://10.0.0.1:6800/jsonrpc'
secret = '88888888'
dir_path = '/mnt/sda1/download/X'

print("\n【开始下载】")
print("="*50)

for i, url in enumerate(all_urls, 1):
    ext = url.split('.')[-1].split('?')[0]
    if ext not in ['jpg', 'jpeg', 'png', 'mp4', 'webm']:
        ext = 'mp4' if 'video' in typ else 'jpg'
    
    filename = f"{prefix}_{i}.{ext}"
    print(f"添加: {filename}")
    
    params = [f"token:{secret}", [url], {"max-connection-per-server": 16, "split": 16, "min-split-size": "1M", "dir": dir_path, "out": filename}]
    payload = json.dumps({"jsonrpc": "2.0", "method": "aria2.addUri", "id": 1, "params": params})
    
    result = subprocess.run(['curl', '-s', '-X', 'POST', rpc_url, '-H', 'Content-Type: application/json', '-d', payload], capture_output=True, text=True)
    resp = result.stdout
    
    if '"result"' in resp:
        gid = re.search(r'"result":\s*"([^"]+)"', resp)
        if gid:
            print(f"  ✓ GID: {gid.group(1)}")
    else:
        print(f"  ✗ 失败")

print("="*50)
print("全部添加完成!")
PYEOF
