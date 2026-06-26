#!/bin/bash
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_env.sh"
# MiMo TTS 基础版本统一入口
# 支持多种实现：NodeJS (优先) → Python → Shell

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEXT="$1"
OUTPUT="${2:-/tmp/mimo-tts-$(date +%s).ogg}"

if [ -z "$TEXT" ]; then
    echo "用法: mimo-tts.sh \"文本内容\" [输出文件]"
    echo ""
    echo "📁 目录结构:"
    echo "  scripts/base/     - 基础版本实现"
    echo "  scripts/smart/    - 智能版本实现"
    echo "  scripts/utils/    - 工具脚本"
    echo "  scripts/examples/ - 示例脚本"
    echo ""
    echo "🔧 实现版本:"
    echo "  - Shell 版本: scripts/base/mimo-tts.sh"
    echo "  - NodeJS 版本: scripts/base/mimo_tts.js"
    echo "  - Python 版本: scripts/base/mimo_tts.py"
    echo ""
    echo "🤖 智能版本:"
    echo "  - scripts/mimo-tts-smart.sh - 自动分析情感的智能版"
    echo ""
    echo "示例:"
    echo "  mimo-tts.sh \"你好世界\""
    echo "  MIMO_STYLE=\"夹子音\" mimo-tts.sh \"主人～我来啦！\""
    echo "  mimo-tts.sh \"<style>悄悄话</style>这是秘密\" output.ogg"
    exit 1
fi

if [ -z "${XIAOMI_API_KEY}" ] && [ -z "${MIMO_API_KEY}" ]; then
    echo "错误: 请设置 XIAOMI_API_KEY 或 MIMO_API_KEY (优先 XIAOMI_API_KEY)"
    echo "  export XIAOMI_API_KEY=your-api-key  # 兼容: 也可设置 MIMO_API_KEY"
    echo "获取 API Key: https://platform.xiaomimimo.com/"
    exit 1
fi

echo "🔍 检查可用实现..."
USE_VERSION=""

# 优先使用 Shell 版本（默认）
if [ -f "$SCRIPT_DIR/base/mimo-tts.sh" ]; then
    echo "  ✓ Shell 版本可用"
    USE_VERSION="shell"
else
    echo "  ⚠️ 没有找到可用实现"
    echo "错误: 基础脚本缺失"
    exit 1
fi

echo "🎤 合成中..."

case "$USE_VERSION" in
    "shell")
        echo "  🟢 使用 Shell 版本"
        # 传递当前环境变量和参数给基础脚本
        env MIMO_STYLE="$MIMO_STYLE" bash "$SCRIPT_DIR/base/mimo-tts.sh" "$TEXT" "$OUTPUT"
        ;;
esac

if [ $? -eq 0 ]; then
    echo "✅ 语音生成完成: $OUTPUT"
    echo "$OUTPUT"
else
    echo "❌ 语音生成失败"
    exit 1
fi
