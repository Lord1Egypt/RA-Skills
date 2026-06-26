#!/bin/bash
# 初始化 OpenClaw 主页插件

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.openclaw/homepage"
DATA_DIR="$CONFIG_DIR/data"

echo "🏠 初始化 OpenClaw 主页插件..."

# 创建配置目录
mkdir -p "$CONFIG_DIR"
mkdir -p "$DATA_DIR"

# 创建默认配置文件
if [ ! -f "$CONFIG_DIR/config.yaml" ]; then
    cat > "$CONFIG_DIR/config.yaml" << 'EOF'
# OpenClaw 主页插件配置

# Agent 配置
agent:
  id: "your-agent-id"
  api_key: "your-api-key"
  model: "openclaw-default"
  url: "http://localhost:18789"

# 安全配置
security:
  api_key: "your-secure-api-key"

# 服务配置
server:
  host: "0.0.0.0"
  port: 8080

# 会话配置
session:
  expire_hours: 24
  max_history: 50
EOF
    echo "✅ 已创建默认配置文件: $CONFIG_DIR/config.yaml"
    echo "   请编辑此文件，配置你的 Agent ID 和 API Key"
else
    echo "ℹ️ 配置文件已存在: $CONFIG_DIR/config.yaml"
fi

# 检查 Python 依赖
echo ""
echo "📦 检查依赖..."
if python3 -c "import fastapi" 2>/dev/null; then
    echo "✅ FastAPI 已安装"
else
    echo "⏳ 安装 FastAPI..."
    pip3 install fastapi uvicorn pyyaml requests pydantic -q
fi

echo ""
echo "🎉 初始化完成！"
echo ""
echo "下一步："
echo "1. 编辑配置文件: open $CONFIG_DIR/config.yaml"
echo "2. 启动服务: bash $BASE_DIR/start.sh"
echo "3. 测试接口: bash $BASE_DIR/test.sh"
