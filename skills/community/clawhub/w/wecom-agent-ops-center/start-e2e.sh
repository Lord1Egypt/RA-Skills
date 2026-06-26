#!/bin/bash
# 企微 Agent Connector - E2E 测试启动脚本
# 用法: bash start-e2e.sh
#
# 启动后：
#   1. 测试 Agent 运行在 :3000
#   2. Connector 连接企微 WebSocket
#   3. 状态面板 :9527
#   4. 在企微给机器人发消息测试！

set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
NODE="/Users/mikeliang/.workbuddy/binaries/node/versions/22.22.2/bin/node"

echo "🚀 启动企微 Agent Connector E2E 测试..."
echo ""

# 清理旧进程
pkill -f "node test-agent.js" 2>/dev/null || true
pkill -f "node connector.js" 2>/dev/null || true
sleep 1

# 启动测试 Agent
echo "📡 启动测试 Agent (port 3000)..."
NO_PROXY=localhost,127.0.0.1 $NODE "$DIR/test-agent.js" &
AGENT_PID=$!
sleep 1

# 验证 Agent
if NO_PROXY=localhost,127.0.0.1 curl -s -X POST http://localhost:3000/chat \
  -H 'Content-Type: application/json' \
  -d '{"msg_id":"health","from":{"user_id":"system"},"content":"health_check","msg_type":"text"}' > /dev/null 2>&1; then
  echo "  ✅ 测试 Agent 就绪"
else
  echo "  ❌ 测试 Agent 启动失败"
  kill $AGENT_PID 2>/dev/null
  exit 1
fi

# 启动 Connector
echo "🔌 启动 Connector..."
NO_PROXY=localhost,127.0.0.1 $NODE "$DIR/connector.js" &
CONNECTOR_PID=$!
sleep 3

# 验证 Connector
if NO_PROXY=localhost,127.0.0.1 curl -s http://127.0.0.1:9527/health > /dev/null 2>&1; then
  echo "  ✅ Connector 就绪"
else
  echo "  ⚠️  Connector 状态面板未响应（可能仍在连接企微）"
fi

echo ""
echo "============================================"
echo "  ✅ E2E 测试环境已启动！"
echo ""
echo "  🧪 测试 Agent: http://localhost:3000/chat"
echo "  📊 状态面板:   http://127.0.0.1:9527"
echo "  🩺 健康检查:   http://127.0.0.1:9527/health"
echo ""
echo "  📱 现在去企微给机器人发一条消息吧！"
echo "============================================"
echo ""
echo "PIDs: agent=$AGENT_PID connector=$CONNECTOR_PID"
echo "按 Ctrl+C 停止所有服务"

# 等待并清理
trap "echo ''; echo '🛑 停止服务...'; kill $AGENT_PID $CONNECTOR_PID 2>/dev/null; echo '👋 已停止'; exit 0" INT TERM

wait
