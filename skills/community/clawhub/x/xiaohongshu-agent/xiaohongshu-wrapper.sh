#!/bin/bash
# 小红书 CLI Wrapper for OpenClaw Skill
# 自动从配置文件读取 Cookies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
XHS_CLI="/root/.openclaw/workspace/skills/xiaohongshu/xiaohongshu-cli.py"
COOKIES_FILE="/root/.openclaw/workspace/xiaohongshu-cookies.md"

# 从环境变量或配置文件读取 Cookie
if [ -n "$XHS_COOKIE" ]; then
    export XHS_COOKIE
else
    # 从配置文件解析
    if [ -f "$COOKIES_FILE" ]; then
        XHS_COOKIE=$(grep "cookie=" "$COOKIES_FILE" | cut -d'=' -f2 | tr -d ' "')
        export XHS_COOKIE
    fi
fi

if [ -z "$XHS_COOKIE" ]; then
    echo "❌ 错误：未找到小红书认证信息"
    echo "请设置环境变量或在 $COOKIES_FILE 中配置 Cookie"
    echo ""
    echo "使用方法:"
    echo "  export XHS_COOKIE='your_cookie'"
    exit 1
fi

# 执行 CLI 命令
python3 "$XHS_CLI" "$@"
