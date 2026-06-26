#!/bin/bash
# 职业教育政策快速抓取脚本
# Quick vocational education policy scraping script

echo "==================================="
echo "职业教育政策快速抓取"
echo "Vocational Education Quick Scraper"
echo "==================================="
echo ""

# 检查日期参数
DAYS=${1:-7}
echo "时间范围: 最近 $DAYS 天"
echo "Time range: Last $DAYS days"
echo ""

# 方法1: curl简单抓取
echo "方法1: 使用curl抓取教育部首页"
echo "Method 1: Using curl to scrape MOE homepage"
echo "-------------------------------------------"

curl -s "https://www.moe.gov.cn/" | \
  grep -i "职业" | \
  grep -oP 'title="[^"]*"' | \
  head -10

echo ""
echo "方法2: 抓取新闻发布页面"
echo "Method 2: Scrape news releases page"
echo "-------------------------------------------"

curl -s "https://www.moe.gov.cn/jyb_xwfb/" | \
  grep -oP '<a[^>]+title="[^"]*职业[^"]*"[^>]*>[^<]+</a>' | \
  head -5

echo ""
echo "方法3: 查找特定日期的内容"
echo "Method 3: Find content from specific dates"
echo "-------------------------------------------"

# 计算日期范围
for ((i=0; i<$DAYS; i++)); do
  DATE=$(date -d "$i days ago" +%Y-%m-%d)
  curl -s "https://www.moe.gov.cn/jyb_xxgk/" | \
    grep "$DATE" | \
    grep -oP 'title="[^"]*"' | \
    head -2
done

echo ""
echo "==================================="
echo "如需更详细的抓取，使用:"
echo "For detailed scraping, use:"
echo "  python3 scripts/simple_scraper.py $DAYS"
echo "==================================="