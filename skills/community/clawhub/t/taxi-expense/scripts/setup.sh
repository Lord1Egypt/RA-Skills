#!/bin/bash
# setup.sh - 安装打车报销技能依赖
# Usage: bash scripts/setup.sh
#
# 训练数据来源优先级:
# 1. 本地已有 (/tmp/tessdata/)
# 2. GitHub 下载（可能需要代理）
# 3. 手动复制（如以上都失败）

set -e
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DEPS_DIR="$SKILL_DIR/deps"
TESSDATA_DIR="$SKILL_DIR/tessdata"

echo "📦 安装依赖到 $DEPS_DIR ..."
mkdir -p "$DEPS_DIR" "$TESSDATA_DIR"

cd "$DEPS_DIR"
npm init -y --silent 2>/dev/null
npm install tesseract.js@4 sharp exceljs --save --silent 2>&1 | tail -3

# 下载 Tesseract 训练数据
PROXY="${http_proxy:-$HTTP_PROXY}"
PROXY_FLAG=""
[ -n "$PROXY" ] && PROXY_FLAG="-x $PROXY"

for lang in chi_sim eng; do
  if [ -f "$TESSDATA_DIR/${lang}.traineddata" ]; then
    echo "✅ ${lang}.traineddata 已存在"
    continue
  fi

  # 尝试从本地已有目录复制
  if [ -f "/tmp/tessdata/${lang}.traineddata" ]; then
    echo "📋 复制 ${lang}.traineddata from /tmp/tessdata/"
    cp "/tmp/tessdata/${lang}.traineddata" "$TESSDATA_DIR/"
    continue
  fi

  # 尝试下载
  echo "📥 下载 ${lang}.traineddata ..."
  GZ_FILE="$TESSDATA_DIR/${lang}.traineddata.gz"
  curl -sL $PROXY_FLAG "https://github.com/tesseract-ocr/tessdata/raw/main/${lang}.traineddata.gz" -o "$GZ_FILE"

  # 检查是否为有效 gzip 文件
  if file "$GZ_FILE" | grep -q "gzip"; then
    gunzip -c "$GZ_FILE" > "$TESSDATA_DIR/${lang}.traineddata"
    rm -f "$GZ_FILE"
    echo "✅ ${lang}.traineddata 解压完成"
  else
    echo "❌ ${lang}.traineddata 下载失败（非 gzip 格式）"
    echo "   请手动复制: cp /your/path/${lang}.traineddata $TESSDATA_DIR/"
  fi
done

echo ""
echo "✅ 依赖安装完成"
echo "   - Tesseract.js v4, sharp, exceljs"
echo "   - 训练数据: $TESSDATA_DIR/"
ls -lh "$TESSDATA_DIR/" 2>/dev/null
