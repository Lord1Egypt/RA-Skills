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

# setup_cmdstan.sh — Detect and configure CmdStan (cross-platform)
set -euo pipefail

CONFIG_PATH="$(dirname "$0")/../../config.json"

# Try to find CmdStan
CMDSTAN_PATH=""
if [ -n "${CMDSTAN:-}" ] && [ -d "$CMDSTAN" ]; then
    CMDSTAN_PATH="$CMDSTAN"
elif [ -d "$HOME/.cmdstan" ]; then
    CMDSTAN_PATH="$HOME/.cmdstan"
elif [ -d "$HOME/.cmdstanpy/cmdstan" ]; then
    CMDSTAN_PATH="$HOME/.cmdstanpy/cmdstan"
elif [ -d "/opt/cmdstan" ]; then
    CMDSTAN_PATH="/opt/cmdstan"
fi

if [ -z "$CMDSTAN_PATH" ]; then
    LANG_ZH "错误: 未找到 CmdStan。请设置 CMDSTAN 环境变量或通过 cmdstanpy 安装，或" "ERROR: CmdStan not found. Set CMDSTAN env var, install via cmdstanpy, or"
    echo "$(LANG_ZH "  推荐固定版本安装（请先核对版本号与脚本内容）：" "  Recommended: pin a fixed version (verify version number and script contents):")"
    echo "  bash -c 'curl -sSL https://raw.githubusercontent.com/stan-dev/cmdstan/v2.37.0/install_cmdstan.sh -o install_cmdstan.sh && cat install_cmdstan.sh && bash install_cmdstan.sh'"
    echo "$(LANG_ZH "  ⚠️ 该命令会联网下载并直接执行脚本，请确认来源可信、已审阅内容后再运行；如需其他版本请替换 v2.37.0 为对应发布标签。" "  ⚠️ This command downloads from the network and runs the script directly. Confirm the source is trusted and review the contents before running. To use another version, replace v2.37.0 with the corresponding release tag.")"
    exit 1
fi

# Get version
VERSION=""
MAKEFILE="$CMDSTAN_PATH/make/local"
if [ -f "$MAKEFILE" ] && grep -q "STAN_THREADS" "$MAKEFILE" 2>/dev/null; then
    VERSION="2.30+"
fi
if [ -f "$CMDSTAN_PATH/VERSION" ]; then
    VERSION=$(cat "$CMDSTAN_PATH/VERSION")
fi


if statsoft_reveal; then
    LANG_ZH "CmdStan: $CMDSTAN_PATH" "CmdStan: $CMDSTAN_PATH"
else
    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
fi
if statsoft_reveal; then
    LANG_ZH "版本: ${VERSION:-unknown}" "Version: ${VERSION:-unknown}"
else
    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
fi

# Config persistence (fail-closed: detection-only by default; persists only on explicit opt-in)
if command -v python3 &>/dev/null; then
    _NEW_CFG=$(python3 - <<EOF
import json, os, sys
cfg_path = "$CONFIG_PATH"
cfg = {}
if os.path.exists(cfg_path):
    with open(cfg_path, 'r') as f:
        cfg = json.load(f)
cfg["CmdStan"] = {
    "installed": True,
    "path": "$CMDSTAN_PATH",
    "version": "${VERSION:-unknown}",
    "mode": "simple"
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
