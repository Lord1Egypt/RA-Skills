#!/bin/bash
# MiniMax 媒体生成工具
# 用法: ./generate.sh [image|video|tts|music] [参数...]

API_KEY="sk-cp-T1RYgh5UDikLnm-KSp7O50eQTXBHjtlzGCEKciumMTO7wJwIL3gCB1DcHj1onVdqgw4C3MdUxthbhG1sRWSAPElJzMbiXDC_BydyutkrItnFnBqGEZeiohY"
BASE_URL="https://api.minimaxi.com"
OUTPUT_DIR="/Users/rocky/Desktop"

case "$1" in
  image)
    prompt="${2:-未来科技风格的大脑神经网络}"
    filename="${3:-output.jpg}"
    echo "生成图片: $prompt"
    url=$(curl -s -X POST "$BASE_URL/v1/image_generation" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"model\":\"image-01\",\"prompt\":\"$prompt\",\"extra_params\":{\"image_size\":\"16:9\"}}" \
      | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('image_urls',[''])[0])")
    if [ -n "$url" ] && [ "$url" != "" ]; then
      curl -s -L "$url" -o "$OUTPUT_DIR/$filename"
      echo "✅ 已保存: $OUTPUT_DIR/$filename"
    else
      echo "❌ 生成失败"
    fi
    ;;
  tts)
    text="${2:-欢迎使用语音合成}"
    voice="${3:-male-qn-qingse}"
    filename="${4:-output.mp3}"
    echo "生成语音: $text"
    curl -s -X POST "$BASE_URL/v1/t2a_v2" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"model\":\"speech-2.8-hd\",\"text\":\"$text\",\"stream\":false,\"voice_setting\":{\"voice_id\":\"$voice\"},\"audio_setting\":{\"format\":\"mp3\"}}" \
      > /tmp/tts_resp.json
    python3 << 'PYEOF'
import json
with open('/tmp/tts_resp.json') as f:
    d = json.load(f)
audio_hex = d.get('data',{}).get('audio','')
if audio_hex:
    with open('/Users/rocky/Desktop/output.mp3','wb') as f:
        f.write(bytes.fromhex(audio_hex))
    print("✅ 已保存: /Users/rocky/Desktop/output.mp3")
PYEOF
    ;;
  video)
    prompt="${2:-大脑神经元活动}"
    echo "生成视频: $prompt"
    task_id=$(curl -s -X POST "$BASE_URL/v1/video_generation" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"model\":\"MiniMax-Hailuo-2.3\",\"prompt\":\"$prompt\"}" \
      | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('task_id',''))")
    echo "task_id: $task_id"
    echo "等待生成完成..."
    for i in {1..30}; do
      sleep 5
      status=$(curl -s "$BASE_URL/v1/query/video_generation?task_id=$task_id" \
        -H "Authorization: Bearer $API_KEY" \
        | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status',''))")
      echo "状态: $status"
      if [ "$status" = "Success" ]; then
        file_id=$(curl -s "$BASE_URL/v1/query/video_generation?task_id=$task_id" \
          -H "Authorization: Bearer $API_KEY" \
          | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('file_id',''))")
        download_url=$(curl -s "$BASE_URL/v1/files/retrieve?file_id=$file_id" \
          -H "Authorization: Bearer $API_KEY" \
          | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('file',{}).get('download_url',''))")
        curl -s -L "$download_url" -o "$OUTPUT_DIR/video.mp4"
        echo "✅ 已保存: $OUTPUT_DIR/video.mp4"
        break
      fi
    done
    ;;
  music)
    prompt="${2:-欢快轻松的背景音乐}"
    lyrics="${3:-无歌词}"
    echo "生成音乐: $prompt"
    curl -s -X POST "$BASE_URL/v1/music_generation" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"model\":\"music-2.6\",\"prompt\":\"$prompt\",\"lyrics\":\"$lyrics\"}" \
      > /tmp/music_resp.json
    python3 << 'PYEOF'
import json
with open('/tmp/music_resp.json') as f:
    d = json.load(f)
audio_hex = d.get('data',{}).get('audio','')
if audio_hex:
    with open('/Users/rocky/Desktop/music.mp3','wb') as f:
        f.write(bytes.fromhex(audio_hex))
    print("✅ 已保存: /Users/rocky/Desktop/music.mp3")
PYEOF
    ;;
  *)
    echo "用法: $0 [image|tts|video|music] [参数...]"
    echo ""
    echo "示例:"
    echo "  $0 image \"未来科技风格的大脑\" output.jpg"
    echo "  $0 tts \"欢迎使用语音合成\" male-qn-qingse voice.mp3"
    echo "  $0 video \"大脑神经元活动\""
    echo "  $0 music \"欢快轻松\" \"歌词内容\""
    ;;
esac
