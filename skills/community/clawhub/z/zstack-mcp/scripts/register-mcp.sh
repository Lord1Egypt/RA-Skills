#!/bin/bash
# Register ZStack MCP server to mcporter config

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$SKILL_DIR/config"

# 检查配置文件
if [[ ! -f "$CONFIG_DIR/zstack.env" ]]; then
    echo "❌ 错误：未找到配置文件"
    echo "请先运行：bash $SCRIPT_DIR/configure.sh"
    exit 1
fi

# 加载配置
source "$CONFIG_DIR/zstack.env"

echo "🔧 注册 ZStack MCP 到 mcporter 配置"
echo "=================================="
echo ""
echo "API 地址：$ZSTACK_API_URL"
echo ""

# 确定配置文件路径（优先使用 clawd 配置）
MCPORTER_CONFIG="${MCPORTER_CONFIG:-$HOME/clawd/config/mcporter.json}"
if [[ ! -f "$MCPORTER_CONFIG" ]]; then
    # 尝试备用路径
    if [[ -f $HOME/.team-os/mcp.json ]]; then
        MCPORTER_CONFIG=$HOME/.team-os/mcp.json
    else
        echo "⚠️  未找到现有配置，创建新配置：$MCPORTER_CONFIG"
        mkdir -p "$(dirname "$MCPORTER_CONFIG")"
        echo '{"mcpServers":{},"imports":[]}' > "$MCPORTER_CONFIG"
    fi
fi

echo "📄 配置文件：$MCPORTER_CONFIG"
echo ""

# 备份原配置
cp "$MCPORTER_CONFIG" "$MCPORTER_CONFIG.bak"

# 使用 Python 更新 JSON 配置（避免 jq 依赖）
python3 <<EOF
import json
import sys

config_path = "$MCPORTER_CONFIG"

with open(config_path, 'r') as f:
    config = json.load(f)

# 构建 MCP 配置（优先使用 SessionID，否则使用用户名密码）
mcp_config = {
    'command': 'zstack-mcp-server',
    'transport': 'stdio',
    'env': {
        'ZSTACK_API_URL': '$ZSTACK_API_URL',
    }
}

# 如果有 SessionID，优先使用
if '$ZSTACK_SESSION_ID' and '$ZSTACK_SESSION_ID' != '':
    mcp_config['env']['ZSTACK_SESSION_ID'] = '$ZSTACK_SESSION_ID'
else:
    # 否则使用用户名密码
    mcp_config['env']['ZSTACK_ACCOUNT'] = '$ZSTACK_ACCOUNT'
    mcp_config['env']['ZSTACK_PASSWORD'] = '$ZSTACK_PASSWORD'

config['mcpServers']['zstack-mcp'] = mcp_config

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ 配置已更新")
EOF

echo ""
echo "📝 验证配置："
echo "   mcporter config list"
echo ""
echo "🚀 测试连接："
echo "   mcporter call zstack-mcp.search_api --args '{\"keywords\":[\"Query\",\"Vm\"]}'"
echo ""
echo "💡 提示：如需启用写操作，编辑配置添加 ZSTACK_ALLOW_ALL_API=true"
