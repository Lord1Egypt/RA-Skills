#!/bin/bash
# Quiz Maker 启动脚本
# 用法: ./start.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
ENV_FILE="$SCRIPT_DIR/.env"
mkdir -p "$LOG_DIR"

echo "🚀 启动 Quiz Maker..."
echo "📁 工作目录: $SCRIPT_DIR"

# 加载环境变量（如果有 .env 文件）
if [ -f "$ENV_FILE" ]; then
  echo "📋 加载环境变量: $ENV_FILE"
  set -a
  source "$ENV_FILE"
  set +a
else
  echo "⚠️  未找到 .env 文件，请创建 $ENV_FILE"
fi

# 检查必要环境变量
if [ -z "$ARK_API_KEY" ]; then
  echo "❌ 错误: ARK_API_KEY 未设置"
  echo "   请在 $ENV_FILE 中设置 ARK_API_KEY"
  exit 1
fi

echo "✅ 环境变量检查通过"

# 启动后端服务
if pgrep -f "node server.js" > /dev/null; then
  echo "✅ 后端服务已在运行"
else
  echo "🔹 启动后端服务..."
  cd "$SCRIPT_DIR"
  nohup node server.js > "$LOG_DIR/server.log" 2>&1 &
  echo "✅ 后端服务已启动 (PID: $!)"
fi

# 启动 Cloudflare Tunnel
if pgrep -f "cloudflared tunnel" > /dev/null; then
  echo "✅ 隧道已在运行"
else
  echo "🔹 启动 Cloudflare 隧道..."
  cloudflared tunnel --url http://localhost:3400 > "$LOG_DIR/tunnel.log" 2>&1 &
  TUNNEL_PID=$!
  echo "✅ 隧道已启动 (PID: $TUNNEL_PID)"
  sleep 5
  TUNNEL_URL=$(grep -o 'https://[^ ]*trycloudflare.com' "$LOG_DIR/tunnel.log" | head -1)
  if [ -n "$TUNNEL_URL" ]; then
    echo ""
    echo "🌐 公网访问地址: $TUNNEL_URL"
    echo "📝 答题页面:     $TUNNEL_URL/quiz.html"
    echo "📊 管理后台:     $TUNNEL_URL/admin.html"
    echo "🏠 创建答题:     $TUNNEL_URL/"
    echo ""
    echo "$TUNNEL_URL" > "$LOG_DIR/tunnel_url.txt"
  else
    echo "⚠️  隧道URL获取失败，请查看 $LOG_DIR/tunnel.log"
  fi
fi

echo "📋 日志查看: tail -f $LOG_DIR/server.log"
