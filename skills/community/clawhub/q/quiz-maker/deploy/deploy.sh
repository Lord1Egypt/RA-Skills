#!/bin/bash
set -e
echo "=== 1/10 安装 Node.js 20 ==="
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs
node -v && npm -v

echo "=== 2/10 安装 Nginx + Certbot ==="
apt-get update -qq
apt-get install -y nginx certbot python3-certbot-nginx

echo "=== 3/10 创建应用目录 ==="
mkdir -p /opt/quiz-maker
echo "目录创建完成"

echo "=== 4/10 复制代码 ==="
# 代码将通过后续 scp 复制，此处只确保目录存在
echo "应用目录: /opt/quiz-maker"

echo "=== 5/10 安装依赖 ==="
cd /opt/quiz-maker
npm install --production 2>&1 | tail -3

echo "=== 6/10 配置 Systemd ==="
cat > /etc/systemd/system/quiz-maker.service << 'EOF'
[Unit]
Description=Quiz Maker Server
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/quiz-maker
ExecStart=/usr/bin/node server.js
Restart=always
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable quiz-maker
echo "Systemd 配置完成"

echo "=== 7/10 启动服务 ==="
systemctl restart quiz-maker
sleep 2
systemctl status quiz-maker --no-pager | head -10

echo "=== 8/10 配置 Nginx ==="
# Nginx 配置将在域名解析后添加
echo "Nginx 待配置（需要域名）"

echo "=== 部署完成！ ==="
echo "当前状态:"
systemctl is-active quiz-maker && echo "✅ quiz-maker 运行中" || echo "❌ quiz-maker 未运行"
