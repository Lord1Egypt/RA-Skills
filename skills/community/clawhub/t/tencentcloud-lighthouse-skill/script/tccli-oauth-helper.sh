#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# tccli OAuth 登录辅助工具
#
# 解决 tccli auth login --browser no 在非交互式环境下无法输入验证码的问题。
#
# 用法:
#   # 第一步: 生成授权链接
#   bash scripts/tccli-oauth-helper.sh --get-url
#
#   # 第二步: 用户访问链接登录后，获取 base64 验证码，然后:
#   bash scripts/tccli-oauth-helper.sh --code "验证码字符串"
#
#   # 或者一步完成（如果已有验证码）:
#   bash scripts/tccli-oauth-helper.sh --code "eyJhY2Nlc3NUb2tlbi..."
#
#   # 检查凭证状态:
#   bash scripts/tccli-oauth-helper.sh --status
#

set -euo pipefail

# ─── 默认常量 ─────────────────────────────────────────────────
APP_ID=100038427476
AUTH_URL="https://cloud.tencent.com/open/authorize"
REDIRECT_URL="https://cli.cloud.tencent.com/oauth"
SITE="cn"
DEFAULT_LANG="zh-CN"
API_ENDPOINT="https://cli.cloud.tencent.com"

# 状态文件路径
STATE_FILE="${HOME}/.tccli/.oauth_state"

# 默认 profile
PROFILE="default"

# ─── 依赖检查 ─────────────────────────────────────────────────
check_deps() {
    local missing=()
    for cmd in curl jq base64; do
        if ! command -v "$cmd" &>/dev/null; then
            missing+=("$cmd")
        fi
    done
    if [ ${#missing[@]} -gt 0 ]; then
        echo "❌ 缺少依赖工具: ${missing[*]}"
        echo ""
        echo "请先安装："
        echo "  macOS:  brew install ${missing[*]}"
        echo "  Ubuntu: sudo apt-get install -y ${missing[*]}"
        echo "  CentOS: sudo yum install -y ${missing[*]}"
        exit 1
    fi
}

# ─── URL 编码 ─────────────────────────────────────────────────
urlencode() {
    local string="$1"
    python3 -c "import urllib.parse; print(urllib.parse.quote_plus('$string'))" 2>/dev/null \
        || printf '%s' "$string" | curl -Gso /dev/null -w '%{url_effective}' --data-urlencode @- '' 2>/dev/null | sed 's/^.\///' \
        || printf '%s' "$string" | sed 's/ /%20/g; s/!/%21/g; s/"/%22/g; s/#/%23/g; s/\$/%24/g; s/&/%26/g; s/'\''/%27/g; s/(/%28/g; s/)/%29/g; s/+/%2B/g; s/,/%2C/g; s/:/%3A/g; s/;/%3B/g; s/=/%3D/g; s/?/%3F/g; s/@/%40/g'
}

# ─── 工具函数 ─────────────────────────────────────────────────

# 生成随机 state (10个字母数字字符)
generate_state() {
    cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | head -c 10
}

# 生成 UUID
generate_uuid() {
    if command -v uuidgen &>/dev/null; then
        uuidgen | tr '[:upper:]' '[:lower:]'
    elif [ -f /proc/sys/kernel/random/uuid ]; then
        cat /proc/sys/kernel/random/uuid
    else
        # 回退：用随机数拼接
        printf '%04x%04x-%04x-%04x-%04x-%04x%04x%04x\n' \
            $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM
    fi
}

# 凭证文件路径
cred_path_of_profile() {
    local profile="${1:-default}"
    echo "${HOME}/.tccli/${profile}.credential"
}

# 保存 state 到文件
save_state() {
    local state="$1"
    local timestamp
    timestamp=$(date +%s)
    mkdir -p "$(dirname "$STATE_FILE")"
    printf '{"state":"%s","timestamp":%s}' "$state" "$timestamp" > "$STATE_FILE"
}

# 加载 state
load_state() {
    if [ ! -f "$STATE_FILE" ]; then
        echo ""
        return
    fi
    local now
    now=$(date +%s)
    local saved_ts
    saved_ts=$(jq -r '.timestamp // 0' "$STATE_FILE" 2>/dev/null || echo "0")
    local diff=$((now - saved_ts))
    # 10分钟超时
    if [ "$diff" -gt 600 ]; then
        echo ""
        return
    fi
    jq -r '.state // empty' "$STATE_FILE" 2>/dev/null || echo ""
}

# 清除 state 文件
clear_state() {
    rm -f "$STATE_FILE"
}

# ─── 生成授权 URL ─────────────────────────────────────────────
get_auth_url() {
    local state="$1"
    local lang="${2:-$DEFAULT_LANG}"

    local redirect_query="browser=no&lang=$(urlencode "$lang")&site=$(urlencode "$SITE")"
    local redirect_url_full="${REDIRECT_URL}?${redirect_query}"

    local url_query="scope=login&app_id=${APP_ID}&redirect_url=$(urlencode "$redirect_url_full")&state=$(urlencode "$state")"
    echo "${AUTH_URL}?${url_query}"
}

# ─── 命令: --get-url ──────────────────────────────────────────
do_get_url() {
    local state
    state=$(generate_state)
    save_state "$state"

    local auth_url
    auth_url=$(get_auth_url "$state")

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔐 腾讯云 OAuth 授权登录"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "请在浏览器中打开以下链接完成登录："
    echo ""
    echo "$auth_url"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "登录后，页面会显示一串 base64 编码的验证码。"
    echo "请复制该验证码，然后运行以下命令完成登录："
    echo ""
    echo "  bash scripts/tccli-oauth-helper.sh --code \"验证码\""
    echo ""
    echo "或发送给 AI 助手，让它帮你完成登录。"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📌 State: ${state} (10分钟内有效)"
}

# ─── 命令: --code ─────────────────────────────────────────────
do_login_with_code() {
    local code="$1"

    # 尝试加载保存的 state
    local saved_state
    saved_state=$(load_state)

    # 解码 base64 验证码
    local token_json
    token_json=$(echo "$code" | base64 -d 2>/dev/null || base64 -D <<< "$code" 2>/dev/null)
    if [ -z "$token_json" ]; then
        echo "❌ 验证码解析失败"
        echo ""
        echo "请确保复制了完整的 base64 验证码字符串。"
        exit 1
    fi

    # 验证 JSON 格式
    if ! echo "$token_json" | jq empty 2>/dev/null; then
        echo "❌ 验证码解析失败: 不是有效的 JSON"
        echo ""
        echo "请确保复制了完整的 base64 验证码字符串。"
        exit 1
    fi

    # 提取 token 字段
    local access_token open_id expires_at refresh_token token_site token_state
    access_token=$(echo "$token_json" | jq -r '.accessToken // empty')
    open_id=$(echo "$token_json" | jq -r '.openId // empty')
    expires_at=$(echo "$token_json" | jq -r '.expiresAt // empty')
    refresh_token=$(echo "$token_json" | jq -r '.refreshToken // empty')
    token_site=$(echo "$token_json" | jq -r '.site // empty')
    token_state=$(echo "$token_json" | jq -r '.state // empty')

    if [ -z "$access_token" ]; then
        echo "❌ 验证码中缺少 accessToken 字段"
        exit 1
    fi

    # 验证 state
    if [ -n "$saved_state" ] && [ -n "$token_state" ] && [ "$token_state" != "$saved_state" ]; then
        echo "⚠️  警告: state 不匹配"
        echo "   期望: ${saved_state}"
        echo "   实际: ${token_state}"
        echo ""
        echo "可能是使用了旧的授权链接。继续尝试..."
    fi

    # 获取临时凭证
    echo "🔄 正在获取临时凭证..."

    local site="${token_site:-$SITE}"
    local trace_id
    trace_id=$(generate_uuid)

    local api_url="${API_ENDPOINT}/get_temp_cred"
    local request_body
    request_body=$(printf '{"TraceId":"%s","AccessToken":"%s","Site":"%s"}' "$trace_id" "$access_token" "$site")

    local response
    response=$(curl -s -X POST "$api_url" \
        -H "Content-Type: application/json" \
        -d "$request_body" 2>&1)

    if [ -z "$response" ]; then
        echo "❌ 登录失败: 无法连接到 API 服务器"
        exit 1
    fi

    # 检查错误
    local has_error
    has_error=$(echo "$response" | jq -r 'has("Error")' 2>/dev/null || echo "true")
    if [ "$has_error" = "true" ]; then
        echo "❌ 登录失败: $response"
        exit 1
    fi

    # 提取凭证
    local secret_id secret_key token cred_expires_at
    secret_id=$(echo "$response" | jq -r '.SecretId')
    secret_key=$(echo "$response" | jq -r '.SecretKey')
    token=$(echo "$response" | jq -r '.Token')
    cred_expires_at=$(echo "$response" | jq -r '.ExpiresAt')

    # 保存凭证
    local cred_path
    cred_path=$(cred_path_of_profile "$PROFILE")
    mkdir -p "$(dirname "$cred_path")"

    cat > "$cred_path" <<EOF
{
    "type": "oauth",
    "secretId": "${secret_id}",
    "secretKey": "${secret_key}",
    "token": "${token}",
    "expiresAt": ${cred_expires_at},
    "oauth": {
        "openId": "${open_id}",
        "accessToken": "${access_token}",
        "expiresAt": ${expires_at:-0},
        "refreshToken": "${refresh_token}",
        "site": "${site}"
    }
}
EOF

    clear_state

    # 格式化过期时间
    local expire_display
    if date --version &>/dev/null 2>&1; then
        # GNU date (Linux)
        expire_display=$(date -d "@${cred_expires_at}" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "$cred_expires_at")
    else
        # BSD date (macOS)
        expire_display=$(date -r "${cred_expires_at}" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "$cred_expires_at")
    fi

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ OAuth 登录成功!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📌 配置文件: ${PROFILE}"
    echo "📌 凭证路径: ${cred_path}"
    echo "📌 过期时间: ${expire_display}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "现在可以使用 tccli 了，例如："
    echo "  tccli lighthouse DescribeInstances --region ap-guangzhou"
    echo ""
}

# ─── 命令: --status ───────────────────────────────────────────
do_status() {
    local cred_path
    cred_path=$(cred_path_of_profile "$PROFILE")

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔍 tccli 凭证状态检查"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📌 配置文件: ${PROFILE}"
    echo "📌 凭证路径: ${cred_path}"
    echo ""

    if [ ! -f "$cred_path" ]; then
        echo "❌ 凭证文件不存在"
        echo ""
        echo "请先运行 OAuth 登录:"
        echo "  bash scripts/tccli-oauth-helper.sh --get-url"
        exit 1
    fi

    local cred_type
    cred_type=$(jq -r '.type // "unknown"' "$cred_path" 2>/dev/null || echo "unknown")
    echo "📌 凭证类型: ${cred_type}"

    if [ "$cred_type" = "oauth" ]; then
        local cred_expires_at now remaining
        cred_expires_at=$(jq -r '.expiresAt // 0' "$cred_path" 2>/dev/null || echo "0")
        now=$(date +%s)

        if [ "$cred_expires_at" -gt "$now" ]; then
            remaining=$((cred_expires_at - now))
            local hours=$((remaining / 3600))
            local minutes=$(( (remaining % 3600) / 60 ))

            local expire_display
            if date --version &>/dev/null 2>&1; then
                expire_display=$(date -d "@${cred_expires_at}" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "$cred_expires_at")
            else
                expire_display=$(date -r "${cred_expires_at}" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "$cred_expires_at")
            fi

            echo "📌 过期时间: ${expire_display}"
            echo "📌 剩余有效期: ${hours}小时${minutes}分钟"
            echo ""
            echo "✅ 凭证有效"
        else
            local expire_display
            if date --version &>/dev/null 2>&1; then
                expire_display=$(date -d "@${cred_expires_at}" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "$cred_expires_at")
            else
                expire_display=$(date -r "${cred_expires_at}" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "$cred_expires_at")
            fi

            echo "📌 过期时间: ${expire_display}"
            echo ""
            echo "❌ 凭证已过期，需要重新登录"
            echo ""
            echo "请运行: bash scripts/tccli-oauth-helper.sh --get-url"
            exit 1
        fi
    else
        # API 密钥方式
        local secret_id
        secret_id=$(jq -r '.secretId // empty' "$cred_path" 2>/dev/null || echo "")
        if [ -n "$secret_id" ]; then
            local id_prefix="${secret_id:0:8}"
            local id_suffix="${secret_id: -4}"
            echo "📌 SecretId: ${id_prefix}...${id_suffix}"
            echo ""
            echo "✅ 使用 API 密钥凭证"
        else
            echo "❌ 凭证文件格式异常"
            exit 1
        fi
    fi

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# ─── 帮助信息 ─────────────────────────────────────────────────
show_help() {
    cat <<'HELP'
tccli OAuth 登录辅助工具

用法:
  bash scripts/tccli-oauth-helper.sh [选项]

选项:
  --get-url             生成 OAuth 授权链接
  --code <验证码>        base64 编码的验证码，用于完成登录
  --status              检查当前凭证状态
  --profile <名称>       配置文件名称 (默认: default)
  --help                显示此帮助信息

示例:
  # 生成授权链接
  bash scripts/tccli-oauth-helper.sh --get-url

  # 使用验证码完成登录
  bash scripts/tccli-oauth-helper.sh --code "eyJhY2Nlc3NUb2tlbi..."

  # 检查凭证状态
  bash scripts/tccli-oauth-helper.sh --status

  # 指定配置文件
  bash scripts/tccli-oauth-helper.sh --code "验证码" --profile myprofile
HELP
}

# ─── 主入口 ───────────────────────────────────────────────────
main() {
    check_deps

    local action=""
    local code_value=""

    while [ $# -gt 0 ]; do
        case "$1" in
            --get-url)
                action="get-url"
                shift
                ;;
            --code)
                action="code"
                code_value="${2:-}"
                if [ -z "$code_value" ]; then
                    echo "❌ --code 需要提供验证码参数"
                    exit 1
                fi
                shift 2
                ;;
            --status)
                action="status"
                shift
                ;;
            --profile)
                PROFILE="${2:-default}"
                shift 2
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                echo "❌ 未知参数: $1"
                echo ""
                show_help
                exit 1
                ;;
        esac
    done

    case "$action" in
        get-url)
            do_get_url
            ;;
        code)
            do_login_with_code "$code_value"
            ;;
        status)
            do_status
            ;;
        *)
            show_help
            exit 1
            ;;
    esac
}

main "$@"
