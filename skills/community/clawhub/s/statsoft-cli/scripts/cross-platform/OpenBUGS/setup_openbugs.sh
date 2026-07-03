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

# Setup script for OpenBUGS
# Bayesian statistical modeling using MCMC

OPENBUGS_VERSION="3.2.3"
CONFIG_FILE="$(dirname "$0")/../../config.json"

LANG_ZH "=== OpenBUGS 贝叶斯分析配置 ===" "=== OpenBUGS Setup ==="
LANG_ZH "版本: $OPENBUGS_VERSION" "Version: $OPENBUGS_VERSION"

# Detect OpenBUGS installation
OPENBUGS_BIN=""
if command -v openbugs &> /dev/null; then
    OPENBUGS_BIN=$(command -v openbugs)
elif [ -f /usr/local/bin/openbugs ]; then
    OPENBUGS_BIN=/usr/local/bin/openbugs
elif [ -f /usr/bin/openbugs ]; then
    OPENBUGS_BIN=/usr/bin/openbugs
elif [ -f "/opt/openbugs/openbugs" ]; then
    OPENBUGS_BIN="/opt/openbugs/openbugs"
fi

if [ -n "$OPENBUGS_BIN" ]; then
    LANG_ZH "找到 OpenBUGS: $OPENBUGS_BIN" "Found OpenBUGS: $OPENBUGS_BIN"
else
    LANG_ZH "未找到 OpenBUGS。" "OpenBUGS not found."
    LANG_ZH "安装选项:" "Install options:"
    echo "  Ubuntu:  apt-get install openbugs"
    echo "  macOS:   brew install openbugs"
    echo "  Windows: Download from https://openbugs.net/"
    OPENBUGS_BIN="NOT_INSTALLED"
fi

# Update config.json
if [ -f "$CONFIG_FILE" ] && [ "$OPENBUGS_BIN" != "NOT_INSTALLED" ]; then
    LANG_ZH "正在更新配置..." "Updating config.json..."
    python3 -c "
import json, sys
with open(sys.argv[1], 'r') as f:
    config = json.load(f)
config['OpenBUGS'] = {
    'version': sys.argv[2],
    'path': sys.argv[3],
    'platform': 'all',
    'mode': 'simple'
}
with open(sys.argv[1], 'w') as f:
    json.dump(config, f, indent=2)
print('config.json updated.')
" "$CONFIG_FILE" "$OPENBUGS_VERSION" "$OPENBUGS_BIN"
fi

LANG_ZH "" ""
LANG_ZH "OpenBUGS CLI 用法:" "OpenBUGS CLI Usage:"
echo "  openbugs --help            # 显示 CLI 选项"
echo "  openbugs -b script.txt    # 通过脚本批执行"
LANG_ZH "" ""
LANG_ZH "支持：贝叶斯分析、MCMC、层次模型" "Supported: Bayesian Analysis, MCMC, Hierarchical Models"
