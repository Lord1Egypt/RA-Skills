#!/bin/bash
# 查服务器进程状态
echo "=== uptime / load ==="
uptime
echo ""
echo "=== memory ==="
free -h 2>/dev/null || echo "no free"
echo ""
echo "=== top 5 CPU ==="
ps aux --sort=-%cpu | head -8
echo ""
echo "=== nginx 进程 ==="
ps aux | grep -E "nginx|api_server|fastapi|python.*api" | grep -v grep
echo ""
echo "=== systemd 状态 ==="
systemctl status nginx --no-pager 2>&1 | head -10
echo ""
systemctl status api-server --no-pager 2>&1 | head -10
echo ""
echo "=== listening ports ==="
ss -tlnp 2>/dev/null | head -20 || netstat -tlnp 2>&1 | head -20
echo ""
echo "=== last 30 lines nginx error ==="
tail -30 /var/log/nginx/error.log 2>&1
