#!/bin/bash
# 财务数据解析脚本（支持无 jq 环境）

DATA_FILE=$1

if [ -z "$DATA_FILE" ] || [ ! -f "$DATA_FILE" ]; then
    echo "用法：$0 <数据文件>"
    exit 1
fi

echo "=== 解析财务数据 ==="
echo "文件：$DATA_FILE"
echo ""

if command -v jq &> /dev/null; then
    jq -r '.revenue // "N/A", .netProfit // "N/A"' "$DATA_FILE" 2>/dev/null
else
    # 使用 grep 和 awk 解析
    echo "使用 grep 解析..."
    grep -oP '"f57":"[^"]*"|"f43":"[^"]*"|"f44":"[^"]*"' "$DATA_FILE"
fi
