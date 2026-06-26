#!/bin/bash
# senseaudio-voice 依赖安装脚本（HTTP 版本）

echo "🔧 安装 senseaudio-voice 依赖..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要安装 Python 3"
    exit 1
fi

# 安装 requests 库（唯一依赖）
echo "📦 安装 Python 依赖..."
pip3 install requests --quiet
echo "   ✅ requests 已安装"

# 检查音频播放器
echo "🔊 检查音频播放器..."
if command -v ffplay &> /dev/null; then
    echo "   ✅ ffplay 已安装"
elif command -v mpv &> /dev/null; then
    echo "   ✅ mpv 已安装"
elif command -v aplay &> /dev/null; then
    echo "   ✅ aplay 已安装"
else
    echo "   ⚠️  未找到音频播放器"
    echo "   建议安装：sudo apt-get install ffmpeg"
fi

# 验证 API Key
echo "🔑 检查 API Key 配置..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 -c "
import json
import os
import sys

api_key = os.environ.get('SENSE_API_KEY')
if api_key:
    print('   ✅ 环境变量 SENSE_API_KEY 已配置')
    sys.exit(0)

config_paths = [
    os.path.expanduser('~/.openclaw/openclaw.json'),
]

for path in config_paths:
    try:
        with open(path, 'r') as f:
            config = json.load(f)
            if config.get('env', {}).get('SENSE_API_KEY'):
                print(f'   ✅ openclaw.json 中已配置')
                sys.exit(0)
    except:
        pass

print('   ❌ 未找到 SENSE_API_KEY')
print('   请在 openclaw.json 的 env 中配置')
sys.exit(1)
"

echo ""
echo "✅ 安装完成！"
echo ""
echo "=== 使用方法 ==="
echo ""
echo "🔊 TTS 语音合成:"
echo "  python3 $SCRIPT_DIR/tts.py --play \"你好，这是测试\""
echo "  python3 $SCRIPT_DIR/tts.py --voice female_0001_a --play \"宝贝，该吃饭啦\""
echo ""
echo "🎤 ASR 语音识别:"
echo "  python3 $SCRIPT_DIR/asr.py audio.mp3"
echo "  python3 $SCRIPT_DIR/asr.py --verbose audio.mp3"
echo ""
echo "📁 音频文件存储:"
echo "  默认保存在：{workspace}/audio/YYYY-MM-DD/"
echo ""
echo "📋 查看帮助:"
echo "  python3 $SCRIPT_DIR/tts.py --help"
echo "  python3 $SCRIPT_DIR/asr.py --help"
echo ""
