#!/bin/bash

# JWT插件快速验证脚本
# 在安装JWT插件后运行

echo "🚀 JWT插件安装验证"
echo "=================="
echo "WordPress站点: https://openow.ai"
echo "验证时间: $(date)"
echo ""

# 检查JWT端点
echo "1. 🔍 检查JWT端点..."
JWT_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X GET "https://openow.ai/wp-json/jwt-auth/v1/token")

if [ "$JWT_RESPONSE" = "405" ]; then
    echo "✅ JWT端点存在 (需要POST请求)"
elif [ "$JWT_RESPONSE" = "404" ]; then
    echo "❌ JWT端点不存在 (404) - 插件可能未安装"
    echo "   请检查:"
    echo "   1. 插件是否已安装并激活"
    echo "   2. 固定链接设置是否正确"
    exit 1
else
    echo "⚠️  JWT端点响应: $JWT_RESPONSE"
fi

# 尝试获取JWT令牌
echo ""
echo "2. 🔐 尝试获取JWT令牌..."
echo "   用户名: inkmind"

TOKEN_RESPONSE=$(curl -s -X POST "https://openow.ai/wp-json/jwt-auth/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"inkmind","password":"SAGI b8Zi QBOm CQhW xl4N lmP1"}' \
  -w "\nHTTP状态码: %{http_code}")

if echo "$TOKEN_RESPONSE" | grep -q "token"; then
    echo "✅ JWT令牌获取成功!"
    TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
    echo "   令牌: ${TOKEN:0:30}..."
else
    echo "❌ JWT令牌获取失败"
    echo "   响应: $TOKEN_RESPONSE"
fi

# 测试WordPress REST API
echo ""
echo "3. 🌐 测试WordPress REST API..."
API_TEST=$(curl -s -o /dev/null -w "%{http_code}" "https://openow.ai/wp-json/wp/v2")

if [ "$API_TEST" = "200" ]; then
    echo "✅ WordPress REST API正常"
else
    echo "❌ WordPress REST API错误: $API_TEST"
fi

echo ""
echo "🎯 验证完成"
echo ""
echo "📋 下一步:"
echo "   如果JWT令牌获取成功，运行完整测试:"
echo "   cd /root/.openclaw/workspace/skills/wordpress-auto-publish"
echo "   node jwt-token-auth-test.js"
echo ""
echo "🔧 如果失败:"
echo "   1. 检查wp-config.php中的JWT配置"
echo "   2. 确认插件已激活"
echo "   3. 重新保存固定链接"
echo "   4. 检查服务器错误日志"