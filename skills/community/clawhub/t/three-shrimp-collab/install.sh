#!/bin/bash

# 🦞 三只虾协同体系 - 一键安装脚本

set -e

echo "🦞 开始安装三只虾协同体系..."
echo ""

# 检查依赖
echo "📦 检查依赖..."
if ! command -v fswatch &> /dev/null; then
    echo "  ⚠️  fswatch 未安装，正在安装..."
    brew install fswatch
else
    echo "  ✅ fswatch 已安装"
fi

# 创建工作目录
echo ""
echo "📁 创建工作目录..."
WORKSPACE="/Users/zhangyang/.openclaw/workspace"
mkdir -p "$WORKSPACE/tasks"
mkdir -p "$WORKSPACE/logs"

# 初始化任务队列
if [ ! -f "$WORKSPACE/tasks/queue.md" ]; then
    echo "  📋 创建任务队列..."
    cat > "$WORKSPACE/tasks/queue.md" << 'EOF'
# 📋 三只虾任务队列

## 待处理
（空）

## 处理中
（空）

## 已完成
（空）
EOF
    echo "  ✅ 任务队列已创建"
else
    echo "  ✅ 任务队列已存在"
fi

# 配置 launchd 服务
echo ""
echo "🚀 配置 launchd 服务..."

LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

# 复制配置文件
cp "scripts/com.openclaw.heartbeat.plist" "$LAUNCH_AGENTS_DIR/"
cp "scripts/com.openclaw.fswatch.plist" "$LAUNCH_AGENTS_DIR/"
echo "  ✅ 配置文件已复制"

# 卸载旧配置（如存在）
if launchctl list | grep -q "com.openclaw.heartbeat"; then
    launchctl unload "$LAUNCH_AGENTS_DIR/com.openclaw.heartbeat.plist" 2>/dev/null || true
fi
if launchctl list | grep -q "com.openclaw.fswatch"; then
    launchctl unload "$LAUNCH_AGENTS_DIR/com.openclaw.fswatch.plist" 2>/dev/null || true
fi

# 加载新配置
launchctl load "$LAUNCH_AGENTS_DIR/com.openclaw.heartbeat.plist"
launchctl load "$LAUNCH_AGENTS_DIR/com.openclaw.fswatch.plist"
echo "  ✅ 服务已启动"

# 验证状态
echo ""
echo "📊 验证状态..."
if launchctl list | grep -q "com.openclaw.heartbeat"; then
    echo "  ✅ 心跳服务运行中"
else
    echo "  ❌ 心跳服务启动失败"
    exit 1
fi

if launchctl list | grep -q "com.openclaw.fswatch"; then
    echo "  ✅ 监控服务运行中"
else
    echo "  ❌ 监控服务启动失败"
    exit 1
fi

# 显示配置信息
echo ""
echo "================================"
echo "✅ 安装完成！"
echo ""
echo "📋 配置信息:"
echo "  工作目录：$WORKSPACE"
echo "  任务队列：$WORKSPACE/tasks/queue.md"
echo "  日志目录：$WORKSPACE/logs"
echo "  心跳时间：8:00-18:00（每小时一次）"
echo "  监控方式：fswatch 实时触发（<1 秒）"
echo ""
echo "🔧 常用命令:"
echo "  查看状态：launchctl list | grep openclaw"
echo "  查看心跳日志：tail -f $WORKSPACE/logs/heartbeat-*.log"
echo "  查看监控日志：tail -f $WORKSPACE/logs/fswatch-monitor.log"
echo "  手动测试：$WORKSPACE/scripts/heartbeat-check.sh"
echo ""
echo "🦞 三只虾协同体系已就绪！"
echo "================================"
