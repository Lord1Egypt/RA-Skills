#!/bin/bash
# 🔐 反向代理配置脚本
# 用法：./setup-proxy.sh <用户名> <端口>

set -e

USERNAME="$1"
PORT="$2"
OPENCLAW_PORT="${3:-19000}"
TOKEN="${4:-}"

# 如果未提供 Token，从环境变量读取
if [ -z "$TOKEN" ]; then
    TOKEN="${OPENCLAW_WEBCHAT_TOKEN:-}"
fi

# 如果还是没有 Token，提示用户
if [ -z "$TOKEN" ]; then
    echo "❌ 错误：未提供 Token"
    echo ""
    echo "请使用以下方式之一提供 Token："
    echo "  1. 命令行参数：$0 <用户名> <端口> <OpenClaw 端口> <Token>"
    echo "  2. 环境变量：export OPENCLAW_WEBCHAT_TOKEN='your-token'"
    echo ""
    echo "⚠️ 安全提醒："
    echo "  - 不要使用默认 Token"
    echo "  - 不要在命令行中明文传递 Token（使用环境变量）"
    echo "  - Token 应该与 OpenClaw 配置一致"
    exit 1
fi

if [ -z "$USERNAME" ] || [ -z "$PORT" ]; then
    echo "❌ 用法：$0 <用户名> <端口> [OpenClaw 端口] [Token]"
    echo "示例：$0 teacher 8081"
    echo "示例：$0 usera 8082"
    exit 1
fi

# 检查 Nginx 是否安装
if ! command -v nginx &> /dev/null; then
    echo "⚠️  Nginx 未安装，正在安装..."
    sudo apt update && sudo apt install -y nginx
fi

echo "🔧 配置反向代理"
echo "=============="
echo "用户名：$USERNAME"
echo "端口：$PORT"
echo "OpenClaw 端口：$OPENCLAW_PORT"
echo ""
echo "⚠️  安全警告："
echo "  - 此操作需要 sudo 权限"
echo "  - 会修改 /etc/nginx 配置"
echo "  - 会重启 Nginx 服务"
echo "  - Token 会通过环境变量传递（不记录日志）"
echo ""
read -p "是否继续？(y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "❌ 操作已取消"
    exit 0
fi
echo ""

# 创建 Nginx 配置文件
CONFIG_FILE="/etc/nginx/sites-available/openclaw-$USERNAME"

echo "📝 创建配置文件：$CONFIG_FILE"

sudo tee "$CONFIG_FILE" > /dev/null << NGINX_EOF
server {
    listen $PORT;
    server_name _;
    
    # 访问日志
    access_log /var/log/nginx/openclaw-$USERNAME-access.log;
    error_log /var/log/nginx/openclaw-$USERNAME-error.log;
    
    location / {
        # 强制绑定 session 参数
        return 302 http://\$host:$OPENCLAW_PORT/?session=$USERNAME&token=$TOKEN;
    }
}
NGINX_EOF

echo "✅ 配置文件已创建"

# 启用配置
echo "🔗 启用配置..."
if [ -L "/etc/nginx/sites-enabled/openclaw-$USERNAME" ]; then
    echo "⚠️  配置已存在，跳过创建"
else
    sudo ln -s "$CONFIG_FILE" "/etc/nginx/sites-enabled/openclaw-$USERNAME"
    echo "✅ 配置已启用"
fi

# 测试配置
echo "🧪 测试配置..."
if sudo nginx -t; then
    echo "✅ 配置测试通过"
else
    echo "❌ 配置测试失败！"
    exit 1
fi

# 重新加载 Nginx
echo "🔄 重新加载 Nginx..."
if sudo systemctl reload nginx; then
    echo "✅ Nginx 已重新加载"
else
    echo "❌ Nginx 重新加载失败！"
    exit 1
fi

echo ""
echo "======================"
echo "🎉 配置完成！"
echo ""
echo "📋 访问信息："
echo "   用户 $USERNAME 专属链接："
echo "   http://$(hostname -I | awk '{print $1}'):$PORT/"
echo ""
echo "📄 配置文件：$CONFIG_FILE"
echo "📊 访问日志：/var/log/nginx/openclaw-$USERNAME-access.log"
echo ""
echo "💡 管理命令："
echo "   查看状态：sudo systemctl status nginx"
echo "   查看日志：sudo tail -f /var/log/nginx/openclaw-$USERNAME-access.log"
echo "   删除用户：sudo rm /etc/nginx/sites-enabled/openclaw-$USERNAME"
