#!/bin/bash
# 飞书 OAuth 授权脚本 - 自动化版本
# 支持：(1) 自动刷新 token (2) 检测消息上下文用户 (3) 静默授权

set -e

# 配置
APP_ID="cli_a92fba8c65e35cc4"
APP_SECRET="UFUvM2wNSkErIxe7t63ZrgyecakLwNQR"
REDIRECT_URI="https://auth.waynec619.com/feishu/oauth/callback"

# 日历相关权限 Scope
SCOPE="contact:user.base:readonly calendar:calendar calendar:calendar.event calendar:room"

# 存储路径
CREDENTIALS_DIR="/root/.openclaw/credentials"
TOKEN_FILE="$CREDENTIALS_DIR/feishu-user-token.json"
STATE_FILE="$CREDENTIALS_DIR/feishu-oauth-state.json"
AUTHORIZED_USERS_FILE="$CREDENTIALS_DIR/feishu-authorized-users.json"

mkdir -p "$CREDENTIALS_DIR"

# 获取 tenant_access_token
get_tenant_token() {
    curl -s "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
        -H "Content-Type: application/json" \
        -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | jq -r '.tenant_access_token'
}

# 检查并获取有效的 user_access_token（自动刷新）
get_valid_user_token() {
    local user_open_id="${1:-}"
    
    # 如果没有指定用户，使用当前已保存的用户
    if [ -z "$user_open_id" ] && [ -f "$TOKEN_FILE" ]; then
        user_open_id=$(cat "$TOKEN_FILE" | jq -r '.user_open_id // empty')
    fi
    
    if [ -z "$user_open_id" ]; then
        echo ""
        return 1
    fi
    
    # 检查已授权用户列表
    if [ -f "$AUTHORIZED_USERS_FILE" ]; then
        local user_data=$(cat "$AUTHORIZED_USERS_FILE" | jq -r --arg id "$user_open_id" '.[$id] // empty')
        if [ -n "$user_data" ] && [ "$user_data" != "null" ]; then
            local access_token=$(echo "$user_data" | jq -r '.access_token // empty')
            local expires_at=$(echo "$user_data" | jq -r '.expires_at // 0')
            local refresh_token=$(echo "$user_data" | jq -r '.refresh_token // empty')
            local now=$(date +%s)
            
            # Token 仍然有效
            if [ -n "$access_token" ] && [ "$expires_at" -gt "$((now + 300))" ]; then
                echo "$access_token"
                return 0
            fi
            
            # Token 过期但有 refresh_token，尝试刷新
            if [ -n "$refresh_token" ]; then
                local new_token=$(refresh_user_token "$user_open_id" "$refresh_token")
                if [ -n "$new_token" ]; then
                    echo "$new_token"
                    return 0
                fi
            fi
        fi
    fi
    
    # 检查旧的 token 文件（兼容）
    if [ -f "$TOKEN_FILE" ]; then
        local token_data=$(cat "$TOKEN_FILE")
        local saved_open_id=$(echo "$token_data" | jq -r '.user_open_id // empty')
        
        if [ "$saved_open_id" = "$user_open_id" ]; then
            local access_token=$(echo "$token_data" | jq -r '.access_token // empty')
            local expires_at=$(echo "$token_data" | jq -r '.expires_at // 0')
            local refresh_token=$(echo "$token_data" | jq -r '.refresh_token // empty')
            local now=$(date +%s)
            
            if [ -n "$access_token" ] && [ "$expires_at" -gt "$((now + 300))" ]; then
                echo "$access_token"
                return 0
            fi
            
            if [ -n "$refresh_token" ]; then
                local new_token=$(refresh_user_token "$user_open_id" "$refresh_token")
                if [ -n "$new_token" ]; then
                    echo "$new_token"
                    return 0
                fi
            fi
        fi
    fi
    
    echo ""
    return 1
}

# 刷新用户 token
refresh_user_token() {
    local user_open_id="$1"
    local refresh_tok="$2"
    
    local tenant_token=$(get_tenant_token)
    
    local result=$(curl -s "https://open.feishu.cn/open-apis/authen/v1/refresh_access_token" \
        -H "Authorization: Bearer $tenant_token" \
        -H "Content-Type: application/json" \
        -d "{\"grant_type\":\"refresh_token\",\"refresh_token\":\"$refresh_tok\"}")
    
    local code_check=$(echo "$result" | jq -r '.code // -1')
    
    if [ "$code_check" != "0" ]; then
        return 1
    fi
    
    local access_token=$(echo "$result" | jq -r '.data.access_token')
    local new_refresh=$(echo "$result" | jq -r '.data.refresh_token')
    local expires_in=$(echo "$result" | jq -r '.data.expires_in')
    local now=$(date +%s)
    
    # 保存到已授权用户列表
    save_user_token "$user_open_id" "$access_token" "$new_refresh" "$((now + expires_in))"
    
    echo "$access_token"
}

# 保存用户 token
save_user_token() {
    local user_open_id="$1"
    local access_token="$2"
    local refresh_token="$3"
    local expires_at="$4"
    local user_name="${5:-}"
    
    # 初始化文件
    if [ ! -f "$AUTHORIZED_USERS_FILE" ]; then
        echo "{}" > "$AUTHORIZED_USERS_FILE"
    fi
    
    # 更新用户数据
    local temp_file=$(mktemp)
    cat "$AUTHORIZED_USERS_FILE" | jq --arg id "$user_open_id" \
        --arg at "$access_token" \
        --arg rt "$refresh_token" \
        --argjson exp "$expires_at" \
        --arg name "$user_name" \
        '.[$id] = {
            "access_token": $at,
            "refresh_token": $rt,
            "expires_at": $exp,
            "user_name": $name,
            "updated_at": (now | todate)
        }' > "$temp_file"
    
    mv "$temp_file" "$AUTHORIZED_USERS_FILE"
    
    # 同时保存到旧的 token 文件（兼容）
    cat > "$TOKEN_FILE" << EOF
{
    "user_open_id": "$user_open_id",
    "user_name": "$user_name",
    "access_token": "$access_token",
    "refresh_token": "$refresh_token",
    "expires_at": $expires_at,
    "created_at": "$(date -Iseconds)",
    "scope": "$SCOPE"
}
EOF
}

# 检查用户授权状态（支持指定用户）
check_auth() {
    local user_open_id="${1:-}"
    
    if [ -z "$user_open_id" ] && [ -f "$TOKEN_FILE" ]; then
        user_open_id=$(cat "$TOKEN_FILE" | jq -r '.user_open_id // empty')
    fi
    
    if [ -z "$user_open_id" ]; then
        echo "NEED_AUTH"
        return 1
    fi
    
    local token=$(get_valid_user_token "$user_open_id")
    if [ -n "$token" ]; then
        echo "AUTHORIZED"
        return 0
    fi
    
    echo "NEED_AUTH"
    return 1
}

# 生成授权链接
generate_auth() {
    local user_open_id="${1:-}"
    local state="feishu_cal_$(date +%s)_$(openssl rand -hex 8)"
    
    # 如果有用户 ID，绑定到 state
    if [ -n "$user_open_id" ]; then
        state="${state}_${user_open_id}"
    fi
    
    local encoded_redirect=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$REDIRECT_URI', safe=''))")
    local encoded_scope=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$SCOPE', safe=''))")
    
    # 保存 state（10分钟过期）
    local now=$(date +%s)
    cat > "$STATE_FILE" << EOF
{
    "state": "$state",
    "user_open_id": "$user_open_id",
    "created_at": $now,
    "expires_at": $((now + 600)),
    "scope": "$SCOPE"
}
EOF
    
    echo "https://open.feishu.cn/open-apis/authen/v1/authorize?app_id=$APP_ID&redirect_uri=$encoded_redirect&response_type=code&state=$state&scope=$encoded_scope"
}

# 用 code 换取 token
exchange_token() {
    local code="$1"
    
    if [ -z "$code" ]; then
        echo "❌ 缺少 code 参数"
        exit 1
    fi
    
    local tenant_token=$(get_tenant_token)
    
    local result=$(curl -s "https://open.feishu.cn/open-apis/authen/v1/access_token" \
        -H "Authorization: Bearer $tenant_token" \
        -H "Content-Type: application/json" \
        -d "{\"grant_type\":\"authorization_code\",\"code\":\"$code\"}")
    
    local code_check=$(echo "$result" | jq -r '.code // -1')
    
    if [ "$code_check" != "0" ]; then
        echo "❌ Token 换取失败: $(echo "$result" | jq -r '.msg')"
        exit 1
    fi
    
    local access_token=$(echo "$result" | jq -r '.data.access_token')
    local refresh_token=$(echo "$result" | jq -r '.data.refresh_token')
    local expires_in=$(echo "$result" | jq -r '.data.expires_in')
    local user_name=$(echo "$result" | jq -r '.data.name')
    local open_id=$(echo "$result" | jq -r '.data.open_id')
    
    local now=$(date +%s)
    
    # 保存
    save_user_token "$open_id" "$access_token" "$refresh_token" "$((now + expires_in))" "$user_name"
    
    echo "✅ 授权成功: $user_name"
}

# 列出已授权用户
list_authorized_users() {
    if [ -f "$AUTHORIZED_USERS_FILE" ]; then
        cat "$AUTHORIZED_USERS_FILE" | jq 'to_entries[] | {open_id: .key, user_name: .value.user_name, expires_at: .value.expires_at}'
    else
        echo "暂无已授权用户"
    fi
}

# 帮助
show_help() {
    cat << EOF
飞书 OAuth 授权工具（自动化版本）

用法:
    $0 check-auth [user_open_id]    检查授权状态
    $0 get-token [user_open_id]     获取有效的 access_token
    $0 generate-auth [user_open_id] 生成授权链接
    $0 exchange-token <code>        用 code 换取 token
    $0 list-users                   列出已授权用户

特性:
    - 自动刷新过期 token
    - 支持多用户授权管理
    - 静默授权（后台刷新）
EOF
}

# 主入口
case "${1:-}" in
    check-auth)
        check_auth "$2"
        ;;
    get-token)
        get_valid_user_token "$2"
        ;;
    generate-auth)
        generate_auth "$2"
        ;;
    exchange-token)
        exchange_token "$2"
        ;;
    list-users)
        list_authorized_users
        ;;
    *)
        show_help
        ;;
esac
