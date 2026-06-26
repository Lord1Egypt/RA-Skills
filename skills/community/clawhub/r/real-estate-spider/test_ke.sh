#!/bin/bash

# 测试贝壳找房

echo "=== 测试贝壳找房爬虫 ==="

# 检查 agent-browser 是否可用
if ! command -v agent-browser &> /dev/null; then
    echo "agent-browser 未安装"
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

echo "2. 访问贝壳找房首页"
agent-browser open "https://ke.com"
agent-browser wait 5000

echo "3. 截图保存首页"
agent-browser screenshot "ke_homepage.png"

echo "4. 获取页面信息"
agent-browser get title
agent-browser get url

echo "5. 查看页面元素"
agent-browser snapshot -i

echo "=== 测试完成 ==="
echo "截图保存在: ke_homepage.png"