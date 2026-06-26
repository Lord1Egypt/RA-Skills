#!/usr/bin/env bash
#
# chat.sh — 通过妙问 API 进行 AI 问答（一站式脚本）
#
# 用法: bash chat.sh "<你的问题>"
#
# 功能:
#   - 自动检查运行环境和依赖工具
#   - 自动检查 Token 文件是否存在
#   - 自动读取 Token 并发起 API 请求
#   - 根据不同错误场景输出明确的提示信息
#
# Token 存储位置: ~/.MIAOWEN_ACCESS_TOKEN
#
# 退出码说明:
#   0 — 请求成功，结果已输出
#   1 — 参数错误（未提供问题）
#   2 — Token 文件不存在，需要用户首次获取 Token
#   3 — Token 文件为空，需要用户重新设置 Token
#   4 — API 返回非 200 状态码（含 Token 失效、权限错误等，由调用方根据响应内容判断）
#   5 — 网络请求失败（curl 执行出错、超时等）
#   6 — 运行环境不满足要求（缺少依赖工具等）
#

set -uo pipefail

API_URL="https://ad.qq.com/ai/gw/ai_customer_service/v1/open_api/chat"

# ============ 环境检查 ============

# 检查 HOME 目录
if [ -z "${HOME:-}" ]; then
    echo "[ENV_ERROR] 无法确定用户 HOME 目录"
    echo ""
    echo "当前系统未设置 HOME 环境变量，请检查："
    echo "  - Linux/macOS: 通常会自动设置，请确认当前用户配置正常"
    echo "  - Windows Git Bash: 请确保 Git Bash 正确安装"
    echo "  - Windows WSL: 请确认 WSL 用户配置正常"
    exit 6
fi

TOKEN_FILE="${HOME}/.MIAOWEN_ACCESS_TOKEN"

# 检查 curl 是否可用
if ! command -v curl &>/dev/null; then
    echo "[ENV_ERROR] 未找到 curl 命令"
    echo ""
    echo "本脚本依赖 curl 发起 HTTP 请求，请先安装 curl："
    echo ""
    # 检测操作系统并给出对应的安装命令
    OS_TYPE="$(uname -s 2>/dev/null || echo "Unknown")"
    case "$OS_TYPE" in
        Darwin*)
            echo "  macOS (Homebrew):  brew install curl"
            echo "  macOS (MacPorts):  sudo port install curl"
            ;;
        Linux*)
            echo "  Ubuntu/Debian:     sudo apt-get install -y curl"
            echo "  CentOS/RHEL:       sudo yum install -y curl"
            echo "  Fedora:            sudo dnf install -y curl"
            echo "  Alpine:            sudo apk add curl"
            echo "  Arch Linux:        sudo pacman -S curl"
            ;;
        MINGW*|MSYS*|CYGWIN*)
            echo "  Windows Git Bash:  curl 通常随 Git for Windows 自带，请尝试重新安装 Git for Windows"
            echo "  Windows Scoop:     scoop install curl"
            echo "  Windows Chocolatey: choco install curl"
            ;;
        *)
            echo "  请根据您的操作系统安装 curl"
            ;;
    esac
    exit 6
fi

QUESTION="${1:-}"

# ============ 参数检查 ============

if [ -z "$QUESTION" ]; then
    echo "[ERROR] 未提供问题参数"
    echo "用法: bash chat.sh \"<你的问题>\""
    exit 1
fi

# ============ Token 检查 ============

if [ ! -f "$TOKEN_FILE" ]; then
    echo "[TOKEN_NOT_FOUND] Token 文件不存在: ${TOKEN_FILE}"
    echo ""
    echo "您需要先获取妙问 API KEY 才能使用问答服务。"
    echo ""
    echo "获取步骤："
    echo "  1. 打开妙问官网 https://miaowen.qq.com/ 并登录"
    echo "  2. 左侧导航栏点击【Skill 社区】"
    echo "  3. 在弹出页面中可以看到「你的 API KEY」，格式为 sk-mw-xxxxx"
    echo "  4. 点击 API KEY 右侧的「刷新」按钮获取 Token，点击「复制」按钮复制"
    echo ""
    echo "获取 Token 后请粘贴给我，我会帮您自动保存。"
    exit 2
fi

# 读取 Token（去除首尾空白和换行）
MIAOWEN_ACCESS_TOKEN=$(tr -d '[:space:]' < "$TOKEN_FILE")

if [ -z "$MIAOWEN_ACCESS_TOKEN" ]; then
    echo "[TOKEN_EMPTY] Token 文件为空: ${TOKEN_FILE}"
    echo ""
    echo "Token 文件存在但内容为空，请重新获取 Token。"
    echo ""
    echo "获取步骤："
    echo "  1. 打开妙问官网 https://miaowen.qq.com/ 并登录"
    echo "  2. 左侧导航栏点击【Skill 社区】"
    echo "  3. 点击 API KEY 右侧的「刷新」按钮获取新 Token，点击「复制」按钮复制"
    echo ""
    echo "获取 Token 后请粘贴给我，我会帮您重新保存。"
    exit 3
fi

# ============ 发起 API 请求 ============

# 转义问题中的特殊字符（用于 JSON）
# 优先使用 python3，不可用时回退到基本的 sed 转义
if command -v python3 &>/dev/null; then
    ESCAPED_QUESTION=$(echo "$QUESTION" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))" 2>/dev/null | sed 's/^"//;s/"$//' || echo "$QUESTION")
else
    # 回退方案：用 sed 处理基本的 JSON 特殊字符
    ESCAPED_QUESTION=$(echo "$QUESTION" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g' 2>/dev/null || echo "$QUESTION")
fi

# 发起请求（设置 3 分钟超时）
RESPONSE=$(curl -s -w "\n%{http_code}" --connect-timeout 10 --max-time 180 -X POST \
    -H "Authorization:Bearer ${MIAOWEN_ACCESS_TOKEN}" \
    -H "Content-Type:application/json" \
    -d "{\"query\":\"${ESCAPED_QUESTION}\"}" \
    "$API_URL" 2>&1)

CURL_EXIT_CODE=$?

# ============ 处理网络错误 ============

if [ $CURL_EXIT_CODE -ne 0 ]; then
    echo "[NETWORK_ERROR] 网络请求失败 (curl exit code: ${CURL_EXIT_CODE})"
    echo ""
    case $CURL_EXIT_CODE in
        6)  echo "原因：无法解析域名，请检查网络连接和 DNS 设置。" ;;
        7)  echo "原因：无法连接到服务器，请检查网络连接。" ;;
        28) echo "原因：请求超时（超过 3 分钟），妙问服务响应较慢，请稍后重试。" ;;
        35) echo "原因：SSL/TLS 连接错误，请检查网络环境。" ;;
        56) echo "原因：接收数据失败，网络连接中断。" ;;
        *)  echo "原因：网络异常 (错误码: ${CURL_EXIT_CODE})，请检查网络连接后重试。" ;;
    esac
    echo ""
    echo "如果问题持续存在，请检查："
    echo "  - 网络是否正常连接"
    echo "  - 是否需要配置代理（如在公司内网环境）"
    echo "  - 妙问服务是否可用: https://miaowen.qq.com/"
    exit 5
fi

# ============ 解析响应 ============

# 分离响应体和状态码
HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
BODY=$(echo "$RESPONSE" | sed '$d')

# 检查 HTTP 状态码，非 200 直接输出原始响应内容（由调用方判断具体错误原因）
if [ "$HTTP_CODE" != "200" ]; then
    echo "[API_ERROR] API 请求失败 (HTTP ${HTTP_CODE})"
    echo ""
    echo "$BODY"
    exit 4
fi

# ============ 输出成功结果 ============

echo "$BODY"
exit 0
