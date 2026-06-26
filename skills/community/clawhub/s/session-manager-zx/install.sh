#!/bin/bash
# Session Manager 安装脚本

set -e

WORKSPACE="$HOME/.openclaw/workspace"
SKILL_DIR="$WORKSPACE/skills/session-manager"
CONFIG_DIR="$HOME/.openclaw/session-manager"
SESSIONS_DIR="$HOME/.openclaw/agents/main/sessions"

echo "🦞 Session Manager 安装"
echo "====================="

# 创建配置目录
mkdir -p "$CONFIG_DIR"

# 复制配置模板
if [ ! -f "$CONFIG_DIR/config.json" ]; then
    cp "$SKILL_DIR/templates/config.example.json" "$CONFIG_DIR/config.json"
    echo "✅ 配置文件已创建: $CONFIG_DIR/config.json"
else
    echo "⚠️  配置文件已存在，跳过创建"
fi

# 设置权限
chmod 600 "$CONFIG_DIR/config.json"

# 创建日志文件
touch "$CONFIG_DIR/cleanup.log"
chmod 600 "$CONFIG_DIR/cleanup.log"

echo "✅ 安装完成！"

# 询问是否配置定时任务
echo ""
read -p "是否配置每日自动清理任务？(y/N): " response
if [[ "$response" == "y" || "$response" == "Y" ]]; then
    echo "📅 配置定时任务..."
    
    # 检查是否已存在任务
    if openclaw cron list | grep -q "会话清理"; then
        echo "⚠️  定时任务已存在，跳过创建"
    else
        # 创建 cron 任务
        openclaw cron add \
            --name "会话清理" \
            --schedule "0 2 * * *" \
            --message "执行会话清理：保留最近 7 天会话，最少保留 5 个" \
            --sessionTarget main
        
        echo "✅ 定时任务已创建（每天凌晨 2:00）"
    fi
else
    echo "⏭️  跳过定时任务配置"
    echo "💡 手动配置命令："
    echo "   openclaw cron add --name \"会话清理\" --schedule \"0 2 * * *\" --message \"执行会话清理\""
fi

echo ""
echo "📋 使用方法："
echo "   cd $SKILL_DIR"
echo "   ./scripts/list-sessions.sh    # 查看会话"
echo "   ./scripts/cleanup-sessions.sh # 手动清理"
echo "   ./scripts/monitor-sessions.sh # 监控状态"

echo ""
echo "🎉 安装完成！"