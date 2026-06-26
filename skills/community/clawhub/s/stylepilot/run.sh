#!/usr/bin/env bash
# 标准 CLI 入口：供 Agent / OpenClaw exec 使用，避免直接 `python3 scripts/wardrobe.py …` 触发 preflight。
# Usage: ./run.sh <wardrobe subcommand and args>
# Example: ./run.sh outfit --scene today --json
set -euo pipefail

# 安全检查：确保只执行预期的命令
VALID_COMMANDS=(init list add outfit feedback)

# 检查是否提供了命令
if [ $# -eq 0 ]; then
    echo "Error: No command provided"
    exit 1
fi

# 检查命令是否有效
COMMAND="$1"
if ! [[ " ${VALID_COMMANDS[*]} " =~ " ${COMMAND} " ]]; then
    echo "Error: Invalid command: $COMMAND"
    exit 1
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$ROOT/scripts/wardrobe.py" "$@"
