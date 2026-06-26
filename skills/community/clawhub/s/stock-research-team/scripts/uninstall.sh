#!/usr/bin/env bash
# ============================================================
# AI 投研团队 — 卸载清理脚本
# 功能：
#   1. 移除虚拟环境
#   2. 从 MCP 配置中移除 stock-analyzer
#
# 用法：bash uninstall.sh
# ============================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()    { echo -e "[INFO] $1"; }
success() { echo -e "${GREEN}[OK]${NC}   $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="$SKILL_DIR/scripts/.venv"
MCP_NAME="stock-analyzer"

echo ""
echo -e "${CYAN}  📈 AI 投研团队 — 卸载清理${NC}"
echo ""

# Step 1: 移除虚拟环境
if [ -d "$VENV_DIR" ]; then
    rm -rf "$VENV_DIR"
    success "虚拟环境已删除: $VENV_DIR"
else
    info "虚拟环境不存在，跳过"
fi

# Step 2: 从 MCP 配置中移除
remove_from_json() {
    local json_file="$1"
    if [ -f "$json_file" ]; then
        python3 -c "
import json, sys
try:
    with open('$json_file', 'r') as f:
        config = json.load(f)
    if 'mcpServers' in config and '$MCP_NAME' in config['mcpServers']:
        del config['mcpServers']['$MCP_NAME']
        with open('$json_file', 'w') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print('已从 $json_file 中移除 $MCP_NAME')
    else:
        print('$json_file 中未找到 $MCP_NAME，跳过')
except Exception as e:
    print(f'处理 $json_file 失败: {e}', file=sys.stderr)
" 2>/dev/null
    fi
}

# 尝试从各平台配置中移除
if command -v openclaw &>/dev/null; then
    openclaw mcp remove "$MCP_NAME" 2>/dev/null \
        && success "已从 OpenClaw 移除 MCP Server" \
        || {
            remove_from_json "$HOME/.openclaw/openclaw.json"
            success "已从 openclaw.json 移除 MCP Server"
        }
fi

remove_from_json "$HOME/.workbuddy/mcp.json"

echo ""
echo -e "${GREEN}  ✅ 卸载完成${NC}"
echo ""
echo "  请重启 OpenClaw / WorkBuddy 使更改生效。"
echo "  如需完全移除 Skill，请执行："
echo "    npx clawhub@latest uninstall stock-research-team"
echo ""
