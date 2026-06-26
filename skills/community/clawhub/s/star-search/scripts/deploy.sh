#!/bin/bash
# star-search v16.1 部署脚本 — 在腾讯云 ubuntu 服务器上跑
# 用法: ssh ubuntu@<服务器IP> "bash ~/star-search/deploy.sh"
set -e
cd ~/star-search

echo "=== 1. chmod ==="
chmod +x scripts/*.py

echo "=== 2. install deps ==="
pip3 install --user -q fastapi uvicorn[standard] httpx pydantic beautifulsoup4 lxml 2>&1 | tail -3 || pip3 install -q fastapi uvicorn[standard] httpx pydantic beautifulsoup4 lxml 2>&1 | tail -3

echo "=== 3. check playwright (already installed in v15) ==="
python3 -c "from playwright.sync_api import sync_playwright; print('playwright ok')" 2>&1 | tail -2

echo "=== 4. test search.py import ==="
python3 scripts/search.py --list 2>&1 | head -5

echo "=== 5. start api_server on :5000 (background) ==="
# 关掉已有的
pkill -f "api_server.py.*--port 5000" 2>/dev/null || true
sleep 1
# 后台启动
nohup python3 scripts/api_server.py --port 5000 --host 0.0.0.0 > /tmp/star-search-api.log 2>&1 &
echo "started pid=$!"
sleep 4

echo "=== 6. health check ==="
curl -s http://127.0.0.1:5000/v1/health
echo ""
echo "=== 7. test search ==="
curl -s -X POST http://127.0.0.1:5000/v1/search -H "Content-Type: application/json" -d '{"query":"鸿蒙","mode":"dev_rss","top":2}' | head -c 500
echo ""

echo "=== 8. show log tail ==="
tail -10 /tmp/star-search-api.log
echo "DEPLOY DONE"
