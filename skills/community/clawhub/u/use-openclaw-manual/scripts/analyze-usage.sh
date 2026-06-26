#!/bin/bash
# analyze-usage.sh - 分析使用日志

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USAGE_LOG="$SCRIPT_DIR/../usage.log"

if [ ! -f "$USAGE_LOG" ]; then
  echo "📊 暂无使用记录"
  exit 0
fi

# 日志轮转：超过 1000 行保留最近 500 行
line_count=$(wc -l < "$USAGE_LOG")
if [ "$line_count" -gt 1000 ]; then
  tail -500 "$USAGE_LOG" > "$USAGE_LOG.tmp"
  mv "$USAGE_LOG.tmp" "$USAGE_LOG"
  echo "🔄 日志轮转完成（保留最近 500 行）"
  echo ""
fi

echo "═══════════════════════════════════════════"
echo "  技能使用统计"
echo "═══════════════════════════════════════════"
echo ""

# 总调用次数
total=$(wc -l < "$USAGE_LOG")
echo "📈 总调用次数：$total"
echo ""

# 按命令类型统计
echo "📋 按命令类型："
grep -o '"command":"[^"]*"' "$USAGE_LOG" | cut -d'"' -f4 | sort | uniq -c | sort -rn | while read count cmd; do
  printf "  %-15s %d\n" "$cmd:" "$count"
done
echo ""

# 成功率
success=$(grep -c '"result":"success"' "$USAGE_LOG" 2>/dev/null || echo 0)
if [ "$total" -gt 0 ]; then
  success_rate=$((success * 100 / total))
  echo "✅ 成功率：$success_rate%"
else
  echo "✅ 成功率：N/A"
fi
echo ""

# 热门搜索词
echo "🔥 热门搜索词："
grep '"command":"search"' "$USAGE_LOG" | grep -o '"args":"[^"]*"' | cut -d'"' -f4 | sort | uniq -c | sort -rn | head -5 | while read count word; do
  printf "  %-20s %d\n" "$word:" "$count"
done
echo ""

# 最近活动
echo "🕐 最近 5 次活动："
tail -5 "$USAGE_LOG" | while read line; do
  timestamp=$(echo "$line" | grep -o '"timestamp":"[^"]*"' | cut -d'"' -f4)
  command=$(echo "$line" | grep -o '"command":"[^"]*"' | cut -d'"' -f4)
  args=$(echo "$line" | grep -o '"args":"[^"]*"' | cut -d'"' -f4)
  result=$(echo "$line" | grep -o '"result":"[^"]*"' | cut -d'"' -f4)
  echo "  $timestamp - $command $args [$result]"
done
echo ""

# 平均耗时
avg_duration=$(grep -o '"duration_ms":[0-9]*' "$USAGE_LOG" | cut -d':' -f2 | awk '{sum+=$1; count++} END {if(count>0) print int(sum/count); else print 0}')
echo "⏱️  平均耗时：${avg_duration}ms"
echo ""
