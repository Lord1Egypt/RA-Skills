#!/bin/bash
# 智谱文件解析脚本

set -e

API_KEY="${ZHIPU_API_KEY:?请设置 ZHIPU_API_KEY 环境变量}"
API_URL="https://open.bigmodel.cn/api/paas/v4/files/parser/sync"

if [ -z "$1" ]; then
    echo "用法: $0 <文件路径> [文件类型]"
    echo "文件类型: WPS (默认), PDF, DOCX, XLSX, PPTX 等"
    echo "示例: $0 /path/to/document.pdf PDF"
    exit 1
fi

FILE_PATH="$1"
FILE_TYPE="${2:-WPS}"

if [ ! -f "$FILE_PATH" ]; then
    echo "错误: 文件不存在: $FILE_PATH"
    exit 1
fi

curl -s --request POST \
    --url "$API_URL" \
    --header "Authorization: Bearer $API_KEY" \
    --form "file=@$FILE_PATH" \
    --form "tool_type=prime-sync" \
    --form "file_type=$FILE_TYPE"
