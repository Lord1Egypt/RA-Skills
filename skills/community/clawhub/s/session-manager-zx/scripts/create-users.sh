#!/bin/bash
# 👥 多用户批量创建脚本
# 用法：./create-users.sh <用户列表文件>

set -e

USER_FILE="$1"
START_PORT="${2:-8081}"
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
    echo "  1. 命令行参数：$0 <用户文件> [起始端口] [OpenClaw 端口] [Token]"
    echo "  2. 环境变量：export OPENCLAW_WEBCHAT_TOKEN='your-token'"
    echo ""
    exit 1
fi

if [ -z "$USER_FILE" ]; then
    echo "👥 多用户批量创建"
    echo "================="
    echo ""
    echo "用法：$0 <用户列表文件> [起始端口] [OpenClaw 端口] [Token]"
    echo ""
    echo "示例："
    echo "   $0 users.txt 8081"
    echo "   $0 users.txt 8081 OPENCLAW_PORT"
    echo ""
    echo "用户列表文件格式（每行一个用户名）："
    echo "   teacher"
    echo "   usera"
    echo "   userb"
    echo ""
    
    # 创建示例文件
    if [ ! -f "users.txt" ]; then
        cat > users.txt << EOF
teacher
usera
userb
EOF
        echo "✅ 已创建示例文件：users.txt"
    fi
    
    exit 0
fi

if [ ! -f "$USER_FILE" ]; then
    echo "❌ 文件不存在：$USER_FILE"
    exit 1
fi

echo "👥 批量创建用户"
echo "=============="
echo "用户列表：$USER_FILE"
echo "起始端口：$START_PORT"
echo "OpenClaw 端口：$OPENCLAW_PORT"
echo ""

# 读取用户列表
CURRENT_PORT=$START_PORT
USER_COUNT=0
SUCCESS_COUNT=0

while IFS= read -r username || [ -n "$username" ]; do
    # 跳过空行和注释
    if [ -z "$username" ] || [[ "$username" == \#* ]]; then
        continue
    fi
    
    USER_COUNT=$((USER_COUNT + 1))
    
    echo "[$USER_COUNT] 创建用户：$username (端口：$CURRENT_PORT)"
    
    # 调用 setup-proxy.sh
    if "$(dirname "$0")/setup-proxy.sh" "$username" "$CURRENT_PORT" "$OPENCLAW_PORT" "$TOKEN"; then
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        echo "✅ $username 创建成功"
    else
        echo "❌ $username 创建失败"
    fi
    
    echo ""
    
    # 端口 +1
    CURRENT_PORT=$((CURRENT_PORT + 1))
    
done < "$USER_FILE"

echo "======================"
echo "📊 创建完成！"
echo "  总用户数：$USER_COUNT"
echo "  成功：$SUCCESS_COUNT"
echo "  失败：$((USER_COUNT - SUCCESS_COUNT))"
echo ""
echo "📋 用户列表："

# 重新读取并显示
CURRENT_PORT=$START_PORT
while IFS= read -r username || [ -n "$username" ]; do
    if [ -z "$username" ] || [[ "$username" == \#* ]]; then
        continue
    fi
    echo "  - $username: http://$(hostname -I | awk '{print $1}'):$CURRENT_PORT/"
    CURRENT_PORT=$((CURRENT_PORT + 1))
done < "$USER_FILE"

echo ""
echo "💡 提示："
echo "  - 查看 Nginx 配置：ls /etc/nginx/sites-available/openclaw-*"
echo "  - 查看运行状态：sudo systemctl status nginx"
echo "  - 删除用户：sudo rm /etc/nginx/sites-enabled/openclaw-<用户名>"
