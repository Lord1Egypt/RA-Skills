#!/usr/bin/env bash
# SCL-90 症状自评量表 - 入口脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/scl90.sh" "$@"