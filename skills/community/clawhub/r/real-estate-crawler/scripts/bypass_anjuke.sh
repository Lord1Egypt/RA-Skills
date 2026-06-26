#!/bin/bash

# 房产中介网站反爬虫绕过脚本
# 支持：安居客、贝壳找房、链家、搜房网

echo "=== 房产中介网站反爬虫脚本 ==="
echo "支持的网站:"
echo "1. 安居客 (anjuke)"
echo "2. 贝壳找房 (ke)"
echo "3. 链家 (lianjia)"
echo "4. 搜房网 (soufun)"

# 选择网站
echo -n "请输入要爬取的网站编号 (1-4): "
read WEBSITE_NUM

case $WEBSITE_NUM in
    1)
        WEBSITE="anjuke"
        URL="https://www.anjuke.com"
        ;;
    2)
        WEBSITE="ke"
        URL="https://ke.com"
        ;;
    3)
        WEBSITE="lianjia"
        URL="https://www.lianjia.com"
        ;;
    4)
        WEBSITE="soufun"
        URL="https://www.soufun.com"
        ;;
    *)
        echo "无效的选择"
        exit 1
        ;;
esac

echo -n "请输入城市 (如: 北京, 上海, 广州): "
read CITY

echo -n "请输入区域 (可选，留空跳过): "
read DISTRICT

echo "=== 开始爬取 $WEBSITE - $CITY ==="

# 检查 agent-browser 是否可用
if ! command -v agent-browser &> /dev/null; then
    echo "agent-browser 未安装"
    echo "请先运行: npm install -g agent-browser"
    exit 1
fi

echo "1. 设置真实浏览器指纹"
agent-browser set viewport 1920 1080
agent-browser set headers '{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}'

echo "2. 访问网站首页"
agent-browser open "$URL"
agent-browser wait 5000

echo "3. 检查是否被重定向到验证码页面"
agent-browser get url
agent-browser wait 2000

echo "4. 设置Cookie模拟真实用户"
agent-browser cookies set "ctid" "16"
agent-browser cookies set "twe" "2"
agent-browser cookies set "obtain_by" "3"
agent-browser cookies set "city" "$CITY"

echo "5. 模拟城市选择"
if [ "$WEBSITE" = "anjuke" ]; then
    agent-browser open "https://$CITY.anjuke.com"
elif [ "$WEBSITE" = "ke" ]; then
    agent-browser open "https://ke.com/city/$CITY"
elif [ "$WEBSITE" = "lianjia" ]; then
    agent-browser open "https://www.lianjia.com/ershoufang/$CITY"
elif [ "$WEBSITE" = "soufun" ]; then
    agent-browser open "https://$CITY.soufun.com"
fi

agent-browser wait 3000

echo "6. 模拟人类浏览行为"
agent-browser snapshot -i
agent-browser scroll down 300
agent-browser wait 1000
agent-browser scroll down 300
agent-browser wait 1000

echo "7. 查找二手房链接"
agent-browser find role link click --name "二手房" || \
agent-browser find text "二手房" click || \
agent-browser find text "二手房源" click || \
agent-browser find role link click --name "二手"

agent-browser wait 4000
agent-browser snapshot -i

echo "8. 检查是否有验证码元素"
agent-browser get text ".pop" || echo "没有找到验证码弹窗"
agent-browser get text ".captcha" || echo "没有找到验证码"
agent-browser get text ".anti-spider" || echo "没有找到反爬虫警告"

echo "9. 截图保存当前页面状态"
agent-browser screenshot "$WEBSITE_$CITY_page.png"

echo "10. 开始获取房源信息"
echo "尝试定位房源列表元素..."

# 根据网站不同定位元素
if [ "$WEBSITE" = "anjuke" ]; then
    agent-browser snapshot -c --scope ".property-list"
elif [ "$WEBSITE" = "ke" ]; then
    agent-browser snapshot -c --scope ".house-list"
elif [ "$WEBSITE" = "lianjia" ]; then
    agent-browser snapshot -c --scope ".list-item"
elif [ "$WEBSITE" = "soufun" ]; then
    agent-browser snapshot -c --scope ".property-item"
else
    agent-browser snapshot -c --scope ".list" --scope ".item" --scope ".property"
fi

agent-browser wait 2000

echo "11. 获取页面文本内容"
agent-browser get text > "$WEBSITE_$CITY_data.txt"

echo "12. 滚动查看更多房源"
for i in {1..5}; do
    echo "滚动第 $i 次..."
    agent-browser scroll down 500
    agent-browser wait 2000
    agent-browser snapshot -i
done

echo "13. 保存会话状态"
agent-browser state save "$WEBSITE_session.json"

echo "14. 输出页面标题和URL"
agent-browser get title
agent-browser get url

echo "15. 获取详细页面信息"
# 尝试点击第一个房源查看详情
agent-browser find first role link click
agent-browser wait 5000
agent-browser screenshot "$WEBSITE_$CITY_detail.png"

echo "16. 保存PDF格式页面"
agent-browser pdf "$WEBSITE_$CITY_data.pdf"

echo "=== 脚本结束 ==="
echo "总结:"
echo "1. 页面截图: $WEBSITE_$CITY_page.png"
echo "2. 详细截图: $WEBSITE_$CITY_detail.png"
echo "3. 文本数据: $WEBSITE_$CITY_data.txt"
echo "4. PDF数据: $WEBSITE_$CITY_data.pdf"
echo "5. 会话状态: $WEBSITE_session.json"

echo "注意事项:"
echo "1. 验证码可能需要人工干预"
echo "2. 建议控制访问频率（每分钟不超过10次）"
echo "3. 如果需要大量数据，建议使用代理IP轮换"
echo "4. 保存的会话状态可用于后续访问"

echo "数据分析建议:"
echo "1. 使用Python脚本提取结构化数据"
echo "2. 分析价格趋势和分布"
echo "3. 统计不同区域的价格差异"
echo "4. 比较不同房产类型的价格"

# Python数据分析脚本建议
echo "
如需进一步分析数据，可使用以下Python脚本:
python3 ~/.openclaw/workspace/skills/real-estate-spider/scripts/real_estate_crawler.py \
  -w $WEBSITE \
  -c $CITY \
  -d '$DISTRICT' \
  -p 1 \
  -o $WEBSITE_$CITY_properties.json \
  -f json
"