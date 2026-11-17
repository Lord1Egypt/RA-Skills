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

# Setup script for GenStat
# Statistical analysis, data mining, and experimental design

GENSTAT_VERSION="23.0"
CONFIG_FILE="$(dirname "$0")/../../config.json"

LANG_ZH "=== GenStat 统计软件配置 ===" "=== GenStat Setup ==="
if statsoft_reveal; then
    LANG_ZH "版本: $GENSTAT_VERSION" "Version: $GENSTAT_VERSION"
else
    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
fi

# Detect GenStat installation
GENSTAT_BIN=""
if command -v genstat &> /dev/null; then
    GENSTAT_BIN=$(command -v genstat)
elif [ -f /usr/local/bin/genstat ]; then
    GENSTAT_BIN=/usr/local/bin/genstat
elif [ -f /usr/bin/genstat ]; then
    GENSTAT_BIN=/usr/bin/genstat
elif [ -f "/opt/genstat/genstat" ]; then
    GENSTAT_BIN="/opt/genstat/genstat"
fi

if [ -n "$GENSTAT_BIN" ]; then
    if statsoft_reveal; then
        LANG_ZH "找到 GenStat: $GENSTAT_BIN" "Found GenStat: $GENSTAT_BIN"
    else
        echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
    fi
else
    LANG_ZH "未找到 GenStat。" "GenStat not found."
    LANG_ZH "安装：从 https://vsni.co.uk/genstat 下载" "Install: Download from https://vsni.co.uk/genstat"
    GENSTAT_BIN="NOT_INSTALLED"
fi

# Config persistence (fail-closed: detection-only by default; persists only on explicit opt-in)
if [ -f "$CONFIG_FILE" ] && [ "$GENSTAT_BIN" != "NOT_INSTALLED" ]; then
    LANG_ZH "默认仅检测；写入需 opt-in（STATSOFT_AUTO_WRITE=1）" "Detection-only by default; write requires opt-in (STATSOFT_AUTO_WRITE=1)"
    _NEW_CFG=$(python3 -c "
import json, sys
with open(sys.argv[1], 'r') as f:
    config = json.load(f)
config['GenStat'] = {
    'version': sys.argv[2],
    'path': sys.argv[3],
    'platform': 'all',
    'mode': 'simple'
}
print(json.dumps(config, ensure_ascii=False))" "$CONFIG_FILE" "$GENSTAT_VERSION" "$GENSTAT_BIN")
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
LANG_ZH "GenStat CLI 用法:" "GenStat CLI Usage:"
echo "  genstat commands.txt      # Run GenStat command file"
echo "  genstat --help            # Show CLI options"
LANG_ZH "" ""
LANG_ZH "支持：混合模型、实验设计、RELD、空间分析、Meta 分析" "Supported: Mixed Models, Experimental Design, REML, Spatial Analysis, Meta-Analysis"
