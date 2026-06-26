#!/bin/bash

# 测试链家使用 agent-browser

echo "=== 链家测试（agent-browser） ==="

# 检查 agent-browser 是否可用
if ! command -v agent-browser &> /dev/null; then
    echo "agent-browser 未安装"
    exit 1
fi

echo "1. 设置真实浏览器指纹（桌面设备）"
agent-browser set viewport 1920 1080
agent-browser set headers '{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.google.com/"
}'

echo "2. 访问链家北京二手房页面"
agent-browser open "https://www.lianjia.com/ershoufang/bj/"
agent-browser wait 5000

echo "3. 截图保存首页"
agent-browser screenshot "lianjia_ershoufang_page.png"

echo "4. 获取页面信息"
agent-browser get title
agent-browser get url

echo "5. 查看页面元素"
agent-browser snapshot -i

echo "6. 模拟人类浏览行为"
agent-browser scroll down 500
agent-browser wait 1500
agent-browser scroll down 500
agent-browser wait 1500
agent-browser scroll down 500
agent-browser wait 1500

echo "7. 截图保存浏览后的页面"
agent-browser screenshot "lianjia_ershoufang_scrolled.png"

echo "8. 查看页面文本内容"
agent-browser get text > "lianjia_ershoufang_content.txt"

echo "9. 检查是否有验证码或反爬虫提示"
agent-browser find role text --name "验证码"
agent-browser find role text --name "人机验证"
agent-browser find role text --name "禁止访问"

echo "10. 查看页面是否包含房产信息"
agent-browser snapshot -c --scope ".list"
agent-browser snapshot -c --scope ".item"
agent-browser snapshot -c --scope ".property"
agent-browser snapshot -c --scope ".house"

echo "11. 尝试点击分类筛选"
agent-browser find role button click --name "区域"
agent-browser wait 2000
agent-browser snapshot -i

echo "12. 搜索特定区域"
agent-browser find role textbox fill @e[textbox] "朝阳区"
agent-browser wait 1000
agent-browser find role button click --name "搜索"

echo "13. 查看搜索结果"
agent-browser wait 3000
agent-browser screenshot "lianjia_search_result.png"

echo "14. 获取房产列表"
agent-browser snapshot -c --scope ".house-list"
agent-browser snapshot -c --scope ".content-list"

echo "=== 测试完成 ==="
echo "截图保存在: lianjia_ershoufang_page.png, lianjia_ershoufang_scrolled.png, lianjia_search_result.png"
echo "文本内容保存在: lianjia_ershoufang_content.txt"

echo "注意事项:"
echo "1. 链家可能也有反爬虫机制"
echo "2. 观察是否有验证码或访问限制"
echo "3. 保存会话状态以备后续使用"
echo "4. 如果遇到验证码，可能需要人工干预"

echo "链家可能的反爬虫措施:"
echo "1. IP限制"
echo "2. Cookie验证"
echo "3. JavaScript检测"
echo "4. 行为模式检测"