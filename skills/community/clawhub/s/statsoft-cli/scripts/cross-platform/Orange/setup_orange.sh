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

set -euo pipefail

statsoft_reveal() { [ "${STATSOFT_REVEAL:-0}" = "1" ]; }
statsoft_verify() { [ "${STATSOFT_VERIFY:-0}" = "1" ]; }

CONFIG_FILE="$(dirname "$0")/../../config.json"

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

# Derive version dynamically; requires opt-in query (no hardcoded version)
if statsoft_verify && [ -n "$ORANGE_BIN" ]; then
    ORANGE_VERSION=$("$ORANGE_BIN" --version 2>&1 | head -1 || echo "unknown")
else
    ORANGE_VERSION="unknown (set STATSOFT_VERIFY=1)"
fi

LANG_ZH "=== Orange 数据挖掘平台配置 ===" "=== Orange Setup ==="
if statsoft_reveal && [ -n "$ORANGE_BIN" ]; then
    LANG_ZH "找到 Orange: $ORANGE_BIN" "Found Orange: $ORANGE_BIN"
    LANG_ZH "版本: $ORANGE_VERSION" "Version: $ORANGE_VERSION"
elif [ -z "$ORANGE_BIN" ]; then
    LANG_ZH "未找到 Orange。" "Orange not found."
    LANG_ZH "安装选项:" "Install options:"
    echo "  pip install orange3"
    echo "  conda install -c conda-forge orange3"
    ORANGE_BIN="NOT_INSTALLED"
else
    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
fi

# Check Python Orange3 module — path only disclosed when REVEAL=1
ORANGE_PY=""
if python3 -c "import Orange" 2>/dev/null; then
    ORANGE_PY=$(python3 -c "import Orange; print(Orange.__path__[0])")
    if statsoft_reveal; then
        LANG_ZH "Orange3 Python 模块: $ORANGE_PY" "Orange3 Python module: $ORANGE_PY"
    else
        echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
    fi
fi

if ([ -n "$ORANGE_BIN" ] && [ "$ORANGE_BIN" != "NOT_INSTALLED" ]) || [ -n "$ORANGE_PY" ]; then
    LANG_ZH "找到 Orange。" "Found Orange."
fi

# Config persistence (fail-closed: detection-only by default; persists only on explicit opt-in)
if [ -f "$CONFIG_FILE" ] && [ "$ORANGE_BIN" != "NOT_INSTALLED" ]; then
    LANG_ZH "默认仅检测；写入需 opt-in（STATSOFT_AUTO_WRITE=1）" "Detection-only by default; write requires opt-in (STATSOFT_AUTO_WRITE=1)"
    _NEW_CFG=$(python3 -c "
import json, sys
with open(sys.argv[1], 'r') as f:
    config = json.load(f)
config['Orange'] = {
    'version': sys.argv[2],
    'path': sys.argv[3],
    'platform': 'all',
    'mode': 'simple'
}
print(json.dumps(config, ensure_ascii=False))" "$CONFIG_FILE" "$ORANGE_VERSION" "$ORANGE_BIN")
    # Fail-closed by default — persist ONLY when explicitly opted in.
    if [ "${STATSOFT_AUTO_WRITE:-0}" = "1" ]; then
        STATSOFT_AUTO_WRITE=1 python3 "$(dirname "$0")/../../common/write_config.py" "$CONFIG_FILE" <<< "$_NEW_CFG"
    elif [ "${STATSOFT_CONFIRM:-0}" = "1" ] && [ -t 0 ]; then
        printf 'Persist detected config to config.json? (y/N) '
        read -r _ans
        case "$_ans" in y|Y|yes) STATSOFT_AUTO_WRITE=1 python3 "$(dirname "$0")/../../common/write_config.py" "$CONFIG_FILE" <<< "$_NEW_CFG" ;; *) echo "Detection-only: config.json NOT modified." ;; esac
    else
        echo "Detection-only: config.json NOT modified. Set STATSOFT_AUTO_WRITE=1 to persist, or STATSOFT_CONFIRM=1 for an interactive prompt."
    fi
fi

LANG_ZH "" ""
LANG_ZH "Orange CLI 用法:" "Orange CLI Usage:"
echo "$(LANG_ZH "  orange-canvas --help       # 显示 CLI 选项" "  orange-canvas --help       # show CLI options")"
echo "$(LANG_ZH "  python3 -m Orange ...      # 直接使用 Orange Python 模块" "  python3 -m Orange ...      # use the Orange Python module directly")"
LANG_ZH "" ""
LANG_ZH "支持：数据挖掘、可视化、机器学习、文本挖掘" "Supported: Data Mining, Visualization, Machine Learning, Text Mining"
