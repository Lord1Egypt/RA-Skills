#!/usr/bin/env bash
# 启动一个带 CDP 调试端口的独立 Chrome，并用 playwright-cli 挂载它。
#
# ⛔ 实测结论（2026-10，Windows Git Bash）：
#   **持久的是 profile 目录，不是浏览器进程。**
#   自起 Chrome + CDP 后，浏览器进程同样会在对话轮次边界被宿主回收（两次尝试都被回收，
#   后台任务方式启动也会被杀掉）。所以"跨轮次保持浏览器活着"这个目标无法达成。
#   真正稳定的是 **profile 目录里的登录态**：cookie（含 id_token）留在
#   $PROFILE_DIR/Default/Cookies 里，进程被回收后不影响。
#   ⇒ 正确用法：**每轮用同一个 PROFILE_DIR 重跑本脚本**，Chrome 重启后会自动带出登录态，
#     实测重启后直接落在 https://creator.rednote.com/publish/publish（无需重新登录）。
#   ⇒ 绝不要为每轮新建 profile 目录，否则每次都要重新短信登录。
#
# 为什么不用 `playwright-cli open --headed`：
#   由 playwright-cli 自己启动的 headed 浏览器**不会写入我们指定的 profile**，
#   进程一被回收登录态就丢了，等于每轮都要重新登录。
#
# 用法:
#   bash bootstrap_browser.sh [workdir] [port] [start_url]
# 示例:
#   bash bootstrap_browser.sh .tmp/xhs-cdp 9222 "https://creator.rednote.com/publish/publish"
set -u

WORKDIR="${1:-.tmp/xhs-cdp}"
PORT="${2:-9222}"
START_URL="${3:-https://creator.rednote.com/publish/publish}"

PROFILE_DIR="$(cd "$(dirname "$WORKDIR")" 2>/dev/null && pwd)/$(basename "$WORKDIR")"
if [ -z "$PROFILE_DIR" ]; then PROFILE_DIR="$WORKDIR"; fi
mkdir -p "$PROFILE_DIR"

find_chrome() {
  for p in \
    "/c/Program Files/Google/Chrome/Application/chrome.exe" \
    "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe" \
    "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
    "/c/Program Files/Microsoft/Edge/Application/msedge.exe"; do
    [ -f "$p" ] && { echo "$p"; return 0; }
  done
  command -v chrome >/dev/null 2>&1 && { command -v chrome; return 0; }
  command -v google-chrome >/dev/null 2>&1 && { command -v google-chrome; return 0; }
  return 1
}

CHROME="$(find_chrome)" || { echo "找不到 Chrome/Edge，请先安装" >&2; exit 1; }
echo "浏览器: $CHROME"

# 端口已占用 → 说明已有实例在跑，直接复用
if curl -s --max-time 3 "http://127.0.0.1:$PORT/json/version" >/dev/null 2>&1; then
  echo "端口 $PORT 已有 CDP 实例，复用"
else
  # ⛔ Chrome >=136：--remote-debugging-port 必须搭配非默认 --user-data-dir 才生效
  "$CHROME" \
    --remote-debugging-port="$PORT" \
    --user-data-dir="$PROFILE_DIR" \
    --no-first-run --no-default-browser-check \
    --window-size=1360,900 --window-position=60,40 \
    "$START_URL" >/dev/null 2>&1 &
  echo "Chrome 已启动 (pid $!)，profile: $PROFILE_DIR"
  for i in $(seq 1 20); do
    sleep 1
    curl -s --max-time 3 "http://127.0.0.1:$PORT/json/version" >/dev/null 2>&1 && break
  done
fi

curl -s --max-time 5 "http://127.0.0.1:$PORT/json/version" | head -c 200; echo ""

# 挂载 playwright-cli（可选；没装也不影响用 playwright-core 直连）
PCLI="$(command -v playwright-cli || true)"
if [ -z "$PCLI" ]; then
  for c in "/c/Users/$USERNAME/.workbuddy/binaries/node/versions"/*/playwright-cli; do
    [ -f "$c" ] && PCLI="$c" && break
  done
fi
if [ -n "$PCLI" ] && [ -x "$PCLI" ]; then
  "$PCLI" kill-all >/dev/null 2>&1
  "$PCLI" -s=xhs attach --cdp "http://127.0.0.1:$PORT" 2>&1 | tail -3
  "$PCLI" list 2>&1 | head -6
  echo "→ 已挂载，playwright-cli -s=xhs <cmd>"
else
  echo "→ playwright-cli 未安装（可选）：npm install -g @playwright/cli@latest"
  echo "→ 或直接用本 skill 的 scripts/publish_note.js（走 playwright-core）"
fi
