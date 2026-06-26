#!/bin/bash

# File Manager Skill - 验证脚本
# 用法: bash scripts/verify.sh

echo "=== 文件管理验证 ==="
echo ""

ERRORS=0

# 检查目录结构
for dir in user_input_files my_outputs; do
  if [ ! -d "/workspace/$dir" ]; then
    echo "❌ 目录缺失: /workspace/$dir"
    ERRORS=$((ERRORS + 1))
  else
    echo "✅ 目录存在: /workspace/$dir"
  fi
done

# 检查子目录
for subdir in images videos pdfs docxs excels others; do
  if [ ! -d "/workspace/user_input_files/$subdir" ]; then
    echo "❌ 子目录缺失: /workspace/user_input_files/$subdir"
    ERRORS=$((ERRORS + 1))
  fi
  if [ ! -d "/workspace/my_outputs/$subdir" ]; then
    echo "❌ 子目录缺失: /workspace/my_outputs/$subdir"
    ERRORS=$((ERRORS + 1))
  fi
done

# 检查是否有文件在根目录（不应该有）
ROOT_FILES=$(ls /workspace/*.jpg /workspace/*.png /workspace/*.mp4 /workspace/*.pdf /workspace/*.xlsx 2>/dev/null | wc -l)
if [ $ROOT_FILES -gt 0 ]; then
  echo "❌ 根目录有遗留文件: $(ls /workspace/*.jpg /workspace/*.png /workspace/*.mp4 /workspace/*.pdf /workspace/*.xlsx 2>/dev/null)"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ 根目录无遗留文件"
fi

# 检查 output 目录是否有嵌套的 output 文件夹（常见错误）
if [ -d "/workspace/my_outputs/output" ]; then
  echo "❌ 发现嵌套目录: /workspace/my_outputs/output"
  ERRORS=$((ERRORS + 1))
fi

echo ""
if [ $ERRORS -eq 0 ]; then
  echo "✅ 验证通过！文件结构正确。"
  exit 0
else
  echo "❌ 验证失败！发现 $ERRORS 个问题，请修复后再交付文件。"
  exit 1
fi
