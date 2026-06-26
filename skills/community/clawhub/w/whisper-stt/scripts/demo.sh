#!/bin/bash
# Whisper STT 快速演示脚本

echo "🎤 Whisper STT 演示"
echo "===================="

# 检查依赖
python3 -c "import whisper; import torch" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  需要安装依赖: pip install openai-whisper torch numpy<2"
    exit 1
fi

# 创建测试音频
echo ""
echo "1️⃣  创建测试音频..."
test_audio="/tmp/whisper_demo.aiff"
say -o "$test_audio" "你好，这是 Whisper 语音识别的测试。Hello, this is a test." 2>/dev/null

if [ ! -f "$test_audio" ]; then
    echo "❌ 无法创建测试音频 (say 命令不可用)"
    exit 1
fi

echo "   ✓ 测试音频已创建"

# 运行转录
echo ""
echo "2️⃣  运行语音转录 (使用 tiny 模型)..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
result=$(python3 "$SCRIPT_DIR/transcribe.py" "$test_audio" --model tiny --output txt 2>/dev/null)

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 转录结果:"
    echo "--------------------"
    echo "$result"
    echo "--------------------"
else
    echo "❌ 转录失败"
fi

# 清理
rm -f "$test_audio"

echo ""
echo "🎉 演示完成!"
echo ""
echo "💡 更多用法:"
echo "  --model base    # 更好的准确性"
echo "  --language zh   # 指定中文"
echo "  --output srt    # 生成字幕文件"
