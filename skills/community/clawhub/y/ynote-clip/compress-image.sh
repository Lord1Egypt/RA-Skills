#!/usr/bin/env bash
set -euo pipefail
# ─────────────────────────────────────────────
# compress-image.sh — 图片压缩 + base64 编码
#
# 由 clip-note.sh 三阶段流水线的阶段 2 调用。
# 将 compressImage（原 clip-note.mjs 中的 JS 函数）移到 .sh 层，
# 使 .mjs 不再需要 import child_process，满足 ClawHub 安全扫描合规。
#
# 输入：manifest.json 路径（由阶段 1 的 --download-images 生成）
#   格式：[{ "index": 0, "path": "/tmp/.../raw_0.bin", "mimeType": "image/jpeg", "url": "...", "origSize": 12345 }, ...]
#
# 输出：更新 manifest.json，为每张图片添加：
#   base64Data — base64 编码（压缩后），skipped 时为空字符串
#   finalMime  — 最终 MIME 类型（可能因压缩变为 image/jpeg）
#   compressed — 是否经过压缩
#   skipped    — 是否因超过 512KB 而跳过
#   finalSize  — 最终文件大小（字节）
#
# macOS 使用内置 sips，Linux 使用 ImageMagick（convert/identify）。
# 工具不可用或压缩失败时，graceful 降级为原图。
# ─────────────────────────────────────────────

MANIFEST="${1:?用法: bash compress-image.sh <manifest.json>}"

MAX_FINAL_SIZE=524288   # 512KB
RESIZE_WIDTH=1920
COMPRESS_THRESHOLD=524288  # > 512KB → compress
IS_MAC=false
[[ "$(uname)" == "Darwin" ]] && IS_MAC=true

# 跨平台文件大小获取
file_size() {
  if $IS_MAC; then
    stat -f%z "$1" 2>/dev/null || echo 0
  else
    stat -c%s "$1" 2>/dev/null || echo 0
  fi
}

# ─────────────────────────────────────────────
# 单张图片压缩（1:1 翻译自 JS compressImage 函数）
# 参数：$1=inputPath $2=mimeType $3=tmpDir
# 输出到 stdout：JSON { finalPath, finalMime, compressed, skipped }
# ─────────────────────────────────────────────
compress_one() {
  local input="$1" mime="$2" tmpdir="$3"
  local final="$input" final_mime="$mime" compressed=false skipped=false

  # SVG → PNG
  if [[ "$mime" == "image/svg+xml" ]]; then
    local png_path="$tmpdir/svg2png.png"
    if $IS_MAC; then
      sips -s format png "$input" --out "$png_path" >/dev/null 2>&1 || true
    else
      convert "$input" "$png_path" 2>/dev/null || true
    fi
    if [[ -f "$png_path" ]] && [[ $(file_size "$png_path") -gt 0 ]]; then
      final="$png_path"; final_mime="image/png"; compressed=true
    fi
    # SVG 不做后续压缩，直接输出
    local sz; sz=$(file_size "$final")
    [[ "$sz" -gt "$MAX_FINAL_SIZE" ]] && skipped=true
    printf '{"finalPath":"%s","finalMime":"%s","compressed":%s,"skipped":%s,"finalSize":%s}' \
      "$final" "$final_mime" "$compressed" "$skipped" "$sz"
    return
  fi

  # 非 GIF 且已在阈值内 → 直接返回
  local input_size; input_size=$(file_size "$input")
  if [[ "$mime" != "image/gif" ]] && [[ "$input_size" -le "$COMPRESS_THRESHOLD" ]]; then
    printf '{"finalPath":"%s","finalMime":"%s","compressed":false,"skipped":false,"finalSize":%s}' \
      "$input" "$mime" "$input_size"
    return
  fi

  # 主压缩流程（整体 try：任何失败都降级为原图）
  (
    if $IS_MAC; then
      # ── macOS: sips ──

      # GIF → 静态 JPEG（sips 自动取第一帧）
      if [[ "$mime" == "image/gif" ]]; then
        local jpg_path="$tmpdir/gif2jpg.jpg"
        sips -s format jpeg -s formatOptions 80 "$input" --out "$jpg_path" >/dev/null 2>&1
        if [[ -f "$jpg_path" ]] && [[ $(file_size "$jpg_path") -gt 0 ]]; then
          final="$jpg_path"; final_mime="image/jpeg"; compressed=true
        fi
      fi

      # 查询宽度
      local width=0
      local sips_out
      sips_out=$(sips -g pixelWidth "$final" 2>/dev/null) || true
      width=$(echo "$sips_out" | grep -o 'pixelWidth: *[0-9]*' | grep -o '[0-9]*' || echo 0)

      # 宽度 > 1920 → 缩放
      if [[ "$width" -gt "$RESIZE_WIDTH" ]]; then
        sips --resampleWidth "$RESIZE_WIDTH" "$final" --out "$final" >/dev/null 2>&1
        compressed=true
      fi

      # 渐进式质量降低：80 → 60 → 40，直到 ≤ 512KB
      for quality in 80 60 40; do
        [[ $(file_size "$final") -le "$MAX_FINAL_SIZE" ]] && break
        local jpg_path="$tmpdir/q${quality}.jpg"
        sips -s format jpeg -s formatOptions "$quality" "$final" --out "$jpg_path" >/dev/null 2>&1
        if [[ -f "$jpg_path" ]] && [[ $(file_size "$jpg_path") -gt 0 ]]; then
          final="$jpg_path"; final_mime="image/jpeg"; compressed=true
        fi
      done

    else
      # ── Linux: ImageMagick ──

      # GIF → 静态 JPEG（取第一帧 [0]）
      if [[ "$mime" == "image/gif" ]]; then
        local jpg_path="$tmpdir/gif2jpg.jpg"
        convert "${input}[0]" -quality 80 "$jpg_path" 2>/dev/null
        if [[ -f "$jpg_path" ]] && [[ $(file_size "$jpg_path") -gt 0 ]]; then
          final="$jpg_path"; final_mime="image/jpeg"; compressed=true
        fi
      fi

      # 查询宽度
      local width=0
      width=$(identify -format '%w' "$final" 2>/dev/null | tr -d ' ' || echo 0)

      # 宽度 > 1920 → 缩放
      if [[ "$width" -gt "$RESIZE_WIDTH" ]]; then
        convert "$final" -resize "${RESIZE_WIDTH}x" "$final" 2>/dev/null
        compressed=true
      fi

      # 渐进式质量降低
      for quality in 80 60 40; do
        [[ $(file_size "$final") -le "$MAX_FINAL_SIZE" ]] && break
        local jpg_path="$tmpdir/q${quality}.jpg"
        convert "$final" -quality "$quality" "$jpg_path" 2>/dev/null
        if [[ -f "$jpg_path" ]] && [[ $(file_size "$jpg_path") -gt 0 ]]; then
          final="$jpg_path"; final_mime="image/jpeg"; compressed=true
        fi
      done
    fi

    local sz; sz=$(file_size "$final")
    [[ "$sz" -gt "$MAX_FINAL_SIZE" ]] && skipped=true
    printf '{"finalPath":"%s","finalMime":"%s","compressed":%s,"skipped":%s,"finalSize":%s}' \
      "$final" "$final_mime" "$compressed" "$skipped" "$sz"
  ) 2>/dev/null || {
    # 工具不可用或压缩失败，使用原图
    local sz; sz=$(file_size "$input")
    local sk=false; [[ "$sz" -gt "$MAX_FINAL_SIZE" ]] && sk=true
    printf '{"finalPath":"%s","finalMime":"%s","compressed":false,"skipped":%s,"finalSize":%s}' \
      "$input" "$mime" "$sk" "$sz"
  }
}

# ─────────────────────────────────────────────
# 主流程：遍历 manifest，逐张压缩 + base64
# ─────────────────────────────────────────────

MANIFEST_DIR="$(cd "$(dirname "$MANIFEST")" && pwd)"
MANIFEST_BASE="$(basename "$MANIFEST")"
MANIFEST_ABS="$MANIFEST_DIR/$MANIFEST_BASE"

# 读取 manifest 条目数
COUNT=$(jq 'length' "$MANIFEST_ABS")

if [[ "$COUNT" -eq 0 ]]; then
  exit 0
fi

# 构建结果数组
RESULTS="[]"

for (( i=0; i<COUNT; i++ )); do
  # 从 manifest 读取当前图片信息
  ENTRY=$(jq ".[$i]" "$MANIFEST_ABS")
  IMG_PATH=$(echo "$ENTRY" | jq -r '.path')
  IMG_MIME=$(echo "$ENTRY" | jq -r '.mimeType')
  IMG_INDEX=$(echo "$ENTRY" | jq -r '.index')

  # 为每张图片创建独立 tmpdir（避免 sips 文件冲突）
  IMG_TMP="$MANIFEST_DIR/img_${IMG_INDEX}"
  mkdir -p "$IMG_TMP"

  # 压缩
  COMPRESS_RESULT=$(compress_one "$IMG_PATH" "$IMG_MIME" "$IMG_TMP")

  # 解析压缩结果
  FINAL_PATH=$(echo "$COMPRESS_RESULT" | jq -r '.finalPath')
  FINAL_MIME=$(echo "$COMPRESS_RESULT" | jq -r '.finalMime')
  COMPRESSED=$(echo "$COMPRESS_RESULT" | jq -r '.compressed')
  SKIPPED=$(echo "$COMPRESS_RESULT" | jq -r '.skipped')
  FINAL_SIZE=$(echo "$COMPRESS_RESULT" | jq -r '.finalSize')

  # base64 编码（skipped 时为空）
  B64=""
  if [[ "$SKIPPED" == "false" ]]; then
    B64=$(base64 < "$FINAL_PATH" | tr -d '\n')
  fi

  # 将结果合入 manifest 条目
  UPDATED=$(echo "$ENTRY" | jq \
    --arg b64 "$B64" \
    --arg fm "$FINAL_MIME" \
    --argjson compressed "$COMPRESSED" \
    --argjson skipped "$SKIPPED" \
    --argjson finalSize "$FINAL_SIZE" \
    '. + {base64Data: $b64, finalMime: $fm, compressed: $compressed, skipped: $skipped, finalSize: $finalSize}')

  RESULTS=$(echo "$RESULTS" | jq ". + [$UPDATED]")
done

# 写回 manifest
echo "$RESULTS" | jq '.' > "$MANIFEST_ABS"
