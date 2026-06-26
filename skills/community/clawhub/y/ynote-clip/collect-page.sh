#!/usr/bin/env bash
set -euo pipefail

# collect-page.sh — 通过 openclaw browser CLI 提取网页内容到文件
#
# 用法：bash collect-page.sh <URL> [DATA_FILE]
#
# 参数：
#   URL        — 目标网页 URL（必需）
#   DATA_FILE  — 输出 JSON 文件路径（默认 /tmp/ynote-clip-data.json）
#
# 输出：
#   文件：DATA_FILE（包含 title、content、imageUrls、source）
#   stdout 最后一行：metadata JSON（仅 title、imageCount、source、contentLength）
#
# bodyHtml 直接写入文件，不经过 agent context window。

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

TARGET_URL="${1:?用法: bash collect-page.sh <URL> [DATA_FILE]}"
DATA_FILE="${2:-/tmp/ynote-clip-data.json}"
PROFILE="openclaw"

# --json 全局选项：禁用 @clack/prompts spinner（否则控制字符污染 stdout）
BROWSER="openclaw browser --json --browser-profile $PROFILE"

# Step 1: 打开页面
$BROWSER open "$TARGET_URL" >/dev/null

# Step 2: 等待加载
$BROWSER wait --load networkidle --timeout-ms 15000 >/dev/null

# Step 3: 注入 collect SDK（预生成文件，无运行时 base64 编码）
$BROWSER evaluate \
    --fn "$(cat "$SCRIPT_DIR/static/inject-sdk.fn.js")" \
    >/dev/null

# Step 4: 等待 SDK 挂载
$BROWSER wait \
    --fn "typeof window.collectParser !== 'undefined'" --timeout-ms 10000 \
    >/dev/null

# Step 5: 解析内容 → 直接写入文件（bodyHtml 绕过 agent）
# --json 输出格式: {"ok":true, "result": {...}}，需提取 .result
$BROWSER evaluate \
    --fn "$(cat "$SCRIPT_DIR/static/parse-page.fn.js")" \
    >"$DATA_FILE.raw"

# 从 --json 包装中提取 .result，写入最终数据文件
node -e "
  const raw = JSON.parse(require('fs').readFileSync('$DATA_FILE.raw','utf-8'));
  const d = raw.result ?? raw;
  require('fs').writeFileSync('$DATA_FILE', JSON.stringify(d));
  console.log(JSON.stringify({ title: d.title, imageCount: (d.imageUrls||[]).length, source: d.source, contentLength: (d.content||'').length }));
"

# 清理临时文件
rm -f "$DATA_FILE.raw"
