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

RATTLE_VERSION="5.5"
CONFIG_FILE="$(dirname "$0")/../../config.json"

LANG_ZH "=== Rattle 数据挖掘工具配置 ===" "=== Rattle Setup ==="
LANG_ZH "版本: $RATTLE_VERSION" "Version: $RATTLE_VERSION"

# Detect Rattle installation
RATTLE_BIN=""
if command -v rattle &> /dev/null; then
    RATTLE_BIN=$(command -v rattle)
elif [ -f /usr/local/bin/rattle ]; then
    RATTLE_BIN=/usr/local/bin/rattle
elif [ -f /usr/bin/rattle ]; then
    RATTLE_BIN=/usr/bin/rattle
fi

# Check R Rattle package
RATTLE_R=""
if Rscript -e "library(rattle)" 2>/dev/null; then
    RATTLE_R=$(Rscript -e "cat(system.file(package='rattle'))")
    LANG_ZH "Rattle R 包: $RATTLE_R" "Rattle R package: $RATTLE_R"
fi

if [ -n "$RATTLE_BIN" ] || [ -n "$RATTLE_R" ]; then
    LANG_ZH "找到 Rattle。" "Found Rattle."
else
    LANG_ZH "未找到 Rattle。" "Rattle not found."
    LANG_ZH "安装选项:" "Install options:"
    echo "  R: install.packages('rattle')"
    echo "  Download from https://rattle.togaware.com/"
    RATTLE_BIN="NOT_INSTALLED"
fi

# Update config.json
if [ -f "$CONFIG_FILE" ] && [ "$RATTLE_BIN" != "NOT_INSTALLED" ]; then
    LANG_ZH "正在更新配置..." "Updating config.json..."
    python3 -c "
import json, sys
with open(sys.argv[1], 'r') as f:
    config = json.load(f)
config['Rattle'] = {
    'version': sys.argv[2],
    'path': sys.argv[3],
    'platform': 'all',
    'mode': 'simple'
}
with open(sys.argv[1], 'w') as f:
    json.dump(config, f, indent=2)
print('config.json updated.')
" "$CONFIG_FILE" "$RATTLE_VERSION" "$RATTLE_BIN"
fi

LANG_ZH "" ""
LANG_ZH "Rattle CLI 用法:" "Rattle CLI Usage:"
echo "  rattle --cli               # CLI 模式运行 Rattle"
echo "  rattle --script file.R    # 执行脚本"
LANG_ZH "" ""
LANG_ZH "支持：数据挖掘、决策树、聚类、关联规则、文本挖掘" "Supported: Data Mining, Decision Trees, Clustering, Association Rules, Text Mining"
