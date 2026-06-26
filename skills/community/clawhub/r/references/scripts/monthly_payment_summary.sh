#!/bin/bash
# 每月付款明细汇总脚本
# 使用方法：./monthly_payment_summary.sh [月份 YYYY-MM]

set -e

WORKSPACE="/Users/mac/.openclaw/workspace"
PAYMENT_DIR="${1:-~/payments}"
SUMMARY_FILE="${PAYMENT_DIR}/summary_${1:-$(date +%Y-%m)}.md"
LOG_FILE="$HOME/monthly-payment-summary.log"

# 检查数据目录是否存在
if [ ! -d "$PAYMENT_DIR" ]; then
    echo "❌ 付款数据目录不存在: $PAYMENT_DIR"
    echo "请先创建并放入你的付款账单文件（支持 PDF、图片等格式）"
    exit 1
fi

# 提取月份参数
MONTH=$(echo "${1:-$(date +%Y-%m)}" | cut -d'-' -f1-2)
YEAR=$(echo "${1:-$(date +%Y-%m)}" | cut -d'-' -f3)

echo "📊 开始汇总 $YEAR-$MONTH 的付款明细..."

# 初始化汇总数据
TOTAL_AMOUNT=0
PAYMENT_COUNT=0
CATEGORIES=""

# 创建支付类别统计
declare -A CATEGORY_TOTALS
declare -A CATEGORY_COUNTS

# 遍历所有账单文件
for FILE in "$PAYMENT_DIR"/*.{pdf,png,jpg,jpeg,txt,csv,json} 2>/dev/null; do
    [ -f "$FILE" ] || continue
    
    echo "📄 处理文件: $(basename $FILE)"
    
    # 提取金额（根据文件格式）
    if [[ "$FILE" == *.csv ]]; then
        # CSV 格式：假设第一列是日期，第二列是金额
        AMOUNT=$(tail -n +2 "$FILE" | awk '{sum += $2} END {print sum}')
        CATEGORY=$(head -1 "$FILE" | grep -oE '类别 [^\s]*|Category.*' | sed 's/[()]//g')
    else
        # PDF/图片：需要 OCR 识别（需额外工具）
        AMOUNT="待识别"
        CATEGORY="其他"
    fi
    
    # 累加统计
    TOTAL_AMOUNT=$(echo "$TOTAL_AMOUNT + $AMOUNT" | bc 2>/dev/null || echo "N/A")
    PAYMENT_COUNT=$((PAYMENT_COUNT + 1))
    
    # 按类别统计（简化版）
    if [ -n "$CATEGORY" ]; then
        CATEGORY_TOTALS[$CATEGORY]=$(echo "${CATEGORY_TOTALS[$CATEGORY]:-0} + $AMOUNT" | bc 2>/dev/null || echo "${CATEGORY_TOTALS[$CATEGORY]}")
        CATEGORY_COUNTS[$CATEGORY]=$((${CATEGORY_COUNTS[$CATEGORY]:-0} + 1))
    fi
done

# 生成 Markdown 汇总文件
echo "✅ 生成汇总报告..."

cat > "$SUMMARY_FILE" << EOF
# 💰 ${YEAR}-${MONTH} 付款明细汇总

> 📅 生成时间：$(date '+%Y-%m-%d %H:%M:%S')

## 📊 总览

| 指标 | 数值 |
|------|------|
| **总金额** | \$${TOTAL_AMOUNT:-待计算} |
| **交易笔数** | ${PAYMENT_COUNT:-0} |

---

## 📁 分类统计

EOF

# 添加类别统计（如果有数据）
if [ ${#CATEGORY_TOTALS[@]} -gt 0 ]; then
    for CAT in "${!CATEGORY_TOTALS[@]}"; do
        cat >> "$SUMMARY_FILE" << EOF
### ${CAT} (\$${CATEGORY_TOTALS[$CAT]:-0})

- 笔数：${CATEGORY_COUNTS[$CAT]}
- 占比：$(echo "scale=1; ${CATEGORY_TOTALS[$CAT]} * 100 / ${TOTAL_AMOUNT:-1}" | bc 2>/dev/null || echo "N/A")%

EOF
    done
else
    cat >> "$SUMMARY_FILE" << EOF
> 📝 暂无分类数据，请检查账单文件格式。

EOF
fi

# 添加文件列表
cat >> "$SUMMARY_FILE" << EOF
---

## 📋 账单文件清单

| 序号 | 文件名 | 格式 | 处理状态 |
|------|--------|------|----------|
EOF

COUNTER=1
for FILE in "$PAYMENT_DIR"/*.{pdf,png,jpg,jpeg,txt,csv,json} 2>/dev/null; do
    [ -f "$FILE" ] || continue
    echo "| $COUNTER | \`$(basename $FILE)\` | ${FILE##*.} | ✅" >> "$SUMMARY_FILE"
    COUNTER=$((COUNTER + 1))
done

echo "✅ 汇总报告已生成：$SUMMARY_FILE"
echo ""
echo "💡 提示："
echo "   - 将账单文件放入目录：$PAYMENT_DIR"
echo "   - 运行命令重新汇总：./monthly_payment_summary.sh YYYY-MM"
echo "   - 首次使用前请先创建目录：mkdir -p $PAYMENT_DIR"

# 记录日志
{
    echo "$(date '+%Y-%m-%d %H:%M:%S') - 生成汇总: $SUMMARY_FILE"
    echo "总金额: \$${TOTAL_AMOUNT:-待计算}, 笔数: $PAYMENT_COUNT"
} >> "$LOG_FILE"
