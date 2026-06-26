#!/usr/bin/env bash
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }
log_ok() { echo -e "${GREEN}[PASS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_fail() { echo -e "${RED}[FAIL]${NC} $1"; }

OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
CONFIG_FILE="${CONFIG_FILE:-$OPENCLAW_HOME/openclaw.json}"
NODE_CONFIG_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/config.json"
TTS_CONFIG_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/tts_config.json"
FAIL_COUNT=0

pass() { log_ok "$1"; }
fail() { log_fail "$1"; FAIL_COUNT=$((FAIL_COUNT + 1)); }

check_http_health() {
  local name="$1"
  local url="$2"
  if curl -fsS "$url" >/dev/null 2>&1; then
    pass "$name 健康检查通过: $url"
  else
    fail "$name 健康检查失败: $url"
  fi
}

check_json_value() {
  local file_path="$1"
  local label="$2"
  local expression="$3"
  if node -e '
const fs = require("node:fs");
const cfg = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
const fn = new Function("cfg", `return (${process.argv[2]});`);
if (!fn(cfg)) process.exit(1);
' "$file_path" "$expression"; then
    pass "$label"
  else
    fail "$label"
  fi
}

log_step "检查本地服务"
check_http_health "Flask TTS" "http://127.0.0.1:5002/api/health"
check_http_health "Node TTS Workflow" "http://127.0.0.1:9002/health"

log_step "检查本地配置文件"
[[ -f "$NODE_CONFIG_FILE" ]] && pass "找到 config.json" || fail "缺少 config.json"
[[ -f "$TTS_CONFIG_FILE" ]] && pass "找到 tts_config.json" || fail "缺少 tts_config.json"

if [[ -f "$NODE_CONFIG_FILE" ]]; then
  check_json_value "$NODE_CONFIG_FILE" "Node 网关监听 9002" 'cfg.port === 9002'
  check_json_value "$NODE_CONFIG_FILE" "Node 网关转发到 Flask 5002" 'cfg.flaskTtsUrl === "http://127.0.0.1:5002/api/tts/synthesize"'
fi

if [[ -f "$TTS_CONFIG_FILE" ]]; then
  check_json_value "$TTS_CONFIG_FILE" "Base 模型已配置" 'Boolean(cfg.qwen3_tts_0_6b_base_openvino || cfg["qwen3_tts_0.6b_base_openvino"])'
  check_json_value "$TTS_CONFIG_FILE" "Custom 模型已配置" 'Boolean(cfg.qwen3_tts_0_6b_custom_openvino || cfg["qwen3_tts_0.6b_custom_openvino"])'
fi

log_step "检查 OpenClaw 配置"
if [[ -f "$CONFIG_FILE" ]]; then
  pass "找到 OpenClaw 配置: $CONFIG_FILE"
  check_json_value "$CONFIG_FILE" "channels.qqbot.xeonTts 已开启" 'cfg.channels?.qqbot?.xeonTts?.enabled === true'
  check_json_value "$CONFIG_FILE" "channels.qqbot.xeonTts.baseUrl 指向 9002" 'cfg.channels?.qqbot?.xeonTts?.baseUrl === "http://127.0.0.1:9002"'
else
  fail "未找到 OpenClaw 配置: $CONFIG_FILE"
fi

log_step "检查 systemd 状态"
if systemctl --user is-enabled xeontts-tts.service >/dev/null 2>&1; then pass "xeontts-tts.service 已启用"; else fail "xeontts-tts.service 未启用"; fi
if systemctl --user is-enabled xeontts-node.service >/dev/null 2>&1; then pass "xeontts-node.service 已启用"; else fail "xeontts-node.service 未启用"; fi

if [[ "$FAIL_COUNT" -gt 0 ]]; then
  log_fail "自检失败，FAIL=$FAIL_COUNT"
  exit 1
fi

log_ok "自检通过"
