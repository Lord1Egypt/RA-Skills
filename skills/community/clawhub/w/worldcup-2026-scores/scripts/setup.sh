#!/usr/bin/env bash
# 2026世界杯实时比分系统 - 一键部署脚本
# 用法: bash scripts/setup.sh

set -e

echo "======================================"
echo " 2026世界杯实时比分系统 - 一键部署"
echo "======================================"

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 需要 Node.js >= 18，请先安装"
    exit 1
fi

NODE_VER=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
echo "✅ Node.js $(node -v)"

# 克隆项目
APP_DIR="$HOME/worldcup-app"
if [ -d "$APP_DIR" ]; then
    echo "📁 目录已存在，拉取更新..."
    cd "$APP_DIR"
    git pull origin master 2>/dev/null || echo "  无法git pull，继续使用本地代码"
else
    echo "📦 克隆项目..."
    git clone https://github.com/liuboacean/WorldCup-2026.git "$APP_DIR"
    cd "$APP_DIR"
fi

# 安装依赖
echo "📦 安装依赖..."
npm install 2>/dev/null || npm install --no-optional

# 创建目录
mkdir -p data/matches cache

# 检查端口
PORT=3001
if lsof -i :$PORT &>/dev/null 2>&1; then
    echo "⚠️  端口 $PORT 已被占用，尝试关闭旧进程..."
    fuser -k $PORT/tcp 2>/dev/null || true
    sleep 2
fi

# 启动
echo "🚀 启动服务器 (端口 $PORT)..."
nohup node server.js > server.log 2>&1 &
sleep 3

# 验证
if curl -s http://localhost:$PORT/api/health &>/dev/null; then
    echo "✅ 部署成功！访问 http://localhost:$PORT"
    echo "📝 日志: tail -f $APP_DIR/server.log"
else
    echo "❌ 启动失败，查看日志: cat $APP_DIR/server.log"
    exit 1
fi
