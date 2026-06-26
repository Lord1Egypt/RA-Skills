#!/bin/bash

# 代码功能测试 Skill 创建脚本

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[*] 创建目录结构..."
mkdir -p "$SKILL_DIR/scripts/log"
mkdir -p "$SKILL_DIR/scripts/release/v1"
mkdir -p "$SKILL_DIR/references"

echo "[*] 安装依赖..."
pip install -r "$SKILL_DIR/scripts/requirements.txt"

echo "[+] code_test skill 创建完成"
echo ""
echo "使用方法:"
echo "  python $SKILL_DIR/scripts/main.py -r '测试需求描述'"
echo "  python $SKILL_DIR/scripts/main.py -r '测试需求' -k '关键词1,关键词2' --fix"
