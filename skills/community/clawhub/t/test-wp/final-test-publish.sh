#!/bin/bash

echo "🎯 最终WordPress发布测试"
echo "========================"
echo "时间: $(date)"
echo ""

# 尝试多种可能的方法
METHODS=(
  "Basic Auth (配置密码)"
  "Basic Auth (应用密码1)"
  "Basic Auth (应用密码2)"
)

PASSWORDS=(
  "QLHH6))acWR&At*PE4uBv5TM"
  "SAGI b8Zi QBOm CQhW xl4N lmP1"
  "HnK3 o7xu KHNy DFtV 2fpZ 7uwG"
)

SUCCESS=false

for i in {0..2}; do
  echo ""
  echo "🔧 尝试方法: ${METHODS[$i]}"
  echo "密码: ${PASSWORDS[$i]:0:10}..."
  
  # 测试发布
  RESPONSE=$(curl -s -w "\nHTTP状态码: %{http_code}" \
    -u "inkmind:${PASSWORDS[$i]}" \
    -X POST "https://openow.ai/wp-json/wp/v2/posts" \
    -H "Content-Type: application/json" \
    -d '{
      "title": "最终测试 - '"$(date +%Y-%m-%d\ %H:%M:%S)"'",
      "content": "<p>这是最终发布测试。</p><p>如果看到这篇文章，说明发布功能已修复！</p>",
      "status": "draft",
      "excerpt": "OpenClaw最终发布测试"
    }')
  
  HTTP_CODE=$(echo "$RESPONSE" | tail -1 | grep -o '[0-9]*$')
  RESPONSE_BODY=$(echo "$RESPONSE" | sed '$d')
  
  echo "状态码: $HTTP_CODE"
  
  if [ "$HTTP_CODE" -eq 201 ] || [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ 发布成功!"
    
    # 提取文章链接
    POST_LINK=$(echo "$RESPONSE_BODY" | grep -o '"link":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    echo "🔗 文章链接: $POST_LINK"
    echo ""
    echo "🎉 成功! 使用的密码: ${METHODS[$i]}"
    
    # 保存结果
    echo "文章链接: $POST_LINK" > final-success.txt
    echo "使用方法: ${METHODS[$i]}" >> final-success.txt
    echo "时间: $(date)" >> final-success.txt
    
    SUCCESS=true
    break
  else
    echo "❌ 失败"
    # 只显示错误消息的前100个字符
    ERROR_MSG=$(echo "$RESPONSE_BODY" | grep -o '"message":"[^"]*"' | head -1 | cut -d'"' -f4 || echo "未知错误")
    echo "错误: ${ERROR_MSG:0:50}..."
  fi
done

echo ""
echo "=".repeat(50)

if [ "$SUCCESS" = true ]; then
  echo "🎊 测试成功完成!"
  echo "文章已发布到WordPress"
  echo "链接已保存到: final-success.txt"
else
  echo "😞 所有方法都失败"
  echo ""
  echo "🔍 可能的原因:"
  echo "1. 用户权限不足 (需要作者或编辑角色)"
  echo "2. REST API写入权限被限制"
  echo "3. 需要启用特定插件"
  echo "4. 密码不正确"
  echo ""
  echo "💡 建议:"
  echo "1. 登录WordPress检查用户角色"
  echo "2. 确认应用程序密码已正确设置"
  echo "3. 检查WordPress REST API设置"
  echo "4. 尝试使用管理员账户"
fi