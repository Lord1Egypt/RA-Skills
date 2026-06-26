#!/bin/bash
# MiMo TTS 智能版统一入口
# 自动分析文本情感和风格，生成语音
# 支持多种实现：NodeJS (优先) → Python → Shell

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEXT="$1"
OUTPUT="${2:-/tmp/mimo-tts-smart-$(date +%s).ogg}"

if [ -z "$TEXT" ]; then
    echo "用法: mimo-tts-smart.sh \"文本内容\" [输出文件]"
    echo ""
    echo "✨ 智能特性:"
    echo "  - 自动检测情感（开心、悲伤、紧张、愤怒、惊讶、温柔）"
    echo "  - 自动识别方言（东北话、四川话、台湾腔、粤语）"
    echo "  - 自动判断效果（悄悄话、夹子音、唱歌）"
    echo "  - 自动识别诗词格式"
    echo "  - 无需手动指定风格标签"
    echo ""
    echo "🎯 实现支持:"
    echo "  - NodeJS (优先): 最完善的智能分析"
    echo "  - Python: 备用方案"
    echo "  - Shell: 基础实现"
    echo ""
    echo "示例:"
    echo "  mimo-tts-smart.sh \"宝宝晚安，爱你哦～\""
    echo "  mimo-tts-smart.sh \"唱首歌给我听吧\""
    echo "  mimo-tts-smart.sh \"老铁，咋整啊？\" output.ogg"
    exit 1
fi

if [ -z "${XIAOMI_API_KEY}" ] && [ -z "${MIMO_API_KEY}" ]; then
    echo "错误: 请设置 XIAOMI_API_KEY 或 MIMO_API_KEY (优先 XIAOMI_API_KEY)"
    echo "  export XIAOMI_API_KEY=your-api-key  # 兼容: 也可设置 MIMO_API_KEY"
    echo "获取 API Key: https://platform.xiaomimimo.com/"
    exit 1
fi

# 检查可用的实现版本
echo "🔍 检查可用实现..."
USE_VERSION=""

# 优先使用 NodeJS 版本（功能最完善）
if command -v node &> /dev/null && [ -f "$SCRIPT_DIR/mimo_tts_smart.js" ]; then
    echo "  ✓ NodeJS 版本可用"
    USE_VERSION="nodejs"
# 其次使用 Python 版本
elif command -v python3 &> /dev/null && [ -f "$SCRIPT_DIR/mimo_tts_smart.py" ]; then
    echo "  ✓ Python 版本可用"
    USE_VERSION="python"
# 最后使用 Shell 版本（智能分析简化版）
elif [ -f "$SCRIPT_DIR/mimo_tts_smart.sh" ]; then
    echo "  ✓ Shell 版本可用"
    USE_VERSION="shell"
else
    echo "  ⚠️ 没有找到智能版本实现"
    echo "  将使用基础版本 + 手动风格检测"
    USE_VERSION="fallback"
fi

echo "🧠 智能分析文本中..."

case "$USE_VERSION" in
    "nodejs")
        echo "  🟢 使用 NodeJS 智能版"
        node "$SCRIPT_DIR/mimo_tts_smart.js" "$TEXT" "$OUTPUT"
        ;;
    "python")
        echo "  🟡 使用 Python 智能版"
        python3 "$SCRIPT_DIR/mimo_tts_smart.py" "$TEXT" "$OUTPUT"
        ;;
    "shell")
        echo "  🟠 使用 Shell 智能版"
        bash "$SCRIPT_DIR/mimo_tts_smart.sh" "$TEXT" "$OUTPUT"
        ;;
    "fallback")
        echo "  🔴 使用基础版本（需手动指定风格）"
        # 基础版本需要手动添加风格标签，这里简化处理
        bash "$SCRIPT_DIR/mimo-tts.sh" "<style>普通话</style>$TEXT" "$OUTPUT"
        ;;
esac

if [ $? -eq 0 ]; then
    echo "✅ 语音生成完成: $OUTPUT"
    echo "$OUTPUT"
else
    echo "❌ 语音生成失败"
    exit 1
fi