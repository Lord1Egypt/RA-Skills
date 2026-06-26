#!/usr/bin/env bash
# apikey — API Key、主人绑定与位置管理
# 委托给 Python3 实现，此文件仅作为兼容入口保留

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$SCRIPT_DIR/main.py" "$@"
fi

echo "❌ 需要 python3（未找到），请先安装 Python 3.8+" >&2
exit 1
