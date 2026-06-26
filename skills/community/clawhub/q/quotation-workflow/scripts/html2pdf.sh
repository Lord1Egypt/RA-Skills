#!/bin/bash
# HTML 转 PDF（使用 Chrome 无头模式）
# 用法：./html2pdf.sh <input.html> [output.pdf]

if [ $# -lt 1 ]; then
    echo "用法：$0 <input.html> [output.pdf]"
    echo "示例：$0 QT-001.html"
    echo "      $0 QT-001.html QT-001.pdf"
    exit 1
fi

INPUT="$1"
OUTPUT="${2:-${1%.html}.pdf}"

# 检查文件
if [ ! -f "$INPUT" ]; then
    echo "❌ 文件不存在：$INPUT"
    exit 1
fi

# 检查 Chrome
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ ! -x "$CHROME" ]; then
    echo "❌ 未找到 Google Chrome"
    echo "请安装：brew install --cask google-chrome"
    exit 1
fi

# 转 PDF
echo "📄 转换中：$INPUT → $OUTPUT"
"$CHROME" --headless --disable-gpu --print-to-pdf="$OUTPUT" "file://$(pwd)/$INPUT" 2>&1

if [ -f "$OUTPUT" ]; then
    echo "✅ 成功！"
    ls -lh "$OUTPUT"
else
    echo "❌ 失败"
    exit 1
fi
