#!/bin/bash
# 智谱网页读取脚本 (Web Reader)
# 使用 Z.AI Coding Plan MCP 端点（免费额度）
# 设置 ZHIPU_USE_MCP=false 切换到旧版 bigmodel API

set -e

API_KEY="${ZHIPU_API_KEY:?请设置 ZHIPU_API_KEY 环境变量}"
USE_MCP="${ZHIPU_USE_MCP:-true}"

if [ -z "$1" ]; then
    echo "用法: $0 <URL>"
    echo "示例: $0 'https://www.example.com'"
    echo ""
    echo "环境变量:"
    echo "  ZHIPU_API_KEY   - 智谱 API Key (必填)"
    echo "  ZHIPU_USE_MCP   - 使用 MCP 模式: true(默认) / false"
    exit 1
fi

TARGET_URL="$1"

# 旧版 bigmodel API 网页读取
_reader_legacy() {
    local url="$1"
    curl -s --request POST \
        --url "https://open.bigmodel.cn/api/paas/v4/reader" \
        --header "Authorization: Bearer $API_KEY" \
        --header 'Content-Type: application/json' \
        --data "{\"url\": \"$url\"}"
}

# MCP 模式网页读取 (Z.AI Coding Plan)
# 端点: https://api.z.ai/api/mcp/web_reader/mcp
# 工具: webReader
_reader_mcp() {
    local url="$1"
    local mcp_url="https://api.z.ai/api/mcp/web_reader/mcp"
    local tmpfile
    tmpfile=$(mktemp)
    trap 'rm -f "$tmpfile"' EXIT

    # Step 1: Initialize
    local init_resp
    init_resp=$(curl -s -D "$tmpfile" --request POST \
        --url "$mcp_url" \
        --header "Authorization: Bearer $API_KEY" \
        --header 'Content-Type: application/json' \
        --header 'Accept: text/event-stream, application/json' \
        --data '{
            "jsonrpc":"2.0","id":1,
            "method":"initialize",
            "params":{
                "protocolVersion":"2024-11-05",
                "capabilities":{},
                "clientInfo":{"name":"openclaw-zhipu-tools","version":"1.1.0"}
            }
        }')

    local session_id
    session_id=$(grep -i 'mcp-session-id' "$tmpfile" | sed 's/.*: *//;s/\r//;s/ *$//' | tr -d '\n')

    if [ -z "$session_id" ]; then
        echo "错误: MCP 初始化失败，未获取到 session id" >&2
        echo "$init_resp" >&2
        return 1
    fi

    # Step 2: Notify initialized
    curl -s --request POST \
        --url "$mcp_url" \
        --header "Authorization: Bearer $API_KEY" \
        --header "Content-Type: application/json" \
        --header "Accept: application/json" \
        --header "Mcp-Session-Id: $session_id" \
        --data '{"jsonrpc":"2.0","method":"notifications/initialized"}' > /dev/null

    # Step 3: Call webReader
    curl -s --request POST \
        --url "$mcp_url" \
        --header "Authorization: Bearer $API_KEY" \
        --header "Content-Type: application/json" \
        --header 'Accept: text/event-stream, application/json' \
        --header "Mcp-Session-Id: $session_id" \
        --data "{
            \"jsonrpc\":\"2.0\",\"id\":2,
            \"method\":\"tools/call\",
            \"params\":{
                \"name\":\"webReader\",
                \"arguments\":{\"url\":\"$url\"}
            }
        }" | sed 's/^data: *//' | grep -v '^$' | python3 -c "
import sys, json
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    try:
        obj = json.loads(line)
        if 'result' in obj and 'content' in obj['result']:
            for c in obj['result']['content']:
                if c.get('type') == 'text':
                    print(c['text'])
        elif 'error' in obj:
            print(json.dumps(obj['error'], ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
    except json.JSONDecodeError:
        print(line)
" 2>/dev/null
}

if [ "$USE_MCP" = "false" ]; then
    _reader_legacy "$TARGET_URL"
else
    _reader_mcp "$TARGET_URL" || _reader_legacy "$TARGET_URL"
fi
