#!/bin/bash
# xhs-mcp 一键安装脚本（macOS & Linux）
# 用法: bash <(curl -sSL https://raw.githubusercontent.com/xpzouying/xiaohongshu-mcp/main/scripts/install.sh)

set -e

OS="$(uname -s)"
ARCH="$(uname -m)"
HOME_DIR="$HOME"
PORT=18060
INSTALL_DIR="$HOME_DIR/xiaohongshu-mcp"

log() { echo "[$(date '+%H:%M:%S')] $1"; }

# ---- 检测架构选二进制 ----
case "$OS-$ARCH" in
  Darwin-x86_64)  ARCH_URL="xiaohongshu-mcp-darwin-amd64.tar.gz" ;;
  Darwin-arm64)   ARCH_URL="xiaohongshu-mcp-darwin-arm64.tar.gz" ;;
  Linux-x86_64)   ARCH_URL="xiaohongshu-mcp-linux-amd64.tar.gz" ;;
  Linux-aarch64)  ARCH_URL="xiaohongshu-mcp-linux-arm64.tar.gz" ;;
  *) log "❌ 不支持: $OS $ARCH"; exit 1 ;;
esac

mkdir -p "$INSTALL_DIR"

# ---- 检查是否已安装并运行 ----
if curl -s --max-time 2 http://localhost:$PORT/health > /dev/null 2>&1; then
  log "✅ 服务已在运行（端口 $PORT），跳过安装"
  exit 0
fi

# ---- 获取最新版本号 ----
log "🔍 查询最新版本..."
TAG=$(curl -sL "https://api.github.com/repos/xpzouying/xiaohongshu-mcp/releases/latest" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d['tag_name'])")
DOWNLOAD_URL="https://github.com/xpzouying/xiaohongshu-mcp/releases/download/${TAG}/${ARCH_URL}"
log "📦 版本: $TAG"

# ---- 下载 ----
log "⬇️  下载 $ARCH_URL ..."
cd "$INSTALL_DIR"
curl -L --progress-bar "$DOWNLOAD_URL" -o ./xhs-mcp.tar.gz

# 解压
log "📂 解压..."
tar xzf ./xhs-mcp.tar.gz
rm ./xhs-mcp.tar.gz

# 找二进制文件
BINARY=$(ls xiaohongshu-mcp-* 2>/dev/null | head -1 || echo "")
if [ -n "$BINARY" ]; then
  mv "$BINARY" ./xhs-mcp-bin
  chmod +x ./xhs-mcp-bin
else
  log "❌ 解压失败，未找到二进制文件"
  ls -la
  exit 1
fi

# ---- 启动服务 ----
log "🚀 启动服务 ..."
# 杀掉旧进程
python3 -c "
import socket, os, signal
try:
    s=socket.socket(); s.bind(('localhost',$PORT)); s.close()
except:
    import subprocess
    r=subprocess.run(['lsof','-ti',':$PORT'],capture_output=True,text=True)
    for pid in r.stdout.strip().split():
        try: os.kill(int(pid),9)
        except: pass
" 2>/dev/null || true

sleep 1
cd "$INSTALL_DIR"
nohup ./xhs-mcp-bin server --port $PORT > mcp.log 2>&1 &
MCP_PID=$!
sleep 3

# ---- 验证 ----
if curl -s --max-time 3 http://localhost:$PORT/health > /dev/null 2>&1; then
  log "✅ 服务启动成功（PID $MCP_PID），端口 $PORT"
else
  log "❌ 启动失败，查看: tail $INSTALL_DIR/mcp.log"
  tail -10 "$INSTALL_DIR/mcp.log"
  exit 1
fi

# ---- 开机自启 ----
if [ "$OS" = "Darwin" ]; then
  PLIST="$HOME_DIR/Library/LaunchAgents/com.openclaw.xhs-mcp.plist"
  mkdir -p "$HOME_DIR/Library/LaunchAgents"
  cat > "$PLIST" << PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.openclaw.xhs-mcp</string>
    <key>ProgramArguments</key>
    <array>
        <string>${INSTALL_DIR}/xhs-mcp-bin</string>
        <string>server</string>
        <string>--port</string>
        <string>${PORT}</string>
    </array>
    <key>WorkingDirectory</key><string>${INSTALL_DIR}</string>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
    <key>StandardOutPath</key><string>${INSTALL_DIR}/mcp.log</string>
    <key>StandardErrorPath</key><string>${INSTALL_DIR}/mcp.log</string>
</dict>
</plist>
PLISTEOF
  launchctl unload "$PLIST" 2>/dev/null || true
  launchctl load "$PLIST"
  log "✅ launchd 开机自启已配置"

elif [ "$OS" = "Linux" ]; then
  cat > /tmp/xhs-mcp.service << SERVICEEOF
[Unit]
Description=Xiaohongshu MCP Service
After=network.target

[Service]
WorkingDirectory=${INSTALL_DIR}
ExecStart=${INSTALL_DIR}/xhs-mcp-bin server --port ${PORT}
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICEEOF
  sudo mv /tmp/xhs-mcp.service /etc/systemd/system/xhs-mcp.service
  sudo systemctl daemon-reload
  sudo systemctl enable xhs-mcp
  sudo systemctl start xhs-mcp
  log "✅ systemd 开机自启已配置"
fi

# ---- 看门狗 ----
cat > "$INSTALL_DIR/watchdog.sh" << 'WATCHDOG'
#!/bin/bash
PORT=18060
LOG="$HOME/xiaohongshu-mcp/watchdog.log"
if ! curl -s --max-time 3 http://localhost:$PORT/health > /dev/null 2>&1; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') 重启服务..." >> "$LOG"
  lsof -ti :$PORT | xargs kill -9 2>/dev/null
  sleep 2
  cd "$HOME/xiaohongshu-mcp"
  nohup ./xhs-mcp-bin server --port $PORT >> mcp.log 2>&1 &
fi
WATCHDOG
chmod +x "$INSTALL_DIR/watchdog.sh"

# macOS crontab 看门狗
if [ "$OS" = "Darwin" ]; then
  (crontab -l 2>/dev/null | grep -v watchdog; echo "*/5 * * * * $INSTALL_DIR/watchdog.sh") | crontab -
  log "✅ 看门狗已配置（每5分钟检查）"
fi

log ""
log "========================================="
log "  ✅ 小红书 MCP 安装完成！"
log "  📍 端口: $PORT"
log "  📁 目录: $INSTALL_DIR"
log "  🔄 服务管理:"
log "     macOS: launchctl unload/load $HOME/Library/LaunchAgents/com.openclaw.xhs-mcp.plist"
log "     Linux:  sudo systemctl restart xhs-mcp"
log "========================================="
log ""
log "📌 下一步：告诉我就行，我会发二维码给你扫码登录 🐹"
