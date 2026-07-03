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

# Setup script for Tanagra Data Mining
# Open source data mining and machine learning

TANAGRA_VERSION="1.8"
CONFIG_FILE="$(dirname "$0")/../../config.json"

LANG_ZH "=== Tanagra 数据挖掘工具配置 ===" "=== Tanagra Setup ==="
LANG_ZH "版本: $TANAGRA_VERSION" "Version: $TANAGRA_VERSION"

# Detect Tanagra installation
TANAGRA_BIN=""
if command -v tanagra &> /dev/null; then
    TANAGRA_BIN=$(command -v tanagra)
elif [ -f /usr/local/bin/tanagra ]; then
    TANAGRA_BIN=/usr/local/bin/tanagra
elif [ -f /usr/bin/tanagra ]; then
    TANAGRA_BIN=/usr/bin/tanagra
elif [ -f "/opt/tanagra/tanagra" ]; then
    TANAGRA_BIN="/opt/tanagra/tanagra"
fi

if [ -n "$TANAGRA_BIN" ]; then
    LANG_ZH "找到 Tanagra: $TANAGRA_BIN" "Found Tanagra: $TANAGRA_BIN"
else
    LANG_ZH "未找到 Tanagra。" "Tanagra not found."
    LANG_ZH "安装：从 http://data.mines-paristech.fr/tanagra/ 下载" "Install: Download from http://data.mines-paristech.fr/tanagra/"
    TANAGRA_BIN="NOT_INSTALLED"
fi

# Update config.json
if [ -f "$CONFIG_FILE" ] && [ "$TANAGRA_BIN" != "NOT_INSTALLED" ]; then
    LANG_ZH "正在更新配置..." "Updating config.json..."
    python3 -c "
import json, sys
with open(sys.argv[1], 'r') as f:
    config = json.load(f)
config['Tanagra'] = {
    'version': sys.argv[2],
    'path': sys.argv[3],
    'platform': 'all',
    'mode': 'simple'
}
with open(sys.argv[1], 'w') as f:
    json.dump(config, f, indent=2)
print('config.json updated.')
" "$CONFIG_FILE" "$TANAGRA_VERSION" "$TANAGRA_BIN"
fi

LANG_ZH "" ""
LANG_ZH "Tanagra CLI 用法:" "Tanagra CLI Usage:"
echo "  tanagra --help            # 显示 CLI 选项"
echo "  tanagra -f script.txt    # 执行批脚本"
LANG_ZH "" ""
LANG_ZH "支持：聚类、分类、关联规则、特征选择" "Supported: Clustering, Classification, Association Rules, Feature Selection"
