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

# setup_jasp.sh — Detect and configure JASP (cross-platform)
set -euo pipefail

CONFIG_PATH="$(dirname "$0")/../../config.json"

JASP_BIN=""
if command -v jasp &>/dev/null; then
    JASP_BIN="$(which jasp)"
elif [ -n "${JASP_HOME:-}" ] && [ -d "$JASP_HOME" ]; then
    JASP_BIN="$JASP_HOME/jasp"
elif [ -f "/Applications/JASP.app/Contents/MacOS/jasp" ]; then
    JASP_BIN="/Applications/JASP.app/Contents/MacOS/jasp"
elif [ -f "/usr/bin/jasp" ]; then
    JASP_BIN="/usr/bin/jasp"
fi

if [ -z "$JASP_BIN" ] || [ ! -f "$JASP_BIN" ]; then
    LANG_ZH "错误: 未找到 JASP。" "ERROR: JASP not found."
    echo "  Download from https://jasp-stats.org/download/"
    exit 1
fi

JASP_DIR="$(dirname "$JASP_BIN")"

LANG_ZH "JASP: $JASP_BIN" "JASP: $JASP_BIN"
LANG_ZH "Dir: $JASP_DIR" "Dir: $JASP_DIR"

if command -v python3 &>/dev/null; then
    python3 - <<EOF 2>/dev/null || LANG_ZH "警告: 无法更新 config.json" "WARN: Could not update config.json"
import json, os
cfg_path = "$CONFIG_PATH"
cfg = {}
if os.path.exists(cfg_path):
    with open(cfg_path, 'r') as f:
        cfg = json.load(f)
cfg["JASP"] = {
    "installed": True,
    "path": "$JASP_DIR",
    "binary": "$JASP_BIN",
    "version": "unknown",
    "platform": "all"
}
with open(cfg_path, 'w') as f:
    json.dump(cfg, f, indent=2)
print("Config updated.")
EOF
fi

LANG_ZH "完成." "Done."
