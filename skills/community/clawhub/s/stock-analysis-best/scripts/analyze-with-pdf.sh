#!/bin/bash
# 股票分析 + PDF 报告生成一体化脚本
# 用法：./analyze-with-pdf.sh <股票代码> <公司名>

STOCK_CODE=$1
COMPANY_NAME=$2

if [ -z "$STOCK_CODE" ]; then
    echo "用法：$0 <股票代码> <公司名>"
    exit 1
fi

echo "=========================================="
echo "📈 股票投资分析 + PDF 报告生成"
echo "=========================================="
echo "标的：$COMPANY_NAME ($STOCK_CODE)"
echo ""

# 1. 执行完整分析
cd /app/skills/stock-analysis/scripts
./analyze.sh "$STOCK_CODE" "$COMPANY_NAME"

# 2. 生成可下载的 HTML/PDF 报告
./generate-pdf-report.sh "$STOCK_CODE" "$COMPANY_NAME"

echo "=========================================="
echo "✅ 分析完成！请使用上面的下载链接"
echo "=========================================="