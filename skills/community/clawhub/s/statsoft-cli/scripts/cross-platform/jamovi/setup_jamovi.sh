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

# setup_jamovi.sh — Detect and configure jamovi (cross-platform)
# ⚠️ SETUP tool: detects software AND persists config to config.json (timestamped backup + explicit y/N confirmation). NOT a read-only scanner. GUI-only software: detection/launch only, no CLI batch.
set -euo pipefail

CONFIG_PATH="$(dirname "$0")/../../config.json"

JAMOVI_BIN=""
if command -v jamovi &>/dev/null; then
    JAMOVI_BIN="$(command -v jamovi)"
elif [ -n "${JAMOVI_HOME:-}" ] && [ -d "$JAMOVI_HOME" ]; then
    JAMOVI_BIN="$JAMOVI_HOME/jamovi"
elif [ -f "/Applications/jamovi.app/Contents/MacOS/jamovi" ]; then
    JAMOVI_BIN="/Applications/jamovi.app/Contents/MacOS/jamovi"
elif [ -f "/usr/bin/jamovi" ]; then
    JAMOVI_BIN="/usr/bin/jamovi"
elif [ -d "$HOME/.local/bin/jamovi" ]; then
    JAMOVI_BIN="$HOME/.local/bin/jamovi"
fi

if [ -z "$JAMOVI_BIN" ] || [ ! -f "$JAMOVI_BIN" ]; then
    LANG_ZH "错误: 未找到 jamovi。" "ERROR: jamovi not found."
    echo "  Download from https://www.jamovi.org/download.html"
    exit 1
fi

JAMOVI_DIR="$(dirname "$JAMOVI_BIN")"

if statsoft_reveal; then
    LANG_ZH "jamovi: $JAMOVI_BIN" "jamovi: $JAMOVI_BIN"
else
    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
fi
if statsoft_reveal; then
    LANG_ZH "Dir: $JAMOVI_DIR" "Dir: $JAMOVI_DIR"
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
cfg["jamovi"] = {
    "installed": True,
    "path": "$JAMOVI_DIR",
    "binary": "$JAMOVI_BIN",
    "version": "unknown",
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
