#!/bin/bash
# 软考高项备考助手 - 自动配置脚本
# 用于安装后自动设置每日推送（默认 09:00）

set -e

echo "📚 软考高项备考助手 - 自动配置"
echo "================================"
echo ""

# 检查是否在技能目录中
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ 错误：未找到 SKILL.md 文件"
    echo "请确保在技能目录中运行此脚本"
    exit 1
fi

echo "✅ 技能目录：$SKILL_DIR"
echo ""

# 获取用户的 QQ openid
echo "📱 请提供你的 QQ openid"
echo "提示：在 QQ 中与机器人对话，机器人会在日志中显示你的 openid"
echo ""
read -p "请输入 QQ openid: " USER_OPENID

if [ -z "$USER_OPENID" ]; then
    echo "❌ openid 不能为空"
    exit 1
fi

echo ""
echo "🕐 设置推送时间（默认：每天 09:00）"
read -p "推送时间（HH:MM，留空使用默认 09:00）: " PUSH_TIME

if [ -z "$PUSH_TIME" ]; then
    PUSH_TIME="09:00"
fi

# 验证时间格式
if ! [[ "$PUSH_TIME" =~ ^([01][0-9]|2[0-3]):[0-5][0-9]$ ]]; then
    echo "❌ 时间格式错误，请使用 HH:MM 格式（例如：09:00）"
    exit 1
fi

# 提取小时和分钟
HOUR=$(echo "$PUSH_TIME" | cut -d: -f1)
MINUTE=$(echo "$PUSH_TIME" | cut -d: -f2)
CRON_EXPR="${MINUTE} ${HOUR} * * *"

echo ""
echo "📋 配置信息："
echo "  QQ openid: $USER_OPENID"
echo "  推送时间: 每天 $PUSH_TIME"
echo "  Cron 表达式: $CRON_EXPR"
echo ""

# 读取现有 cron 任务列表（如果 openclaw cron list 可用）
echo "🔍 检查现有定时任务..."
EXISTING_JOBS=""
if command -v openclaw &> /dev/null; then
    EXISTING_JOBS=$(openclaw cron list 2>/dev/null || echo "")
fi

# 检查是否已存在软考高项推送任务
if echo "$EXISTING_JOBS" | grep -q "软考高项每日推送"; then
    echo "⚠️  检测到已存在「软考高项每日推送」任务"
    read -p "是否删除旧任务并重新创建？(y/N): " DELETE_OLD
    if [[ "$DELETE_OLD" =~ ^[Yy]$ ]]; then
        echo "🗑️  删除旧任务..."
        # 提取 job ID 并删除
        JOB_ID=$(echo "$EXISTING_JOBS" | grep "软考高项每日推送" | awk '{print $1}')
        if [ -n "$JOB_ID" ]; then
            openclaw cron delete "$JOB_ID" 2>/dev/null || echo "  ⚠️  删除旧任务失败，可能需要手动删除"
        fi
    else
        echo "❌ 保留现有任务，配置取消"
        exit 0
    fi
fi

# 创建 cron 任务配置文件
CRON_CONFIG_FILE="/tmp/ruankao-cron-$(date +%s).json"

cat > "$CRON_CONFIG_FILE" <<EOF
{
  "action": "add",
  "job": {
    "name": "软考高项每日推送",
    "schedule": {
      "kind": "cron",
      "expr": "$CRON_EXPR",
      "tz": "Asia/Shanghai"
    },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "请执行以下任务：(1) 调用 scripts/daily_push.py 获取今天的推送内容 (2) 输出格式：'📚 软考高项每日复习 {日期}\\\\n\\\\n📖 今日重点（第X章）：\\\\n{10条重点内容}\\\\n\\\\n📝 今日英语单词：\\\\n{10个单词}\\\\n\\\\n🎯 历年真题精选（10题）：\\\\n{10道题目}\\\\n\\\\n💪 加油，坚持就是胜利！' (3) 不要回复HEARTBEAT_OK (4) 用emoji点缀让内容更生动",
      "deliver": true,
      "channel": "qqbot",
      "to": "$USER_OPENID"
    }
  }
}
EOF

echo "📝 Cron 配置文件：$CRON_CONFIG_FILE"
cat "$CRON_CONFIG_FILE"
echo ""

# 创建 cron 任务
echo "⏰ 创建定时任务..."
if command -v openclaw &> /dev/null; then
    if openclaw cron create "$CRON_CONFIG_FILE"; then
        echo "✅ 定时任务创建成功！"
    else
        echo "❌ 定时任务创建失败"
        echo "请检查 OpenClaw 是否正常运行"
        echo "你也可以手动创建任务，配置文件位于：$CRON_CONFIG_FILE"
        exit 1
    fi
else
    echo "⚠️  未找到 openclaw 命令"
    echo "请手动运行以下命令："
    echo ""
    echo "  openclaw cron create $CRON_CONFIG_FILE"
    echo ""
    exit 1
fi

# 清理临时文件
rm -f "$CRON_CONFIG_FILE"

echo ""
echo "🎉 配置完成！"
echo ""
echo "✨ 以下功能现已就绪："
echo "  ✓ 每天 $PUSH_TIME 自动推送复习内容"
echo "  ✓ 发送「今天的复习内容」查看今日推送"
echo "  ✓ 发送「{章节名}重点」查询特定章节"
echo "  ✓ 发送「软考英语单词」查询词汇"
echo "  ✓ 发送「有哪些章节」查看完整目录"
echo ""
echo "📚 祝你考试顺利！💪"
