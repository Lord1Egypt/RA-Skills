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
LANG_ZH "版本: $JAGS_VERSION" "Version: $JAGS_VERSION"

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
    LANG_ZH "找到 JAGS: $JAGS_BIN" "Found JAGS: $JAGS_BIN"
    JAGS_VER=$($JAGS_BIN --version 2>&1 | head -1 || echo "unknown")
    LANG_ZH "版本: $JAGS_VER" "Version: $JAGS_VER"
else
    LANG_ZH "未找到 JAGS。" "JAGS not found."
    LANG_ZH "安装选项:" "Install options:"
    echo "  macOS:   brew install jags"
    echo "  Ubuntu:  apt-get install jags"
    echo "  Windows: Download from https://sourceforge.net/projects/mcmc-jags/"
    JAGS_BIN="NOT_INSTALLED"
fi

# Update config.json
if [ -f "$CONFIG_FILE" ] && [ "$JAGS_BIN" != "NOT_INSTALLED" ]; then
    LANG_ZH "正在更新配置..." "Updating config.json..."
    # Use Python to update JSON (more reliable than jq)
    python3 -c "
import json, sys
with open(sys.argv[1], 'r') as f:
    config = json.load(f)
config['JAGS'] = {
    'version': sys.argv[2],
    'path': sys.argv[3],
    'platform': 'all',
    'mode': 'simple'
}
with open(sys.argv[1], 'w') as f:
    json.dump(config, f, indent=2)
print('config.json 已更新。')
" "$CONFIG_FILE" "$JAGS_VERSION" "$JAGS_BIN"
fi

LANG_ZH "" ""
LANG_ZH "JAGS CLI 用法:" "JAGS CLI Usage:"
echo "  jags scriptfile          # Run JAGS script"
echo "  jags-script script.txt   # Batch execution"
LANG_ZH "" ""
LANG_ZH "支持：贝叶斯层次模型、MCMC 模拟" "Supported: Bayesian hierarchical models, MCMC simulation"
