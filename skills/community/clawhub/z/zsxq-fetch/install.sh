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

# 2. 验证（无额外依赖，Node.js 内置模块即可运行）
echo ""
echo "==> 验证安装..."
node -e "
require('https');
require('url');
console.log('  Node.js 内置模块: OK');
console.log('');
console.log('==> 全部就绪！');
"
