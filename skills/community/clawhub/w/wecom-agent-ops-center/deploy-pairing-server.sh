#!/bin/bash
# ============================================================
# 企微 Agent Connector — 配对服务器部署脚本
# 目标服务器：www.hermesai.ltd (腾讯云)
# ============================================================

set -e

SERVER="txcloud"
REMOTE_DIR="/var/www/hermesai/pairing-server"
NODE_BIN="/usr/bin/node"  # 服务器上的 Node.js 路径（v24.14.1）

echo "🚀 部署配对服务器到 www.hermesai.ltd..."
echo ""

# 1. 上传文件
echo "📦 上传文件..."
ssh $SERVER "sudo mkdir -p $REMOTE_DIR && sudo chown ubuntu:ubuntu $REMOTE_DIR"
scp pairing-server.js $SERVER:$REMOTE_DIR/
scp package.json $SERVER:$REMOTE_DIR/

# 2. 安装依赖
echo ""
echo "📥 安装依赖..."
ssh $SERVER "cd $REMOTE_DIR && npm install --omit=dev 2>&1 | tail -5"

# 3. 创建 systemd 服务（自动重启）
echo ""
echo "⚙️ 配置 systemd 服务..."
ssh $SERVER "sudo tee /etc/systemd/system/pairing-server.service > /dev/null << 'EOF'
[Unit]
Description=企微 Agent Connector 配对服务器
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=$REMOTE_DIR
ExecStart=$NODE_BIN pairing-server.js
Restart=always
RestartSec=5
StandardOutput=append:/var/log/pairing-server.log
StandardError=append:/var/log/pairing-server.log

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload && sudo systemctl enable pairing-server && sudo systemctl restart pairing-server"
sleep 2

# 4. 验证
echo ""
echo "🔍 验证服务..."
HEALTH=$(ssh $SERVER "curl -s http://localhost:19527/health 2>/dev/null || echo 'FAIL'")
if echo "$HEALTH" | grep -q '"status":"ok"'; then
  echo "✅ 配对服务器运行正常！"
  echo "   HTTP API:  https://www.hermesai.ltd"
  echo "   WebSocket: wss://www.hermesai.ltd/ws"
  echo "   健康检查:  https://www.hermesai.ltd/health"
else
  echo "❌ 服务未正常启动，检查日志:"
  ssh $SERVER "sudo journalctl -u pairing-server --no-pager -n 20 2>/dev/null || tail -20 /var/log/pairing-server.log"
fi

echo ""
echo "📋 部署完成。接下来："
echo "   1. 确保防火墙开放 19527 端口"
echo "   2. 在 config.yaml 中将 signaling_server 设为 https://www.hermesai.ltd"
echo "   3. 测试: curl https://www.hermesai.ltd/health"
