#!/bin/bash
# Video to Doc 技能依赖安装脚本

echo "=== Video to Doc 依赖安装 ==="

# 检测操作系统
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    echo "不支持的操作系统: $OSTYPE"
    exit 1
fi

# 安装 ffmpeg
echo ""
echo "[1/3] 检查 ffmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✓ ffmpeg 已安装"
else
    echo "正在安装 ffmpeg..."
    if [ "$OS" == "linux" ]; then
        sudo apt update && sudo apt install -y ffmpeg
    elif [ "$OS" == "macos" ]; then
        brew install ffmpeg
    fi
fi

# 安装 Python 依赖
echo ""
echo "[2/3] 安装 Python 依赖..."
pip install python-docx pillow faster-whisper

# 检查安装结果
echo ""
echo "[3/3] 验证安装..."
python3 -c "import docx; print('✓ python-docx')" || echo "✗ python-docx 安装失败"
python3 -c "import PIL; print('✓ pillow')" || echo "✗ pillow 安装失败"
python3 -c "import faster_whisper; print('✓ faster-whisper')" || echo "✗ faster-whisper 安装失败"
python3 -c "import subprocess; subprocess.run(['ffmpeg', '-version'], capture_output=True); print('✓ ffmpeg')" || echo "✗ ffmpeg 安装失败"

echo ""
echo "=== 安装完成 ==="
echo ""
echo "使用方法："
echo "  python video_to_doc.py your_video.mp4"
echo ""
