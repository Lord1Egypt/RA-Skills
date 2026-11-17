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

# Setup script for JAGS (Just Another Gibbs Sampler)
# Bayesian hierarchical models via MCMC

JAGS_VERSION="4.3.0"
CONFIG_FILE="$(dirname "$0")/../../config.json"

LANG_ZH "=== JAGS 贝叶斯抽样器配置 ===" "=== JAGS Setup ==="
if statsoft_reveal; then
    LANG_ZH "版本: $JAGS_VERSION" "Version: $JAGS_VERSION"
else
    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
fi

# Detect JAGS installation
JAGS_BIN=""
if command -v jags &> /dev/null; then
    JAGS_BIN=$(command -v jags)
elif [ -f /usr/local/bin/jags ]; then
    JAGS_BIN=/usr/local/bin/jags
elif [ -f /usr/bin/jags ]; then
    JAGS_BIN=/usr/bin/jags
fi

if [ -n "$JAGS_BIN" ]; then
    if statsoft_reveal; then
        LANG_ZH "找到 JAGS: $JAGS_BIN" "Found JAGS: $JAGS_BIN"
    else
        echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
    fi
    JAGS_VER="unknown"
    if [ "${STATSOFT_VERIFY:-0}" = "1" ]; then
        JAGS_VER=$($JAGS_BIN --version 2>&1 | head -1 || echo "unknown")
    fi
    if statsoft_reveal; then
        LANG_ZH "版本: $JAGS_VER" "Version: $JAGS_VER"
    else
        echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
    fi
else
    LANG_ZH "未找到 JAGS。" "JAGS not found."
    LANG_ZH "安装选项:" "Install options:"
    echo "  macOS:   brew install jags"
    echo "  Ubuntu:  apt-get install jags"
    echo "  Windows: Download from https://sourceforge.net/projects/mcmc-jags/"
    JAGS_BIN="NOT_INSTALLED"
fi

# Config persistence (fail-closed: detection-only by default; persists only on explicit opt-in)
if [ -f "$CONFIG_FILE" ] && [ "$JAGS_BIN" != "NOT_INSTALLED" ]; then
    LANG_ZH "默认仅检测；写入需 opt-in（STATSOFT_AUTO_WRITE=1）" "Detection-only by default; write requires opt-in (STATSOFT_AUTO_WRITE=1)"
    # Use Python to update JSON (more reliable than jq)
    _NEW_CFG=$(python3 -c "
import json, sys
with open(sys.argv[1], 'r') as f:
    config = json.load(f)
config['JAGS'] = {
    'version': sys.argv[2],
    'path': sys.argv[3],
    'platform': 'all',
    'mode': 'simple'
}
print(json.dumps(config, ensure_ascii=False))" "$CONFIG_FILE" "$JAGS_VERSION" "$JAGS_BIN")
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
LANG_ZH "JAGS CLI 用法:" "JAGS CLI Usage:"
echo "  jags scriptfile          # Run JAGS script"
echo "  jags-script script.txt   # Batch execution"
LANG_ZH "" ""
LANG_ZH "支持：贝叶斯层次模型、MCMC 模拟" "Supported: Bayesian hierarchical models, MCMC simulation"
