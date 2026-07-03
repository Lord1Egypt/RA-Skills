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

# Setup script for TSP (Time Series Processor)
# Econometric analysis and forecasting

TSP_VERSION="5.0"
CONFIG_FILE="$(dirname "$0")/../../config.json"

LANG_ZH "=== TSP 时间序列分析配置 ===" "=== TSP Setup ==="
LANG_ZH "版本: $TSP_VERSION" "Version: $TSP_VERSION"

# Detect TSP installation
TSP_BIN=""
if command -v tsp &> /dev/null; then
    TSP_BIN=$(command -v tsp)
elif [ -f /usr/local/bin/tsp ]; then
    TSP_BIN=/usr/local/bin/tsp
elif [ -f /usr/bin/tsp ]; then
    TSP_BIN=/usr/bin/tsp
elif [ -f "/opt/tsp/tsp" ]; then
    TSP_BIN="/opt/tsp/tsp"
fi

if [ -n "$TSP_BIN" ]; then
    LANG_ZH "找到 TSP: $TSP_BIN" "Found TSP: $TSP_BIN"
else
    LANG_ZH "未找到 TSP。" "TSP not found."
    LANG_ZH "安装：从 https://www.tsp.com/ 下载" "Install: Download from https://www.tsp.com/"
    TSP_BIN="NOT_INSTALLED"
fi

# Update config.json
if [ -f "$CONFIG_FILE" ] && [ "$TSP_BIN" != "NOT_INSTALLED" ]; then
    LANG_ZH "正在更新配置..." "Updating config.json..."
    python3 -c "
import json, sys
with open(sys.argv[1], 'r') as f:
    config = json.load(f)
config['TSP'] = {
    'version': sys.argv[2],
    'path': sys.argv[3],
    'platform': 'all',
    'mode': 'simple'
}
with open(sys.argv[1], 'w') as f:
    json.dump(config, f, indent=2)
print('config.json updated.')
" "$CONFIG_FILE" "$TSP_VERSION" "$TSP_BIN"
fi

LANG_ZH "" ""
LANG_ZH "TSP CLI 用法:" "TSP CLI Usage:"
echo "  tsp commands.txt          # 执行 TSP 命令文件"
echo "  tsp --help               # 显示 CLI 选项"
LANG_ZH "" ""
LANG_ZH "支持：时间序列、计量经济学、假设检验" "Supported: Time Series, Econometrics, Hypothesis Testing"
