#!/bin/bash

echo "🔐 测试应用程序密码发布..."
echo "=========================="

# 使用应用程序密码
APP_PASSWORD="SAGI b8Zi QBOm CQhW xl4N lmP1"

# 创建简单的测试文章
JSON_DATA='{
  "title": "应用程序密码测试文章",
  "content": "<p>这是一个使用应用程序密码发布的测试文章。</p><p>测试时间: $(date)</p>",
  "status": "draft",
  "excerpt": "测试WordPress应用程序密码功能"
}'

echo "尝试发布文章..."

RESPONSE=$(curl -s -w "\nHTTP状态码: %{http_code}" \
  -u "inkmind:$APP_PASSWORD" \
  -X POST "https://openow.ai/wp-json/wp/v2/posts" \
  -H "Content-Type: application/json" \
  -d "$JSON_DATA")

HTTP_CODE=$(echo "$RESPONSE" | tail -1 | grep -o '[0-9]*$')
RESPONSE_BODY=$(echo "$RESPONSE" | sed '$d')

echo "HTTP状态码: $HTTP_CODE"

if [ "$HTTP_CODE" -eq 201 ] || [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ 发布成功!"
    
    POST_ID=$(echo "$RESPONSE_BODY" | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)
    POST_LINK=$(echo "$RESPONSE_BODY" | grep -o '"link":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    echo "文章ID: $POST_ID"
    echo "文章链接: $POST_LINK"
    
    # 保存结果
    echo "文章ID: $POST_ID" > app-password-result.txt
    echo "文章链接: $POST_LINK" >> app-password-result.txt
    echo "应用程序密码: $APP_PASSWORD" >> app-password-result.txt
else
    echo "❌ 发布失败"
    echo "响应: $RESPONSE_BODY"
fi