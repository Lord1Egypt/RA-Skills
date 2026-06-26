#!/bin/bash
# Sequoia-X 安装脚本
set -e

INSTALL_DIR="${HOME}/sequoia-x"

echo "📦 开始安装 Sequoia-X V2 ..."

# 1. 克隆仓库
if [ -d "$INSTALL_DIR" ]; then
    echo "✅ 已存在，跳过 clone（删除 $INSTALL_DIR 可重装）"
else
    echo "⬇️  克隆仓库 ..."
    git clone https://github.com/sngyai/Sequoia-X.git "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# 2. 安装依赖
echo "📦 安装 Python 依赖 ..."
pip install akshare "pydantic-settings>=2.0" "rich>=13.0" "pandas>=2.0" "requests>=2.31" python-dotenv

# 3. 生成配置文件
if [ -f ".env" ]; then
    echo "⚠️  .env 已存在，跳过"
else
    echo "⚙️  生成 .env 配置文件 ..."
    cp .env.example .env
    echo ""
    echo "⚠️  请编辑 $INSTALL_DIR/.env 填入飞书 Webhook URL"
fi

echo ""
echo "✅ 安装完成！"
echo "   目录：$INSTALL_DIR"
echo "   配置：$INSTALL_DIR/.env"
echo "   运行：bash $INSTALL_DIR/../.openclaw/skills/sequoia-x/scripts/run.sh"
echo ""
echo "⚠️  首次运行前，请先编辑 $INSTALL_DIR/.env 填入飞书 Webhook URL"
