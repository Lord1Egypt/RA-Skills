#!/bin/bash
# 企业微信 Webhook 公共函数库

# 全局变量
WECOM_CURRENT_URL=""    # 当前使用的 webhook URL
WECOM_CURRENT_CHATID="" # 当前使用的会话 ID

# 注册表文件路径（可通过环境变量覆盖）
WECOM_REGISTRY_FILE="${WECOM_REGISTRY_FILE:-$HOME/.wecom/chat_registry.json}"

# ============================================================================
# 注册表管理函数
# ============================================================================

# 确保注册表目录和文件存在
ensure_registry() {
    local dir
    dir=$(dirname "$WECOM_REGISTRY_FILE")
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
    fi
    if [ ! -f "$WECOM_REGISTRY_FILE" ]; then
        echo '{}' > "$WECOM_REGISTRY_FILE"
    fi
}

# 注册 name -> { url, chatid, chat_type } 映射
# 用法: register_chat <name> <webhook_url> [chatid] [chat_type]
# chatid 可选，不提供则发送到 webhook 默认群
# chat_type 可选，single 表示私聊，group 表示群聊（默认）
register_chat() {
    local name="$1"
    local url="$2"
    local chatid="${3:-}"
    local chat_type="${4:-group}"

    if [ -z "$name" ] || [ -z "$url" ]; then
        echo "错误: 需要提供名称和 webhook URL" >&2
        return 1
    fi

    ensure_registry

    local tmp_file
    tmp_file=$(mktemp)

    if [ -n "$chatid" ]; then
        jq --arg name "$name" --arg url "$url" --arg chatid "$chatid" --arg chat_type "$chat_type" \
            '.[$name] = { url: $url, chatid: $chatid, chat_type: $chat_type }' "$WECOM_REGISTRY_FILE" > "$tmp_file"
        echo "✅ 已注册: $name"
        echo "   类型: $chat_type"
        echo "   URL: $url"
        echo "   ChatID: $chatid"
    else
        jq --arg name "$name" --arg url "$url" --arg chat_type "$chat_type" \
            '.[$name] = { url: $url, chat_type: $chat_type }' "$WECOM_REGISTRY_FILE" > "$tmp_file"
        echo "✅ 已注册: $name"
        echo "   类型: $chat_type"
        echo "   URL: $url"
        echo "   ChatID: (默认群)"
    fi

    mv "$tmp_file" "$WECOM_REGISTRY_FILE"
}

# 删除注册
# 用法: unregister_chat <name>
unregister_chat() {
    local name="$1"

    if [ -z "$name" ]; then
        echo "错误: 需要提供名称" >&2
        return 1
    fi

    ensure_registry

    local tmp_file
    tmp_file=$(mktemp)
    jq --arg name "$name" 'del(.[$name])' "$WECOM_REGISTRY_FILE" > "$tmp_file" \
        && mv "$tmp_file" "$WECOM_REGISTRY_FILE"

    echo "✅ 已删除: $name"
}

# 通过名称查找注册信息
# 用法: lookup_chat <name>
# 设置全局变量 WECOM_CURRENT_URL 和 WECOM_CURRENT_CHATID
# 返回: 0 成功, 1 失败
lookup_chat() {
    local name="$1"

    if [ -z "$name" ]; then
        return 1
    fi

    ensure_registry

    local entry
    entry=$(jq -r --arg name "$name" '.[$name] // empty' "$WECOM_REGISTRY_FILE")

    if [ -z "$entry" ]; then
        return 1
    fi

    # 提取 url 和 chatid
    local url chatid
    url=$(echo "$entry" | jq -r '.url // empty')
    chatid=$(echo "$entry" | jq -r '.chatid // empty')

    if [ -n "$url" ]; then
        WECOM_CURRENT_URL="$url"
    fi
    if [ -n "$chatid" ]; then
        WECOM_CURRENT_CHATID="$chatid"
    fi

    return 0
}

# 列出所有注册
# 用法: list_chats
list_chats() {
    ensure_registry

    local count
    count=$(jq 'length' "$WECOM_REGISTRY_FILE")

    if [ "$count" -eq 0 ]; then
        echo "注册表为空"
        return 0
    fi

    echo "已注册的会话 ($count 个):"
    echo "========================================"

    jq -r 'to_entries | .[] | "\(.key):\n  类型: \(.value.chat_type // "group")\n  URL: \(.value.url)\n  ChatID: \(.value.chatid // "(默认群)")\n"' "$WECOM_REGISTRY_FILE"
}

# ============================================================================
# 参数解析函数
# ============================================================================

# 解析 --url、--chatid、--to 参数，返回剩余参数
# 用法: eval "$(parse_wecom_args "$@")"
# 设置 WECOM_CURRENT_URL、WECOM_CURRENT_CHATID 并输出剩余参数
parse_wecom_args() {
    local url=""
    local chatid=""
    local to_name=""
    local args=()

    while [ $# -gt 0 ]; do
        case "$1" in
            --url)
                url="$2"
                shift 2
                ;;
            --url=*)
                url="${1#--url=}"
                shift
                ;;
            --chatid)
                chatid="$2"
                shift 2
                ;;
            --chatid=*)
                chatid="${1#--chatid=}"
                shift
                ;;
            --to)
                to_name="$2"
                shift 2
                ;;
            --to=*)
                to_name="${1#--to=}"
                shift
                ;;
            *)
                args+=("$1")
                shift
                ;;
        esac
    done

    # --to 参数：通过名称查找 url 和 chatid
    if [ -n "$to_name" ]; then
        if ! lookup_chat "$to_name"; then
            echo "错误: 未找到名称 '$to_name' 的注册，请先用 register_chat.sh 注册" >&2
            exit 1
        fi
        # lookup_chat 已设置 WECOM_CURRENT_URL 和 WECOM_CURRENT_CHATID
    fi

    # 命令行参数覆盖注册表的值
    if [ -n "$url" ]; then
        WECOM_CURRENT_URL="$url"
    elif [ -z "$WECOM_CURRENT_URL" ]; then
        WECOM_CURRENT_URL="${WECOM_WEBHOOK_URL:-}"
    fi

    if [ -n "$chatid" ]; then
        WECOM_CURRENT_CHATID="$chatid"
    elif [ -z "$WECOM_CURRENT_CHATID" ]; then
        WECOM_CURRENT_CHATID="${WECOM_CHATID:-}"
    fi

    # 输出剩余参数供调用方使用
    printf '%q ' "${args[@]}"
}

# 兼容旧版函数名
parse_url_arg() {
    parse_wecom_args "$@"
}

# ============================================================================
# URL 和发送函数
# ============================================================================

# 检查 webhook URL 是否已设置
check_wecom_url() {
    if [ -z "$WECOM_CURRENT_URL" ]; then
        echo "错误: 未指定 Webhook URL" >&2
        echo "方式1: --to '<已注册名称>'" >&2
        echo "方式2: --url 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx'" >&2
        echo "方式3: export WECOM_WEBHOOK_URL='https://...'" >&2
        echo "获取: 企业微信群 → 群设置 → 群机器人 → 添加 → 复制 Webhook 地址" >&2
        exit 1
    fi
}

# 兼容旧版：检查环境变量（已弃用，保留兼容）
check_wecom_env() {
    if [ -z "$WECOM_CURRENT_URL" ]; then
        WECOM_CURRENT_URL="${WECOM_WEBHOOK_URL:-}"
    fi
    check_wecom_url
}

# 构建发送 URL（不含 chatid，chatid 放在 body 中）
build_send_url() {
    echo "${WECOM_CURRENT_URL:-$WECOM_WEBHOOK_URL}"
}

# 发送消息（底层封装）
# chatid 会自动注入到 JSON body 中
wecom_send() {
    local body="$1"
    local url
    url=$(build_send_url)

    # 如果有 chatid，注入到 JSON body 中
    if [ -n "$WECOM_CURRENT_CHATID" ]; then
        body=$(echo "$body" | jq --arg chatid "$WECOM_CURRENT_CHATID" '. + {chatid: $chatid}')
    fi

    local resp
    resp=$(curl -s -X POST "$url" \
        -H "Content-Type: application/json" \
        -d "$body")

    local errcode
    errcode=$(echo "$resp" | jq -r '.errcode // -1')
    if [ "$errcode" != "0" ]; then
        local errmsg
        errmsg=$(echo "$resp" | jq -r '.errmsg // "未知错误"')
        echo "错误: 发送失败 (errcode=${errcode}): ${errmsg}" >&2
        return 1
    fi

    return 0
}
