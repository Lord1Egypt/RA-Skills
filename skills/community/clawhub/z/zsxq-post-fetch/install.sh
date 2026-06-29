#!/bin/bash
# install.sh — 安装 zsxq-fetch skill 的依赖
# 用法: bash install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "==> 安装目录: $SCRIPT_DIR"

# 1. 检查 Node.js
if ! command -v node &>/dev/null; then
    echo "ERROR: 未找到 Node.js，请先安装 Node.js >= 18" && exit 1
fi

NODE_MAJOR=$(node -v | sed 's/v//' | cut -d. -f1)
if [ "$NODE_MAJOR" -lt 18 ]; then
    echo "ERROR: 需要 Node.js >= 18（当前: $(node -v)）" && exit 1
fi
echo "==> Node $(node -v), npm $(npm -v)"

# 2. 检查官方 zsxq-cli
if ! command -v zsxq-cli &>/dev/null; then
    echo ""
    echo "==> 未找到官方 zsxq-cli，尝试安装..."
    if ! command -v npm &>/dev/null; then
        echo "ERROR: 未找到 npm，无法自动安装 zsxq-cli"
        echo "请手动安装 Node.js/npm 后运行: npm install -g zsxq-cli"
        exit 1
    fi

    if ! npm install -g zsxq-cli; then
        echo "ERROR: 自动安装 zsxq-cli 失败"
        echo "请手动运行: npm install -g zsxq-cli"
        exit 1
    fi
fi

echo "==> zsxq-cli: $(command -v zsxq-cli)"

# 3. 验证本地运行环境
echo ""
echo "==> 验证安装..."
node -e "
require('child_process');
require('https');
require('url');
console.log('  Node.js 内置模块: OK');
"

echo ""
echo "==> 检查 zsxq-cli 登录状态..."
if ! zsxq-cli auth status; then
    echo ""
    echo "尚未完成官方 CLI 登录，请运行:"
    echo "  zsxq-cli auth login"
fi

echo ""
echo "==> 安装检查完成"
