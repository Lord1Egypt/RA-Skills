#!/usr/bin/env bash

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

# setup_weka.sh — Detect and configure Weka (cross-platform)
set -euo pipefail

CONFIG_PATH="$(dirname "$0")/../../config.json"

WEKA_DIR=""
if command -v weka &>/dev/null; then
    WEKA_DIR="$(dirname "$(command -v weka)")"
elif [ -n "${WEKA_HOME:-}" ] && [ -d "$WEKA_HOME" ]; then
    WEKA_DIR="$WEKA_HOME"
elif [ -d "/usr/share/weka" ]; then
    WEKA_DIR="/usr/share/weka"
elif [ -d "/usr/local/share/weka" ]; then
    WEKA_DIR="/usr/local/share/weka"
elif [ -d "$HOME/weka" ]; then
    WEKA_DIR="$HOME/weka"
elif [ -d "$HOME/.local/share/weka" ]; then
    WEKA_DIR="$HOME/.local/share/weka"
fi

if [ -z "$WEKA_DIR" ]; then
    LANG_ZH "错误: 未找到 Weka。" "ERROR: Weka not found."
    echo "  Install from https://www.cs.waikato.ac.nz/ml/weka/downloading.html"
    echo "  Or set WEKA_HOME env var"
    exit 1
fi

# Detect WEKA version
VERSION=""
if [ -f "$WEKA_DIR/weka.jar" ]; then
    # Try to extract version from manifest
    VERSION=$(unzip -p "$WEKA_DIR/weka.jar" META-INF/MANIFEST.MF 2>/dev/null | grep -i "Implementation-Version" | head -1 | awk '{print $2}' | tr -d '\r\n')
    [ -z "$VERSION" ] && VERSION="installed"
fi

if statsoft_reveal; then
    LANG_ZH "Weka: $WEKA_DIR" "Weka: $WEKA_DIR"
else
    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
fi
if statsoft_reveal; then
    LANG_ZH "版本: ${VERSION:-unknown}" "Version: ${VERSION:-unknown}"
else
    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
fi

# Write to config
if command -v python3 &>/dev/null; then
    _NEW_CFG=$(python3 - <<EOF
import json, os
cfg_path = "$CONFIG_PATH"
cfg = {}
if os.path.exists(cfg_path):
    with open(cfg_path, 'r') as f:
        cfg = json.load(f)
cfg["Weka"] = {
    "installed": True,
    "path": "$WEKA_DIR",
    "version": "${VERSION:-unknown}",
    "platform": "all"
}
print(json.dumps(cfg, ensure_ascii=False))
EOF
)
    # Fail-closed by default — persist ONLY when explicitly opted in.
    if [ "${STATSOFT_AUTO_WRITE:-0}" = "1" ]; then
        STATSOFT_AUTO_WRITE=1 python3 "$(dirname "$0")/../../common/write_config.py" "$CONFIG_PATH" <<< "$_NEW_CFG"
    elif [ "${STATSOFT_CONFIRM:-0}" = "1" ] && [ -t 0 ]; then
        printf 'Persist detected config to config.json? (y/N) '
        read -r _ans
        case "$_ans" in y|Y|yes) STATSOFT_AUTO_WRITE=1 python3 "$(dirname "$0")/../../common/write_config.py" "$CONFIG_PATH" <<< "$_NEW_CFG" ;; *) echo "Detection-only: config.json NOT modified." ;; esac
    else
        echo "Detection-only: config.json NOT modified. Set STATSOFT_AUTO_WRITE=1 to persist, or STATSOFT_CONFIRM=1 for an interactive prompt."
    fi
fi

LANG_ZH "完成." "Done."
