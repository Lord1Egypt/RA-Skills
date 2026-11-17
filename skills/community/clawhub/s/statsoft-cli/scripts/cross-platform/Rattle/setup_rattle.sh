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

# Setup script for Rattle (R data mining GUI / CLI)
# Data mining with R, GUI + CLI

set -euo pipefail

statsoft_reveal() { [ "${STATSOFT_REVEAL:-0}" = "1" ]; }
statsoft_verify() { [ "${STATSOFT_VERIFY:-0}" = "1" ]; }

CONFIG_FILE="$(dirname "$0")/../../config.json"

# Detect Rattle installation
RATTLE_BIN=""
if command -v rattle &> /dev/null; then
    RATTLE_BIN=$(command -v rattle)
elif [ -f /usr/local/bin/rattle ]; then
    RATTLE_BIN=/usr/local/bin/rattle
elif [ -f /usr/bin/rattle ]; then
    RATTLE_BIN=/usr/bin/rattle
fi

# Derive version dynamically; requires opt-in query (no hardcoded version)
if statsoft_verify && [ -n "$RATTLE_BIN" ]; then
    RATTLE_VERSION=$("$RATTLE_BIN" --version 2>&1 | head -1 || echo "unknown")
else
    RATTLE_VERSION="unknown (set STATSOFT_VERIFY=1)"
fi

LANG_ZH "=== Rattle 数据挖掘工具配置 ===" "=== Rattle Setup ==="
if statsoft_reveal && [ -n "$RATTLE_BIN" ]; then
    LANG_ZH "找到 Rattle: $RATTLE_BIN" "Found Rattle: $RATTLE_BIN"
    LANG_ZH "版本: $RATTLE_VERSION" "Version: $RATTLE_VERSION"
elif [ -z "$RATTLE_BIN" ]; then
    LANG_ZH "未找到 Rattle。" "Rattle not found."
    LANG_ZH "安装选项:" "Install options:"
    echo "  R: install.packages('rattle')"
    echo "  Download from https://rattle.togaware.com/"
    RATTLE_BIN="NOT_INSTALLED"
else
    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
fi

# Check R Rattle package — Rscript invocation is gated by the VERIFY gate (SDI-1).
# Only execute the R interpreter when VERIFY=1; otherwise use passive path detection.
# The path is disclosed only when REVEAL=1 (Issue 7).
RATTLE_R=""
if statsoft_verify; then
    if Rscript -e "library(rattle)" 2>/dev/null; then
        RATTLE_R=$(Rscript -e "cat(system.file(package='rattle'))")
        if statsoft_reveal; then
            LANG_ZH "Rattle R 包: $RATTLE_R" "Rattle R package: $RATTLE_R"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
    fi
else
    # Passive detection: check known R package install locations without executing R.
    for rpath in \
        /usr/local/lib/R/site-library/rattle \
        /usr/lib/R/site-library/rattle \
        /usr/share/R/library/rattle \
        "$HOME/R/x86_64-pc-linux-gnu-library/rattle" \
        "$HOME/R/i386-pc-linux-gnu-library/rattle"; do
        if [ -d "$rpath" ]; then
            RATTLE_R="$rpath"
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
            break
        fi
    done
    if [ -z "$RATTLE_R" ] && command -v Rscript &>/dev/null; then
        echo "$(LANG_ZH "Rscript 可用，设置 STATSOFT_VERIFY=1 查询 R 包元数据" "Rscript available; set STATSOFT_VERIFY=1 to query R package metadata.")"
    fi
fi

if ([ -n "$RATTLE_BIN" ] && [ "$RATTLE_BIN" != "NOT_INSTALLED" ]) || [ -n "$RATTLE_R" ]; then
    LANG_ZH "找到 Rattle。" "Found Rattle."
fi

# Config persistence (fail-closed: detection-only by default; persists only on explicit opt-in)
if [ -f "$CONFIG_FILE" ] && [ "$RATTLE_BIN" != "NOT_INSTALLED" ]; then
    LANG_ZH "默认仅检测；写入需 opt-in（STATSOFT_AUTO_WRITE=1）" "Detection-only by default; write requires opt-in (STATSOFT_AUTO_WRITE=1)"
    _RATTLE_PATH_REVEALED=$(statsoft_reveal && echo "$RATTLE_BIN" || echo "REDACTED")
    _NEW_CFG=$(python3 -c "
import json, sys
with open(sys.argv[1], 'r') as f:
    config = json.load(f)
config['Rattle'] = {
    'version': sys.argv[2],
    'path': sys.argv[3],
    'platform': 'all',
    'mode': 'simple'
}
print(json.dumps(config, ensure_ascii=False))" "$CONFIG_FILE" "$RATTLE_VERSION" "$_RATTLE_PATH_REVEALED")
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
LANG_ZH "Rattle CLI 用法:" "Rattle CLI Usage:"
echo "$(LANG_ZH "  rattle --cli               # CLI 模式运行 Rattle" "  rattle --cli               # run Rattle in CLI mode")"
echo "$(LANG_ZH "  rattle --script file.R    # 执行脚本" "  rattle --script file.R    # execute script")"
LANG_ZH "" ""
LANG_ZH "支持：数据挖掘、决策树、聚类、关联规则、文本挖掘" "Supported: Data Mining, Decision Trees, Clustering, Association Rules, Text Mining"
