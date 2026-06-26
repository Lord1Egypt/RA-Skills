#!/bin/bash
# YouTube Transcriber - Auto Install Script

echo "🎯 YouTube Transcriber - Auto Install"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✅ Python: $(python3 --version)"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install pip3"
    exit 1
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Installation complete!"
    echo ""
    echo "Usage:"
    echo "  python3 transcribe.py <URL> [language]"
    echo ""
    echo "Example:"
    echo "  python3 transcribe.py 'https://youtube.com/watch?v=VIDEO_ID' zh"
else
    echo ""
    echo "❌ Installation failed. Please install manually:"
    echo "  pip3 install yt-dlp faster-whisper"
    exit 1
fi
