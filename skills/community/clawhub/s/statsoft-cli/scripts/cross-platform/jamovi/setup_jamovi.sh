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

# setup_jamovi.sh — Detect and configure jamovi (cross-platform)
set -euo pipefail

CONFIG_PATH="$(dirname "$0")/../../config.json"

JAMOVI_BIN=""
if command -v jamovi &>/dev/null; then
    JAMOVI_BIN="$(which jamovi)"
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

LANG_ZH "jamovi: $JAMOVI_BIN" "jamovi: $JAMOVI_BIN"
LANG_ZH "Dir: $JAMOVI_DIR" "Dir: $JAMOVI_DIR"

if command -v python3 &>/dev/null; then
    python3 - <<EOF 2>/dev/null || LANG_ZH "警告: 无法更新 config.json" "WARN: Could not update config.json"
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
with open(cfg_path, 'w') as f:
    json.dump(cfg, f, indent=2)
print("Config updated.")
EOF
fi

LANG_ZH "完成." "Done."
