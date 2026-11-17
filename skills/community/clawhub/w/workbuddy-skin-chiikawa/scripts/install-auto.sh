#!/bin/bash
# install-auto.sh — 安装「开 WorkBuddy 自动换肤」
# 注册 LaunchAgent：登录自启 watch.sh，常驻检测、自动注入
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LABEL="com.workbuddy.skin"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"

# 找 node（launchd 环境没有用户 PATH，必须绝对路径）
NODE="$(command -v node || true)"
if [ -z "$NODE" ]; then
  for c in /opt/homebrew/bin/node /usr/local/bin/node "$HOME"/.local/share/fnm/node-versions/*/installation/bin/node; do
    [ -x "$c" ] && NODE="$c" && break
  done
fi
if [ -z "$NODE" ]; then
  echo "✗ 找不到 node。请先安装 Node.js（如 brew install node）再运行本脚本" >&2
  exit 1
fi
echo "· node: $NODE"

# 生成 watch.sh（烘焙绝对路径）
sed -e "s|__ROOT__|$ROOT|g" -e "s|__NODE__|$NODE|g" \
  "$ROOT/scripts/watch.sh" > "$ROOT/scripts/watch.local.sh"
chmod +x "$ROOT/scripts/watch.local.sh"

# 生成并加载 LaunchAgent
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array><string>/bin/bash</string><string>$ROOT/scripts/watch.local.sh</string></array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>$ROOT/scripts/watch.log</string>
  <key>StandardErrorPath</key><string>$ROOT/scripts/watch.log</string>
</dict>
</plist>
EOF

launchctl bootout "gui/$(id -u)/${LABEL}" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "✓ 自动换肤已开启：今后正常打开 WorkBuddy 即可，皮肤会自动生效"
echo "· 日志：$ROOT/scripts/watch.log；卸载：scripts/uninstall-auto.sh"
