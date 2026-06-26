#!/bin/bash
# PPT Generator - Wrapper Script
# 
# 使用方法: ./generate-ppt.sh --topic "主题" --style "风格" --pages 页数
#
# 风格选项: comic, tech, minimalist, chinese, nature, corporate
# 默认: 根据内容自动检测

TOPIC="My Presentation"
STYLE=""
PAGES=5
REQUEST=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --topic)
            TOPIC="$2"
            shift 2
            ;;
        --style)
            STYLE="$2"
            shift 2
            ;;
        --pages)
            PAGES="$2"
            shift 2
            ;;
        --request)
            REQUEST="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# 运行Node脚本
cd /tmp && node /root/.openclaw/workspace/skills/ppt-generator/scripts/generate-ppt.js \
    --topic "$TOPIC" \
    --style "$STYLE" \
    --pages "$PAGES" \
    --request "$REQUEST"
