#!/bin/bash
# 分段视频下载脚本
# 用法: bash download_segmented.sh <api_url_or_vid> <output_path> [--site sohu]
#
# 支持的站点：
#   sohu - 搜狐视频（默认）
#   其他站点可扩展
#
# 示例：
#   bash download_segmented.sh 660968419 ~/Desktop/video.mp4 --site sohu
#   bash download_segmented.sh "https://my.tv.sohu.com/play/videonew.do?vid=660968419" ~/Desktop/video.mp4

set -e

INPUT="${1:?用法: download_segmented.sh <api_url_or_vid> <output_path> [--site <site>]}"
OUTPUT_PATH="${2:-~/Desktop/video.mp4}"
SITE="sohu"

# 解析参数
shift 2 2>/dev/null || true
while [[ $# -gt 0 ]]; do
  case $1 in
    --site) SITE="$2"; shift 2 ;;
    *) shift ;;
  esac
done

OUTPUT_DIR="/tmp/video_segments_$$"
BATCH_SIZE=5  # 每N个分片刷新API token

# 确保ffmpeg可用
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

# ===== 搜狐视频下载 =====
download_sohu() {
  local vid="$1"
  
  # 构造API URL
  if [[ "$vid" == http* ]]; then
    API_URL="$vid"
  else
    API_URL="https://my.tv.sohu.com/play/videonew.do?vid=$vid&ver=1&ssl=1"
  fi
  
  echo "=== 搜狐视频下载 ==="
  echo "API: $API_URL"
  
  # 获取API数据
  get_api_data() {
    curl -s -L --max-time 15 \
      -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
      -H "Referer: https://yule.sohu.com/" \
      "$API_URL"
  }
  
  # 获取视频信息
  api_data=$(get_api_data)
  video_name=$(echo "$api_data" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['tvName'])" 2>/dev/null || echo "未知视频")
  total_segments=$(echo "$api_data" | python3 -c "import sys,json; print(len(json.load(sys.stdin)['data']['mp4PlayUrl']))" 2>/dev/null || echo "25")
  total_duration=$(echo "$api_data" | python3 -c "import sys,json; d=json.load(sys.stdin)['data']; print(sum(d['clipsDuration'])//1000)" 2>/dev/null || echo "?")
  
  echo "视频名称: $video_name"
  echo "分片数量: $total_segments"
  echo "总时长: ${total_duration}秒 ($((total_duration/60))分钟)"
  echo ""
  
  # 下载单个分片
  download_segment() {
    local index=$1
    local api_url=$2
    
    # 获取CDN真实地址
    cdn_url=$(curl -s -L --max-time 15 \
      -H "User-Agent: Mozilla/5.0" \
      -H "Referer: https://yule.sohu.com/" \
      "$api_url" 2>/dev/null | \
      python3 -c "import sys,json; d=json.load(sys.stdin); print(d['servers'][0]['url'] if d.get('servers') else '')" 2>/dev/null)
    
    if [ -z "$cdn_url" ]; then
      echo "  [$index] ❌ CDN获取失败"
      return 1
    fi
    
    # 下载分片
    curl -s -L --max-time 300 \
      -H "User-Agent: Mozilla/5.0" \
      -H "Referer: https://yule.sohu.com/" \
      "$cdn_url" -o "$OUTPUT_DIR/seg_$(printf '%02d' $index).mp4"
    
    local size
    size=$(stat -f%z "$OUTPUT_DIR/seg_$(printf '%02d' $index).mp4" 2>/dev/null || stat -c%s "$OUTPUT_DIR/seg_$(printf '%02d' $index).mp4" 2>/dev/null || echo 0)
    if [ "$size" -gt 100000 ]; then
      printf "  [%02d/%02d] ✅ %.1fMB\n" "$index" "$((total_segments-1))" "$(echo "$size" | awk '{print $1/1024/1024}')"
      return 0
    else
      echo "  [$index] ❌ 下载失败 (${size}B)"
      return 1
    fi
  }
  
  # 下载所有分片
  echo "=== 下载分片 ==="
  success=0
  failed=()
  
  for i in $(seq 0 $((total_segments-1))); do
    # 每BATCH_SIZE个刷新API
    if [ $((i % BATCH_SIZE)) -eq 0 ]; then
      api_data=$(get_api_data)
    fi
    
    api_url=$(echo "$api_data" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['mp4PlayUrl'][$i])")
    
    if download_segment "$i" "$api_url"; then
      success=$((success + 1))
    else
      failed+=($i)
    fi
  done
  
  echo ""
  echo "下载完成: $success/$total_segments"
  
  if [ ${#failed[@]} -gt 0 ]; then
    echo "失败分片: ${failed[*]}"
    # 重试失败的分片
    echo "重试失败分片..."
    for idx in "${failed[@]}"; do
      api_data=$(get_api_data)
      api_url=$(echo "$api_data" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['mp4PlayUrl'][$idx])")
      download_segment "$idx" "$api_url" && success=$((success+1))
    done
  fi
  
  if [ $success -lt $((total_segments - 5)) ]; then
    echo "❌ 分片下载不足，无法合并"
    exit 1
  fi
}

# ===== 合并视频 =====
merge_video() {
  echo ""
  echo "=== 合并视频 ==="
  
  # MP4 → TS
  echo "[1/3] MP4 → TS 转换..."
  for f in "$OUTPUT_DIR"/seg_*.mp4; do
    [ -f "$f" ] || continue
    ts_file="${f%.mp4}.ts"
    $FFMPEG -i "$f" -c copy -bsf:v h264_mp4toannexb -f mpegts "$ts_file" -y -loglevel warning 2>/dev/null
    echo "  $(basename "$f") → $(basename "$ts_file")"
  done
  
  # concat protocol 合并
  echo "[2/3] TS → MP4 合并..."
  local ts_list=""
  for f in $(ls "$OUTPUT_DIR"/seg_*.ts 2>/dev/null | sort); do
    [ -n "$ts_list" ] && ts_list="${ts_list}|"
    ts_list="${ts_list}${f}"
  done
  
  if [ -z "$ts_list" ]; then
    echo "❌ 没有TS文件可合并"
    exit 1
  fi
  
  $FFMPEG -i "concat:$ts_list" \
    -c copy -bsf:a aac_adtstoasc \
    -movflags +faststart \
    "$OUTPUT_PATH" -y -loglevel warning
  
  # 验证
  echo "[3/3] 验证..."
  if [ -f "$OUTPUT_PATH" ]; then
    local final_size
    final_size=$(stat -f%z "$OUTPUT_PATH" 2>/dev/null || stat -c%s "$OUTPUT_PATH")
    printf "\n✅ 完成: %.1fMB\n" "$(echo "$final_size" | awk '{print $1/1024/1024}')"
    echo "   文件: $OUTPUT_PATH"
    
    # 显示视频信息
    $FFMPEG -i "$OUTPUT_PATH" -hide_banner 2>&1 | grep -E "Duration|Stream" | head -5
  else
    echo "❌ 合并失败"
    exit 1
  fi
}

# ===== 主流程 =====
echo "=========================================="
echo "  通用网页视频下载器 - 分段模式"
echo "=========================================="
echo ""

ensure_ffmpeg
mkdir -p "$OUTPUT_DIR"

case "$SITE" in
  sohu)
    download_sohu "$INPUT"
    ;;
  *)
    echo "❌ 暂不支持站点: $SITE"
    echo "支持: sohu"
    echo ""
    echo "其他站点请使用CDP监听模式："
    echo "  node scripts/cdp_capture.js <cdp_ws_url>"
    echo "  bash scripts/download_from_urls.sh /tmp/captured_video_urls.json output.mp4"
    exit 1
    ;;
esac

merge_video

# 清理
echo ""
read -p "清理临时分片文件？[Y/n] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
  rm -rf "$OUTPUT_DIR"
  echo "✅ 临时文件已清理"
else
  echo "📁 临时文件保留在: $OUTPUT_DIR"
fi