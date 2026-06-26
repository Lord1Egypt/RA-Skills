#!/bin/bash
# 测试 OpenClaw 主页插件接口

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.openclaw/homepage"

# 读取配置
if [ -f "$CONFIG_DIR/config.yaml" ]; then
    API_KEY=$(grep "^[[:space:]]*api_key:" "$CONFIG_DIR/config.yaml" | awk '{print $2}' || echo "")
    PORT=$(grep "^[[:space:]]*port:" "$CONFIG_DIR/config.yaml" | head -1 | awk '{print $2}' || echo "8080")
else
    PORT=8080
    API_KEY=""
fi

SESSION_ID="test-$(date +%s)"

echo "🧪 测试 OpenClaw 主页插件"
echo "   端口: $PORT"
echo "   Session: $SESSION_ID"
echo ""

# 健康检查
echo "1️⃣ 健康检查..."
curl -s "http://localhost:$PORT/homepage/health" | python3 -m json.tool 2>/dev/null || echo "   ❌ 失败 - 服务可能未启动"
echo ""

# 测试聊天接口
echo "2️⃣ 测试聊天..."
RESPONSE=$(curl -s -X POST "http://localhost:$PORT/homepage/chat" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $API_KEY" \
    -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"你好，请介绍一下自己\"}")

echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
echo ""

# 列出会话
echo "3️⃣ 列出会话..."
curl -s "http://localhost:$PORT/homepage/sessions" | python3 -m json.tool 2>/dev/null || echo "   失败"
