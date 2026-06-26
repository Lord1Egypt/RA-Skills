#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# mcp-call.sh — YNote MCP Tool 调用（纯 curl 实现）
#
# 通过 SSE 传输协议调用 MCP Server 的 Tool。
# 协议：GET /mcp/sse → endpoint → POST initialize → POST tool/call → 读 SSE 响应
#
# 依赖：curl, jq
# 用法：
#   YNOTE_API_KEY=<key> bash {baseDir}/mcp-call.sh <tool_name> '<json_args>'
#
# 示例：
#   bash mcp-call.sh createNote '{"title":"测试","content":"# 内容","folderId":""}'
#   bash mcp-call.sh searchNotes '{"keyword":"MCP"}'
# ─────────────────────────────────────────────

TOOL_NAME="${1:?用法: mcp-call.sh <tool_name> '<json_args>'}"
TOOL_ARGS="${2+$2}"
[ -z "$TOOL_ARGS" ] && TOOL_ARGS='{}'
SSE_URL="${YNOTE_MCP_URL:-https://open.mail.163.com/api/ynote/mcp/sse}"
API_KEY="${YNOTE_API_KEY:?请设置 YNOTE_API_KEY 环境变量}"
TIMEOUT="${YNOTE_MCP_TIMEOUT:-30}"

# BASE_URL = scheme + host（从 SSE_URL 中提取，endpoint 是绝对路径）
BASE_URL=$(echo "$SSE_URL" | sed 's|^\(https\{0,1\}://[^/]*\).*|\1|')

TMPDIR_MCP=$(mktemp -d)
trap 'kill "$SSE_PID" 2>/dev/null; wait "$SSE_PID" 2>/dev/null; rm -rf "$TMPDIR_MCP"' EXIT

SSE_OUT="$TMPDIR_MCP/sse.out"
touch "$SSE_OUT"

# ─── Step 1: SSE 连接，获取 message endpoint ───

curl -sfN \
    -H "Accept: text/event-stream" \
    -H "Cache-Control: no-cache" \
    -H "x-api-key: $API_KEY" \
    "$SSE_URL" >>"$SSE_OUT" 2>/dev/null &
SSE_PID=$!

ENDPOINT=""
for _ in $(seq 1 100); do
    ENDPOINT=$(grep '^data:' "$SSE_OUT" 2>/dev/null | head -1 | sed 's/^data://' || true)
    [ -n "$ENDPOINT" ] && break
    sleep 0.1
done

if [ -z "$ENDPOINT" ]; then
    echo '{"error":"SSE 连接超时，未获取到 endpoint"}' >&2
    exit 1
fi

MESSAGE_URL="${BASE_URL}${ENDPOINT}"

# ─── Step 2: MCP 握手（initialize + initialized）───

curl -sf -X POST "$MESSAGE_URL" \
    -H "Content-Type: application/json" \
    -H "x-api-key: $API_KEY" \
    --max-time "$TIMEOUT" \
    -d "$(jq -nc '{jsonrpc:"2.0",id:1,method:"initialize",params:{protocolVersion:"2024-11-05",capabilities:{},clientInfo:{name:"ynote-clip",version:"1.0.0"}}}')" \
    >/dev/null 2>&1

sleep 0.5

curl -sf -X POST "$MESSAGE_URL" \
    -H "Content-Type: application/json" \
    -H "x-api-key: $API_KEY" \
    --max-time "$TIMEOUT" \
    -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' \
    >/dev/null 2>&1

# ─── Step 3: 调用目标 Tool ───

curl -sf -X POST "$MESSAGE_URL" \
    -H "Content-Type: application/json" \
    -H "x-api-key: $API_KEY" \
    --max-time "$TIMEOUT" \
    -d "$(jq -nc --arg name "$TOOL_NAME" --argjson args "$TOOL_ARGS" \
        '{jsonrpc:"2.0",id:2,method:"tools/call",params:{name:$name,arguments:$args}}')" \
    >/dev/null 2>&1

# ─── Step 4: 从 SSE 流提取 id=2 响应 ───

RESULT=""
for _ in $(seq 1 $((TIMEOUT * 10))); do
    RESULT=$(grep '^data:{' "$SSE_OUT" 2>/dev/null |
        sed 's/^data://' |
        jq -c 'select(.id == 2)' 2>/dev/null |
        head -1 || true)
    [ -n "$RESULT" ] && break
    sleep 0.1
done

if [ -z "$RESULT" ]; then
    echo '{"error":"Tool 调用超时，未收到响应"}' >&2
    exit 1
fi

# 输出 Tool 结果文本（MCP 标准格式：result.content[].text）
echo "$RESULT" | jq -r '.result.content[]?.text // .error.message // "未知响应"'
