#!/bin/bash
# 一键切换企微 Agent Ops Center 到 v2.4.0
# 用法：在本地终端执行
#   ssh root@www.hermesai.ltd < deploy-v2.4.0.sh

set -e

echo "=========================================="
echo "  企微 Agent Ops Center — 切换到 v2.4.0"
echo "=========================================="

cd /var/www/hermesai/pairing-server

# 1. 查看当前运行的进程
echo ""
echo "[1/5] 查看当前运行进程..."
ps aux | grep -E 'node.*connector|node.*pairing-server' | grep -v grep || echo "  未找到运行中的进程"

# 2. 备份当前版本（如果存在）
if [ -f connector.js ]; then
    BACKUP_DIR="/var/www/hermesai/backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    cp -r . "$BACKUP_DIR/"
    echo "[2/5] 已备份当前版本到：$BACKUP_DIR"
else
    echo "[2/5] connector.js 不存在，跳过备份"
fi

# 3. 停止旧进程（找 PID 并 kill）
echo ""
echo "[3/5] 停止旧进程..."
OLD_PIDS=$(ps aux | grep -E 'node.*connector|node.*pairing-server' | grep -v grep | awk '{print $2}')
if [ -n "$OLD_PIDS" ]; then
    echo "  找到旧进程 PID: $OLD_PIDS"
    for pid in $OLD_PIDS; do
        echo "  kill $pid ..."
        kill $pid 2>/dev/null || true
    done
    sleep 2
    # 强制 kill 残留进程
    OLD_PIDS2=$(ps aux | grep -E 'node.*connector|node.*pairing-server' | grep -v grep | awk '{print $2}')
    if [ -n "$OLD_PIDS2" ]; then
        echo "  强制终止残留进程..."
        for pid in $OLD_PIDS2; do
            kill -9 $pid 2>/dev/null || true
        done
    fi
    echo "  ✅ 旧进程已停止"
else
    echo "  ℹ️  未找到运行中的旧进程"
fi

# 4. 重新 npm install（确保依赖正确）
echo ""
echo "[4/5] 安装/更新依赖..."
npm install --production 2>&1 | tail -5

# 5. 启动 v2.4.0
echo ""
echo "[5/5] 启动 v2.4.0 ..."
# 用 nohup 后台启动，输出到日志文件
mkdir -p logs
nohup node connector.js > logs/connector.log 2>&1 &
NEW_PID=$!
sleep 3

# 验证启动成功
if ps -p $NEW_PID > /dev/null 2>&1; then
    echo "  ✅ v2.4.0 启动成功！PID: $NEW_PID"
else
    echo "  ❌ 启动失败，查看日志："
    tail -20 logs/connector.log
    exit 1
fi

# 6. 验证健康检查
echo ""
echo "验证健康检查..."
sleep 2
HEALTH=$(curl -s http://localhost:9527/health || echo "FAILED")
if echo "$HEALTH" | grep -q "ok\|healthy"; then
    echo "  ✅ 健康检查通过！"
    echo "$HEALTH" | head -5
else
    echo "  ⚠️  健康检查未通过，响应："
    echo "$HEALTH" | head -10
fi

# 7. 验证 pairing-server 端口
echo ""
echo "验证端口监听状态..."
sleep 1
if command -v ss &> /dev/null; then
    ss -tlnp | grep -E '9527|19527' || echo "  端口未监听，检查日志"
else
    netstat -tlnp 2>/dev/null | grep -E '9527|19527' || echo "  端口未监听，检查日志"
fi

echo ""
echo "=========================================="
echo "  ✅ 切换完成！"
echo "  日志文件：/var/www/hermesai/pairing-server/logs/connector.log"
echo "  查看日志：tail -f logs/connector.log"
echo "  停止服务：kill $NEW_PID"
echo "=========================================="
