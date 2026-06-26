#!/bin/bash
# 太极架构 Skills 自动化卸载脚本
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TAICHI_DIR="$SCRIPT_DIR/taichi-framework"
WORKSPACE_DIR="${TAICHI_WORKSPACE:-$TAICHI_DIR/workspace}"

echo "=== 太极架构卸载脚本 ==="

read -p "确认卸载太极架构 Skills？[y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "取消卸载"
    exit 0
fi

echo "[1/3] 停止 Redis..."
if pgrep -x redis-server > /dev/null 2>&1; then
    redis-cli shutdown 2>/dev/null || true
    echo "  Redis 已停止"
else
    echo "  Redis 未运行，跳过"
fi

echo "[2/3] 删除 Python 虚拟环境..."
if [ -d "$TAICHI_DIR/venv" ]; then
    rm -rf "$TAICHI_DIR/venv"
    echo "  venv 已删除"
else
    echo "  venv 不存在，跳过"
fi

echo "[3/3] 删除运行时数据..."
if [ -d "$WORKSPACE_DIR" ]; then
    rm -rf "$WORKSPACE_DIR"
    echo "  工作区已删除"
else
    echo "  工作区不存在，跳过"
fi

echo ""
echo "=== 卸载完成 ==="
echo "Skills 目录保留，如需彻底删除请手动移除: $SCRIPT_DIR"
