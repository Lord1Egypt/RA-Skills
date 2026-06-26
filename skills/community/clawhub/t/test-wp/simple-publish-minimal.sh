#!/bin/bash

# 最小化WordPress发布测试
echo "📝 WordPress最小化发布测试"
echo "=========================="

# 创建简单的JSON数据（避免特殊字符问题）
JSON_DATA='{
  "title": "OpenClaw测试文章 - 2026-04-12",
  "content": "<h1>OpenClaw测试文章</h1><p>这是一个通过OpenClaw自动发布的测试文章。</p><p>测试时间: 2026年4月12日 08:17</p>",
  "status": "draft",
  "excerpt": "OpenClaw WordPress发布功能测试"
}'

echo "📤 发布文章..."
echo "标题: OpenClaw测试文章 - 2026-04-12"

# 发布文章
RESPONSE=$(curl -s -w "\nHTTP状态码: %{http_code}" \
  -u "inkmind:QLHH6))acWR&At*PE4uBv5TM" \
  -X POST "https://openow.ai/wp-json/wp/v2/posts" \
  -H "Content-Type: application/json" \
  -d "$JSON_DATA")

# 提取HTTP状态码
HTTP_CODE=$(echo "$RESPONSE" | tail -1 | grep -o '[0-9]*$')
RESPONSE_BODY=$(echo "$RESPONSE" | sed '$d')

echo ""
echo "📊 发布结果:"
echo "HTTP状态码: $HTTP_CODE"

if [ "$HTTP_CODE" -eq 201 ] || [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ 文章发布成功!"
    
    # 提取文章ID和链接
    POST_ID=$(echo "$RESPONSE_BODY" | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)
    POST_LINK=$(echo "$RESPONSE_BODY" | grep -o '"link":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    echo "📝 文章ID: $POST_ID"
    echo "🔗 文章链接: $POST_LINK"
    
    # 保存结果
    echo "文章ID: $POST_ID" > publish-result.txt
    echo "文章链接: $POST_LINK" >> publish-result.txt
    echo "发布时间: $(date)" >> publish-result.txt
    
    echo ""
    echo "📁 结果已保存到: publish-result.txt"
    
    # 显示文章链接
    echo ""
    echo "🎯 文章已成功发布!"
    echo "🔗 链接: $POST_LINK"
else
    echo "❌ 文章发布失败"
    echo "错误响应:"
    echo "$RESPONSE_BODY" | head -c 500
fi