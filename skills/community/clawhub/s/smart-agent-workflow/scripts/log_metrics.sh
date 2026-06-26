#!/bin/bash
# 记录性能指标

if [ $# -lt 6 ]; then
    echo "用法: $0 <input_token> <output_token> <task_type> <used_memory> <correction_count> <duration_min>"
    exit 1
fi

METRICS_FILE="$(dirname "$0")/../logs/metrics.md"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")

INPUT_TOKEN=$1
OUTPUT_TOKEN=$2
TASK_TYPE=$3
USED_MEMORY=$4
CORRECTION_COUNT=$5
DURATION_MIN=$6
TOTAL_TOKEN=$((INPUT_TOKEN + OUTPUT_TOKEN))

# 创建文件（如果不存在）
if [ ! -f "$METRICS_FILE" ]; then
    echo "# 性能指标日志" > "$METRICS_FILE"
    echo "" >> "$METRICS_FILE"
fi

# 追加记录
cat >> "$METRICS_FILE" << EOF

## $TIMESTAMP

| 指标 | 值 |
|------|-----|
| Input Token | $INPUT_TOKEN |
| Output Token | $OUTPUT_TOKEN |
| Total Token | $TOTAL_TOKEN |
| 任务类型 | $TASK_TYPE |
| 是否使用 memory | $USED_MEMORY |
| 用户纠正次数 | $CORRECTION_COUNT |
| 完成时间 | $DURATION_MIN 分钟 |
EOF

echo "✅ 已记录性能数据: $TOTAL_TOKEN tokens, $DURATION_MIN min"
