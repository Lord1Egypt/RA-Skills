#!/bin/bash

# File Manager Skill - 修复嵌套目录问题
# 用法: bash scripts/fix-nested.sh

echo "=== 修复嵌套目录问题 ==="
echo ""

# 检查并修复 my_outputs/output 嵌套问题
if [ -d "/workspace/my_outputs/output" ]; then
  echo "发现嵌套目录: /workspace/my_outputs/output"
  
  # 移动文件
  if [ -d "/workspace/my_outputs/output/images" ]; then
    mv /workspace/my_outputs/output/images/* /workspace/my_outputs/images/ 2>/dev/null
    echo "✅ 移动 images"
  fi
  
  if [ -d "/workspace/my_outputs/output/videos" ]; then
    mv /workspace/my_outputs/output/videos/* /workspace/my_outputs/videos/ 2>/dev/null
    echo "✅ 移动 videos"
  fi
  
  if [ -d "/workspace/my_outputs/output/pdfs" ]; then
    mv /workspace/my_outputs/output/pdfs/* /workspace/my_outputs/pdfs/ 2>/dev/null
    echo "✅ 移动 pdfs"
  fi
  
  if [ -d "/workspace/my_outputs/output/excels" ]; then
    mv /workspace/my_outputs/output/excels/* /workspace/my_outputs/excels/ 2>/dev/null
    echo "✅ 移动 excels"
  fi
  
  if [ -d "/workspace/my_outputs/output/others" ]; then
    mv /workspace/my_outputs/output/others/* /workspace/my_outputs/others/ 2>/dev/null
    echo "✅ 移动 others"
  fi
  
  # 删除空嵌套目录
  rm -rf /workspace/my_outputs/output
  echo "✅ 删除嵌套目录"
else
  echo "✅ 无嵌套目录问题"
fi

echo ""
# 运行验证
bash "$(dirname "$0")/verify.sh"
