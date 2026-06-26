#!/bin/bash

# 上海落户公示查询脚本
# 功能：抓取上海国际人才网的落户公示信息

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 公示列表页 URL
LIST_URL="https://www.sh-italent.com/News/NewsList.aspx?TagID=5696"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    上海落户公示信息查询${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 创建临时文件
TEMP_DIR=$(mktemp -d)
LIST_FILE="$TEMP_DIR/list.html"
TALENT_FILE="$TEMP_DIR/talent.html"
JUZHUAN_FILE="$TEMP_DIR/juzhuan.html"

cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

echo -e "${YELLOW}[1/4] 获取公示列表页面...${NC}"
curl -s -L "$LIST_URL" -o "$LIST_FILE" \
    -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

if [ ! -s "$LIST_FILE" ]; then
    echo -e "${RED}错误：无法获取公示列表页面${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 列表页面获取成功${NC}"
echo ""

# 解析人才引进公示链接
echo -e "${YELLOW}[2/4] 解析人才引进公示信息...${NC}"
TALENT_URL=$(grep -o 'https://www.sh-italent.com/Article/[0-9]*/[0-9]*\.shtml' "$LIST_FILE" | head -1)

if [ -z "$TALENT_URL" ]; then
    # 尝试另一种解析方式
    TALENT_URL=$(grep -oP '(?<=href=")/Article/\d+/\d+\.shtml(?=")' "$LIST_FILE" | head -1 | sed 's|^|https://www.sh-italent.com|')
fi

if [ -n "$TALENT_URL" ]; then
    echo -e "${GREEN}✓ 找到人才引进公示链接: $TALENT_URL${NC}"
    curl -s -L "$TALENT_URL" -o "$TALENT_FILE" \
        -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    # 提取公示标题
    TALENT_TITLE=$(grep -oP '(?<=<title>)[^<]+' "$TALENT_FILE" | head -1 || echo "未知标题")
    
    # 提取公示时间
    TALENT_DATE=$(grep -oP '\d{4}-\d{2}-\d{2}' "$TALENT_FILE" | head -1 || echo "未知日期")
    
    # 提取公示人数（通过表格行数估算）
    TALENT_COUNT=$(grep -c "<tr" "$TALENT_FILE" 2>/dev/null || echo "未知")
    if [ "$TALENT_COUNT" != "未知" ] && [ "$TALENT_COUNT" -gt 5 ]; then
        TALENT_COUNT=$((TALENT_COUNT - 3))  # 减去表头行
    fi
    
    echo -e "  标题: ${GREEN}$TALENT_TITLE${NC}"
    echo -e "  日期: ${GREEN}$TALENT_DATE${NC}"
    echo -e "  链接: ${GREEN}$TALENT_URL${NC}"
else
    echo -e "${RED}✗ 未找到人才引进公示链接${NC}"
fi

echo ""

# 解析居转户公示链接
echo -e "${YELLOW}[3/4] 解析居转户公示信息...${NC}"
JUZHUAN_URL=$(grep -o 'https://www.sh-italent.com/Article/[0-9]*/[0-9]*\.shtml' "$LIST_FILE" | grep -v "$TALENT_URL" | head -1)

if [ -z "$JUZHUAN_URL" ]; then
    # 尝试另一种解析方式
    JUZHUAN_URL=$(grep -oP '(?<=href=")/Article/\d+/\d+\.shtml(?=")' "$LIST_FILE" | head -2 | tail -1 | sed 's|^|https://www.sh-italent.com|')
fi

if [ -n "$JUZHUAN_URL" ]; then
    echo -e "${GREEN}✓ 找到居转户公示链接: $JUZHUAN_URL${NC}"
    curl -s -L "$JUZHUAN_URL" -o "$JUZHUAN_FILE" \
        -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    # 提取公示标题
    JUZHUAN_TITLE=$(grep -oP '(?<=<title>)[^<]+' "$JUZHUAN_FILE" | head -1 || echo "未知标题")
    
    # 提取公示时间
    JUZHUAN_DATE=$(grep -oP '\d{4}-\d{2}-\d{2}' "$JUZHUAN_FILE" | head -1 || echo "未知日期")
    
    # 提取公示人数
    JUZHUAN_COUNT=$(grep -c "<tr" "$JUZHUAN_FILE" 2>/dev/null || echo "未知")
    if [ "$JUZHUAN_COUNT" != "未知" ] && [ "$JUZHUAN_COUNT" -gt 5 ]; then
        JUZHUAN_COUNT=$((JUZHUAN_COUNT - 3))
    fi
    
    echo -e "  标题: ${GREEN}$JUZHUAN_TITLE${NC}"
    echo -e "  日期: ${GREEN}$JUZHUAN_DATE${NC}"
    echo -e "  链接: ${GREEN}$JUZHUAN_URL${NC}"
else
    echo -e "${RED}✗ 未找到居转户公示链接${NC}"
fi

echo ""

# 输出汇总信息
echo -e "${YELLOW}[4/4] 生成查询结果...${NC}"
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    查询结果汇总${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}【一】人才引进公示${NC}"
if [ -n "$TALENT_URL" ]; then
    echo -e "  公示标题: $TALENT_TITLE"
    echo -e "  公示日期: $TALENT_DATE"
    echo -e "  公示链接: $TALENT_URL"
else
    echo -e "  ${RED}未找到公示信息${NC}"
fi
echo ""
echo -e "${GREEN}【二】居转户公示${NC}"
if [ -n "$JUZHUAN_URL" ]; then
    echo -e "  公示标题: $JUZHUAN_TITLE"
    echo -e "  公示日期: $JUZHUAN_DATE"
    echo -e "  公示链接: $JUZHUAN_URL"
else
    echo -e "  ${RED}未找到公示信息${NC}"
fi
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "查询时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "${BLUE}========================================${NC}"

# 使用 AppleScript 打开浏览器
echo ""
echo -e "${YELLOW}正在打开浏览器查看公示页面...${NC}"

osascript <<EOF
tell application "Safari"
    activate
    set urlList to {}
    
    -- 打开公示列表页
    open location "$LIST_URL"
    delay 1
    
    -- 打开人才引进公示页面（新标签页）
    ${TALENT_URL:+open location "$TALENT_URL"}
    delay 0.5
    
    -- 打开居转户公示页面（新标签页）
    ${JUZHUAN_URL:+open location "$JUZHUAN_URL"}
end tell
EOF

echo -e "${GREEN}✓ 浏览器已打开${NC}"
echo ""
echo -e "${YELLOW}提示：公示期通常为 5 天，每月两次公示（月中和月底）${NC}"
