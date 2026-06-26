#!/bin/bash
# star-search v16.1 在 root context 启动（用现成 playwright+chromium）
# 用法（协作同事操作）:
#   sudo cp /home/ubuntu/star-search/scripts/api-server-root.service /etc/systemd/system/
#   sudo systemctl daemon-reload
#   sudo systemctl enable --now api-server-root
#   sudo systemctl status api-server-root

set -e
echo "=== 检查 root playwright 是否完整 ==="
PYTHON=/usr/bin/python3
$PYTHON -c "import playwright; print('playwright', playwright.__version__)" 2>&1
echo "---"
# 用现成 chromium-1217
CHROME=/root/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome
ls -la $CHROME 2>&1
$CHROME --version 2>&1
echo "---"
echo "=== 装缺失的系统包（如需要）==="
apt-get update -qq 2>&1 | tail -3
apt-get install -y --no-install-recommends \
  libatk1.0-0 libatk-bridge2.0-0 libcups2 libxcomposite1 libxdamage1 \
  libxfixes3 libxrandr2 libgbm1 libxkbcommon0 libpango-1.0-0 libcairo2 \
  libasound2 libatspi2.0-0 libnss3 2>&1 | tail -5
echo "---"
echo "=== 验证 ubuntu 用户的 star-search 目录 ==="
ls -la /home/ubuntu/star-search/scripts/ | head -10
echo "---"
echo "=== 复制到 root 路径 ==="
mkdir -p /opt/star-search
cp -r /home/ubuntu/star-search/* /opt/star-search/ 2>&1 | head -3
chown -R root:root /opt/star-search
echo "---"
echo "=== systemd 启停 ==="
cat > /etc/systemd/system/api-server-root.service << 'SVCEOF'
[Unit]
Description=star-search v16.1 API server (root context for playwright)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/star-search/scripts
ExecStart=/usr/bin/python3 /opt/star-search/scripts/api_server.py --host 127.0.0.1 --port 5000
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

[Install]
WantedBy=multi-user.target
SVCEOF

systemctl daemon-reload
systemctl enable --now api-server-root
sleep 3
systemctl status api-server-root --no-pager | head -15
echo "---"
echo "=== test ==="
curl -s --max-time 5 http://127.0.0.1:5000/v1/health
echo ""
echo "DONE"
