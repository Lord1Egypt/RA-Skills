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

# setup_pspp.sh — Detect and configure PSPP (cross-platform, SPSS alternative)
set -euo pipefail

CONFIG_PATH="$(dirname "$0")/../../config.json"

PSPP_BIN=""
if command -v pspp &>/dev/null; then
    PSPP_BIN="$(which pspp)"
elif [ -n "${PSPP_HOME:-}" ] && [ -d "$PSPP_HOME" ]; then
    PSPP_BIN="$PSPP_HOME/pspp"
elif [ -f "/usr/bin/pspp" ]; then
    PSPP_BIN="/usr/bin/pspp"
elif [ -f "/usr/local/bin/pspp" ]; then
    PSPP_BIN="/usr/local/bin/pspp"
elif [ -f "/Applications/pspp.app/Contents/MacOS/pspp" ]; then
    PSPP_BIN="/Applications/pspp.app/Contents/MacOS/pspp"
fi

if [ -z "$PSPP_BIN" ] || [ ! -f "$PSPP_BIN" ]; then
    LANG_ZH "错误: 未找到 PSPP。" "ERROR: PSPP not found."
    echo "  Install from https://www.gnu.org/software/pspp/"
    exit 1
fi

PSPP_DIR="$(dirname "$PSPP_BIN")"

LANG_ZH "PSPP: $PSPP_BIN" "PSPP: $PSPP_BIN"
LANG_ZH "Dir: $PSPP_DIR" "Dir: $PSPP_DIR"

if command -v python3 &>/dev/null; then
    python3 - <<EOF 2>/dev/null || LANG_ZH "警告: 无法更新 config.json" "WARN: Could not update config.json"
import json, os
cfg_path = "$CONFIG_PATH"
cfg = {}
if os.path.exists(cfg_path):
    with open(cfg_path, 'r') as f:
        cfg = json.load(f)
cfg["PSPP"] = {
    "installed": True,
    "path": "$PSPP_DIR",
    "binary": "$PSPP_BIN",
    "version": "unknown",
    "platform": "all"
}
with open(cfg_path, 'w') as f:
    json.dump(cfg, f, indent=2)
print("Config updated.")
EOF
fi

LANG_ZH "完成." "Done."
