#!/usr/bin/env bash
# cad_measure_to_input 跨平台 CLI 入口（macOS / Linux；Windows 用 python scripts/cad_measure_to_input.py）。
# 统一运行时解析（Python / 识图底座 / vendor）见 scripts/runtime_env.sh
set -euo pipefail
_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$_HERE/runtime_env.sh"
exec "$PYTHON_BIN" "$_HERE/cad_measure_to_input.py" "$@"
