#!/bin/bash
# 批量转换 Excel/Word 为 PDF
# 用法：./convert-to-pdf.sh file.xlsx [file2.docx ...]

if [ $# -eq 0 ]; then
    echo "用法：$0 <文件1> [文件2 ...]"
    echo "示例：$0 QT-20260314-001.xlsx"
    echo "      $0 *.xlsx *.docx"
    exit 1
fi

# 检查 LibreOffice 是否安装
if ! command -v soffice &> /dev/null; then
    echo "❌ LibreOffice 未安装"
    echo "请运行：brew install --cask libreoffice"
    exit 1
fi

# 输出目录（默认当前目录）
OUTPUT_DIR="${OUTPUT_DIR:-.}"

echo "📄 转换 PDF..."
echo "输出目录：$OUTPUT_DIR"
echo ""

# 转换每个文件
for file in "$@"; do
    if [ ! -f "$file" ]; then
        echo "⚠️  文件不存在：$file"
        continue
    fi
    
    echo "正在转换：$file"
    soffice --headless --convert-to pdf "$file" --outdir "$OUTPUT_DIR"
    
    if [ $? -eq 0 ]; then
        echo "✅ 成功：$(basename "$file" .${file##*.}).pdf"
    else
        echo "❌ 失败：$file"
    fi
    echo ""
done

echo "完成！"
