#!/bin/bash

# =============================================================================
# Whisper Transcriber - 测试脚本
# =============================================================================
# 用途：验证安装是否成功

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_AUDIO="/tmp/whisper-test-sample.wav"

echo "🎤 Whisper Transcriber 安装测试"
echo ""

# 1. 检查依赖
echo "1. 检查依赖..."
if command -v whisper-cli &> /dev/null; then
    echo "   ✓ whisper-cli 已安装"
else
    echo "   ✗ whisper-cli 未安装"
    exit 1
fi

if command -v ffmpeg &> /dev/null; then
    echo "   ✓ ffmpeg 已安装"
else
    echo "   ✗ ffmpeg 未安装"
    exit 1
fi
echo ""

# 2. 检查模型
echo "2. 检查模型..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODEL_DIR_SKILL="$SCRIPT_DIR/assets/models"
MODEL_DIR_USER="${WHISPER_MODEL_DIR_USER:-$SKILL_DIR/assets/models}"

# 优先检查技能目录
if [ -f "$MODEL_DIR_SKILL/ggml-base.bin" ]; then
    MODEL_DIR="$MODEL_DIR_SKILL"
    echo "   ✓ 使用技能目录模型：$MODEL_DIR_SKILL"
elif [ -d "$MODEL_DIR_USER" ]; then
    MODEL_DIR="$MODEL_DIR_USER"
    model_count=$(ls -1 "$MODEL_DIR_USER"/ggml-*.bin 2>/dev/null | wc -l)
    echo "   ✓ 使用用户目录模型：$MODEL_DIR_USER"
    echo "   ✓ 已安装模型数：$model_count"
else
    echo "   ✗ 模型目录不存在"
fi
echo ""

# 3. 创建测试音频
echo "3. 生成测试音频..."
if command -v ffmpeg &> /dev/null; then
    # 生成 3 秒静音测试音频
    ffmpeg -f lavfi -i anullsrc=r=16000:cl=mono -t 3 -y "$TEST_AUDIO" 2>/dev/null
    echo "   ✓ 测试音频已生成：$TEST_AUDIO"
else
    echo "   ✗ 无法生成测试音频"
fi
echo ""

# 4. 测试转写
echo "4. 测试转写..."
if [ -f "$TEST_AUDIO" ] && [ -f "$MODEL_DIR/ggml-base.bin" ]; then
    result=$(whisper-cli -m "$MODEL_DIR/ggml-base.bin" -l zh "$TEST_AUDIO" 2>&1 | grep -E "^\[|total time" || true)
    if [ -n "$result" ]; then
        echo "   ✓ 转写测试通过"
        echo "   输出示例："
        echo "$result" | head -3 | sed 's/^/     /'
    else
        echo "   ⚠ 转写完成但无输出（静音文件正常）"
    fi
else
    echo "   ⚠ 跳过转写测试（缺少模型或测试文件）"
fi
echo ""

# 5. 清理
rm -f "$TEST_AUDIO"
echo "5. 清理临时文件... ✓"
echo ""

# 6. 显示技能路径
echo "6. 技能信息:"
echo "   技能目录：$SCRIPT_DIR"
echo "   转写脚本：$SCRIPT_DIR/scripts/transcribe.sh"
echo "   安装脚本：$SCRIPT_DIR/scripts/install.sh"
echo ""

echo "═══════════════════════════════════════"
echo "✅ 安装测试完成！"
echo "═══════════════════════════════════════"
echo ""
echo "快速开始："
echo "  $SCRIPT_DIR/scripts/transcribe.sh your-audio.ogg"
echo ""
