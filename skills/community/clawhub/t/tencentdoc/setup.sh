#!/bin/bash
#
# Setup script for 腾讯文档 MCP Skill 一体化配置与授权脚本
#
# 功能：
#   1. 检查 mcporter 是否已配置 tencent-docs（含 Authorization 可用）
#   2. 未配置或 Token 失效时，展示授权链接同时后台异步轮询 Token
#   3. 无需用户回复"已授权"，Token 获取后自动写入 mcporter 并继续
#   4. 对超时、过期、错误等场景给出友好提示
#
# 用法（供 AI Agent 调用）：
#   第一步：检查状态（立即返回，不阻塞）
#     bash ./setup.sh tdoc_check_and_start_auth
#     输出：
#       READY                  → 服务已就绪，直接执行用户任务，无需第二步
#       AUTH_REQUIRED:<url>    → 立即向用户展示授权链接，然后执行第二步
#       ERROR:*                → 告知用户对应错误
#
#   第二步：等待授权完成（仅 AUTH_REQUIRED 时执行，阻塞最多约 135s）
#     bash ./setup.sh tdoc_wait_auth
#     输出：
#       TOKEN_READY:*          → 授权成功，继续执行用户任务
#       AUTH_TIMEOUT           → 告知用户：授权超时，请重新发起请求
#       ERROR:expired          → 告知用户：授权码已过期，请重新发起请求
#       ERROR:token_invalid    → 告知用户：Token 已失效，请重新授权
#       ERROR:*                → 告知用户对应错误
#
# 直接执行（排查问题）：
#   bash ./setup.sh
#

# ── 全局配置 ──────────────────────────────────────────────────────────────────
_TDOC_API_BASE="${TDOC_API_BASE_URL:-https://docs.qq.com}"
_TDOC_AUTH_BASE="${TDOC_AUTH_BASE_URL:-https://docs.qq.com/scenario/open-claw.html}"
_TDOC_MCP_URL="https://docs.qq.com/openapi/mcp"
_TDOC_SERVICE_NAME="tencent-docs"

# 轮询参数：每 10s 一次，最多 12 次（约 120s）
_TDOC_POLL_INTERVAL=10
_TDOC_POLL_MAX=12

# 临时文件
_TDOC_CODE_FILE="${TMPDIR:-/tmp}/.tdoc_auth_code"
_TDOC_TOKEN_FILE="${TMPDIR:-/tmp}/.tdoc_auth_token"
_TDOC_ERR_FILE="${TMPDIR:-/tmp}/.tdoc_auth_token.err"
_TDOC_PID_FILE="${TMPDIR:-/tmp}/.tdoc_auth_pid"
_TDOC_URL_FILE="${TMPDIR:-/tmp}/.tdoc_auth_url"

# ── 清理函数 ──────────────────────────────────────────────────────────────────
_tdoc_cleanup() {
    rm -f "$_TDOC_CODE_FILE" "$_TDOC_TOKEN_FILE" "$_TDOC_ERR_FILE" "$_TDOC_PID_FILE" "$_TDOC_URL_FILE"
}

# ── 检查 mcporter 是否已安装 ──────────────────────────────────────────────────
_tdoc_check_mcporter() {
    if ! command -v mcporter &> /dev/null; then
        echo "⚠️  未找到 mcporter，正在安装..."
        if command -v npm &>/dev/null; then
            npm install -g mcporter@0.8.1 2>&1 | tail -3
            echo "✅ mcporter 安装完成"
        else
            echo "ERROR:no_npm"
            return 1
        fi
    fi
    return 0
}

# 从 mcporter config get 读取当前 Authorization Token
# 输出：token 字符串（空则表示服务未注册或 Token 未配置）
_tdoc_get_token() {
    local output
    output=$(mcporter config get "$_TDOC_SERVICE_NAME" 2>/dev/null) || return 1

    # 从输出中提取 Authorization 头的值
    local token
    token=$(echo "$output" | grep -i '^\s*Authorization:' | sed 's/.*Authorization:[[:space:]]*//' | tr -d '[:space:]')
    echo "$token"
}

# ── 将 Token 写入 mcporter 配置 ───────────────────────────────────────────────
# 用法：_tdoc_save_token <token>
_tdoc_save_token() {
    # 添加 MCP 配置
    echo "🔧 配置 mcporter..."

    local token="$1"
    [[ -z "$token" ]] && return 1

    # 使用传入的 token 写入 mcporter 配置（tencent-docs）
    mcporter config add "$_TDOC_SERVICE_NAME" "$_TDOC_MCP_URL" \
        --header "Authorization=$token" \
        --transport http \
        --scope home

    # 同时配置 tencent-docengine（DOC 编辑引擎，独立 API 端点，复用同一 Token）
    mcporter config add tencent-docengine "https://docs.qq.com/api/v6/doc/mcp" \
        --header "Authorization=$token" \
        --transport http \
        --scope home
    
    # 同时配置 tencent-sheetengine（Sheet编辑引擎，独立 API 端点，复用同一 Token）
    mcporter config add tencent-sheetengine "https://docs.qq.com/api/v6/sheet/mcp" \
        --header "Authorization=$token" \
        --transport http \
        --scope home

    echo ""
    echo "✅ 配置完成！"
    echo ""

    echo "🧪 验证配置..."
    if mcporter list 2>&1 | grep -q "$_TDOC_SERVICE_NAME"; then
        echo "✅ tencent-docs 配置验证成功！"
        echo ""
        mcporter list | grep -A 1 "$_TDOC_SERVICE_NAME" || true
    else
        echo "⚠️  tencent-docs 配置验证失败，请检查网络或 Token 是否有效"
    fi

    if mcporter list 2>&1 | grep -q "tencent-docengine"; then
        echo "✅ tencent-docengine 配置验证成功！"
        echo ""
        mcporter list | grep -A 1 "tencent-docengine" || true
    else
        echo "⚠️  tencent-docengine 配置验证失败，请检查网络或 Token 是否有效"
    fi

    if mcporter list 2>&1 | grep -q "tencent-sheetengine"; then
        echo "✅ tencent-sheetengine 配置验证成功！"
        echo ""
        mcporter list | grep -A 1 "tencent-sheetengine" || true
    else
        echo "⚠️  tencent-sheetengine 配置验证失败，请检查网络或 Token 是否有效"
    fi

    echo ""
    echo "如有问题，请访问 ${_TDOC_API_BASE}/scenario/open-claw.html?nlc=1 获取 Token"

    echo ""
    echo "─────────────────────────────────────"
    echo "🎉 设置完成！"
    echo ""
    echo "📖 使用方法："
    echo "   mcporter call ${_TDOC_SERVICE_NAME}.create_smartcanvas_by_markdown"
    echo "   mcporter call tencent-docengine.find"
    echo "   mcporter call tencent-docengine.insert_text"
    echo "   mcporter call tencent-sheetengine.get_sheet_info"
    echo "   mcporter call tencent-sheetengine.set_cell_value"
    echo ""
    echo "🏠 腾讯文档主页：${_TDOC_API_BASE}/home"
    echo ""
    echo "📖 更多信息请查看 SKILL.md"
    echo ""
    return 0
}

# ── 检查 tencent-docs 服务状态 ────────────────────────────────────────────────
# 返回值：
#   0 = 服务正常可用（有 Token）
#   1 = 服务未注册（mcporter config get 失败）
#   2 = Token 为空或未配置
_tdoc_check_service() {
    if ! mcporter list 2>/dev/null | grep -q "$_TDOC_SERVICE_NAME"; then
        return 1
    fi

    local token
    token=$(_tdoc_get_token)
    local rc=$?

    # mcporter config get 返回非 0 表示服务未注册
    if [[ $rc -ne 0 ]]; then
        return 1
    fi

    # Token 为空表示服务已注册但未配置 Authorization
    if [[ -z "$token" ]]; then
        return 2
    fi

    return 0
}

# ── 生成授权链接 ──────────────────────────────────────────────────────────────
# 输出：auth_url 字符串
_tdoc_generate_auth_url() {
    local code
    code=$(openssl rand -hex 8 2>/dev/null || \
           cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' 2>/dev/null | head -c 16 || \
           date +%s%N 2>/dev/null | sha256sum 2>/dev/null | head -c 16 || \
           echo "$(date +%s)$$")

    echo "$code" > "$_TDOC_CODE_FILE"
    echo "${_TDOC_AUTH_BASE}?nlc=1&authType=1&code=${code}&mcp_source=desktop"
}

# ── 后台异步轮询 Token ────────────────────────────────────────────────────────
# 调用前必须已写入 $_TDOC_CODE_FILE
# 成功：写入 $_TDOC_TOKEN_FILE
# 失败：写入 $_TDOC_ERR_FILE（内容：expired / timeout / err_<code>）
_tdoc_start_bg_poll() {
    rm -f "$_TDOC_TOKEN_FILE" "$_TDOC_ERR_FILE"

    local code_file="$_TDOC_CODE_FILE"
    local token_file="$_TDOC_TOKEN_FILE"
    local err_file="$_TDOC_ERR_FILE"
    local pid_file="$_TDOC_PID_FILE"
    local api_base="$_TDOC_API_BASE"
    local poll_interval="$_TDOC_POLL_INTERVAL"
    local poll_max="$_TDOC_POLL_MAX"

    (
        # 等待 code 文件就绪（最多 10s）
        local waited=0
        while [[ ! -f "$code_file" && $waited -lt 10 ]]; do
            sleep 1; waited=$((waited + 1))
        done
        if [[ ! -f "$code_file" ]]; then
            echo "code_timeout" > "$err_file"
            exit 1
        fi

        local code
        code=$(cat "$code_file")
        local url="${api_base}/oauth/v2/mcp/token/get?code=${code}"

        for ((i=1; i<=poll_max; i++)); do
            local response
            response=$(curl -s -f -L "$url" 2>/dev/null) || {
                sleep "$poll_interval"
                continue
            }

            # 提取 token
            local token
            token=$(echo "$response" | jq -r '.data.token // empty' 2>/dev/null || echo "")
            if [[ -n "$token" ]]; then
                echo "$token" > "$token_file"
                rm -f "$code_file" "$pid_file"
                exit 0
            fi

            # 提取错误码
            local ret
            ret=$(echo "$response" | jq -r '.ret // empty' 2>/dev/null || echo "")
            # 11510 = 用户还未授权，继续等待
            if [[ "$ret" == "11510" ]]; then
                sleep "$poll_interval"
                continue
            fi
            local expired
            expired=$(echo "$response" | jq -r '.data.expired // empty' 2>/dev/null || echo "")
            if [[ "$expired" == "true" ]]; then
                echo "expired" > "$err_file"
                rm -f "$code_file" "$pid_file"
                exit 1
            fi
            # 其他错误场景区分
            case "$ret" in
                "14151"|"14152")
                    # 授权码已过期或失效
                    echo "expired" > "$err_file"
                    rm -f "$code_file" "$pid_file"
                    exit 1
                    ;;
                "400006")
                    # Token 鉴权失败
                    echo "err_400006" > "$err_file"
                    rm -f "$code_file" "$pid_file"
                    exit 1
                    ;;
                *)
                    # 其他错误：记录但继续等待，给用户更多时间
                    sleep "$poll_interval"
                    continue
                    ;;
            esac
        done

        # 轮询超时
        echo "timeout" > "$err_file"
        rm -f "$code_file" "$pid_file"
    ) &

    local bg_pid=$!
    echo "$bg_pid" > "$_TDOC_PID_FILE"
    echo "BG_POLL_STARTED:$bg_pid"
}

# ── 前台等待 Token 就绪 ────────────────────────────────────────
# 用法：_tdoc_wait_token [max_seconds]
# 输出：
#   TOKEN_READY:<token>   授权成功
#   AUTH_TIMEOUT          超时
#   ERROR:<reason>        错误
_tdoc_wait_token() {
    local max_wait=$((_TDOC_POLL_MAX * _TDOC_POLL_INTERVAL + 15))
    local elapsed=0

    while [[ $elapsed -lt $max_wait ]]; do
        # Token 就绪
        if [[ -f "$_TDOC_TOKEN_FILE" ]]; then
            local token
            token=$(cat "$_TDOC_TOKEN_FILE")
            if [[ -n "$token" ]]; then
                echo "TOKEN_READY"
                return 0
            fi
        fi

        # 出现错误
        if [[ -f "$_TDOC_ERR_FILE" ]]; then
            local err
            err=$(cat "$_TDOC_ERR_FILE")
            echo "ERROR:$err"
            return 1
        fi

        sleep 1
        elapsed=$((elapsed + 1))
    done

    echo "AUTH_TIMEOUT"
    return 2
}

# ── 执行授权流程（第一阶段）：生成链接并启动后台轮询 ─────────────────────────
# 输出：
#   AUTH_REQUIRED:<url>   立即输出到 stdout，同时写入 $_TDOC_URL_FILE
# 调用方拿到 AUTH_REQUIRED 后应立即展示给用户，然后调用 _tdoc_wait_auth_result
_tdoc_do_auth_start() {
    _tdoc_cleanup

    # 生成授权链接（同时写入 code 文件）
    local auth_url
    auth_url=$(_tdoc_generate_auth_url)

    # 将 URL 写入文件，供后续阶段读取
    echo "$auth_url" > "$_TDOC_URL_FILE"

    # ★ 立即启动后台轮询（与用户操作并行进行）
    _tdoc_start_bg_poll > /dev/null

    # ★ 立即输出授权链接（调用方可立即展示给用户）
    echo "AUTH_REQUIRED:$auth_url"
    return 0
}

# ── 执行授权流程（第二阶段）：等待 Token 并写入配置 ──────────────────────────
# 调用方在展示授权链接后调用此函数，等待用户完成授权
# 输出：
#   TOKEN_READY:<token>   授权成功
#   AUTH_TIMEOUT          超时
#   ERROR:*               错误
_tdoc_wait_auth_result() {
    local result
    result=$(_tdoc_wait_token)

    case "$result" in
        TOKEN_READY)
            local token=$(cat "$_TDOC_TOKEN_FILE")
            if _tdoc_save_token "$token"; then
                _tdoc_cleanup
                echo "TOKEN_READY:$token"
                return 0
            else
                _tdoc_cleanup
                echo "ERROR:save_token_failed"
                return 1
            fi
            ;;
        AUTH_TIMEOUT)
            _tdoc_cleanup
            echo "AUTH_TIMEOUT"
            return 2
            ;;
        ERROR:expired)
            _tdoc_cleanup
            echo "ERROR:expired - 授权码已过期，请重新发起请求"
            return 1
            ;;
        ERROR:err_400006)
            _tdoc_cleanup
            echo "ERROR:token_invalid - Token 鉴权失败，请重新授权"
            return 1
            ;;
        ERROR:*)
            _tdoc_cleanup
            echo "ERROR:unknown - 授权异常，请联系腾讯文档客服"
            return 1
            ;;
    esac
}

# ── 主入口函数 A：检查状态 / 生成授权链接（立即返回，不阻塞）────────────────
#
# AI Agent 第一步调用此函数，命令执行完毕后立即拿到输出：
#   READY                  服务已就绪，直接执行用户任务，无需第二步
#   AUTH_REQUIRED:<url>    需要授权：立即展示链接给用户，然后执行第二步
#   ERROR:*                错误信息
#
tdoc_check_and_start_auth() {
    _tdoc_check_mcporter || {
        echo "ERROR:mcporter_not_found - 请先安装 Node.js 和 npm 后重试"
        return 1
    }

    _tdoc_check_service
    local status=$?

    case $status in
        0)
            echo "READY"
            return 0
            ;;
        1|2)
            _tdoc_do_auth_start
            return 0
            ;;
    esac
}

# ── 主入口函数 B：等待授权完成（阻塞，最多约 135s）────────────────────────────
#
# AI Agent 在展示授权链接后调用此函数，等待用户完成授权：
#   TOKEN_READY:<token>    授权成功，Token 已写入配置，直接执行用户任务
#   AUTH_TIMEOUT           超时，告知用户重新发起请求
#   ERROR:*                错误信息
#
tdoc_wait_auth() {
    _tdoc_wait_auth_result
    return $?
}


# ── 直接执行时的交互式安装流程 ───────────────────────────────────────────────
_tdoc_interactive_setup() {
    echo ""
    echo "╔══════════════════════════════════════════════╗"
    echo "║     腾讯文档 MCP Skill 配置向导              ║"
    echo "╚══════════════════════════════════════════════╝"
    echo ""

    # 检查 mcporter
    echo "🔍 检查 mcporter..."
    if ! _tdoc_check_mcporter; then
        echo "❌ mcporter 安装失败，请先安装 Node.js (https://nodejs.org) 后重试"
        exit 1
    fi
    echo "✅ mcporter 已就绪"
    echo ""

    # 检查服务状态
    echo "🔍 检查 tencent-docs 服务配置..."
    _tdoc_check_service
    local status=$?

    case $status in
        0)
            echo "✅ tencent-docs 服务已配置且运行正常！"
            echo ""
            echo "🎉 无需重新配置，您可以直接使用腾讯文档功能。"
            echo ""
            echo "📖 使用示例："
            echo "   mcporter call tencent-docs manage.recent_online_file --args '{\"num\":10}'"
            return 0
            ;;
        1|2)
            echo "⚠️  Token 未配置，需要授权..."
            ;;
    esac

    echo ""
    echo "🔐 需要完成腾讯文档授权"
    echo ""

    # 清理旧状态
    _tdoc_cleanup

    # 生成授权链接（同时写入 code 文件）
    local auth_url
    auth_url=$(_tdoc_generate_auth_url)

    echo "┌─────────────────────────────────────────────────────────┐"
    echo "│  请在浏览器中打开以下链接完成授权：                      │"
    echo "│                                                         │"
    printf "│  %s\n" "$auth_url"
    echo "│                                                         │"
    echo "│  ⚠️  请使用 QQ 或微信 扫码 / 登录授权                   │"
    echo "└─────────────────────────────────────────────────────────┘"
    echo ""
    echo "⏳ 正在等待您完成授权，无需任何额外操作..."
    echo "   （最多等待 $(( (_TDOC_POLL_MAX * _TDOC_POLL_INTERVAL) + 15 )) 秒）"
    echo ""

    # ★ 立即启动后台轮询（与用户操作并行）
    _tdoc_start_bg_poll > /dev/null

    # ★ 前台等待 Token（自动检测，无需用户回复）
    local result
    result=$(_tdoc_wait_token)

    case "$result" in
        TOKEN_READY)
            local token=$(cat "$_TDOC_TOKEN_FILE")
            echo ""
            echo "✅ 授权成功！正在保存配置..."
            if _tdoc_save_token "$token"; then
                _tdoc_cleanup
                echo "✅ Token 已写入 mcporter 配置"
                echo ""
                echo "🎉 配置完成！现在可以直接使用腾讯文档功能了。"
                echo ""
                echo "📖 使用示例："
                echo "   mcporter call ${_TDOC_SERVICE_NAME} manage.recent_online_file --args '{\"num\":10}'"
                echo ""
                echo "🏠 腾讯文档主页：${_TDOC_API_BASE}/home"
            else
                echo "⚠️  Token 写入配置失败"
                echo "   请手动运行：mcporter config add ${_TDOC_SERVICE_NAME} ${_TDOC_MCP_URL} --header \"Authorization=${token}\" --transport http --scope home"
            fi
            ;;
        AUTH_TIMEOUT)
            echo ""
            echo "⏳ 授权超时（未在时限内完成授权）"
            echo "   请重新运行：bash ./setup.sh"
            exit 1
            ;;
        ERROR:expired)
            echo ""
            echo "❌ 授权码已过期，请重新运行：bash ./setup.sh"
            exit 1
            ;;
        ERROR:err_400006)
            echo ""
            echo "❌ Token 鉴权失败，请重新运行：bash ./setup.sh"
            exit 1
            ;;
        ERROR:*)
            echo ""
            echo "❌ 授权失败：$result"
            echo "   如问题持续，请联系腾讯文档客服：${_TDOC_API_BASE}/home/feedback"
            exit 1
            ;;
    esac

    return 0
}

# ── 脚本入口 ──────────────────────────────────────────────────────────────────
# 直接执行时：
#   bash ./setup.sh tdoc_check_and_start_auth  → 第一步：检查状态 / 生成授权链接
#   bash ./setup.sh tdoc_wait_auth             → 第二步：等待授权完成
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [[ -n "$1" ]]; then
        # 参数分发：将第一个参数作为函数名执行
        case "$1" in
            tdoc_check_and_start_auth|tdoc_wait_auth)
                "$1"
                exit $?
                ;;
            setup)
                echo "🚀 腾讯文档 MCP Skill 人工配置向导"
                echo ""
                _tdoc_interactive_setup
                ;;           
            *)
                echo "ERROR:unknown_command - 未知命令: $1"
                echo "可用命令: tdoc_check_and_start_auth, tdoc_wait_auth, setup"
                exit 1
                ;;
        esac
    else
        echo "用法："
        echo "  bash ./setup.sh tdoc_check_and_start_auth   # 第一步：检查状态 / 生成授权链接"
        echo "  bash ./setup.sh tdoc_wait_auth              # 第二步：等待授权完成"
    fi
fi