#!/bin/bash
# redis-memory-system v3.3.0 — 一键安装脚本
set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SCRIPTS_DIR="$WORKSPACE/scripts"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "🔧 redis-memory-system v3.3.0 安装中..."
echo ""

# 1. 检查 Redis
if ! command -v redis-cli &>/dev/null; then
  echo "📦 安装 Redis..."
  if command -v apt &>/dev/null; then
    apt update -qq && apt install -y -qq redis-server 2>/dev/null
  elif command -v yum &>/dev/null; then
    yum install -y redis 2>/dev/null
  else
    echo "❌ 请手动安装 Redis（apt install redis-server 或 yum install redis）"
    exit 1
  fi
fi

# 2. 确保 Redis 运行
redis-server --daemonize yes 2>/dev/null || true
sleep 1
if redis-cli PING >/dev/null 2>&1; then
  echo "✅ Redis 运行中"
  echo "   版本: $(redis-cli INFO server 2>/dev/null | grep redis_version | cut -d: -f2)"
else
  echo "❌ Redis 无法连接，请检查 Redis 服务"
  exit 1
fi

# 3. 创建 workspace 脚本目录
mkdir -p "$SCRIPTS_DIR"

# 4. 拷贝脚本
for script in memory.sh extract_dialog.py; do
  cp "$SKILL_DIR/scripts/$script" "$SCRIPTS_DIR/"
  chmod +x "$SCRIPTS_DIR/$script"
  echo "  ✅ $script"
done
echo "✅ 脚本已安装到 $SCRIPTS_DIR"

# 5. 配置系统 cron 保底监控（每小时）
CRON_JOB="0 * * * * $SCRIPTS_DIR/memory.sh heartbeat >> /tmp/memory-heartbeat.log 2>&1"
(crontab -l 2>/dev/null | grep -v "memory.sh heartbeat"; echo "$CRON_JOB") | crontab -
echo "✅ 系统 cron 已注册（每小时监控哨兵）"

# 6. 安装验证
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  验证安装..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if bash "$SCRIPTS_DIR/memory.sh ping" 2>/dev/null; then
  echo "  ✅ 脚本可用"
else
  echo "  ⚠️ 脚本测试跳过"
fi

# 7. 配置提示
echo ""
echo "📖 配置用户（选一种）："
echo "  1. 环境变量:  export MEMORY_USERS=\"用户名1,用户名2\""
echo "  2. 配置文件:  echo \"用户名1\" > /etc/memory-users.conf"
echo "  3. 单次执行:  bash memory.sh sync --user 用户名"
echo ""
echo "📖 配置 OpenClaw cron 自动同步："
echo "  openclaw cron add --name \"记忆自动同步\" --every 1h \\"
echo "    --session isolated --timeout-seconds 180 \\"
echo "    --thinking minimal --tools \"exec,read\" --no-deliver \\"
echo "    --message \"用 memory.sh sync 检查并写入对话摘要到 Redis，用户列表从环境变量 MEMORY_USERS 读取\""
echo ""
echo "🎉 redis-memory-system v3.3.0 安装完成！"
echo ""
echo "试试："
echo "  bash $SCRIPTS_DIR/memory.sh get 你的用户名"
echo "  bash $SCRIPTS_DIR/memory.sh stats"
