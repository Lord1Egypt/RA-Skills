#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

SESSION_KEY="default"
STATE_ROOT="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/weixin-plugin-installer"
SESSION_DIR="$STATE_ROOT/$SESSION_KEY"
INSTALL_LOG="$SESSION_DIR/install.log"

mkdir -p "$SESSION_DIR"

emit_json() {
  local ok="$1"
  local state="$2"
  local message="${3:-}"
  cat <<JSON
{"ok":$ok,"session_key":"$SESSION_KEY","state":"$state","message":"${message//\"/\\\"}"}
JSON
}

plugin_installed() {
  openclaw plugins list 2>/dev/null | grep -Fq 'openclaw-weixin'
}

plugin_enabled() {
  local raw
  raw="$(openclaw config get plugins.entries.openclaw-weixin.enabled 2>/dev/null | tr -d '"'"'\"[:space:]'"'"' || true)"
  [[ "$raw" == "true" || "$raw" == "1" || "$raw" == "yes" ]]
}

gateway_reload_mode() {
  local raw
  raw="$(openclaw config get gateway.reload.mode 2>/dev/null | tr -d '"'"'\"[:space:]'"'"' | tr '[:upper:]' '[:lower:]' || true)"
  if [[ -n "$raw" ]]; then
    printf '%s' "$raw"
    return 0
  fi
  printf '%s' "hybrid"
}

run_step() {
  local description="$1"
  shift
  if ! "$@" >>"$INSTALL_LOG" 2>&1; then
    tail_msg="$(tail -n 40 "$INSTALL_LOG" 2>/dev/null | tr '\n' ' ' | sed 's/"/\\"/g')"
    emit_json false "failed" "${tail_msg:-$description失败}"
    exit 0
  fi
}

: > "$INSTALL_LOG"

if plugin_installed && plugin_enabled; then
  exec bash "$SCRIPT_DIR/refresh_weixin_qr.sh" "$SESSION_KEY" 20
fi

if ! plugin_installed; then
  run_step "安装微信插件" bash -lc 'openclaw plugins install "@tencent-weixin/openclaw-weixin"'
fi

if ! plugin_enabled; then
  run_step "启用微信插件" bash -lc 'openclaw plugins enable openclaw-weixin'
fi

RELOAD_MODE="$(gateway_reload_mode)"

case "$RELOAD_MODE" in
  hybrid|restart)
    emit_json true "starting" "微信插件已安装并启用。Gateway 将自动重载或重启；为避免中断当前对话，本轮不继续生成二维码。请等待 5 到 10 秒后发送“刷新微信二维码”。"
    ;;
  hot|off)
    emit_json true "starting" "微信插件已安装并启用。当前配置不会自动完成插件级重启；请在宿主机外部执行 openclaw gateway restart，完成后再发送“刷新微信二维码”。"
    ;;
  *)
    emit_json true "starting" "微信插件已安装并启用。当前无法确认 Gateway 的自动重载模式；请等待 5 到 10 秒后发送“刷新微信二维码”。如果仍无响应，再在宿主机外部执行 openclaw gateway restart。"
    ;;
esac
