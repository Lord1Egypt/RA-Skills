#!/bin/sh
# 保洁下单工具启动脚本（未扰乱版）
# 用法：sh dist/run.sh <command> [args...]
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec node "$SCRIPT_DIR/local-outpost.js" "$@"
