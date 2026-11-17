#!/usr/bin/env bash
# 装饰算量 -> lis-skill-bus 可选接线（薄壳，逻辑在 zhuangshi_statesync.py）。
# 用法：`bash zhuangshi_statesync.sh push|pull --project 项目 ...`，见对应 .py --help。
# 运行时解析（Python / 底座 / vendor）见 scripts/runtime_env.sh
set -uo pipefail
_HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "$_HERE/runtime_env.sh"
exec "${PYTHON_BIN}" "$_HERE/zhuangshi_statesync.py" "$@"
