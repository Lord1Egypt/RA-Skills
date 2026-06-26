#!/bin/bash

# 多搜索引擎对照搜索示例脚本
# 同时搜索 Google 和 Bing，如果 Google 失败则使用夸克AI替代

cd "$(dirname "$0")"

echo "=========================================="
echo "多搜索引擎对照搜索示例"
echo "=========================================="
echo ""

# 示例1: 搜索A股热点
echo "示例1: 搜索A股今日热点"
echo "------------------------------------------"
node multi-search.js "A股今日热点" --max-results=5
echo ""

# 示例2: 搜索股票信息
echo "示例2: 搜索股票信息"
echo "------------------------------------------"
node multi-search.js "贵州茅台 财报" --max-results=3
echo ""

# 示例3: 仅使用Bing搜索
echo "示例3: 仅使用Bing搜索"
echo "------------------------------------------"
node multi-search.js "人工智能新闻" --bing-only --max-results=5
echo ""

echo "=========================================="
echo "搜索完成！"
echo "=========================================="
echo ""
echo "使用提示:"
echo "  1. 默认同时搜索 Google + Bing"
echo "  2. Google 失败时自动使用夸克AI替代"
echo "  3. 可使用 --google-only, --bing-only, --quark-only 指定单一引擎"
echo "  4. 使用 --format=json 输出JSON格式"
echo ""