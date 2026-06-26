#!/bin/bash
# 太极架构 Skills 打包脚本
# 生成可分发的 zip 包
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT="$SCRIPT_DIR/taichi-skill.zip"

echo "=== 打包太极架构 Skills ==="

# 排除运行时生成的文件
cd "$SCRIPT_DIR"
zip -r "$OUTPUT" \
    taichi-framework/orchestrator.py \
    taichi-framework/core/ \
    taichi-framework/configs/ \
    taichi-framework/tests/ \
    taichi-framework/install.sh \
    taichi-framework/start.sh \
    taichi-framework/uninstall.sh \
    taichi-framework/requirements.txt \
    taichi-framework/README.md \
    SKILL.md \
    install.sh \
    uninstall.sh \
    package.sh \
    -x "*/__pycache__/*" \
    -x "*/venv/*" \
    -x "*/workspace/*" \
    -x "*/.git/*" \
    -x "*/node_modules/*"

echo ""
echo "=== 打包完成 ==="
echo "包位置: $OUTPUT"
echo ""
echo "使用方法:"
echo "  1. 解压到任意目录"
echo "  2. 运行 ./install.sh 安装依赖"
echo "  3. 启动: ./taichi-framework/start.sh --mode centralized --request 'test'"
