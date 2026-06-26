#!/bin/bash
# 视频合并脚本
# 用法: bash merge.sh <segments_dir> <output_path>
#
# 支持两种输入：
# 1. MP4分片（自动转为TS再合并）
# 2. TS分片（直接合并）
#
# 核心原理：
#   MP4分片有独立moov atom，直接拼接只有第一段可播
#   解决：MP4→TS（无容器头）→concat protocol→MP4（+faststart确保moov在文件头）

set -e

SEGMENTS_DIR="${1:?用法: merge.sh <segments_dir> <output_path>}"
OUTPUT_PATH="${2:-~/Desktop/video.mp4}"

echo "=== 视频合并器 ==="
echo "分片目录: $SEGMENTS_DIR"
echo "输出路径: $OUTPUT_PATH"

# 确保ffmpeg
if ! command -v ffmpeg &>/dev/null; then
  if [ -x "/tmp/ffmpeg" ]; then
    FFMPEG="/tmp/ffmpeg"
  else
    echo "[ffmpeg] 下载静态版本..."
    curl -sL 'https://evermeet.cx/ffmpeg/getrelease/ffmpeg/zip' -o /tmp/ffmpeg.zip
    cd /tmp && unzip -o ffmpeg.zip && chmod +x /tmp/ffmpeg
    FFMPEG="/tmp/ffmpeg"
  fi
else
  FFMPEG="ffmpeg"
fi

# 检查分片
mp4_count=$(ls "$SEGMENTS_DIR"/seg_*.mp4 2>/dev/null | wc -l | tr -d ' ')
ts_count=$(ls "$SEGMENTS_DIR"/seg_*.ts 2>/dev/null | wc -l | tr -d ' ')

if [ "$mp4_count" -gt 0 ]; then
  echo "找到 $mp4_count 个MP4分片"
  NEED_CONVERT=true
elif [ "$ts_count" -gt 0 ]; then
  echo "找到 $ts_count 个TS分片"
  NEED_CONVERT=false
else
  echo "❌ 未找到分片文件（seg_*.mp4 或 seg_*.ts）"
  exit 1
fi

# MP4 → TS 转换
if [ "$NEED_CONVERT" = true ]; then
  echo ""
  echo "=== MP4 → TS ==="
  converted=0
  for f in $(ls "$SEGMENTS_DIR"/seg_*.mp4 2>/dev/null | sort); do
    ts_file="${f%.mp4}.ts"
    if $FFMPEG -i "$f" -c copy -bsf:v h264_mp4toannexb -f mpegts "$ts_file" -y -loglevel warning 2>/dev/null; then
      converted=$((converted + 1))
      echo "  $(basename "$f") → $(basename "$ts_file") ✅"
    else
      echo "  $(basename "$f") → 转换失败 ❌"
    fi
  done
  echo "转换完成: $converted/$mp4_count"
fi

# concat protocol 合并
echo ""
echo "=== TS → MP4 ==="
ts_list=""
for f in $(ls "$SEGMENTS_DIR"/seg_*.ts 2>/dev/null | sort); do
  [ -n "$ts_list" ] && ts_list="${ts_list}|"
  ts_list="${ts_list}${f}"
done

if [ -z "$ts_list" ]; then
  echo "❌ 没有TS文件可合并"
  exit 1
fi

echo "合并 $(ls "$SEGMENTS_DIR"/seg_*.ts | wc -l | tr -d ' ') 个TS分片..."

$FFMPEG -i "concat:$ts_list" \
  -c copy \
  -bsf:a aac_adtstoasc \
  -movflags +faststart \
  "$OUTPUT_PATH" -y \
  -loglevel warning

# 验证
echo ""
echo "=== 验证 ==="

if [ ! -f "$OUTPUT_PATH" ]; then
  echo "❌ 合并失败，输出文件不存在"
  exit 1
fi

final_size=$(stat -f%z "$OUTPUT_PATH" 2>/dev/null || stat -c%s "$OUTPUT_PATH")
printf "文件大小: %.1fMB\n" "$(echo "$final_size" | awk '{print $1/1024/1024}')"

# 检查moov atom
echo ""
echo "Atom结构:"
python3 << 'PYEOF'
import struct, os, sys
p = os.environ.get('OUTPUT_PATH', '')
p = p.replace('~', os.path.expanduser('~'))
if not os.path.exists(p):
    print("  文件不存在")
    sys.exit(0)

with open(p, 'rb') as f:
    pos = 0
    atoms = []
    file_size = os.path.getsize(p)
    while pos < file_size:
        f.seek(pos)
        h = f.read(8)
        if len(h) < 8:
            break
        s = struct.unpack('>I', h[:4])[0]
        n = h[4:8].decode('ascii', errors='replace')
        if s == 0:
            s = file_size - pos
        elif s == 1:
            ext = f.read(8)
            s = struct.unpack('>Q', ext)[0]
        atoms.append(n)
        if len(atoms) <= 10:
            print(f"  {n} @ {pos/1024/1024:.2f}MB ({s/1024/1024:.2f}MB)")
        pos += s
        if s < 8:
            break

if 'moov' in atoms:
    print("\n✅ moov atom存在")
    if atoms[0] == 'ftyp' and atoms[1] == 'moov':
        print("✅ moov在文件开头（faststart兼容）")
else:
    print("\n❌ moov atom缺失！视频可能无法正常播放")

PYEOF

# 显示视频信息
echo ""
$FFMPEG -i "$OUTPUT_PATH" -hide_banner 2>&1 | grep -E "Duration|Stream" | head -5

echo ""
echo "✅ 合并完成: $OUTPUT_PATH"