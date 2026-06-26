#!/bin/bash
# Configure ZStack MCP authentication

set -e

echo "🔧 ZStack MCP 配置向导"
echo "====================="
echo ""

# 检查 mcporter 是否安装
if ! command -v mcporter &> /dev/null; then
    echo "❌ 错误：mcporter 未安装"
    echo "请先运行：npm install -g mcporter"
    exit 1
fi

# 检查 ZStack MCP Server 是否安装
if ! command -v zstack-mcp-server &> /dev/null && ! python3 -c "import zstack_mcp" 2>/dev/null; then
    echo "❌ 错误：ZStack MCP Server 未安装"
    echo "请运行：pip install zstack-mcp-server"
    echo "或使用 uv：uv pip install zstack-mcp-server"
    exit 1
fi

echo "✅ 依赖检查通过"
echo ""

# 读取配置
read -p "ZStack API 地址 (例如 http://192.168.1.100:8080): " ZSTACK_API_URL
read -p "用户名 (默认 admin): " ZSTACK_ACCOUNT
ZSTACK_ACCOUNT=${ZSTACK_ACCOUNT:-admin}
read -sp "密码: " ZSTACK_PASSWORD
echo ""

# 测试连接
echo ""
echo "🔍 测试连接..."

# 尝试登录获取 SessionID（使用 ZStack 标准 API 格式）
SESSION_ID=$(python3 <<PYEOF
import requests
import sys

url = '$ZSTACK_API_URL/zstack/api'
data = {
    "org.zstack.header.identity.APILoginMessage": {
        "accountName": '$ZSTACK_ACCOUNT',
        "password": '$ZSTACK_PASSWORD'
    }
}

try:
    resp = requests.post(url, json=data, timeout=10)
    if resp.status_code == 200:
        # 从响应头获取 Session Token
        session = resp.headers.get('X-ZStack-Session-Token', '')
        if not session:
            # 尝试从 Cookie 获取
            cookie = resp.headers.get('Set-Cookie', '')
            if 'token=' in cookie:
                session = cookie.split('token=')[1].split(';')[0]
        if session:
            print(session)
        else:
            print('ERROR: No session token in response headers')
    else:
        print(f'ERROR: {resp.status_code} - {resp.text[:200]}')
except Exception as e:
    print(f'ERROR: {e}')
PYEOF
)

if [[ "$SESSION_ID" == "ERROR"* ]] || [[ -z "$SESSION_ID" ]]; then
    echo "❌ 登录失败，请检查 API 地址和凭证"
    exit 1
fi

echo "✅ 登录成功，SessionID: ${SESSION_ID:0:8}..."

# 保存到配置文件
CONFIG_DIR="$(dirname "$(dirname "$0")")/config"
mkdir -p "$CONFIG_DIR"

cat > "$CONFIG_DIR/zstack.env" <<EOF
# ZStack MCP 配置
# 生成时间：$(date -Iseconds)

ZSTACK_API_URL="$ZSTACK_API_URL"
ZSTACK_ACCOUNT="$ZSTACK_ACCOUNT"
ZSTACK_PASSWORD="$ZSTACK_PASSWORD"
ZSTACK_SESSION_ID="$SESSION_ID"
# ZSTACK_ALLOW_ALL_API="false"  # 取消注释以启用写操作
EOF

echo ""
echo "✅ 配置已保存到：$CONFIG_DIR/zstack.env"
echo ""
echo "📝 下一步："
echo "1. 运行注册脚本：bash ~/clawd/skills/zstack-mcp/scripts/register-mcp.sh"
echo "2. 或在 shell 中加载配置：source $CONFIG_DIR/zstack.env"
echo ""
echo "⚠️  注意：SessionID 会过期，过期后重新运行此脚本或使用用户名密码自动登录"
