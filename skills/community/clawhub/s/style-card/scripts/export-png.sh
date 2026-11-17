#!/usr/bin/env bash
# export-png.sh — 把单文件 HTML 知识卡截图为 PNG
# 用法: bash export-png.sh input.html [output.png] [width] [height]
# 依赖: node + npx playwright（首次运行自动安装 chromium，约150MB）
set -euo pipefail

INPUT="${1:?用法: export-png.sh input.html [output.png] [width] [height]}"
OUTPUT="${2:-${INPUT%.html}.png}"
WIDTH="${3:-}"
HEIGHT="${4:-}"

[ -f "$INPUT" ] || { echo "✗ 找不到 $INPUT"; exit 1; }
command -v node >/dev/null || { echo "✗ 需要 Node.js"; exit 1; }

# 尺寸：未指定则从 html 的 CSS 变量 --card-width/--card-height 里读，兜底 1170x1560
if [ -z "$WIDTH" ] || [ -z "$HEIGHT" ]; then
  WIDTH=$(grep -Eo -- '--card-width:[[:space:]]*[0-9]+px' "$INPUT" | grep -Eo '[0-9]+' | head -1 || true)
  HEIGHT=$(grep -Eo -- '--card-height:[[:space:]]*[0-9]+px' "$INPUT" | grep -Eo '[0-9]+' | head -1 || true)
  WIDTH="${WIDTH:-1170}"; HEIGHT="${HEIGHT:-1560}"
fi

echo "▶ 画布 ${WIDTH}x${HEIGHT} → $OUTPUT"

# 确保 chromium 就位（首次较慢）
npx playwright --version >/dev/null 2>&1 || npm i -g playwright >/dev/null 2>&1
npx playwright screenshot \
  --viewport-size="${WIDTH},${HEIGHT}" \
  --wait-for-timeout=3000 \
  "$INPUT" "$OUTPUT"

[ -f "$OUTPUT" ] && echo "✓ 已导出 $OUTPUT ($(du -h "$OUTPUT" | cut -f1))" || { echo "✗ 导出失败"; exit 1; }
