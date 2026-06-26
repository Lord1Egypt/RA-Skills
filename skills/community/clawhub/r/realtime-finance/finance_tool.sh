#!/bin/bash
# OpenClaw 财经数据工具包装器
# 用法: ./finance_tool.sh "查询内容"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/realtime_finance.py" "$@"
