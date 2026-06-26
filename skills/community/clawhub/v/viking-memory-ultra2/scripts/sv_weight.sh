#!/bin/bash
# Viking Memory System - sv_weight
# 记忆权重计算 - Phase 2 优化版
#
# 权重公式: W = importance_factor × (1/(days+1)^0.3) × ln(access_count+1) × context_correlation
#
# Phase 2 改进点:
# 1. access_count 改为对数增长 ln(count+1)，防止无限膨胀
# 2. 新增 context_correlation 系数（0.5-1.5），基于上下文相关性调整
#
# 层级判定:
#   L0: weight >= 10 (完整细节)
#   L1: weight >= 5  (核心轮廓)
#   L2: weight >= 2  (关键词)
#   L3: weight >= 0.5(极简标签)
#   L4: weight < 0.5 (归档)
#
# 用法:
#   sv_weight <file>              # 只计算
#   sv_weight <file> --update     # 计算并更新
#   sv_weight <file> --update --context-correlation 0.8   # 指定上下文相关性

set -e

VIKING_HOME="${VIKING_HOME:-$HOME/.openclaw/viking}"
UPDATE=false
CONTEXT_CORRELATION=1.0  # 默认1.0（无调整）

# 解析参数
while [ $# -gt 0 ]; do
    case "$1" in
        --update) UPDATE=true; shift ;;
        --context-correlation)
            CONTEXT_CORRELATION="$2"
            shift 2 ;;
        *) [ -z "$FILE" ] && FILE="$1"; shift ;;
    esac
done

if [ -z "$FILE" ]; then
    echo "用法: sv_weight <记忆文件> [--update] [--context-correlation 0.8]"
    exit 1
fi

if [ ! -f "$FILE" ]; then
    echo "✗ 文件不存在: $FILE"
    exit 1
fi

# ============ 解析 frontmatter ============
parse_fm() {
    awk -v key="$2" -- '
        BEGIN { in_fm=0 }
        /^---$/ { in_fm=1; next }
        /^---$/ && in_fm { exit }
        in_fm && $0 ~ "^" key ": *" {
            sub("^" key ": *", "")
            gsub(/^[ \t]+|[ \t]+$/, "")
            print; exit
        }
    ' "$1" 2>/dev/null
}

IMPORTANCE=$(parse_fm "$FILE" "importance")
LAST_ACCESS=$(parse_fm "$FILE" "last_access")
ACCESS_COUNT=$(parse_fm "$FILE" "access_count")
CREATED=$(parse_fm "$FILE" "created")

[ -z "$IMPORTANCE" ] && IMPORTANCE="medium"
[ -z "$ACCESS_COUNT" ] && ACCESS_COUNT="1"
[ -z "$CREATED" ] && CREATED=$(date -Iseconds)

# 重要性因子
case "$IMPORTANCE" in
    high|important) FACTOR=3.0 ;;
    medium) FACTOR=1.5 ;;
    low) FACTOR=0.5 ;;
    *) FACTOR=1.0 ;;
esac

# 计算天数
if [ -n "$LAST_ACCESS" ]; then
    REF_TIME="$LAST_ACCESS"
else
    REF_TIME="$CREATED"
fi

REF_EPOCH=$(date -d "$REF_TIME" +%s 2>/dev/null) || REF_EPOCH=$(date +%s)
DAYS=$(( ($(date +%s) - REF_EPOCH) / 86400 ))

# ============ Phase 2 核心改进：对数增长 + 上下文相关性 ============
# 旧: W = factor × (1/(days+1)^0.3) × (access_count+1)
# 新: W = factor × (1/(days+1)^0.3) × ln(access_count+1) × context_correlation

ACCESS_NUM=$(echo "$ACCESS_COUNT" | awk '{print ($0+0)}')
LN_BOOST=$(awk "BEGIN {printf \"%.4f\", log($ACCESS_NUM + 1)}" 2>/dev/null || echo "1.0")
TIME_DECAY=$(awk "BEGIN {printf \"%.4f\", 1 / (($DAYS + 1) ** 0.3)}" 2>/dev/null || echo "1.0")
CONTEXT_CORR=$(echo "$CONTEXT_CORRELATION" | awk '{print ($0+0)}')

# 最终权重计算
WEIGHT=$(awk "BEGIN {printf \"%.2f\", $FACTOR * $TIME_DECAY * $LN_BOOST * $CONTEXT_CORR}" 2>/dev/null || echo "1.0")

# ============ 层级判定 ============
WEIGHT_NUM=$(echo "$WEIGHT" | awk '{print ($0+0)}')
if awk "BEGIN {exit !($WEIGHT_NUM >= 10)}"; then
    LAYER="L0"
elif awk "BEGIN {exit !($WEIGHT_NUM >= 5)}"; then
    LAYER="L1"
elif awk "BEGIN {exit !($WEIGHT_NUM >= 2)}"; then
    LAYER="L2"
elif awk "BEGIN {exit !($WEIGHT_NUM >= 0.5)}"; then
    LAYER="L3"
else
    LAYER="L4"
fi

echo "=== 权重计算 (Phase 2) ==="
echo "文件: $(basename "$FILE")"
echo "重要性: $IMPORTANCE (factor: $FACTOR)"
echo "距上次访问: ${DAYS} 天"
echo "访问次数: $ACCESS_COUNT"
echo "---"
echo "【Phase 2 改进】"
echo "  ln(access_count+1): $LN_BOOST (对数增长)"
echo "  上下文相关性: $CONTEXT_CORR × (0.5-1.5)"
echo "  时间衰减: $TIME_DECAY"
echo "---"
echo "权重: $WEIGHT"
echo "层级: $LAYER"

# ============ 更新文件 ============
if [ "$UPDATE" = true ]; then
    # 备份
    cp "$FILE" "${FILE}.weight.bak"

    # 更新 weight
    sed -i "s/^weight:.*/weight: $WEIGHT/" "$FILE" || true

    # 更新 context_correlation（如果存在）
    if grep -q "^context_correlation:" "$FILE" 2>/dev/null; then
        sed -i "s/^context_correlation:.*/context_correlation: $CONTEXT_CORR/" "$FILE" || true
    else
        # 在 last_access 后插入
        sed -i "/^last_access:/a context_correlation: $CONTEXT_CORR" "$FILE" || true
    fi

    # 更新 current_layer
    sed -i "s/^current_layer:.*/current_layer: $LAYER/" "$FILE" || true

    rm -f "${FILE}.weight.bak"
    echo "✓ 已更新文件元数据"
fi

exit 0
