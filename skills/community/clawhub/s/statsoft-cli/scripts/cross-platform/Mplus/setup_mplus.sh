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

# setup_mplus.sh — Detect and configure Mplus (macOS/Linux)
set -euo pipefail

CONFIG_PATH="$(dirname "$0")/../../config.json"

# Search common Mplus paths
MPLUS_BIN=""
if [ -n "${MPLUS_HOME:-}" ] && [ -d "$MPLUS_HOME" ]; then
    MPLUS_BIN="$MPLUS_HOME/mplus"
elif [ -f "/Applications/Mplus/mplus" ]; then
    MPLUS_BIN="/Applications/Mplus/mplus"
elif [ -f "/usr/local/bin/mplus" ]; then
    MPLUS_BIN="/usr/local/bin/mplus"
elif [ -f "$HOME/mplus/mplus" ]; then
    MPLUS_BIN="$HOME/mplus/mplus"
fi

if [ -z "$MPLUS_BIN" ] || [ ! -f "$MPLUS_BIN" ]; then
    LANG_ZH "错误: 未找到 Mplus。" "ERROR: Mplus not found."
    echo "  Download from https://www.statmodel.com/"
    echo "  Or set MPLUS_HOME env var"
    exit 1
fi

MPLUS_DIR="$(dirname "$MPLUS_BIN")"

if statsoft_reveal; then
    LANG_ZH "Mplus: $MPLUS_BIN" "Mplus: $MPLUS_BIN"
else
    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
fi
if statsoft_reveal; then
    LANG_ZH "Dir: $MPLUS_DIR" "Dir: $MPLUS_DIR"
else
    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
fi

if command -v python3 &>/dev/null; then
    _NEW_CFG=$(python3 - <<EOF
import json, os
cfg_path = "$CONFIG_PATH"
cfg = {}
if os.path.exists(cfg_path):
    with open(cfg_path, 'r') as f:
        cfg = json.load(f)
cfg["Mplus"] = {
    "installed": True,
    "path": "$MPLUS_DIR",
    "binary": "$MPLUS_BIN",
    "version": "unknown",
    "platform": "macos"
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
