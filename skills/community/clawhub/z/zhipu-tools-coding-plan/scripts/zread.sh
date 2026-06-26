#!/bin/bash
# 智谱 Zread 脚本 - GitHub 开源仓库文档搜索
# 使用 Z.AI Coding Plan MCP 端点（免费额度）
#
# 端点: https://api.z.ai/api/mcp/zread/mcp
# 工具: search_doc, get_repo_structure, read_file
#
# 用法:
#   bash scripts/zread.sh search <repo> <query>          搜索仓库文档
#   bash scripts/zread.sh structure <repo> [path]        查看仓库目录结构
#   bash scripts/zread.sh read <repo> <file_path>        读取仓库文件
#
# 示例:
#   ZHIPU_API_KEY=xxx bash scripts/zread.sh search "openai/openai" "how to use"
#   ZHIPU_API_KEY=xxx bash scripts/zread.sh structure "openai/openai"
#   ZHIPU_API_KEY=xxx bash scripts/zread.sh read "openai/openai" "README.md"

set -e

API_KEY="${ZHIPU_API_KEY:?请设置 ZHIPU_API_KEY 环境变量}"
MCP_URL="https://api.z.ai/api/mcp/zread/mcp"

if [ -z "$1" ]; then
    echo "智谱 Zread - GitHub 仓库文档搜索工具"
    echo ""
    echo "用法:"
    echo "  $0 search <repo> <query>          搜索仓库文档"
    echo "  $0 structure <repo> [path]        查看目录结构"
    echo "  $0 read <repo> <file_path>        读取仓库文件"
    echo ""
    echo "参数:"
    echo "  repo       - GitHub 仓库 (如 'openai/openai')"
    echo "  query      - 搜索关键词"
    echo "  path       - 目录或文件路径"
    echo ""
    echo "环境变量:"
    echo "  ZHIPU_API_KEY   - 智谱 API Key (必填)"
    exit 1
fi

COMMAND="$1"
shift

# 构建 MCP 初始化并获取 session_id
_mcp_init() {
    local tmpfile
    tmpfile=$(mktemp)
    trap 'rm -f "$tmpfile"' EXIT

    local init_resp
    init_resp=$(curl -s -D "$tmpfile" --request POST \
        --url "$MCP_URL" \
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
        exit 1
    fi

    # Notify initialized
    curl -s --request POST \
        --url "$MCP_URL" \
        --header "Authorization: Bearer $API_KEY" \
        --header "Content-Type: application/json" \
        --header "Accept: application/json" \
        --header "Mcp-Session-Id: $session_id" \
        --data '{"jsonrpc":"2.0","method":"notifications/initialized"}' > /dev/null

    echo "$session_id"
}

# MCP 工具调用
_mcp_call() {
    local session_id="$1"
    local tool_name="$2"
    local arguments="$3"

    curl -s --request POST \
        --url "$MCP_URL" \
        --header "Authorization: Bearer $API_KEY" \
        --header "Content-Type: application/json" \
        --header 'Accept: text/event-stream, application/json' \
        --header "Mcp-Session-Id: $session_id" \
        --data "{
            \"jsonrpc\":\"2.0\",\"id\":2,
            \"method\":\"tools/call\",
            \"params\":{
                \"name\":\"$tool_name\",
                \"arguments\":$arguments
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

# 获取 session
SESSION_ID=$(_mcp_init)

# 执行命令
case "$COMMAND" in
    search)
        REPO="${1:?请指定 GitHub 仓库，如 'openai/openai'}"
        QUERY="${2:?请指定搜索关键词}"
        _mcp_call "$SESSION_ID" "search_doc" "{\"repo\":\"$REPO\",\"query\":\"$QUERY\"}"
        ;;
    structure)
        REPO="${1:?请指定 GitHub 仓库，如 'openai/openai'}"
        SUBPATH="${2:-}"
        if [ -n "$SUBPATH" ]; then
            _mcp_call "$SESSION_ID" "get_repo_structure" "{\"repo\":\"$REPO\",\"path\":\"$SUBPATH\"}"
        else
            _mcp_call "$SESSION_ID" "get_repo_structure" "{\"repo\":\"$REPO\"}"
        fi
        ;;
    read)
        REPO="${1:?请指定 GitHub 仓库，如 'openai/openai'}"
        FILE_PATH="${2:?请指定文件路径，如 'README.md'}"
        _mcp_call "$SESSION_ID" "read_file" "{\"repo\":\"$REPO\",\"path\":\"$FILE_PATH\"}"
        ;;
    *)
        echo "错误: 未知命令 '$COMMAND'" >&2
        echo "支持: search, structure, read" >&2
        exit 1
        ;;
esac
