#!/bin/bash
# Sequoia-X 运行脚本
set -e

INSTALL_DIR="${HOME}/sequoia-x"

if [ ! -d "$INSTALL_DIR" ]; then
    echo "❌ 未安装，请先运行 install.sh"
    exit 1
fi

cd "$INSTALL_DIR"
python main.py
