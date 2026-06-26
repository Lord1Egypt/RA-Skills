#!/bin/bash
# 小红书封面图生成脚本（纯ImageMagick版本）
# 功能：使用ImageMagick的caption功能生成3:4封面图
# 自动选择美观的颜色组合，保持浅色和深色对比，固定字体大小80px
#
# 用法:
#   bash cover.sh "标题文字" [输出路径]
#
# 参数:
#   $1 - 标题文字（必填）
#   $2 - 输出路径（可选，默认 /tmp/xhs_cover.png）
#
# 最终封面尺寸: 1080x1440 (3:4)

set -e

TITLE="${1:-}"
OUTPUT="${2:-/tmp/xhs_cover.png}"

# 尺寸定义
COVER_W=1080
COVER_H=1440

# 固定字体大小
FONT_SIZE=96

# 临时文件
TMP_DIR=$(mktemp -d)

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

# ==================== 参数检查 ====================

if [ -z "$TITLE" ]; then
  echo "❌ 错误: 请提供标题文字"
  echo "用法: bash $0 \"标题文字\" [输出路径]"
  exit 1
fi

# 检查 ImageMagick
if ! command -v magick &> /dev/null && ! command -v convert &> /dev/null; then
  echo "❌ 错误: 未安装 ImageMagick，请先执行: apt install -y imagemagick"
  exit 1
fi

# 确定 ImageMagick 命令
if command -v magick &> /dev/null; then
  MAGICK="magick"
  IDENTIFY="magick identify"
else
  MAGICK="convert"
  IDENTIFY="identify"
fi

# ==================== 自动颜色选择 ====================

# 基于标题内容生成一个简单的哈希值来决定颜色组合
TITLE_HASH=$(echo -n "$TITLE" | md5sum | cut -c1-8)
HASH_NUM=$((0x$TITLE_HASH % 100))

# 定义美观的颜色组合库
# 格式: 背景颜色,文字颜色,组合名称
COLOR_COMBINATIONS=(
  "#FFFFFF,#000000,经典白黑"
  "#F8F9FA,#2C3E50,专业灰蓝"
  "#E3F2FD,#1565C0,清新蓝调"
  "#E8F5E9,#2E7D32,自然绿意"
  "#FCE4EC,#C2185B,温馨粉红"
  "#FFFDE7,#F57C00,活力橙黄"
  "#F3E5F5,#7B1FA2,优雅紫韵"
  "#FFF3E0,#EF6C00,温暖橙调"
  "#E0F2F1,#00695C,薄荷绿意"
  "#F5F0FF,#6A1B9A,梦幻紫罗兰"
  "#FFEBEE,#D32F2F,热情红调"
  "#FFF8E1,#FF8F00,阳光橙黄"
  "#EDE7F6,#512DA8,淡紫深紫"
  "#E1F5FE,#0277BD,天空蓝调"
  "#F1F8E9,#558B2F,春意盎然"
  "#FBE9E7,#D84315,珊瑚橙红"
  "#F5F5F5,#424242,高级灰黑"
  "#E8EAF6,#283593,宁静蓝紫"
  "#FFE5E5,#C62828,甜美红粉"
  "#F0F4C3,#827717,嫩黄橄榄"
)

# 选择颜色组合
COLOR_INDEX=$((HASH_NUM % ${#COLOR_COMBINATIONS[@]}))
SELECTED_COMBO="${COLOR_COMBINATIONS[$COLOR_INDEX]}"

# 解析颜色组合
BG_COLOR=$(echo "$SELECTED_COMBO" | cut -d',' -f1)
TEXT_COLOR=$(echo "$SELECTED_COMBO" | cut -d',' -f2)
COMBO_NAME=$(echo "$SELECTED_COMBO" | cut -d',' -f3)

echo "🎨 开始生成小红书封面图（纯ImageMagick版本）..."
echo "   标题: ${TITLE}"
echo "   输出: ${OUTPUT}"
echo "   颜色组合: ${COMBO_NAME}"
echo "   背景色: ${BG_COLOR}"
echo "   文字色: ${TEXT_COLOR}"
echo "   比例: 3:4 (1080x1440)"
echo "   字体大小: 固定 ${FONT_SIZE}px"
echo "   功能: 使用caption功能（自动换行）"
echo "   选择方式: 基于标题内容自动选择"
echo ""

# ==================== 生成封面图 ====================

echo "🔄 生成封面图..."

# 查找可用的中文字体（优先粗体）
FONT=""
for f in \
  "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc" \
  "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" \
  "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc" \
  "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc" \
  "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc" \
  "/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc" \
  "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf" \
  "/usr/share/fonts/noto/NotoSansSC-Bold.ttf" \
  "/usr/share/fonts/truetype/noto/NotoSansSC-Bold.ttf"; do
  if [ -f "$f" ]; then
    FONT="$f"
    break
  fi
done

# 如果没有找到中文字体，尝试用 fc-list 搜索
if [ -z "$FONT" ]; then
  FONT=$(fc-list :lang=zh -f "%{file}\n" 2>/dev/null | head -1)
fi

FONT_ARG=""
if [ -n "$FONT" ]; then
  FONT_ARG="-font $FONT"
  echo "   使用字体: $(basename "$FONT")"
else
  echo "   ⚠️ 未找到中文字体，使用系统默认字体（中文可能显示为方块）"
  echo "   建议安装: apt install -y fonts-noto-cjk"
fi

# 使用ImageMagick的caption功能生成封面
# caption会自动换行以适应宽度
echo "   使用caption功能生成（自动换行）..."
$MAGICK -background "$BG_COLOR" \
  -fill "$TEXT_COLOR" \
  $FONT_ARG \
  -pointsize "$FONT_SIZE" \
  -gravity center \
  -size "${COVER_W}x${COVER_H}" \
  caption:"$TITLE" \
  "$OUTPUT"

# 验证最终尺寸
FINAL_SIZE=$($IDENTIFY -format "%wx%h" "$OUTPUT" 2>/dev/null)
COLOR_DEPTH=$($IDENTIFY -format "%q-bit" "$OUTPUT" 2>/dev/null)

echo ""
echo "✅ 封面图生成完成！"
echo "   路径: ${OUTPUT}"
echo "   尺寸: ${FINAL_SIZE} (目标: ${COVER_W}x${COVER_H})"
echo "   颜色深度: ${COLOR_DEPTH}"
echo "   比例: 3:4"
echo "   字体大小: 固定 ${FONT_SIZE}px"
echo "   颜色组合: ${COMBO_NAME}"
echo "   背景色: ${BG_COLOR}"
echo "   文字色: ${TEXT_COLOR}"
echo ""
echo "📐 设计说明:"
echo "   ┌─────────────────────────────┐"
echo "   │                             │"
echo "   │     颜色主题: ${COMBO_NAME}        │"
echo "   │                             │"
echo "   │     背景颜色: ${BG_COLOR}        │"
echo "   │                             │"
echo "   │     文字颜色: ${TEXT_COLOR}        │"
echo "   │                             │"
echo "   │     「${TITLE:0:20}...」    │"
echo "   │     （自动换行显示）        │"
echo "   │                             │"
echo "   └─────────────────────────────┘"
echo "   总计: ${COVER_W}x${COVER_H} (3:4)"
echo ""
echo "💡 提示:"
echo "   • 此版本使用ImageMagick的caption功能"
echo "   • 固定字体大小80px，文字自动换行"
echo "   • 颜色组合基于标题内容自动选择"
echo "   • 共20种精心设计的颜色组合"
echo ""
echo "🎨 可用颜色组合:"
for combo in "${COLOR_COMBINATIONS[@]}"; do
  name=$(echo "$combo" | cut -d',' -f3)
  bg=$(echo "$combo" | cut -d',' -f1)
  text=$(echo "$combo" | cut -d',' -f2)
  echo "   • ${name}: ${bg} + ${text}"
done
