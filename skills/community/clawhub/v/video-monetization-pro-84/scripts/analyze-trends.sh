#!/bin/bash
# analyze-trends.sh - 热点分析脚本
# 用途：搜索当日热点，生成 MV 主题建议

set -e

OUTPUT_DIR="${OUTPUT_DIR:-/Users/huang/.openclaw/workspace/knowledge/video/daily-mv-tasks}"
DATE=$(date +%Y-%m-%d)

echo "🔥 分析今日热点..."

# 搜索热点关键词
SEARCH_QUERIES=(
  "今日热点新闻 2026"
  "抖音热门话题"
  "B 站热门视频"
  "微博热搜榜"
  "爆款视频主题"
)

RESULTS_FILE="$OUTPUT_DIR/$DATE-trends-raw.md"
ANALYSIS_FILE="$OUTPUT_DIR/$DATE-mv-task.md"

mkdir -p "$OUTPUT_DIR"

# 使用 web_search 搜索热点（通过 OpenClaw 调用）
cat > "$RESULTS_FILE" << 'EOF'
# 热点分析原始数据

搜索时间：$(date '+%Y-%m-%d %H:%M:%S')

## 搜索查询
EOF

for query in "${SEARCH_QUERIES[@]}"; do
  echo "- $query" >> "$RESULTS_FILE"
done

echo "" >> "$RESULTS_FILE"
echo "## 结果" >> "$RESULTS_FILE"
echo "（通过 OpenClaw web_search 填充）" >> "$RESULTS_FILE"

# 生成 MV 主题建议
cat > "$ANALYSIS_FILE" << EOF
# 🎵 每日 MV 任务 - $DATE

## 热点摘要
（待填充：从 $RESULTS_FILE 提取）

## 推荐 MV 主题

### 主题 1：（待填充）
- **热点来源**：
- **爆款概率**：
- **预计播放**：
- **执行难度**：

### 主题 2：（待填充）

### 主题 3：（待填充）

## 今日推荐
⭐⭐⭐⭐⭐ （待填充）

## 法律审查提醒
- [ ] 检查敏感词
- [ ] 检查广告法合规
- [ ] 检查著作权风险

---
*生成时间：$(date '+%Y-%m-%d %H:%M:%S')*
*下一步：运行 generate-lyrics.sh*
EOF

echo "✅ 热点分析完成"
echo "📄 原始数据：$RESULTS_FILE"
echo "📄 MV 任务：$ANALYSIS_FILE"
echo ""
echo "下一步："
echo "1. 查看 $ANALYSIS_FILE 选择主题"
echo "2. 运行：./generate-lyrics.sh [主题]"
