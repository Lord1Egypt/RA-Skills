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
if statsoft_reveal; then
    LANG_ZH "版本: $TSP_VERSION" "Version: $TSP_VERSION"
else
    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
fi

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
    if statsoft_reveal; then
        LANG_ZH "找到 TSP: $TSP_BIN" "Found TSP: $TSP_BIN"
    else
        echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
    fi
else
    LANG_ZH "未找到 TSP。" "TSP not found."
    LANG_ZH "安装：从 https://www.tsp.com/ 下载" "Install: Download from https://www.tsp.com/"
    TSP_BIN="NOT_INSTALLED"
fi

# Config persistence (fail-closed: detection-only by default; persists only on explicit opt-in)
if [ -f "$CONFIG_FILE" ] && [ "$TSP_BIN" != "NOT_INSTALLED" ]; then
    LANG_ZH "默认仅检测；写入需 opt-in（STATSOFT_AUTO_WRITE=1）" "Detection-only by default; write requires opt-in (STATSOFT_AUTO_WRITE=1)"
    _NEW_CFG=$(python3 -c "
import json, sys
with open(sys.argv[1], 'r') as f:
    config = json.load(f)
config['TSP'] = {
    'version': sys.argv[2],
    'path': sys.argv[3],
    'platform': 'all',
    'mode': 'simple'
}
statsoft_reveal() { [ "${STATSOFT_REVEAL:-0}" = "1" ]; }
statsoft_verify() { [ "${STATSOFT_VERIFY:-0}" = "1" ]; }
print(json.dumps(config, ensure_ascii=False))" "$CONFIG_FILE" "$TSP_VERSION" "$TSP_BIN")
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
LANG_ZH "TSP CLI 用法:" "TSP CLI Usage:"
echo "$(LANG_ZH "  tsp commands.txt          # 执行 TSP 命令文件" "  tsp commands.txt          # execute TSP command file")"
echo "$(LANG_ZH "  tsp --help               # 显示 CLI 选项" "  tsp --help               # show CLI options")"
LANG_ZH "" ""
LANG_ZH "支持：时间序列、计量经济学、假设检验" "Supported: Time Series, Econometrics, Hypothesis Testing"
