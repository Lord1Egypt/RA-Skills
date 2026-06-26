#!/bin/bash

# 🦞 三只虾心跳自动配置脚本
# 一键配置 macOS launchd 自动心跳

set -e

echo "🦞 开始配置三只虾自动心跳..."
echo ""

# 定义路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_FILE="$SCRIPT_DIR/com.openclaw.heartbeat.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

# 创建 LaunchAgents 目录（如不存在）
if [ ! -d "$LAUNCH_AGENTS_DIR" ]; then
    echo "📁 创建 LaunchAgents 目录..."
    mkdir -p "$LAUNCH_AGENTS_DIR"
fi

# 复制 plist 文件
echo "📋 复制配置文件..."
cp "$PLIST_FILE" "$LAUNCH_AGENTS_DIR/"
echo "  ✅ 已复制到 $LAUNCH_AGENTS_DIR/com.openclaw.heartbeat.plist"

# 卸载旧配置（如存在）
echo ""
echo "🔄 卸载旧配置（如存在）..."
if launchctl list | grep -q "com.openclaw.heartbeat"; then
    launchctl unload "$LAUNCH_AGENTS_DIR/com.openclaw.heartbeat.plist" 2>/dev/null || true
    echo "  ✅ 已卸载旧配置"
else
    echo "  ℹ️  无旧配置"
fi

# 加载新配置
echo ""
echo "🚀 加载新配置..."
launchctl load "$LAUNCH_AGENTS_DIR/com.openclaw.heartbeat.plist"
echo "  ✅ 已加载配置"

# 检查状态
echo ""
echo "📊 检查状态..."
if launchctl list | grep -q "com.openclaw.heartbeat"; then
    echo "  ✅ 心跳服务已启动！"
else
    echo "  ❌ 启动失败，请检查日志"
    exit 1
fi

# 显示配置信息
echo ""
echo "================================"
echo "✅ 配置完成！"
echo ""
echo "📋 配置信息:"
echo "  服务名称：com.openclaw.heartbeat"
echo "  工作时间：8:00-18:00（每小时一次）"
echo "  日志目录：/Users/zhangyang/.openclaw/logs/"
echo ""
echo "🔧 常用命令:"
echo "  查看状态：launchctl list | grep openclaw.heartbeat"
echo "  查看日志：tail -f /Users/zhangyang/.openclaw/logs/heartbeat-stdout.log"
echo "  卸载服务：launchctl unload ~/Library/LaunchAgents/com.openclaw.heartbeat.plist"
echo "  手动测试：$SCRIPT_DIR/heartbeat-check.sh"
echo ""
echo "🦞 三只虾心跳已就绪！"
echo "================================"
