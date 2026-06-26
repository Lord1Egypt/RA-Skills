#!/bin/bash
# 小红书工具快速启动脚本（无需 MCP）

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 小红书自动发布工具 - 快速启动"
echo "📍 工具目录: $SCRIPT_DIR"
echo ""

# 检查必需组件
echo "🔍 检查环境..."

# 检查 python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi
echo "✅ Python3 已安装"

# 检查 OpenClaw
if ! command -v openclaw &> /dev/null; then
    echo "❌ OpenClaw 未安装"
    exit 1
fi
echo "✅ OpenClaw 已安装"

# 检查浏览器状态
echo "🔍 检查浏览器状态..."
browser_status=$(openclaw browser --browser-profile openclaw status 2>&1 || echo "stopped")

if echo "$browser_status" | grep -q "running"; then
    echo "✅ 浏览器已运行"
else
    echo "🚀 启动浏览器..."
    openclaw browser --browser-profile openclaw start
    sleep 3
    echo "✅ 浏览器启动完成"
fi

# 创建上传目录
mkdir -p /tmp/openclaw/uploads
echo "✅ 上传目录已准备"

# 检查登录状态
echo "🔍 检查小红书登录状态..."
python3 "$SCRIPT_DIR/scripts/login_keeper.py" --mode check 2>/dev/null && login_ok=true || login_ok=false

if [ "$login_ok" = true ]; then
    echo "✅ 小红书登录状态正常"
else
    echo "⚠️  小红书未登录，需要手动登录一次"
    echo "   请运行: browser --browser-profile openclaw navigate https://creator.xiaohongshu.com"
    echo "   然后扫码登录"
fi

echo ""
echo "🎯 工具使用方法:"
echo "1. 基础发布:"
echo "   python3 $SCRIPT_DIR/scripts/publish.py \\"
echo "     --title '你的标题' \\"
echo "     --content '你的内容' \\"
echo "     --image '/path/to/image.jpg'"
echo ""
echo "2. 登录保活设置:"
echo "   $SCRIPT_DIR/scripts/setup_keepalive.sh"
echo ""
echo "3. 生成封面:"
echo "   python3 $SCRIPT_DIR/scripts/cover_generator.py \\"
echo "     --title 'AI热点' --output '/tmp/openclaw/uploads/cover.jpg'"
echo ""
echo "4. AI日报示例:"
echo "   python3 $SCRIPT_DIR/examples/daily_news.py"
echo ""
echo "📚 详细文档: $SCRIPT_DIR/README.md"
echo "🔗 在线帮助: https://clawhub.com/xiaohongshu-publish-kit"

# 如果有参数，直接执行发布
if [ $# -gt 0 ]; then
    echo ""
    echo "🚀 执行发布命令..."
    python3 "$SCRIPT_DIR/scripts/publish.py" "$@"
fi