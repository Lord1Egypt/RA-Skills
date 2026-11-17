#!/bin/bash
# install-flag.sh — 让 WorkBuddy 每次启动都自带 CDP 调试端口（任何启动方式都生效）
# 原理：MacOS/Electron 改名为 Electron.real，原位放转发脚本附带 --remote-debugging-port
# 注意：WorkBuddy 更新后会被覆盖，需重跑本脚本
set -e

APP="/Applications/WorkBuddy.app"
BIN="$APP/Contents/MacOS/Electron"
PORT=9223

[ -d "$APP" ] || { echo "✗ 未找到 $APP" >&2; exit 1; }

if [ -f "$BIN.real" ]; then
  echo "· 已安装过，跳过（如需改端口请先 uninstall-flag.sh）"
  exit 0
fi

mv "$BIN" "$BIN.real"
cat > "$BIN" <<EOF
#!/bin/bash
exec "\$(dirname "\$0")/Electron.real" --remote-debugging-port=$PORT "\$@"
EOF
chmod +x "$BIN"
echo "✓ 已安装启动引子：今后 WorkBuddy 无论怎么启动都带调试端口（$PORT）"
echo "· WorkBuddy 更新覆盖后需重跑本脚本；还原：scripts/uninstall-flag.sh"
