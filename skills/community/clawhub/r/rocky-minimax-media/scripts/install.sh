#!/bin/bash
# MiniMax 媒体生成插件安装脚本 v1.3.0
# 
# 功能：
# 1. 检查 OpenClaw 是否已配置 minimax 模型
# 2. 如未配置，交互式输入 API Key
# 3. 将配置写入 openclaw.json
#

set -e

# 颜色
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

log() { echo -e "${GREEN}[✓]${NC} $1"; }
err() { echo -e "${RED}[✗]${NC} $1"; }
info() { echo -e "${YELLOW}[i]${NC} $1"; }
step() { echo -e "${BLUE}[➤]${NC} $1"; }

OPENCLAW_JSON="$HOME/.openclaw/openclaw.json"

echo ""
echo "=========================================="
echo "  MiniMax 媒体生成插件 - 安装向导"
echo "=========================================="
echo ""

# 步骤1：检查是否已有 minimax 配置
step "检查 OpenClaw 配置..."
echo ""

if [ ! -f "$OPENCLAW_JSON" ]; then
  err "未找到 openclaw.json 文件: $OPENCLAW_JSON"
  echo "请先安装并配置 OpenClaw"
  exit 1
fi

# 检查是否有 minimax-portal 配置
MINIMAX_CONFIG=$(python3 -c "
import json
with open('$OPENCLAW_JSON') as f:
    config = json.load(f)
providers = config.get('models', {}).get('providers', {})
minimax = providers.get('minimax-portal', {})
print('FOUND' if minimax.get('apiKey') else 'NOT_FOUND')
" 2>/dev/null)

if [ "$MINIMAX_CONFIG" = "FOUND" ]; then
  log "检测到已配置的 MiniMax 模型"
  info "API Key 已存在于 openclaw.json"
  echo ""
  echo "安装完成！插件将自动从 openclaw.json 读取 API Key"
  exit 0
fi

# 步骤2：检查是否需要 MiniMax 模型
info "未检测到 MiniMax API Key"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ⚠️  使用本插件需要 MiniMax API Key"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "获取方式:"
echo "  1. 访问 https://platform.minimaxi.com/"
echo "  2. 注册/登录账号"
echo "  3. 在 API Keys 页面创建新的 API Key"
echo ""
read -p "请输入您的 MiniMax API Key: " API_KEY

if [ -z "$API_KEY" ]; then
  err "API Key 不能为空，安装取消"
  exit 1
fi

# 步骤3：写入 openclaw.json
step "配置 MiniMax 模型..."

# 使用 python 来安全地修改 JSON
python3 << PYEOF
import json
import os

config_path = os.path.expanduser('$OPENCLAW_JSON')

with open(config_path) as f:
    config = json.load(f)

# 确保 models.providers 结构存在
if 'models' not in config:
    config['models'] = {}
if 'providers' not in config['models']:
    config['models']['providers'] = {}

# 添加 minimax-portal 配置
config['models']['providers']['minimax-portal'] = {
    "baseUrl": "https://api.minimaxi.com/anthropic",
    "apiKey": "$API_KEY",
    "api": "anthropic-messages",
    "authHeader": True,
    "models": [
        {
            "id": "MiniMax-M2.7-highspeed",
            "name": "MiniMax-M2.7-highspeed",
            "contextWindow": 131072,
            "maxTokens": 8192
        }
    ]
}

# 写回文件
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print('SUCCESS')
PYEOF

if [ $? -eq 0 ]; then
  log "API Key 已保存到 openclaw.json"
else
  err "保存失败，请手动配置"
  exit 1
fi

echo ""
echo "=========================================="
log "安装完成！"
echo "=========================================="
echo ""
echo "下一步:"
echo "  重启 OpenClaw 网关使配置生效"
echo "  命令: openclaw gateway restart"
echo ""
