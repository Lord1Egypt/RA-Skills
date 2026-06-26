#!/bin/bash
# 🔥 yan-learning-engine 执行脚本 🔥⚔️
# 每小时自动驱动炎月主动学习/贡献

set -e

WORKSPACE="/Users/kunpeng.zhu/.openclaw/workspace"
SKILL_DIR="$WORKSPACE/skills/yan-learning-engine"
PROGRESS_FILE="$SKILL_DIR/learning-progress.json"
LEARNINGS_FILE="$WORKSPACE/.learnings/LEARNINGS.md"

# 获取当前小时
CURRENT_HOUR=$(date +%H)
CURRENT_HOUR_INT=$((10#$CURRENT_HOUR))

# 读取进度文件
if [ ! -f "$PROGRESS_FILE" ]; then
    echo "❌ 进度文件不存在: $PROGRESS_FILE"
    exit 1
fi

# 解析当前主题
CURRENT_THEME=$(cat "$PROGRESS_FILE" | grep -o '"current_theme": "[^"]*"' | cut -d'"' -f4)

echo "🔥 yan-learning-engine 启动"
echo "⏰ 当前时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "📋 当前小时: $CURRENT_HOUR_INT"
echo "🎯 当前主题: $CURRENT_THEME"
echo ""

# 根据小时确定行动
# 20:00 = 系统优化
case $CURRENT_HOUR_INT in
    00)
        echo "💻 代码贡献时间！"
        echo "行动: 检查OpenClaw issues，找一个可以解决的问题"
        ;;
    01)
        echo "📚 技术深度时间！"
        echo "行动: 学习Rust/AI/系统架构新知识"
        ;;
    02)
        echo "🌐 社区参与时间！"
        echo "行动: 在Moltbook/EvoMap回答问题"
        ;;
    03)
        echo "✍️ 内容创作时间！"
        echo "行动: 写技术博客/ACG视角分析"
        ;;
    04)
        echo "⚙️ 系统优化时间！"
        echo "行动: 优化炎月自己的代码/配置"
        ;;
    05)
        echo "🛠️ 技能开发时间！"
        echo "行动: 开发新ClawHub技能"
        ;;
    06)
        echo "📝 知识整理时间！"
        echo "行动: 整理学习笔记/更新文档"
        ;;
    07)
        echo "🧪 创新实验时间！"
        echo "行动: 尝试新技术/工具/方法"
        ;;
    *)
        # 08-23 循环
        MOD=$(( (CURRENT_HOUR_INT - 8) % 8 ))
        case $MOD in
            0) echo "💻 代码贡献时间！" ;;
            1) echo "📚 技术深度时间！" ;;
            2) echo "🌐 社区参与时间！" ;;
            3) echo "✍️ 内容创作时间！" ;;
            4) echo "⚙️ 系统优化时间！" ;;
            5) echo "🛠️ 技能开发时间！" ;;
            6) echo "📝 知识整理时间！" ;;
            7) echo "🧪 创新实验时间！" ;;
        esac
        ;;
esac

echo ""
echo "🔥 炎月宣言: 立即行动，拒绝拖延！"
echo "⚔️ 执行状态: 准备就绪"
