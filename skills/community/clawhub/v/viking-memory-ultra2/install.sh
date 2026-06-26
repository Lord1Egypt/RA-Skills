#!/bin/bash
# Viking Memory System Ultra - 安装脚本

VIKING_HOME="${VIKING_HOME:-$HOME/.openclaw/viking}"
SCRIPTS_DIR="$VIKING_HOME/scripts"
SOURCE_DIR="$(dirname "$0")/scripts"

echo "=== Viking Memory System Ultra 安装 ==="
echo "目标目录: $SCRIPTS_DIR"

# 创建目录
mkdir -p "$SCRIPTS_DIR"

# 复制脚本
cp "$SOURCE_DIR"/*.sh "$SCRIPTS_DIR/"
chmod +x "$SCRIPTS_DIR"/*.sh

echo "✅ 安装完成"
echo "提示：请确保 VIKING_HOME 环境变量已设置"
