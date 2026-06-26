#!/bin/sh
# 月嫂下单客资工具启动脚本
# 用法：sh dist/run.sh <command> [args...]
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec node "$SCRIPT_DIR/cli.js" "$@"
