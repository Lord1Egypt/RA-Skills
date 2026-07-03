#!/bin/bash

# ============================================================
# Language Detection
# ============================================================
if [[ "${LANG:-}" == zh_* ]] || [[ "${LC_ALL:-}" == zh_* ]] || [[ "${LANGUAGE:-}" == zh_* ]]; then
    SCRIPT_LANG="zh"
else
    SCRIPT_LANG="en"
fi

LANG_ZH() { [[ "$SCRIPT_LANG" == "zh" ]] && echo "$1" || echo "$2"; }

# Setup script for Orange Data Mining
# Data mining, visualization, and machine learning

ORANGE_VERSION="3.36"
CONFIG_FILE="$(dirname "$0")/../../config.json"

LANG_ZH "=== Orange 数据挖掘平台配置 ===" "=== Orange Setup ==="
LANG_ZH "版本: $ORANGE_VERSION" "Version: $ORANGE_VERSION"

# Detect Orange installation
ORANGE_BIN=""
if command -v orange-canvas &> /dev/null; then
    ORANGE_BIN=$(command -v orange-canvas)
elif [ -f /usr/local/bin/orange-canvas ]; then
    ORANGE_BIN=/usr/local/bin/orange-canvas
elif [ -f /usr/bin/orange-canvas ]; then
    ORANGE_BIN=/usr/bin/orange-canvas
elif [ -f "/opt/orange/orange-canvas" ]; then
    ORANGE_BIN="/opt/orange/orange-canvas"
elif [ -f "/Applications/Orange.app/Contents/MacOS/Orange" ]; then
    ORANGE_BIN="/Applications/Orange.app/Contents/MacOS/Orange"
fi

# Check Python Orange3 module
ORANGE_PY=""
if python3 -c "import Orange" 2>/dev/null; then
    ORANGE_PY=$(python3 -c "import Orange; print(Orange.__path__[0])")
    LANG_ZH "Orange3 Python 模块: $ORANGE_PY" "Orange3 Python module: $ORANGE_PY"
fi

if [ -n "$ORANGE_BIN" ] || [ -n "$ORANGE_PY" ]; then
    LANG_ZH "找到 Orange。" "Found Orange."
else
    LANG_ZH "未找到 Orange。" "Orange not found."
    LANG_ZH "安装选项:" "Install options:"
    echo "  pip install orange3"
    echo "  conda install -c conda-forge orange3"
    ORANGE_BIN="NOT_INSTALLED"
fi

# Update config.json
if [ -f "$CONFIG_FILE" ] && [ "$ORANGE_BIN" != "NOT_INSTALLED" ]; then
    LANG_ZH "正在更新配置..." "Updating config.json..."
    python3 -c "
import json, sys
with open(sys.argv[1], 'r') as f:
    config = json.load(f)
config['Orange'] = {
    'version': sys.argv[2],
    'path': sys.argv[3],
    'platform': 'all',
    'mode': 'simple'
}
with open(sys.argv[1], 'w') as f:
    json.dump(config, f, indent=2)
print('config.json updated.')
" "$CONFIG_FILE" "$ORANGE_VERSION" "$ORANGE_BIN"
fi

LANG_ZH "" ""
LANG_ZH "Orange CLI 用法:" "Orange CLI Usage:"
echo "  orange-canvas --help       # 显示 CLI 选项"
echo "  python3 -m Orange ...      # 直接使用 Orange Python 模块"
LANG_ZH "" ""
LANG_ZH "支持：数据挖掘、可视化、机器学习、文本挖掘" "Supported: Data Mining, Visualization, Machine Learning, Text Mining"
