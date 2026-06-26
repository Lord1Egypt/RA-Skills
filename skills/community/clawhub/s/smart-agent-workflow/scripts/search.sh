#!/bin/bash
# 快速搜索日志

if [ -z "$1" ]; then
  echo "用法: ./search.sh [关键词]"
  exit 1
fi

echo "搜索关键词: $1"
echo "---"
grep -r "$1" ../logs/2026/ | head -20
