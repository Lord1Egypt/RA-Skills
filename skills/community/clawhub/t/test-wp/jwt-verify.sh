#!/bin/bash

# JWT插件安装验证脚本
# 在安装JWT插件并配置wp-config.php后运行

echo "🔍 JWT插件安装验证"
echo "=================="
echo "WordPress站点: https://openow.ai"
echo "验证时间: $(date)"
echo "用户名: inkmind"
echo ""

# 1. 检查JWT端点
echo "1. 🔍 检查JWT端点..."
JWT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET "https://openow.ai/wp-json/jwt-auth/v1/token")

case $JWT_STATUS in
    405)
        echo "✅ JWT端点存在 (需要POST请求)"
        ;;
    404)
        echo "❌ JWT端点不存在 (404)"
        echo "   可能的问题:"
        echo "   - JWT插件未安装或未激活"
        echo "   - 固定链接设置不正确"
        echo "   - 服务器配置问题"
        exit 1
        ;;
    500)
        echo "🔥 JWT端点服务器错误 (500)"
        echo "   可能的问题:"
        echo "   - JWT_AUTH_SECRET_KEY 未配置"
        echo "   - wp-config.php 配置错误"
        echo "   - PHP错误"
        exit 1
        ;;
    *)
        echo "⚠️  JWT端点响应: $JWT_STATUS"
        ;;
esac

# 2. 尝试获取JWT令牌
echo ""
echo "2. 🔐 尝试获取JWT令牌..."
TOKEN_RESPONSE=$(curl -s -X POST "https://openow.ai/wp-json/jwt-auth/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"inkmind","password":"SAGI b8Zi QBOm CQhW xl4N lmP1"}')

# 检查响应
if echo "$TOKEN_RESPONSE" | grep -q '"token"'; then
    echo "✅ JWT令牌获取成功!"
    
    # 提取令牌信息
    TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
    USER_EMAIL=$(echo "$TOKEN_RESPONSE" | grep -o '"user_email":"[^"]*"' | cut -d'"' -f4)
    USER_NAME=$(echo "$TOKEN_RESPONSE" | grep -o '"user_display_name":"[^"]*"' | cut -d'"' -f4)
    
    echo "   令牌: ${TOKEN:0:30}..."
    echo "   用户: $USER_NAME ($USER_EMAIL)"
    
    # 保存令牌到文件（可选）
    echo "$TOKEN" > /tmp/jwt-token.txt
    echo "   令牌已保存到: /tmp/jwt-token.txt"
    
elif echo "$TOKEN_RESPONSE" | grep -q '"message"'; then
    ERROR_MSG=$(echo "$TOKEN_RESPONSE" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
    echo "❌ JWT令牌获取失败: $ERROR_MSG"
    
    if echo "$ERROR_MSG" | grep -qi "invalid username"; then
        echo "   可能的问题: 用户名或密码错误"
    elif echo "$ERROR_MSG" | grep -qi "not logged in"; then
        echo "   可能的问题: 认证失败"
    fi
    
else
    echo "❌ JWT令牌获取失败，未知响应"
    echo "   响应: $TOKEN_RESPONSE"
fi

# 3. 如果获取到令牌，测试API访问
if [ -n "$TOKEN" ]; then
    echo ""
    echo "3. 🌐 测试JWT API访问..."
    
    # 测试用户信息端点
    USER_RESPONSE=$(curl -s -X GET "https://openow.ai/wp-json/wp/v2/users/me" \
      -H "Authorization: Bearer $TOKEN")
    
    if echo "$USER_RESPONSE" | grep -q '"name"'; then
        USER_NAME=$(echo "$USER_RESPONSE" | grep -o '"name":"[^"]*"' | cut -d'"' -f4)
        echo "✅ JWT API访问成功"
        echo "   用户: $USER_NAME"
        
        # 测试文章发布
        echo ""
        echo "4. 📝 测试JWT发布功能..."
        echo "   运行完整测试:"
        echo "   cd /root/.openclaw/workspace/skills/wordpress-auto-publish"
        echo "   node jwt-token-auth-test.js"
    else
        echo "❌ JWT API访问失败"
        echo "   响应: $USER_RESPONSE"
    fi
fi

# 4. 测试WordPress REST API基础
echo ""
echo "5. 🔧 测试WordPress REST API基础..."
API_TEST=$(curl -s -o /dev/null -w "%{http_code}" "https://openow.ai/wp-json/wp/v2")

if [ "$API_TEST" = "200" ]; then
    echo "✅ WordPress REST API正常"
else
    echo "❌ WordPress REST API错误: $API_TEST"
fi

echo ""
echo "🎯 验证完成"
echo ""
echo "📋 总结:"
if [ -n "$TOKEN" ]; then
    echo "✅ JWT插件安装配置成功!"
    echo "   可以开始使用JWT令牌自动发布文章"
else
    echo "❌ JWT插件配置有问题"
    echo "   请检查安装和配置步骤"
fi
echo ""
echo "🚀 下一步:"
echo "   运行完整测试: node jwt-token-auth-test.js"
echo ""
echo "🔧 如果遇到问题:"
echo "   1. 检查 wp-config.php 中的JWT配置"
echo "   2. 确认插件已激活"
echo "   3. 重新保存固定链接"
echo "   4. 查看服务器错误日志"