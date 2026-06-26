#!/bin/bash
# 维加斯通道做 T 分析 - 快捷运行脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/scripts/vegas_analyzer.py"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3"
    exit 1
fi

# 检查依赖
python3 -c "import sys; sys.exit(0)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Python 环境异常"
    exit 1
fi

# 运行分析
python3 "$PYTHON_SCRIPT" "$@"
