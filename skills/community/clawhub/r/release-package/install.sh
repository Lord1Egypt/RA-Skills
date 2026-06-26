#!/bin/bash
# 收纳管家安装脚本

set -e

echo "🚀 开始安装收纳管家技能..."
echo "=========================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要Python 3环境"
    exit 1
fi

# 检查必要的Python包
echo "检查Python依赖..."
python3 -c "import requests" 2>/dev/null || {
    echo "安装requests库..."
    pip3 install requests
}

# 创建可执行文件
echo "创建可执行文件..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
chmod +x "$SCRIPT_DIR/cli.py"
chmod +x "$SCRIPT_DIR/storage_manager.py"

# 创建符号链接
if [ -d "$HOME/.local/bin" ]; then
    echo "创建符号链接到 ~/.local/bin/storage-manager"
    ln -sf "$SCRIPT_DIR/cli.py" "$HOME/.local/bin/storage-manager"
    chmod +x "$HOME/.local/bin/storage-manager"
fi

# 创建配置文件示例
echo "创建配置文件示例..."
CONFIG_EXAMPLE="$SCRIPT_DIR/config.example.env"
cat > "$CONFIG_EXAMPLE" << EOF
# 飞书收纳管家配置
# 复制此文件为 .env 并填写实际值

# 飞书应用配置
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 多维表格配置
FEISHU_BITABLE_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_TABLE_ID=tblxxxxxxxxxxxxxxx

# 可选：日志级别
LOG_LEVEL=INFO
EOF

echo ""
echo "✅ 安装完成！"
echo ""
echo "📋 下一步："
echo "1. 配置飞书应用"
echo "2. 创建多维表格"
echo "3. 配置环境变量"
echo "4. 使用技能命令"
echo ""
echo "📚 详细文档请参考 SKILL.md"