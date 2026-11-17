#!/usr/bin/env bash
# generate_work_product 跨平台 CLI 入口（macOS / Linux；Windows 用 scripts/generate_work_product.cmd 或 python scripts/generate_work_product.py）。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/generate_work_product.py" "$@"
