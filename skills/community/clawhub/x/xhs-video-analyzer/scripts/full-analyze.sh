#!/bin/bash
# 完整的小红书视频分析流程

set -e

URL="$1"
WORK_DIR="${2:-/tmp/xhs-analysis-$(date +%s)}"

if [ -z "$URL" ]; then
    echo "Usage: $0 <xhs_url> [work_dir]"
    exit 1
fi

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 创建工作目录
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎬 小红书视频分析器"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 1: 下载视频
echo "📥 Step 1: 下载视频..."
python3 "$SCRIPT_DIR/download.py" "$URL" "$WORK_DIR"

if [ ! -f "video.mp4" ]; then
    echo ""
    echo "❌ 视频下载失败，尝试使用 yt-dlp..."
    yt-dlp "$URL" -o "video.%(ext)s" --no-playlist 2>/dev/null || true
    
    # 重命名文件
    for ext in mp4 webm mkv; do
        if [ -f "video.$ext" ]; then
            mv "video.$ext" "video.mp4"
            break
        fi
    done
fi

if [ ! -f "video.mp4" ]; then
    echo "❌ 无法下载视频"
    exit 1
fi

echo ""
# Step 2: 提取音频
echo "🎵 Step 2: 提取音频..."
ffmpeg -i video.mp4 -vn -acodec libmp3lame -ab 192k audio.mp3 -y 2>/dev/null

if [ ! -f "audio.mp3" ]; then
    echo "❌ 音频提取失败"
    exit 1
fi

echo "✅ 音频已提取: audio.mp3"
echo ""

# Step 3: 语音转文字 (使用 Poe API + Gemini)
echo "🎙️ Step 3: 语音转文字..."
echo ""

# 检查 API Key
if [ -z "$POE_API_KEY" ]; then
    # 尝试从 openclaw.json 读取
    POE_API_KEY=$(python3 -c "
import json
try:
    with open('$HOME/.openclaw/openclaw.json') as f:
        d = json.load(f)
        print(d.get('models', {}).get('providers', {}).get('poe', {}).get('apiKey', ''))
except:
    print('')
" 2>/dev/null)
fi

if [ -z "$POE_API_KEY" ]; then
    echo "❌ 未找到 POE_API_KEY，请设置环境变量或在 ~/.openclaw/openclaw.json 中配置"
    exit 1
fi

# 分割音频为60秒的chunks
echo "📂 分割音频文件..."
mkdir -p chunks
ffmpeg -i audio.mp3 -f segment -segment_time 180 -c copy chunks/chunk_%03d.mp3 -y 2>/dev/null

# 获取chunk数量
CHUNK_COUNT=$(ls chunks/chunk_*.mp3 2>/dev/null | wc -l | tr -d ' ')
echo "✅ 分割为 $CHUNK_COUNT 个片段"
echo ""

# 转录每个chunk
mkdir -p transcripts
TRANSCRIPT_FILE="audio.txt"
> "$TRANSCRIPT_FILE"

for chunk_file in chunks/chunk_*.mp3; do
    if [ -f "$chunk_file" ]; then
        chunk_name=$(basename "$chunk_file" .mp3)
        echo "🔄 处理: $chunk_name..."
        
        # 使用 Poe API + Gemini 转录
        AUDIO_BASE64=$(base64 -i "$chunk_file")
        
        # 创建请求JSON
        cat > request.json << EOF
{
  "model": "gemini-3-flash",
  "messages": [{
    "role": "user",
    "content": [
      {"type": "text", "text": "请完整转录这段音频中的所有中文内容，不要遗漏任何内容。只输出转录的文字。"},
      {
        "type": "file",
        "file": {
          "filename": "audio.mp3",
          "file_data": "data:audio/mp3;base64,$AUDIO_BASE64"
        }
      }
    ]
  }]
}
EOF
        
        # 发送请求
        response=$(curl -sS https://api.poe.com/v1/chat/completions \
            -H "Authorization: Bearer $POE_API_KEY" \
            -H "Content-Type: application/json" \
            -d @request.json 2>&1)
        
        # 提取转录内容
        transcript=$(echo "$response" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d['choices'][0]['message']['content'])
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
" 2>/dev/null)
        
        if [ -n "$transcript" ]; then
            echo "$transcript" >> "$TRANSCRIPT_FILE"
            echo "✅ $chunk_name 完成"
        else
            echo "⚠️ $chunk_name 转录失败"
        fi
    fi
done

# 清理临时文件
rm -f request.json

if [ ! -s "$TRANSCRIPT_FILE" ]; then
    echo "❌ 转录失败"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 转录结果"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat "$TRANSCRIPT_FILE"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📁 工作目录: $WORK_DIR"
echo "   - video.mp4  (原始视频)"
echo "   - audio.mp3  (提取的音频)"
echo "   - audio.txt  (转录文本)"
echo "   - chunks/    (音频片段)"
