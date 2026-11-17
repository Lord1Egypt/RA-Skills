#!/usr/bin/env bash
set -euo pipefail

# collect-page.sh — 通过 openclaw browser CLI 提取网页内容到文件
#
# 用法：bash collect-page.sh <URL> [DATA_FILE]
#
# 参数：
#   URL        — 目标网页 URL（必需）
#   DATA_FILE  — 输出 JSON 文件路径（默认 /tmp/youdaonote-clip-data.json）
#
# 输出：
#   文件：DATA_FILE（包含 title、content、imageUrls、source，调试时含 _debugKey）
#   stdout 最后一行：metadata JSON（仅 title、imageCount、source、contentLength）
#
# 环境变量：
#   YOUDAONOTE_CLIP_DEBUG — 调试日志目录（可选，设置后生成 _debugKey 并写入 collect.log）
#
# bodyHtml 直接写入文件，不经过 agent context window。
#
# v1.4.0 性能优化：
#   - 合并步骤：5 步 → 3 步（减少 2 次进程启动）
#   - 动态超时：根据页面大小调整 networkidle 超时
#   - 预期收益：节省 200-400ms + 小页面减少 5s 等待

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# === 环境引导（确保 Node >= 22 且 openclaw 可用）===
# Gateway exec 子进程可能：1) 缺少 nvm PATH  2) Volta shim 覆盖 node 为 v18
_need_nvm=false
if ! command -v openclaw &>/dev/null; then
  _need_nvm=true
else
  _node_major=$(node --version 2>/dev/null | sed 's/v//' | cut -d. -f1)
  [[ -z "$_node_major" || "$_node_major" -lt 22 ]] && _need_nvm=true
fi
if $_need_nvm; then
  if [[ -z "${NVM_DIR:-}" ]]; then
    for dir in "$HOME/.nvm" "/usr/local/opt/nvm"; do
      [[ -s "$dir/nvm.sh" ]] && export NVM_DIR="$dir" && break
    done
  fi
  [[ -n "${NVM_DIR:-}" && -s "${NVM_DIR}/nvm.sh" ]] && source "${NVM_DIR}/nvm.sh" 2>/dev/null || true
  # 二次检查：若 Volta shim 仍覆盖 node，强制前置 nvm 路径
  _node_major=$(node --version 2>/dev/null | sed 's/v//' | cut -d. -f1)
  if [[ -z "$_node_major" || "$_node_major" -lt 22 ]] && [[ -n "${NVM_DIR:-}" ]]; then
    for _nvm_bin in "${NVM_DIR}"/versions/node/v22*/bin; do
      [[ -d "$_nvm_bin" ]] && export PATH="$_nvm_bin:$PATH" && break
    done
  fi
fi
unset _need_nvm _node_major _nvm_bin

TARGET_URL="${1:?用法: bash collect-page.sh <URL> [DATA_FILE]}"
DATA_FILE="${2:-/tmp/youdaonote-clip-data.json}"
PROFILE="openclaw"

# --json 全局选项：禁用 @clack/prompts spinner（否则控制字符污染 stdout）
BROWSER="openclaw browser --json --browser-profile $PROFILE"

# === 动态超时调整（A3 优化）===
# 根据 Content-Length 预估页面大小，动态调整 networkidle 超时
# 小页面（<500KB）用 8s，中等页面（500KB-2MB）用 12s，大页面（>2MB）用 20s
get_network_timeout() {
  local url="$1"
  local content_length=0

  # 尝试获取 Content-Length（快速 HEAD 请求，超时 3s）
  content_length=$(curl -sfI --max-time 3 "$url" 2>/dev/null | grep -i '^content-length:' | awk '{print $2}' | tr -d '\r' || echo 0)

  if [ "$content_length" -gt 2000000 ]; then
    echo 20000  # >2MB: 20s
  elif [ "$content_length" -gt 500000 ]; then
    echo 12000  # 500KB-2MB: 12s
  else
    echo 15000  # <500KB 或未知: 15s
  fi
}

NETWORK_TIMEOUT=$(get_network_timeout "$TARGET_URL")

# Step 1: 打开页面
$BROWSER open "$TARGET_URL" >/dev/null

# Step 2: 等待加载（动态超时）
$BROWSER wait --load domcontentloaded --timeout-ms "$NETWORK_TIMEOUT" >/dev/null 2>&1 || true

# Step 3: 注入 collect SDK（本地内联，不加载外部 CDN）
$BROWSER evaluate --fn "$(cat "$SCRIPT_DIR/static/inject-sdk.fn.js")" >/dev/null 2>&1

# Step 4: 合并等待 + 解析（A1 优化）
# 将 wait SDK 和 parse 合并为单个 evaluate，减少 1 次进程启动
$BROWSER evaluate \
    --fn "$(cat "$SCRIPT_DIR/static/wait-and-parse.fn.js")" \
    >"$DATA_FILE.raw"

# 从 --json 包装中提取 .result，写入最终数据文件（含 _debugKey 供 clip-note 串联日志）
# 仅使用 process.env.YOUDAONOTE_CLIP_DEBUG（OpenClaw 注入），不读取 openclaw.json
TARGET_URL="$TARGET_URL" DATA_FILE="$DATA_FILE" YOUDAONOTE_CLIP_DEBUG="${YOUDAONOTE_CLIP_DEBUG:-}" node -e "
  const fs = require('fs');
  const path = require('path');
  const raw = JSON.parse(fs.readFileSync(process.env.DATA_FILE + '.raw', 'utf-8'));
  const d = raw.result ?? raw;
  const debugDir = (process.env.YOUDAONOTE_CLIP_DEBUG || '').trim();
  if (debugDir) {
    d._debugKey = require('crypto').randomUUID().slice(0, 8);
    const logDir = path.join(debugDir, d._debugKey);
    fs.mkdirSync(logDir, { recursive: true });
    const ts = new Date().toISOString();
    const url = process.env.TARGET_URL || '';
    fs.appendFileSync(path.join(logDir, 'collect.log'), '[' + ts + '] 路径: C (collect-page 浏览器) URL=' + url + ' steps=open,wait,parse\n');
  }
  d._source = 'collect';
  fs.writeFileSync(process.env.DATA_FILE, JSON.stringify(d));
  console.log(JSON.stringify({ title: d.title, imageCount: (d.imageUrls||[]).length, source: d.source, contentLength: (d.content||'').length }));
"

# 清理临时文件
rm -f "$DATA_FILE.raw"
