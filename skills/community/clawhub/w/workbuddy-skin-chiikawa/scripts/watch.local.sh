#!/bin/bash
# watch.sh — 常驻看守：WorkBuddy 在跑而皮肤不在时，自动 apply
# 由 install-auto.sh 注册为 LaunchAgent，登录自启

ROOT="/Users/kuzen/Developer/workbuddy-skin"
NODE="/Users/kuzen/.local/share/fnm/node-versions/v24.15.0/installation/bin/node"
PORT=9223

LAST_PID=""

while true; do
  PID=$(pgrep -f "WorkBuddy.app/Contents/MacOS/Electron" | head -1)
  if [ -z "$PID" ]; then
    LAST_PID=""   # 已退出，复位等下次启动
  elif [ "$PID" != "$LAST_PID" ]; then
    # 新实例：renderer 起好就注入（apply 幂等，已挂皮肤会跳过重启逻辑）
    if curl -s --max-time 1 "http://127.0.0.1:${PORT}/json/list" 2>/dev/null | grep -q "renderer/index.html"; then
      "$NODE" "$ROOT/src/apply.mjs" >>"$ROOT/scripts/watch.log" 2>&1 && LAST_PID=$PID
    fi
  fi
  sleep 2
done
