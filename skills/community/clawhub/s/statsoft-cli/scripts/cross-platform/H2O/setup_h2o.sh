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
statsoft_reveal() { [ "${STATSOFT_REVEAL:-0}" = "1" ]; }
statsoft_verify() { [ "${STATSOFT_VERIFY:-0}" = "1" ]; }

# Setup script for H2O.ai
# Open source machine learning platform and AutoML

CONFIG_FILE="$(dirname "$0")/../../config.json"

LANG_ZH "=== H2O.ai 机器学习平台配置 ===" "=== H2O.ai Setup ==="

# Detect H2O installation
H2O_BIN=""
H2O_VERSION="unknown"
if command -v h2o &> /dev/null; then
    H2O_BIN=$(command -v h2o)
elif [ -f /usr/local/bin/h2o ]; then
    H2O_BIN=/usr/local/bin/h2o
elif [ -f /usr/bin/h2o ]; then
    H2O_BIN=/usr/bin/h2o
elif [ -f "$HOME/h2o/h2o.jar" ]; then
    H2O_BIN="$HOME/h2o/h2o.jar"
fi

# Version detection requires VERIFY gate (SDI-4)
if [ -n "$H2O_BIN" ] && statsoft_verify; then
    H2O_VERSION=$("$H2O_BIN" --version 2>/dev/null | head -1 || echo "unknown")
fi

# Check Python H2O module
H2O_PY=""
if python3 -c "import h2o" 2>/dev/null; then
    if statsoft_reveal; then
        H2O_PY=$(python3 -c "import h2o; print(h2o.__path__[0])")
        LANG_ZH "H2O Python 模块: $H2O_PY" "H2O Python module: $H2O_PY"
    else
        LANG_ZH "H2O Python 模块已安装（路径已隐藏）" "H2O Python module installed (path hidden)"
    fi
fi

if statsoft_reveal; then
    LANG_ZH "版本: $H2O_VERSION" "Version: $H2O_VERSION"
else
    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
fi

if [ -n "$H2O_BIN" ] || [ -n "$H2O_PY" ]; then
    LANG_ZH "找到 H2O.ai。" "Found H2O.ai."
else
    LANG_ZH "未找到 H2O。" "H2O not found."
    # Issue 3 fix: installation guidance only printed on opt-in.
    if [ "${STATSOFT_INSTALL_OPT_IN:-0}" = "1" ]; then
        LANG_ZH "安装选项:" "Install options:"
        echo "  pip install h2o"
        echo "  Download jar from https://h2o.ai/download/"
    else
        LANG_ZH "设置 STATSOFT_INSTALL_OPT_IN=1 获取安装指引。" "Set STATSOFT_INSTALL_OPT_IN=1 for install guidance."
    fi
    H2O_BIN="NOT_INSTALLED"
fi

# Config persistence (fail-closed: detection-only by default)
if [ -f "$CONFIG_FILE" ] && [ "$H2O_BIN" != "NOT_INSTALLED" ]; then
    LANG_ZH "默认仅检测；写入需 opt-in（STATSOFT_AUTO_WRITE=1）" "Detection-only by default; write requires opt-in (STATSOFT_AUTO_WRITE=1)"
    _NEW_CFG=$(python3 -c "
import json, sys
config = json.load(open(sys.argv[1]))
config['H2O'] = {
    'version': sys.argv[2],
    'path': sys.argv[3],
    'platform': 'all',
    'mode': 'simple'
}
print(json.dumps(config, ensure_ascii=False))" "$CONFIG_FILE" "$H2O_VERSION" "$H2O_BIN")
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
LANG_ZH "H2O CLI 用法:" "H2O CLI Usage:"
echo "  h2o --help                # Show CLI options"
echo "  h2o start                 # Start H2O server"
echo "  python3 -c 'import h2o; h2o.init()'  # Initialize via Python"
LANG_ZH "" ""
LANG_ZH "支持：分布式机器学习、AutoML、深度学习、NLP、时间序列" "Supported: Distributed ML, AutoML, Deep Learning, NLP, Time Series"
