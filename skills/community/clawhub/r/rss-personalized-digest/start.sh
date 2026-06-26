#!/bin/bash
# RSS 个性化摘要系统 - 一键启动脚本
# 用法: bash start.sh

set -e

echo "=== RSS 追踪摘要系统启动 ==="

# 1. 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    exit 1
fi
echo "✓ Node.js: $(node --version)"

# 2. 启动中转服务器
if ss -tlnp | grep -q 7890; then
    echo "✓ 中转服务器已在运行 (port 7890)"
else
    echo "→ 启动中转服务器..."
    node /tmp/rss-redirect-server.js > /tmp/redirect.log 2>&1 &
    sleep 2
    if ss -tlnp | grep -q 7890; then
        echo "✓ 中转服务器启动成功"
    else
        echo "❌ 中转服务器启动失败"
        exit 1
    fi
fi

# 3. 检查/启动隧道
if ps aux | grep -v grep | grep -q "serveo.net"; then
    echo "✓ serveo 隧道已在运行"
else
    echo "→ 启动 serveo 隧道..."
    ssh -o StrictHostKeyChecking=no \
        -o ServerAliveInterval=30 \
        -R 80:localhost:7890 \
        serveo.net > /tmp/serveo.log 2>&1 &
    sleep 6
    if grep -q "Forwarding HTTP" /tmp/serveo.log; then
        TUNNEL_URL=$(grep "Forwarding HTTP" /tmp/serveo.log | awk '{print $NF}')
        echo "✓ 隧道已启动: $TUNNEL_URL"
        # 更新配置
        python3 -c "
import json
with open('/root/.openclaw/workspace/rss-weights.json') as f:
    w = json.load(f)
w['redirect_base'] = '$TUNNEL_URL'
with open('/root/.openclaw/workspace/rss-weights.json', 'w') as f:
    json.dump(w, f, ensure_ascii=False, indent=2)
"
        echo "✓ 配置已更新"
    else
        echo "❌ 隧道启动失败"
        cat /tmp/serveo.log
        exit 1
    fi
fi

# 4. 健康检查
echo ""
echo "=== 健康检查 ==="
curl -s http://localhost:7890/health
echo ""
echo ""

# 5. 最近点击
echo "=== 最近点击 ==="
tail -5 /tmp/rss-clicks.log 2>/dev/null || echo "(暂无记录)"

# 6. 当前权重
echo ""
echo "=== 当前关键词权重 ==="
python3 -c "
import json
with open('/root/.openclaw/workspace/rss-weights.json') as f:
    w = json.load(f)
for k, v in sorted(w.get('keywords', {}).items(), key=lambda x: -x[1])[:10]:
    print(f'  {k}: {v}')
"

echo ""
echo "=== 启动完成 ==="
