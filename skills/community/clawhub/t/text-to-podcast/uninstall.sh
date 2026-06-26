#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

echo "🗑️  卸载 text-to-podcast..."

read -p "删除配置和输出文件？(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f "$BASE_DIR/.env"
    rm -rf "$BASE_DIR/output"
    echo "✅ 已删除"
fi

echo "✅ 卸载完成！"