#!/bin/bash
# 每周AI前沿动态生成脚本
# Usage: generate_weekly_report.sh [output_dir] [days] [--send]

set -e

SKILL_DIR="$HOME/.openclaw/skills/weekly-ai-news"
OUTPUT_DIR="${1:-$HOME/weekly-ai-news}"
DAYS="${2:-}"
SEND_MODE="${3:-}"

mkdir -p "$OUTPUT_DIR"

echo "=== 每周AI前沿动态生成 ==="
echo "输出目录: $OUTPUT_DIR"

# 步骤1: 抓取 RSS 数据
echo "[1/3] 正在抓取 RSS 源..."
if [ -n "$DAYS" ]; then
    echo "抓取天数: 过去 $DAYS 天"
    python3 "$SKILL_DIR/scripts/fetch_rss.py" --days "$DAYS" > "$OUTPUT_DIR/news.json"
else
    echo "抓取范围: 上周一至今"
    python3 "$SKILL_DIR/scripts/fetch_rss.py" > "$OUTPUT_DIR/news.json"
fi
NEWS_COUNT=$(python3 -c "import json; print(len(json.load(open('$OUTPUT_DIR/news.json'))))")
echo "      获取到 $NEWS_COUNT 条 AI 应用新闻"
echo ""

# 步骤2: 生成 HTML 简报
echo "[2/3] 正在生成旧报纸风格 HTML..."
python3 "$SKILL_DIR/scripts/generate_newspaper.py" \
    --input "$OUTPUT_DIR/news.json" \
    --output "$OUTPUT_DIR/weekly-ai-news.html"
echo ""

# 步骤3: 发送到飞书（如果指定了 --send）
if [ "$SEND_MODE" = "--send" ] || [ "$SEND_MODE" = "send" ]; then
    echo "[3/3] 正在发送到飞书..."
    MSG=$(python3 "$SKILL_DIR/scripts/format_feishu_msg.py" \
        --news-json "$OUTPUT_DIR/news.json" \
        --html-file "$OUTPUT_DIR/weekly-ai-news.html")
    
    # 使用 openclaw 命令发送消息
    # 注意：需要在 OpenClaw 环境中运行
    echo "$MSG" > "$OUTPUT_DIR/message.txt"
    echo "      消息已格式化，保存至 $OUTPUT_DIR/message.txt"
    echo ""
    echo "请使用以下命令发送："
    echo "  openclaw message send \"$MSG\""
fi

# 完成
echo "✅ 完成!"
echo ""
echo "生成文件:"
echo "  - $OUTPUT_DIR/news.json"
echo "  - $OUTPUT_DIR/weekly-ai-news.html"
echo ""
echo "请在浏览器中打开: file://$OUTPUT_DIR/weekly-ai-news.html"

# 如果指定了发送，显示提示
if [ "$SEND_MODE" = "--send" ] || [ "$SEND_MODE" = "send" ]; then
    echo ""
    echo "📬 消息已准备，请手动发送或使用 OpenClaw 消息功能"
fi
