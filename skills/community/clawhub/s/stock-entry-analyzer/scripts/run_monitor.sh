#!/bin/bash
# 股票监控报告生成脚本
# 用于定时任务调用

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📊 开始生成股票监控报告..."
python3 "$SCRIPT_DIR/analyze_stocks.py"
