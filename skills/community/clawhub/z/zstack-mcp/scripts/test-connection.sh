#!/bin/bash
# Test ZStack MCP connection

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$(dirname "$SCRIPT_DIR")/config"

echo "🔍 ZStack MCP 连接测试"
echo "===================="
echo ""

# 检查配置文件
if [[ ! -f "$CONFIG_DIR/zstack.env" ]]; then
    echo "❌ 未找到配置文件"
    echo "请先运行：bash $SCRIPT_DIR/configure.sh"
    exit 1
fi

# 加载配置
source "$CONFIG_DIR/zstack.env"

echo "📍 API 地址：$ZSTACK_API_URL"
echo "👤 认证方式：$([ -n "$ZSTACK_SESSION_ID" ] && echo "SessionID" || echo "用户名密码 ($ZSTACK_ACCOUNT)")"
echo ""

# 测试 1: 检查 mcporter 配置
echo "1️⃣  检查 mcporter 配置..."
if mcporter config list 2>/dev/null | grep -q "zstack-mcp"; then
    echo "   ✅ MCP 配置已注册"
else
    echo "   ⚠️  MCP 配置未注册，运行：bash $SCRIPT_DIR/register-mcp.sh"
fi
echo ""

# 测试 2: 测试 MCP 连接
echo "2️⃣  测试 MCP 连接..."
RESULT=$(mcporter call zstack-mcp.search_api --args '{"keywords":["Query"],"limit":1}' 2>&1)
if echo "$RESULT" | grep -q '"success": true'; then
    echo "   ✅ MCP 连接成功"
    COUNT=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('count',0))" 2>/dev/null || echo "?")
    echo "   📊 找到 $COUNT 个匹配 API"
else
    echo "   ❌ MCP 连接失败"
    echo "$RESULT" | head -5
    exit 1
fi
echo ""

# 测试 3: 测试 ZStack API（直接调用）
echo "3️⃣  测试 ZStack API 直接连接..."
if [[ -n "$ZSTACK_SESSION_ID" ]]; then
    # 使用 SessionID
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$ZSTACK_API_URL/zstack/api" \
        -H "Content-Type: application/json" \
        -H "X-ZStack-Session-Token: $ZSTACK_SESSION_ID" \
        -d '{"org.zstack.header.vm.APIQueryVmInstanceMessage":{"conditions":[],"limit":1}}' 2>/dev/null)
else
    # 使用用户名密码登录
    LOGIN_RESPONSE=$(curl -s -X POST "$ZSTACK_API_URL/zstack/api" \
        -H "Content-Type: application/json" \
        -d "{\"org.zstack.header.identity.APILoginMessage\":{\"accountName\":\"$ZSTACK_ACCOUNT\",\"password\":\"$ZSTACK_PASSWORD\"}}" 2>/dev/null)
    
    SESSION=$(echo "$LOGIN_RESPONSE" | python3 -c "
import sys
for line in sys.stdin:
    if 'X-ZStack-Session-Token' in line or 'token=' in line:
        print('OK')
        break
" 2>/dev/null || echo "")
    
    if [[ -n "$SESSION" ]]; then
        echo "   ✅ 登录成功"
    else
        echo "   ⚠️  登录响应异常（可能仍成功）"
    fi
fi
echo ""

# 测试 4: 查询 VM 数量
echo "4️⃣  查询运行中的 VM 数量..."
RESULT=$(mcporter call zstack-mcp.execute_api --args '{"api_name":"QueryVmInstance","parameters":{"conditions":[{"name":"state","op":"=","value":"Running"}],"limit":1}}' 2>&1)
if echo "$RESULT" | grep -q '"success": true'; then
    COUNT=$(echo "$RESULT" | grep -o '"resultCount": [0-9]*' | grep -o '[0-9]*' || echo "?")
    echo "   ✅ 查询成功：$COUNT 个运行中的 VM"
else
    echo "   ⚠️  查询失败（可能是权限问题）"
fi
echo ""

echo "✅ 所有测试完成！"
