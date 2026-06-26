#!/bin/bash

# JWT插件完整安装和配置脚本
# 需要WordPress管理员权限

echo "🚀 WordPress JWT插件完整安装指南"
echo "================================="
echo "站点: https://openow.ai"
echo "时间: $(date)"
echo ""

echo "📋 安装前检查清单:"
echo "1. ✅ WordPress版本: 6.9.4 (支持JWT)"
echo "2. ❓ JWT插件状态: 未安装"
echo "3. ❓ 管理员权限: 需要确认"
echo "4. ❓ 服务器访问: 需要确认"
echo ""

echo "🎯 安装方案选择:"
echo ""
echo "方案A: 通过WordPress后台安装 (推荐)"
echo "   适合: 有WordPress后台管理员权限"
echo "   步骤:"
echo "   1. 访问 https://openow.ai/wp-admin"
echo "   2. 登录管理员账号"
echo "   3. 进入 插件 → 安装插件"
echo "   4. 搜索 'JWT Authentication for WP REST API'"
echo "   5. 安装并激活"
echo ""
echo "方案B: 手动安装插件"
echo "   适合: 有服务器/FTP访问权限"
echo "   步骤:"
echo "   1. 下载插件: https://downloads.wordpress.org/plugin/jwt-authentication-for-wp-rest-api.zip"
echo "   2. 上传到 /wp-content/plugins/"
echo "   3. 在后台激活插件"
echo ""
echo "方案C: 使用WP-CLI安装"
echo "   适合: 有SSH访问权限，已安装WP-CLI"
echo "   命令:"
echo "   wp plugin install jwt-authentication-for-wp-rest-api --activate"
echo ""

echo "🔧 配置步骤 (安装后必须执行):"
echo ""
echo "步骤1: 配置 wp-config.php"
echo "   1. 备份 wp-config.php"
echo "   2. 编辑文件，在 'stop editing' 之前添加:"
cat << 'EOF'

// ========================
// JWT Authentication 配置
// ========================

// JWT密钥 - 必须设置，使用强密码
define('JWT_AUTH_SECRET_KEY', 'your-very-strong-secret-key-here');

// 启用CORS支持
define('JWT_AUTH_CORS_ENABLE', true);

// 可选: 调整令牌过期时间 (秒)
// define('JWT_AUTH_EXPIRE', 86400); // 24小时
EOF
echo ""
echo "步骤2: 生成安全密钥"
echo "   运行以下命令生成32字符密钥:"
echo "   openssl rand -base64 32"
echo "   或使用在线生成器: https://randomkeygen.com/"
echo ""
echo "步骤3: 验证安装"
echo "   运行验证脚本:"
echo "   cd /root/.openclaw/workspace/skills/wordpress-auto-publish"
echo "   ./jwt-verify.sh"
echo ""

echo "🚀 快速测试脚本 (安装配置后运行):"
cat << 'EOF'
#!/bin/bash
# jwt-verify.sh

echo "🔍 JWT插件安装验证"
echo "站点: https://openow.ai"
echo ""

# 测试JWT端点
echo "1. 测试JWT端点..."
curl -s -o /dev/null -w "状态码: %{http_code}\n" -X GET "https://openow.ai/wp-json/jwt-auth/v1/token"

echo ""
echo "2. 测试获取JWT令牌..."
curl -X POST "https://openow.ai/wp-json/jwt-auth/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"inkmind","password":"SAGI b8Zi QBOm CQhW xl4N lmP1"}' \
  -w "\n"

echo ""
echo "3. 如果成功，测试发布文章..."
echo "   运行: node jwt-token-auth-test.js"
EOF
echo ""

echo "📋 故障排除:"
echo ""
echo "问题1: JWT端点返回404"
echo "   解决:"
echo "   1. 确认插件已激活"
echo "   2. 重新保存固定链接设置"
echo "   3. 检查 .htaccess 文件"
echo ""
echo "问题2: JWT认证返回500错误"
echo "   解决:"
echo "   1. 检查 JWT_AUTH_SECRET_KEY 是否设置"
echo "   2. 确保密钥足够长 (≥32字符)"
echo "   3. 检查PHP错误日志"
echo ""
echo "问题3: 令牌获取成功但API访问失败"
echo "   解决:"
echo "   1. 检查令牌是否过期"
echo "   2. 验证用户权限"
echo "   3. 检查服务器时间同步"
echo ""

echo "🎯 成功标志:"
echo "✅ https://openow.ai/wp-json/jwt-auth/v1/token 返回JWT令牌"
echo "✅ 可以使用令牌访问 /wp-json/wp/v2/users/me"
echo "✅ 可以发布文章到WordPress"
echo ""

echo "⏱️  预计时间:"
echo "   安装插件: 5分钟"
echo "   配置 wp-config.php: 5分钟"
echo "   测试验证: 5分钟"
echo "   总计: 约15分钟"
echo ""

echo "📞 需要帮助?"
echo "   1. 提供具体的错误信息"
echo "   2. 确认是否有管理员权限"
echo "   3. 检查服务器错误日志"
echo ""

echo "🚀 立即行动:"
echo "   1. 登录WordPress后台安装JWT插件"
echo "   2. 配置 wp-config.php"
echo "   3. 运行验证测试"
echo "   4. 开始自动发布文章"
echo ""

echo "🔗 参考链接:"
echo "   - 插件页面: https://wordpress.org/plugins/jwt-authentication-for-wp-rest-api/"
echo "   - 配置指南: https://wordpress.org/plugins/jwt-authentication-for-wp-rest-api/#installation"
echo "   - GitHub: https://github.com/Tmeister/wp-api-jwt-auth"
echo ""

echo "🎯 安装完成后，运行完整测试:"
echo "cd /root/.openclaw/workspace/skills/wordpress-auto-publish"
echo "node jwt-token-auth-test.js"