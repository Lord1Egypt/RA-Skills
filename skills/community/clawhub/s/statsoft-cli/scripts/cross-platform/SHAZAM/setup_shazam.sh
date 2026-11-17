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

# Setup script for SHAZAM Econometrics Software
# Comprehensive econometrics, statistics and analytics

set -euo pipefail

statsoft_reveal() { [ "${STATSOFT_REVEAL:-0}" = "1" ]; }
statsoft_verify() { [ "${STATSOFT_VERIFY:-0}" = "1" ]; }

CONFIG_FILE="$(dirname "$0")/../../config.json"

# Detect SHAZAM installation
SHAZAM_BIN=""
if command -v shazam &> /dev/null; then
    SHAZAM_BIN=$(command -v shazam)
elif [ -f /usr/local/bin/shazam ]; then
    SHAZAM_BIN=/usr/local/bin/shazam
elif [ -f /usr/bin/shazam ]; then
    SHAZAM_BIN=/usr/bin/shazam
elif [ -f "/opt/shazam/shazam" ]; then
    SHAZAM_BIN="/opt/shazam/shazam"
fi

LANG_ZH "=== SHAZAM 计量经济学配置 ===" "=== SHAZAM Setup ==="
if statsoft_reveal && [ -n "$SHAZAM_BIN" ]; then
    LANG_ZH "找到 SHAZAM: $SHAZAM_BIN" "Found SHAZAM: $SHAZAM_BIN"
elif [ -z "$SHAZAM_BIN" ]; then
    LANG_ZH "未找到 SHAZAM。" "SHAZAM not found."
    LANG_ZH "安装：从 https://www.econometrics.com/ 下载" "Install: Download from https://www.econometrics.com/"
    SHAZAM_BIN="NOT_INSTALLED"
else
    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
fi

# Derive version dynamically; requires opt-in query (no hardcoded version)
SHAZAM_VER="unknown (set STATSOFT_VERIFY=1)"
if statsoft_verify && [ -n "$SHAZAM_BIN" ] && [ "$SHAZAM_BIN" != "NOT_INSTALLED" ]; then
    SHAZAM_VER=$("$SHAZAM_BIN" --version 2>&1 | head -1 || echo "unknown")
fi
if statsoft_reveal; then
    LANG_ZH "版本: $SHAZAM_VER" "Version: $SHAZAM_VER"
else
    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
fi

# Config persistence (fail-closed: detection-only by default; persists only on explicit opt-in)
if [ -f "$CONFIG_FILE" ] && [ "$SHAZAM_BIN" != "NOT_INSTALLED" ]; then
    LANG_ZH "默认仅检测；写入需 opt-in（STATSOFT_AUTO_WRITE=1）" "Detection-only by default; write requires opt-in (STATSOFT_AUTO_WRITE=1)"
    _NEW_CFG=$(python3 -c "
import json, sys
with open(sys.argv[1], 'r') as f:
    config = json.load(f)
config['SHAZAM'] = {
    'version': sys.argv[2],
    'path': sys.argv[3],
    'platform': 'all',
    'mode': 'simple'
}
print(json.dumps(config, ensure_ascii=False))" "$CONFIG_FILE" "$SHAZAM_VER" "$SHAZAM_BIN")
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
LANG_ZH "SHAZAM CLI 用法:" "SHAZAM CLI Usage:"
echo "  shazam < commands.txt       # Run SHAZAM command file"
LANG_ZH "" ""
LANG_ZH "支持：计量经济学、时间序列、假设检验、回归" "Supported: Econometrics, Time Series, Hypothesis Testing, Regression"
