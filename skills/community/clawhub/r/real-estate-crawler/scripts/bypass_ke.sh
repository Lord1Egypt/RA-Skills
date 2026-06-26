#!/bin/bash

# 测试贝壳找房使用 agent-browser

echo "=== 贝壳找房测试（agent-browser） ==="

# 检查 agent-browser 是否可用
if ! command -v agent-browser &> /dev/null; then
    echo "agent-browser 未安装"
    exit 1
fi

echo "1. 设置更真实的浏览器指纹（移动设备）"
agent-browser set device "iPhone 14"
agent-browser set viewport 375 812
agent-browser set headers '{
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}'

echo "2. 访问贝壳找房北京二手房页面"
agent-browser open "https://bj.ke.com/ershoufang"
agent-browser wait 5000

echo "3. 截图保存首页"
agent-browser screenshot "ke_ershoufang_page.png"

echo "4. 获取页面信息"
agent-browser get title
agent-browser get url

echo "5. 查看页面元素"
agent-browser snapshot -i

echo "6. 模拟人类浏览行为"
agent-browser scroll down 300
agent-browser wait 1000
agent-browser scroll down 300
agent-browser wait 1000

echo "7. 截图保存浏览后的页面"
agent-browser screenshot "ke_ershoufang_scrolled.png"

echo "8. 查看页面文本内容"
agent-browser get text > "ke_ershoufang_content.txt"

echo "9. 检查是否有验证码"
agent-browser find role text --name "人机验证"
agent-browser find role text --name "CAPTCHA"
agent-browser find role text --name "验证"

echo "10. 如果看到验证码，尝试手动处理"
echo "可能需要手动完成验证码，然后继续浏览"

echo "11. 查看页面是否包含房产信息"
agent-browser snapshot -c --scope ".house-list"
agent-browser snapshot -c --scope ".property-list"
agent-browser snapshot -c --scope ".list"

echo "=== 测试完成 ==="
echo "截图保存在: ke_ershoufang_page.png, ke_ershoufang_scrolled.png"
echo "文本内容保存在: ke_ershoufang_content.txt"

echo "注意事项:"
echo "1. 贝壳找房有严格的反爬虫机制"
echo "2. 可能需要手动处理验证码"
echo "3. 使用移动设备UA可能降低被检测概率"
echo "4. 随机延迟和行为模拟是关键"