#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

echo "🔧 安装 text-to-podcast..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要 Python 3"
    exit 1
fi

# 安装依赖
echo "📦 安装 Python 依赖..."
pip3 install openai python-dotenv --quiet

# 创建 .env 配置
if [ ! -f "$BASE_DIR/.env" ]; then
    echo "📝 创建 .env 配置文件..."
    cat > "$BASE_DIR/.env" << 'EOF'
OPENAI_API_KEY=your-api-key-here
EOF
    echo "⚠️  请编辑 $BASE_DIR/.env 文件，填入你的 OPENAI_API_KEY"
fi

# 创建输出目录
mkdir -p "$BASE_DIR/output"

# 设置权限
chmod +x "$SCRIPT_DIR/source/podcast_generator.py"

echo "✅ 安装完成！"
echo ""
echo "使用：text-to-podcast convert <file> --voice alloy"
echo "文档：cat $BASE_DIR/SKILL.md"