#!/usr/bin/env bash
# ============================================================
# AI 投研团队 — 安装后配置脚本
# 功能：
#   1. 检测 Python 环境（≥3.10）
#   2. 创建虚拟环境并安装依赖
#   3. 注册 MCP Server 到 OpenClaw
#   4. 验证安装
#
# 用法：bash setup.sh
# ============================================================

set -euo pipefail

# ---- 颜色输出 ----
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC}   $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
fail()    { echo -e "${RED}[FAIL]${NC} $1"; }

# ---- 路径设定 ----
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="$SKILL_DIR/scripts"
VENV_DIR="$SCRIPTS_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python3"
SERVER_PY="$SCRIPTS_DIR/server.py"
REQUIREMENTS="$SKILL_DIR/references/requirements.txt"
MCP_NAME="stock-analyzer"

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  📈 AI 投研团队 — 配置安装${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ============================================================
# Step 1: 检测 Python 环境
# ============================================================
info "Step 1/4: 检测 Python 环境..."

PYTHON_CMD=""

# 优先检测高版本 Python
for cmd in python3.12 python3.11 python3.10 python3; do
    if command -v "$cmd" &>/dev/null; then
        ver=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
        major=$(echo "$ver" | cut -d. -f1)
        minor=$(echo "$ver" | cut -d. -f2)
        if [ "$major" -ge 3 ] && [ "$minor" -ge 10 ]; then
            PYTHON_CMD="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    fail "未找到 Python ≥ 3.10"
    echo ""
    echo "  请安装 Python 3.10+："
    echo "    macOS:  brew install python@3.12"
    echo "    Ubuntu: sudo apt install python3.12 python3.12-venv"
    echo "    通用:   https://www.python.org/downloads/"
    echo ""
    exit 1
fi

PYTHON_VER=$("$PYTHON_CMD" --version 2>&1)
success "Python: $PYTHON_VER ($(command -v "$PYTHON_CMD"))"

# ============================================================
# Step 2: 创建虚拟环境并安装依赖
# ============================================================
info "Step 2/4: 创建虚拟环境并安装依赖..."

if [ -d "$VENV_DIR" ] && [ -x "$VENV_PYTHON" ]; then
    info "虚拟环境已存在: $VENV_DIR"
else
    # 优先使用 uv（速度更快）
    if command -v uv &>/dev/null; then
        info "使用 uv 创建虚拟环境..."
        uv venv --python "$PYTHON_CMD" "$VENV_DIR"
    else
        info "使用 venv 创建虚拟环境..."
        "$PYTHON_CMD" -m venv "$VENV_DIR"
    fi

    if [ ! -x "$VENV_PYTHON" ]; then
        fail "虚拟环境创建失败"
        exit 1
    fi
    success "虚拟环境已创建"
fi

# 安装依赖
info "安装 Python 依赖..."
if command -v uv &>/dev/null; then
    uv pip install --python "$VENV_PYTHON" -r "$REQUIREMENTS"
else
    "$VENV_PYTHON" -m pip install --upgrade pip -q
    "$VENV_PYTHON" -m pip install -r "$REQUIREMENTS" -q
fi

# 验证依赖
local_ok=true
"$VENV_PYTHON" -c "import mcp"     2>/dev/null && success "mcp 安装成功"     || { warn "mcp 安装失败"; local_ok=false; }
"$VENV_PYTHON" -c "import akshare" 2>/dev/null && success "akshare 安装成功" || { warn "akshare 安装失败（A股数据将不可用）"; }
"$VENV_PYTHON" -c "import yfinance" 2>/dev/null && success "yfinance 安装成功" || { warn "yfinance 安装失败（美股数据将不可用）"; }

if [ "$local_ok" = false ]; then
    fail "核心依赖 mcp 安装失败，请检查 Python 版本和网络连接"
    exit 1
fi

# ============================================================
# Step 3: 注册 MCP Server
# ============================================================
info "Step 3/4: 注册 MCP Server..."

# 检测运行平台
if command -v openclaw &>/dev/null; then
    # OpenClaw 环境：使用 openclaw mcp add
    info "检测到 OpenClaw 环境"
    openclaw mcp add --transport stdio "$MCP_NAME" \
        "$VENV_PYTHON" "$SERVER_PY" 2>/dev/null \
        && success "MCP Server 已注册到 OpenClaw" \
        || {
            warn "openclaw mcp add 失败，尝试手动配置..."
            # 备用方案：直接写入 openclaw.json
            OPENCLAW_JSON="$HOME/.openclaw/openclaw.json"
            if [ -f "$OPENCLAW_JSON" ]; then
                "$VENV_PYTHON" -c "
import json, sys
try:
    with open('$OPENCLAW_JSON', 'r') as f:
        config = json.load(f)
    if 'mcpServers' not in config:
        config['mcpServers'] = {}
    config['mcpServers']['$MCP_NAME'] = {
        'command': '$VENV_PYTHON',
        'args': ['$SERVER_PY'],
        'transport': 'stdio'
    }
    with open('$OPENCLAW_JSON', 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print('MCP Server 已写入 openclaw.json')
except Exception as e:
    print(f'写入失败: {e}', file=sys.stderr)
    sys.exit(1)
"
                success "MCP Server 已写入 openclaw.json"
            fi
        }
elif [ -d "$HOME/.workbuddy" ]; then
    # WorkBuddy 环境
    info "检测到 WorkBuddy 环境"
    MCP_JSON="$HOME/.workbuddy/mcp.json"
    if [ -f "$MCP_JSON" ]; then
        "$VENV_PYTHON" -c "
import json
with open('$MCP_JSON', 'r') as f:
    config = json.load(f)
if 'mcpServers' not in config:
    config['mcpServers'] = {}
config['mcpServers']['$MCP_NAME'] = {
    'command': '$VENV_PYTHON',
    'args': ['$SERVER_PY'],
    'transport': 'stdio'
}
with open('$MCP_JSON', 'w') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
print('OK')
"
        success "MCP Server 已注册到 WorkBuddy"
    else
        warn "未找到 $MCP_JSON，请手动配置 MCP Server"
    fi
else
    warn "未检测到 OpenClaw 或 WorkBuddy 环境"
    echo ""
    echo "  请手动将以下配置添加到你的 MCP 配置文件中："
    echo ""
    echo "  {\"$MCP_NAME\": {"
    echo "    \"command\": \"$VENV_PYTHON\","
    echo "    \"args\": [\"$SERVER_PY\"],"
    echo "    \"transport\": \"stdio\""
    echo "  }}"
    echo ""
fi

# ============================================================
# Step 4: 验证
# ============================================================
info "Step 4/4: 验证安装..."

"$VENV_PYTHON" -c "
import mcp, akshare, yfinance
print('All dependencies OK')
" 2>/dev/null && success "所有依赖验证通过" || warn "部分依赖验证失败"

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  ✅ 配置完成！${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "  下一步："
if command -v openclaw &>/dev/null; then
    echo "    1. 重启 OpenClaw 网关: openclaw gateway restart"
    echo "    2. 在对话中输入: 分析一下贵州茅台"
else
    echo "    1. 重启 WorkBuddy / 你的 AI 客户端"
    echo "    2. 在对话中输入: 分析一下贵州茅台"
fi
echo ""
echo "  MCP Server: $MCP_NAME"
echo "  Python:     $VENV_PYTHON"
echo "  Server:     $SERVER_PY"
echo ""
