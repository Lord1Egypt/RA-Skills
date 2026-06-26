#!/bin/bash
# Taro 项目构建脚本
# 用法: bash build_project.sh [weapp|h5]

set -e

TYPE=${1:-weapp}

echo "🔨 正在构建 $TYPE ..."

if [ "$TYPE" = "weapp" ]; then
  NODE_OPTIONS=--openssl-legacy-provider npm run build:weapp
elif [ "$TYPE" = "h5" ]; then
  NODE_OPTIONS=--openssl-legacy-provider npm run build:h5
else
  echo "❌ 未知类型: $TYPE，使用 weapp 或 h5"
  exit 1
fi

echo "✅ 构建完成，输出在 dist/"
