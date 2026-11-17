#!/bin/bash
# ============================================================
# socratic-reading-coach · AI 伴读启动脚本
# 用法：bash start.sh
# ============================================================
set -e

# 定位到 Skill 根目录（scripts/ 的上一级）
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SKILL_DIR"

PORT=3456
SERVER_JS="$SKILL_DIR/assets/server.js"

# ---------- 1. 检查 Node.js ----------
if ! command -v node &>/dev/null; then
  echo "❌ 未检测到 Node.js，请先安装：https://nodejs.org/"
  exit 1
fi
echo "✅ Node.js $(node --version)"

# ---------- 2. 检查微信读书 API Key ----------
# 注意：不 source shell 配置文件（避免执行任意启动代码），
# 只从配置文件中静态提取 WEREAD_API_KEY 一行。
if [ -z "$WEREAD_API_KEY" ]; then
  for rcfile in ~/.zshrc ~/.bashrc ~/.bash_profile ~/.profile; do
    if [ -f "$rcfile" ]; then
      key_line="$(grep -h '^[[:space:]]*export[[:space:]]\+WEREAD_API_KEY=' "$rcfile" 2>/dev/null | tail -1)"
      if [ -n "$key_line" ]; then
        WEREAD_API_KEY="${key_line#*WEREAD_API_KEY=}"
        # 去掉可能的引号
        WEREAD_API_KEY="${WEREAD_API_KEY%\"}"; WEREAD_API_KEY="${WEREAD_API_KEY#\"}"
        WEREAD_API_KEY="${WEREAD_API_KEY%\'}"; WEREAD_API_KEY="${WEREAD_API_KEY#\'}"
        export WEREAD_API_KEY
      fi
    fi
  done
fi
if [ -z "$WEREAD_API_KEY" ]; then
  echo "⚠️  未检测到 WEREAD_API_KEY，微信读书搜索功能将不可用"
  echo "   配置方式：在 ~/.zshrc 或 ~/.bashrc 中添加"
  echo "   export WEREAD_API_KEY=你的微信读书API Key"
else
  echo "✅ 微信读书 API Key 已配置"
fi

# ---------- 3. 停掉本应用残留的旧服务（凭 PID 文件，不误杀其他进程） ----------
OLD_PID=""
if [ -f "$SKILL_DIR/assets/.server.pid" ]; then
  OLD_PID="$(cat "$SKILL_DIR/assets/.server.pid" 2>/dev/null || true)"
  if [ -n "$OLD_PID" ] && ! kill -0 "$OLD_PID" 2>/dev/null; then
    rm -f "$SKILL_DIR/assets/.server.pid"; OLD_PID=""
  fi
fi
if [ -n "$OLD_PID" ]; then
  echo "ℹ️  检测到本应用的旧服务（PID $OLD_PID），正在停止…"
  kill "$OLD_PID" 2>/dev/null || true
  for i in 1 2 3 4 5; do kill -0 "$OLD_PID" 2>/dev/null || break; sleep 0.5; done
fi
if command -v lsof &>/dev/null; then
  PIDS="$(lsof -ti :"$PORT" 2>/dev/null || true)"
  if [ -n "$PIDS" ] && [ "$PIDS" != "$OLD_PID" ]; then
    echo "❌ 端口 $PORT 被其他程序占用（不属于本应用），不会自动终止它。"
    echo "   请确认后手动释放端口 $PORT，或修改 server.js 中的 PORT 后重试。"
    lsof -i :"$PORT" 2>/dev/null | head -5 || true
    exit 1
  fi
fi

# ---------- 4. 启动服务 ----------
echo ""
echo "🚀 启动 AI 伴读服务（socratic-reading-coach）..."
echo "   访问地址：http://localhost:${PORT}"
echo "   停止服务：按 Ctrl+C，或运行 bash scripts/stop.sh"
echo ""

node "$SERVER_JS"
