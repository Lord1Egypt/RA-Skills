#!/bin/bash

echo "🔄 测试更新现有文章..."
echo "======================"

POST_ID=75

# 尝试更新文章
JSON_DATA='{
  "title": "[更新测试] How to Build an AI Tools Stack Without Paying for Overlap",
  "content": "<p>这是一个更新测试，用于验证WordPress API的更新权限。</p><p>原始文章已被临时修改用于测试目的。</p><p>测试时间: $(date)</p>"
}'

echo "尝试更新文章ID: $POST_ID"

RESPONSE=$(curl -s -w "\nHTTP状态码: %{http_code}" \
  -u "inkmind:QLHH6))acWR&At*PE4uBv5TM" \
  -X POST "https://openow.ai/wp-json/wp/v2/posts/$POST_ID" \
  -H "Content-Type: application/json" \
  -d "$JSON_DATA")

HTTP_CODE=$(echo "$RESPONSE" | tail -1 | grep -o '[0-9]*$')
RESPONSE_BODY=$(echo "$RESPONSE" | sed '$d')

echo "HTTP状态码: $HTTP_CODE"

if [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ 更新成功!"
    
    POST_LINK=$(echo "$RESPONSE_BODY" | grep -o '"link":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    echo "文章链接: $POST_LINK"
    
    # 保存结果
    echo "文章ID: $POST_ID" > update-result.txt
    echo "文章链接: $POST_LINK" >> update-result.txt
    echo "更新时间: $(date)" >> update-result.txt
    
    echo ""
    echo "🎯 文章已成功更新!"
    echo "🔗 链接: $POST_LINK"
else
    echo "❌ 更新失败"
    echo "响应:"
    echo "$RESPONSE_BODY" | head -c 500
fi