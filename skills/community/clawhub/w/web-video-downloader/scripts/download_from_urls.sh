#!/bin/bash
# 从URL列表下载视频
# 用法: bash download_from_urls.sh <urls_json> <output_path>
#
# urls_json 格式（cdp_capture.js 输出）：
# {
#   "urls": [
#     { "url": "https://...", "headers": { "Referer": "...", ... } },
#     ...
#   ]
# }
#
# 也支持纯文本URL列表（每行一个URL）

set -e

URLS_FILE="${1:?用法: download_from_urls.sh <urls_json_or_txt> <output_path>}"
OUTPUT_PATH="${2:-~/Desktop/video.mp4}"
OUTPUT_DIR="/tmp/video_segments_$$"

# 确保ffmpeg
ensure_ffmpeg() {
  if command -v ffmpeg &>/dev/null; then
    FFMPEG="ffmpeg"
  elif [ -x "/tmp/ffmpeg" ]; then
    FFMPEG="/tmp/ffmpeg"
  else
    echo "[ffmpeg] 下载静态版本..."
    curl -sL 'https://evermeet.cx/ffmpeg/getrelease/ffmpeg/zip' -o /tmp/ffmpeg.zip
    cd /tmp && unzip -o ffmpeg.zip && chmod +x /tmp/ffmpeg
    FFMPEG="/tmp/ffmpeg"
  fi
}

echo "=========================================="
echo "  从URL列表下载视频"
echo "=========================================="
echo "URL文件: $URLS_FILE"
echo "输出路径: $OUTPUT_PATH"
echo ""

ensure_ffmpeg
mkdir -p "$OUTPUT_DIR"

# 检测文件类型
if python3 -c "import json; json.load(open('$URLS_FILE'))" 2>/dev/null; then
  # JSON格式（CDP捕获输出）
  echo "检测到JSON格式URL列表"
  
  urls=$(python3 -c "
import json
with open('$URLS_FILE') as f:
    data = json.load(f)
entries = data.get('urls', data) if isinstance(data, dict) else data
for i, e in enumerate(entries):
    url = e['url'] if isinstance(e, dict) else e
    print(url)
" 2>/dev/null)
  
  # 提取headers（用于需要Referer的下载）
  headers_json=$(python3 -c "
import json
with open('$URLS_FILE') as f:
    data = json.load(f)
entries = data.get('urls', data) if isinstance(data, dict) else data
for e in entries:
    if isinstance(e, dict) and e.get('headers'):
        h = e['headers']
        referer = h.get('Referer', h.get('referer', ''))
        if referer:
            print(referer)
            break
" 2>/dev/null)
  
  REFERER="${headers_json:-}"
else
  # 纯文本格式
  echo "检测到文本格式URL列表"
  urls=$(cat "$URLS_FILE" | grep -v '^#' | grep -v '^$')
  REFERER=""
fi

# 分类URL
mp4_urls=()
m3u8_urls=()
ts_urls=()
other_urls=()

while IFS= read -r url; do
  [ -z "$url" ] && continue
  case "$url" in
    *.mp4*) mp4_urls+=("$url") ;;
    *.m3u8*) m3u8_urls+=("$url") ;;
    *.ts*) ts_urls+=("$url") ;;
    *) other_urls+=("$url") ;;
  esac
done <<< "$urls"

echo "URL分类:"
echo "  MP4:  ${#mp4_urls[@]} 个"
echo "  M3U8: ${#m3u8_urls[@]} 个"
echo "  TS:   ${#ts_urls[@]} 个"
echo "  其他: ${#other_urls[@]} 个"
echo ""

# 策略1: 如果有M3U8，优先用ffmpeg下载（最可靠）
if [ ${#m3u8_urls[@]} -gt 0 ]; then
  echo "=== 策略: M3U8/HLS流 ==="
  m3u8_url="${m3u8_urls[0]}"
  echo "M3U8地址: $m3u8_url"
  
  if [ -n "$REFERER" ]; then
    $FFMPEG -i "$m3u8_url" -headers "Referer: $REFERER" -c copy -movflags +faststart "$OUTPUT_PATH" -y
  else
    $FFMPEG -i "$m3u8_url" -c copy -movflags +faststart "$OUTPUT_PATH" -y
  fi
  
  if [ -f "$OUTPUT_PATH" ]; then
    echo "✅ 下载完成: $OUTPUT_PATH"
    exit 0
  fi
fi

# 策略2: 如果只有1个MP4，直接下载
if [ ${#mp4_urls[@]} -eq 1 ]; then
  echo "=== 策略: 单个MP4直链 ==="
  curl -L -o "$OUTPUT_PATH" -H "Referer: ${REFERER}" "${mp4_urls[0]}"
  
  if [ -f "$OUTPUT_PATH" ] && [ "$(stat -f%z "$OUTPUT_PATH" 2>/dev/null || stat -c%s "$OUTPUT_PATH")" -gt 100000 ]; then
    echo "✅ 下载完成: $OUTPUT_PATH"
    exit 0
  fi
fi

# 策略3: 多个MP4分片，下载后合并
if [ ${#mp4_urls[@]} -gt 1 ]; then
  echo "=== 策略: 多MP4分片下载+合并 ==="
  
  # 下载所有分片
  idx=0
  for url in "${mp4_urls[@]}"; do
    seg_file="$OUTPUT_DIR/seg_$(printf '%02d' $idx).mp4"
    printf "  下载分片 %02d/%02d..." "$idx" "${#mp4_urls[@]}"
    
    if [ -n "$REFERER" ]; then
      curl -s -L --max-time 300 -H "Referer: $REFERER" -o "$seg_file" "$url"
    else
      curl -s -L --max-time 300 -o "$seg_file" "$url"
    fi
    
    size=$(stat -f%z "$seg_file" 2>/dev/null || stat -c%s "$seg_file" 2>/dev/null || echo 0)
    if [ "$size" -gt 100000 ]; then
      printf " ✅ %.1fMB\n" "$(echo "$size" | awk '{print $1/1024/1024}')"
    else
      echo " ❌"
    fi
    
    idx=$((idx + 1))
  done
  
  # MP4 → TS
  echo "[合并] MP4 → TS..."
  for f in "$OUTPUT_DIR"/seg_*.mp4; do
    [ -f "$f" ] || continue
    $FFMPEG -i "$f" -c copy -bsf:v h264_mp4toannexb -f mpegts "${f%.mp4}.ts" -y -loglevel warning 2>/dev/null
  done
  
  # concat protocol
  echo "[合并] TS → MP4..."
  ts_list=""
  for f in $(ls "$OUTPUT_DIR"/seg_*.ts 2>/dev/null | sort); do
    [ -n "$ts_list" ] && ts_list="${ts_list}|"
    ts_list="${ts_list}${f}"
  done
  
  $FFMPEG -i "concat:$ts_list" -c copy -bsf:a aac_adtstoasc -movflags +faststart "$OUTPUT_PATH" -y -loglevel warning
  
  if [ -f "$OUTPUT_PATH" ]; then
    echo "✅ 下载完成: $OUTPUT_PATH"
  fi
fi

# 策略4: TS分片直接合并
if [ ${#ts_urls[@]} -gt 0 ] && [ ! -f "$OUTPUT_PATH" ]; then
  echo "=== 策略: TS分片下载+合并 ==="
  
  idx=0
  for url in "${ts_urls[@]}"; do
    ts_file="$OUTPUT_DIR/seg_$(printf '%02d' $idx).ts"
    printf "  下载TS分片 %02d/%02d..." "$idx" "${#ts_urls[@]}"
    curl -s -L --max-time 120 -o "$ts_file" "$url"
    size=$(stat -f%z "$ts_file" 2>/dev/null || stat -c%s "$ts_file" 2>/dev/null || echo 0)
    [ "$size" -gt 1000 ] && echo " ✅" || echo " ❌"
    idx=$((idx + 1))
  done
  
  ts_list=""
  for f in $(ls "$OUTPUT_DIR"/seg_*.ts 2>/dev/null | sort); do
    [ -n "$ts_list" ] && ts_list="${ts_list}|"
    ts_list="${ts_list}${f}"
  done
  
  $FFMPEG -i "concat:$ts_list" -c copy -movflags +faststart "$OUTPUT_PATH" -y -loglevel warning
  
  if [ -f "$OUTPUT_PATH" ]; then
    echo "✅ 下载完成: $OUTPUT_PATH"
  fi
fi

# 最终验证
if [ -f "$OUTPUT_PATH" ]; then
  final_size=$(stat -f%z "$OUTPUT_PATH" 2>/dev/null || stat -c%s "$OUTPUT_PATH")
  printf "\n✅ 完成: %.1fMB\n" "$(echo "$final_size" | awk '{print $1/1024/1024}')"
  $FFMPEG -i "$OUTPUT_PATH" -hide_banner 2>&1 | grep -E "Duration|Stream" | head -5
else
  echo "❌ 下载失败"
  exit 1
fi

# 清理
rm -rf "$OUTPUT_DIR"
echo "临时文件已清理"