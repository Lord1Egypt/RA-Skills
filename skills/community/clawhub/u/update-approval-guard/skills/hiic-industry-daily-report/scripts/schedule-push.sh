#!/bin/bash
# HIIC 产业日报定时推送脚本
# 用法: ./schedule-push.sh <industry> <keywords> <time>

set -e

INDUSTRY="${1:-石油}"
KEYWORDS="${2:-油价,石油,原油,OPEC,中石油,炼油}"
TIME="${3:-09:00}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_SCRIPT="$SCRIPT_DIR/generate-report-v7.3.mjs"
OUTPUT_DIR="$HOME/.openclaw/workspace/hiic-reports"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 解析时间
HOUR=$(echo "$TIME" | cut -d: -f1)
MINUTE=$(echo "$TIME" | cut -d: -f2)

# 生成cron表达式
CRON_EXPR="$MINUTE $HOUR * * *"

# 生成唯一ID
SUBSCRIPTION_ID="hiic-$(echo "$INDUSTRY" | md5sum | cut -c1-8)"

echo "📅 配置产业日报定时推送"
echo "================================"
echo ""
echo "📋 订阅信息:"
echo "   产业: $INDUSTRY"
echo "   关键词: $KEYWORDS"
echo "   推送时间: 每天 $TIME"
echo "   订阅ID: $SUBSCRIPTION_ID"
echo ""

# 创建推送脚本
PUSH_SCRIPT="$SCRIPT_DIR/push-$SUBSCRIPTION_ID.sh"

cat > "$PUSH_SCRIPT" << EOF
#!/bin/bash
# 自动生成的推送脚本 - $INDUSTRY

set -e

INDUSTRY="$INDUSTRY"
KEYWORDS="$KEYWORDS"
DATE=\$(date +%Y-%m-%d)
OUTPUT_FILE="$OUTPUT_DIR/\${INDUSTRY}-\${DATE}.md"

echo "📰 生成 $INDUSTRY 产业日报..."

# 生成日报
node "$REPORT_SCRIPT" \\
  --industry "\$INDUSTRY" \\
  --keywords "\$KEYWORDS" \\
  --maxResults 30 \\
  --output "\$OUTPUT_FILE" \\
  --saveToBitable true \\
  --verbose

if [ \$? -eq 0 ]; then
  echo "✅ 日报已生成: \$OUTPUT_FILE"
  
  # TODO: 推送到飞书/企业微信/Telegram
  # 示例：
  # curl -X POST "https://open.feishu.cn/open-apis/bot/v2/hook/xxx" \\
  #   -H "Content-Type: application/json" \\
  #   -d "{\\"msg_type\\":\\"text\\",\\"content\\":{\\"text\\":\\"$INDUSTRY 产业日报已生成\\"}}"
else
  echo "❌ 日报生成失败"
  exit 1
fi
EOF

chmod +x "$PUSH_SCRIPT"

echo "📝 推送脚本已创建: $PUSH_SCRIPT"
echo ""

# 添加到 crontab
echo "⏰ 添加定时任务..."
(crontab -l 2>/dev/null | grep -v "$SUBSCRIPTION_ID"; echo "$CRON_EXPR $PUSH_SCRIPT >> $OUTPUT_DIR/$SUBSCRIPTION_ID.log 2>&1 # $SUBSCRIPTION_ID") | crontab -

if [ $? -eq 0 ]; then
  echo "✅ 定时任务已添加到 crontab"
  echo ""
  echo "🔍 查看定时任务:"
  echo "   crontab -l"
  echo ""
  echo "📝 查看日志:"
  echo "   tail -f $OUTPUT_DIR/$SUBSCRIPTION_ID.log"
  echo ""
  echo "🗑️  取消订阅:"
  echo "   crontab -e  # 删除包含 $SUBSCRIPTION_ID 的行"
  echo ""
  echo "================================"
  echo "✅ 配置完成！"
else
  echo "❌ 添加定时任务失败"
  exit 1
fi
