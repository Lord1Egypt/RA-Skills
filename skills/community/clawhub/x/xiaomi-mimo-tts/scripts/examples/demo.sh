#!/bin/bash
# MiMo TTS 演示脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🎤 MiMo TTS 演示"
echo "========================"

# 检查 API Key
if [ -z "${XIAOMI_API_KEY}" ] && [ -z "${MIMO_API_KEY}" ]; then
    echo "错误: 请设置 XIAOMI_API_KEY 或 MIMO_API_KEY (优先 XIAOMI_API_KEY)"
    echo "  export XIAOMI_API_KEY=your-api-key  # 兼容: 也可设置 MIMO_API_KEY"
    exit 1
fi

echo "📁 目录结构:"
echo "  $PARENT_DIR/base/     - 基础版本"
echo "  $PARENT_DIR/smart/    - 智能版本"
echo "  $PARENT_DIR/utils/    - 工具脚本"
echo "  $PARENT_DIR/examples/ - 示例脚本"
echo ""

echo "🔧 可用命令:"
echo "  1. 基础版本: $PARENT_DIR/mimo-tts.sh"
echo "  2. 智能版本: $PARENT_DIR/mimo-tts-smart.sh"
echo ""

# 演示基础版本
echo "🎯 演示 1: 基础版本"
echo "-----------------------"
echo "执行: $PARENT_DIR/mimo-tts.sh \"你好，我是小米小爱同学\""
"$PARENT_DIR/mimo-tts.sh" "你好，我是小米小爱同学" 2>/dev/null && echo "✓ 基础版本测试完成"
echo ""

# 演示智能版本
echo "🎯 演示 2: 智能版本（自动情感检测）"
echo "-----------------------"
echo "执行: $PARENT_DIR/mimo-tts-smart.sh \"宝宝晚安，爱你哦～\""
"$PARENT_DIR/mimo-tts-smart.sh" "宝宝晚安，爱你哦～" 2>/dev/null && echo "✓ 智能版本测试完成"
echo ""

# 演示不同风格
echo "🎯 演示 3: 不同风格示例"
echo "-----------------------"
echo "1. 东北话:"
echo "   $PARENT_DIR/mimo-tts-smart.sh \"老铁，咋整啊？\""
echo ""
echo "2. 悄悄话:"
echo "   $PARENT_DIR/mimo-tts-smart.sh \"悄悄告诉你一个秘密...\""
echo ""
echo "3. 唱歌:"
echo "   $PARENT_DIR/mimo-tts-smart.sh \"唱一首歌给我听吧\""
echo ""

echo "📋 更多示例:"
echo "  # 指定输出文件"
echo "  $PARENT_DIR/mimo-tts.sh \"文本内容\" output.ogg"
echo ""
echo "  # 手动指定风格"
echo "  MIMO_STYLE=\"夹子音\" $PARENT_DIR/mimo-tts.sh \"主人～我来啦！\""
echo ""
echo "  # 使用 style 标签"
echo "  $PARENT_DIR/mimo-tts.sh \"<style>台湾腔</style>真的假的？好喔！\""
echo ""
echo "✅ 演示完成！"