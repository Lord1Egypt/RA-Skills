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

# Setup script for OxMetrics Econometrics Software
# Comprehensive econometrics, time series, and forecasting

OX_VERSION="8.0"
CONFIG_FILE="$(dirname "$0")/../../config.json"

LANG_ZH "=== OxMetrics 计量经济学配置 ===" "=== OxMetrics Setup ==="
if statsoft_reveal; then
    LANG_ZH "版本: $OX_VERSION" "Version: $OX_VERSION"
else
    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
fi

# Detect OxMetrics installation
OX_BIN=""
if command -v oxmetrics &> /dev/null; then
    OX_BIN=$(command -v oxmetrics)
elif [ -f /usr/local/bin/oxmetrics ]; then
    OX_BIN=/usr/local/bin/oxmetrics
elif [ -f /usr/bin/oxmetrics ]; then
    OX_BIN=/usr/bin/oxmetrics
elif [ -f "/opt/oxmetrics/oxmetrics" ]; then
    OX_BIN="/opt/oxmetrics/oxmetrics"
elif [ -f "/Applications/OxMetrics8/oxmetrics" ]; then
    OX_BIN="/Applications/OxMetrics8/oxmetrics"
fi

if [ -n "$OX_BIN" ]; then
    if statsoft_reveal; then
        LANG_ZH "找到 OxMetrics: $OX_BIN" "Found OxMetrics: $OX_BIN"
    else
        echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
    fi
else
    LANG_ZH "未找到 OxMetrics。" "OxMetrics not found."
    LANG_ZH "安装：从 https://www.oxmetrics.net/ 下载" "Install: Download from https://www.oxmetrics.net/"
    OX_BIN="NOT_INSTALLED"
fi

# Config persistence (fail-closed: detection-only by default; persists only on explicit opt-in)
if [ -f "$CONFIG_FILE" ] && [ "$OX_BIN" != "NOT_INSTALLED" ]; then
    LANG_ZH "默认仅检测；写入需 opt-in（STATSOFT_AUTO_WRITE=1）" "Detection-only by default; write requires opt-in (STATSOFT_AUTO_WRITE=1)"
    _NEW_CFG=$(python3 -c "
import json, sys
with open(sys.argv[1], 'r') as f:
    config = json.load(f)
config['OxMetrics'] = {
    'version': sys.argv[2],
    'path': sys.argv[3],
    'platform': 'all',
    'mode': 'simple'
}
print(json.dumps(config, ensure_ascii=False))" "$CONFIG_FILE" "$OX_VERSION" "$OX_BIN")
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
LANG_ZH "OxMetrics CLI 用法:" "OxMetrics CLI Usage:"
echo "$(LANG_ZH "  oxmetrics --help          # 显示 CLI 选项" "  oxmetrics --help          # show CLI options")"
echo "$(LANG_ZH "  oxmetrics -b commands.txt # 执行批命令" "  oxmetrics -b commands.txt # execute batch command")"
LANG_ZH "" ""
LANG_ZH "支持：计量经济学、时间序列、预测、面板数据" "Supported: Econometrics, Time Series, Forecasting, Panel Data"
