#!/bin/bash
# 生成性能周报

LOGS_DIR="$(dirname "$0")/../logs"
REPORTS_DIR="$(dirname "$0")/../reports"
METRICS_FILE="$LOGS_DIR/metrics.md"

mkdir -p "$REPORTS_DIR"

WEEK_END=$(date "+%Y-%m-%d")
REPORT_FILE="$REPORTS_DIR/weekly-$WEEK_END.md"

echo "🔍 生成性能报告..."

# 检查 metrics.md 是否存在
if [ ! -f "$METRICS_FILE" ]; then
    echo "❌ 未找到性能数据: $METRICS_FILE"
    exit 1
fi

# 生成报告
cat > "$REPORT_FILE" << 'EOF'
# 性能报告

## Token 消耗趋势

EOF

# 提取最近 7 天的 Token 数据
grep "Total Token" "$METRICS_FILE" | tail -20 >> "$REPORT_FILE"

echo "" >> "$REPORT_FILE"
echo "## 统计摘要" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 计算平均值
total_tokens=$(grep "Total Token" "$METRICS_FILE" | tail -20 | awk -F'|' '{sum+=$3} END {print sum/NR}')
echo "- 平均 Token 消耗: ${total_tokens:-N/A}" >> "$REPORT_FILE"

echo "" >> "$REPORT_FILE"
echo "✅ 报告已生成: $REPORT_FILE"
cat "$REPORT_FILE"
