#!/bin/bash

# Logistics CLI 快捷脚本
# 用法：./logistics.sh <command> [args]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_PATH="$SCRIPT_DIR/../cli/logistics_cli.js"

# 检查 Node.js 是否安装
if ! command -v node &> /dev/null; then
    echo "❌ 错误：Node.js 未安装"
    exit 1
fi

# 检查 CLI 文件是否存在
if [ ! -f "$CLI_PATH" ]; then
    echo "❌ 错误：CLI 文件不存在：$CLI_PATH"
    exit 1
fi

# 执行 CLI
node "$CLI_PATH" "$@"
