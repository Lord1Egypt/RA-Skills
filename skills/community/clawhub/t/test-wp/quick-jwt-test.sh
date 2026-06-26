#!/bin/bash

# JWT插件快速测试脚本
# 在安装JWT插件后运行

echo "🚀 JWT插件快速测试"
echo "=================="
echo "WordPress站点: https://openow.ai"
echo "测试时间: $(date)"
echo ""

# 测试1: 检查JWT端点是否存在
echo "1. 🔍 检查JWT端点..."
curl -s -o /dev/null -w "%{http_code}" -X GET "https://openow.ai/wp-json/jwt-auth/v1/token"
JWT_STATUS=$?

if [ $JWT_STATUS -eq 0 ]; then
    echo "✅ JWT端点响应正常"
else
    echo "❌ JWT端点无响应"
fi

# 测试2: 尝试获取JWT令牌
echo ""
echo "2. 🔐 尝试获取JWT令牌..."
echo "   使用用户名: inkmind"
echo "   密码: [已设置]"

curl -X POST "https://openow.ai/wp-json/jwt-auth/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"inkmind","password":"SAGI b8Zi QBOm CQhW xl4N lmP1"}' \
  -w "\nHTTP状态码: %{http_code}\n"

# 测试3: 检查WordPress REST API
echo ""
echo "3. 🌐 检查WordPress REST API..."
curl -s "https://openow.ai/wp-json/wp/v2" | grep -o '"name":"[^"]*"' | head -1

# 测试4: 检查插件列表API
echo ""
echo "4. 🧩 检查插件端点..."
curl -s -o /dev/null -w "插件端点状态码: %{http_code}\n" "https://openow.ai/wp-json/wp/v2/plugins"

echo ""
echo "🎯 测试完成"
echo ""
echo "📋 如果JWT端点返回404:"
echo "   1. 确认插件已安装并激活"
echo "   2. 检查wp-config.php配置"
echo "   3. 检查Nginx服务器配置"
echo "   4. 尝试重新保存固定链接"
echo ""
echo "📋 如果返回500错误:"
echo "   1. 检查JWT_AUTH_SECRET_KEY是否设置"
echo "   2. 检查PHP错误日志"
echo "   3. 确保密钥足够长（32+字符）"
echo ""
echo "📋 如果返回401/403:"
echo "   1. 检查用户名和密码"
echo "   2. 检查用户权限"
echo "   3. 尝试使用应用程序密码"