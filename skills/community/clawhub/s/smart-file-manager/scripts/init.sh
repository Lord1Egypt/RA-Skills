#!/bin/bash

# File Manager Skill - 初始化目录结构
# 用法: bash scripts/init.sh

echo "=== 初始化文件管理目录 ==="
echo ""

# 创建目录结构
mkdir -p /workspace/user_input_files/{images,videos,pdfs,excels,others}
mkdir -p /workspace/my_outputs/{images,videos,pdfs,excels,others}

echo "✅ 目录结构创建完成"

# 运行验证
bash "$(dirname "$0")/verify.sh"
