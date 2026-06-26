#!/bin/bash
# bili-login.sh - B 站扫码登录获取 Cookies
# 用法：./bili-login.sh [输出文件]
# 默认输出路径：~/.cookies/bilibili_cookies.txt

set -e

COOKIE_FILE="${1:-$HOME/.cookies/bilibili_cookies.txt}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# biliup login 默认在当前工作目录保存 cookies.json
# 使用临时目录，避免在 skill 目录内留下 cookie 文件
BILIUP_COOKIE_DIR=$(mktemp -d)
BILIUP_COOKIE="$BILIUP_COOKIE_DIR/cookies.json"

# 登录完成后清理临时 cookie 文件
cleanup() {
    rm -rf "$BILIUP_COOKIE_DIR" 2>/dev/null || true
}
trap cleanup EXIT

echo "================================"
echo "📱 B 站扫码登录"
echo "================================"
echo ""

# 检查 biliup 是否安装
if ! command -v biliup &>/dev/null; then
    echo "❌ biliup 未安装"
    echo ""
    echo "安装命令:"
    echo "  pip3 install biliup --break-system-packages"
    exit 1
fi

# 创建输出目录
mkdir -p "$(dirname "$COOKIE_FILE")"

# 在临时目录执行登录，cookies.json 写入临时目录
cd "$BILIUP_COOKIE_DIR"

# 执行扫码登录
echo "请使用 B 站 APP 扫码："
echo ""
biliup login

# 检查登录是否成功
if [[ ! -f "$BILIUP_COOKIE" ]]; then
    echo ""
    echo "❌ 登录失败，未找到 cookies.json"
    exit 1
fi

echo ""
echo "✅ 登录成功"
echo ""

# 转换格式
echo "🔄 转换 Cookies 格式..."
python3 "$SCRIPT_DIR/convert-bili-cookie.py" "$BILIUP_COOKIE" "$COOKIE_FILE"

if [[ $? -eq 0 && -f "$COOKIE_FILE" ]]; then
    # 限制文件权限：仅所有者可读写
    chmod 600 "$COOKIE_FILE"
    echo "✅ Cookies 已保存：$COOKIE_FILE（权限 600）"
    echo ""
    echo "📊 统计:"
    wc -l "$COOKIE_FILE" | awk '{print "   共 " $1 " 行"}'
    echo ""
    echo "⚠️  临时 cookies.json 已自动清理"
else
    echo "❌ 格式转换失败"
    exit 1
fi

echo ""
echo "================================"
echo "✅ 登录完成"
echo "================================"
