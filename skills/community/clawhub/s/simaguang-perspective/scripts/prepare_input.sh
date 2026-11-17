#!/usr/bin/env bash
# prepare_input 跨平台 CLI 入口（macOS / Linux；Windows 用 scripts/prepare_input.cmd 或 python scripts/prepare_input.py）。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/prepare_input.py" "$@"
