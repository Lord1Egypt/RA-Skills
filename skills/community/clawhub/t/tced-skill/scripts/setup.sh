#!/bin/bash
# 腾讯云企业网盘 TCED Skill 环境检查脚本
# 用法:
#   setup.sh --check       检查环境状态和 tced-mcp 可用性

set -e

# 颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 官方生产域名（固定，不可覆盖）
OFFICIAL_PAN_DOMAIN="https://pan.tencent.com"
OFFICIAL_API_BASE_PATH="https://api.tencentsmh.cn"
# 推荐锁定的版本号
RECOMMENDED_VERSION="1.0.2"

ok()   { echo -e "${GREEN}✓${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; }
warn() { echo -e "${YELLOW}!${NC} $1"; }

# ========== 检查函数 ==========

check_node() {
  if command -v node &>/dev/null; then
    local ver
    ver=$(node --version)
    local major
    major=$(echo "$ver" | sed 's/v//' | cut -d'.' -f1)
    if [ "$major" -ge 18 ]; then
      ok "Node.js $ver (>= v18 ✓)"
      return 0
    else
      fail "Node.js $ver (需要 >= v18)"
      return 1
    fi
  else
    fail "Node.js 未安装"
    return 1
  fi
}

check_npm() {
  if command -v npm &>/dev/null; then
    ok "npm $(npm --version)"
    return 0
  else
    fail "npm 未安装"
    return 1
  fi
}

check_npx() {
  if command -v npx &>/dev/null; then
    ok "npx 可用"
    return 0
  else
    fail "npx 不可用"
    return 1
  fi
}

check_tced_mcp_package() {
  # 检查 tced-mcp 是否可从 npm 获取
  if npm view tced-mcp version &>/dev/null 2>&1; then
    local ver
    ver=$(npm view tced-mcp version 2>/dev/null)
    ok "tced-mcp v${ver} 已发布到 npm"
    if [ "$ver" != "$RECOMMENDED_VERSION" ]; then
      warn "推荐锁定版本 ${RECOMMENDED_VERSION}，当前最新版为 ${ver}。升级前请查看 changelog。"
    fi
    return 0
  else
    fail "tced-mcp 未在 npm 上找到"
    return 1
  fi
}

check_tced_mcp_global() {
  # 检查是否已全局安装
  if command -v tced-mcp &>/dev/null; then
    ok "tced-mcp 已全局安装"
    return 0
  else
    warn "tced-mcp 未全局安装（可通过 npx 直接运行，无需全局安装）"
    return 0
  fi
}

check_gui_environment() {
  # macOS 始终有桌面环境
  if [[ "$OSTYPE" == "darwin"* ]]; then
    ok "macOS 桌面环境"
    return 0
  fi
  # Windows (Git Bash / MSYS / Cygwin)
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    ok "Windows 桌面环境"
    return 0
  fi
  # WSL 环境（可通过 wslview 唤起 Windows 浏览器）
  if grep -qi microsoft /proc/version 2>/dev/null; then
    ok "WSL 环境（可通过 wslview 唤起浏览器）"
    return 0
  fi
  # Linux: 检查 DISPLAY（X11）或 WAYLAND_DISPLAY
  if [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ]; then
    ok "Linux 桌面环境 (DISPLAY=${DISPLAY:-$WAYLAND_DISPLAY})"
    return 0
  fi
  # 未检测到图形界面
  fail "未检测到图形界面环境（Headless 服务器）"
  echo "    tced-mcp 需要唤起浏览器完成 OAuth2 授权登录，不支持无界面服务器。"
  echo "    请在有桌面环境的机器上使用（macOS / Windows / Linux 桌面 / WSL）。"
  return 1
}

check_env_vars() {
  # TCED_PAN_DOMAIN 检查
  if [ -n "$TCED_PAN_DOMAIN" ]; then
    if [ "$TCED_PAN_DOMAIN" = "$OFFICIAL_PAN_DOMAIN" ]; then
      ok "TCED_PAN_DOMAIN = $TCED_PAN_DOMAIN (官方地址 ✓)"
    else
      fail "TCED_PAN_DOMAIN = $TCED_PAN_DOMAIN (非官方地址！应为 $OFFICIAL_PAN_DOMAIN)"
      echo "    ⚠️  非官方域名可能导致 Token 泄露，请确认是否为可信的私有化部署地址。"
    fi
  else
    warn "TCED_PAN_DOMAIN 未设置（建议在 mcp.json 的 env 中显式配置为 $OFFICIAL_PAN_DOMAIN）"
  fi
  # TCED_BASE_PATH 检查
  if [ -n "$TCED_BASE_PATH" ]; then
    if [ "$TCED_BASE_PATH" = "$OFFICIAL_API_BASE_PATH" ]; then
      ok "TCED_BASE_PATH = $TCED_BASE_PATH (官方地址 ✓)"
    else
      fail "TCED_BASE_PATH = $TCED_BASE_PATH (非官方地址！应为 $OFFICIAL_API_BASE_PATH)"
      echo "    ⚠️  非官方域名可能导致 Token 泄露，请确认是否为可信的私有化部署地址。"
    fi
  else
    warn "TCED_BASE_PATH 未设置（建议在 mcp.json 的 env 中显式配置为 $OFFICIAL_API_BASE_PATH）"
  fi
  return 0
}

check_auth_file() {
  local auth_file="$HOME/.tced-mcp/auth.json"
  if [ -f "$auth_file" ]; then
    ok "凭据文件存在: $auth_file"
    # 检查文件权限
    local perms
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux"* ]]; then
      perms=$(stat -f '%Lp' "$auth_file" 2>/dev/null || stat -c '%a' "$auth_file" 2>/dev/null)
      if [ "$perms" = "600" ]; then
        ok "文件权限 $perms (仅所有者可读写 ✓)"
      else
        warn "文件权限 $perms (建议设置为 600: chmod 600 $auth_file)"
      fi
    fi
    # 检查域名配置是否指向官方地址
    if command -v python3 &>/dev/null; then
      local api_base pan_domain
      api_base=$(python3 -c "import json; d=json.load(open('$auth_file')); print(d.get('apiBasePath',''))" 2>/dev/null)
      pan_domain=$(python3 -c "import json; d=json.load(open('$auth_file')); print(d.get('panDomain',''))" 2>/dev/null)
      if [ -n "$api_base" ] && [ "$api_base" != "$OFFICIAL_API_BASE_PATH" ]; then
        fail "auth.json 中 apiBasePath = $api_base (非官方地址！)"
        echo "    应为 $OFFICIAL_API_BASE_PATH。请在 mcp.json 中配置 env.TCED_BASE_PATH 后重启 MCP 进程。"
      elif [ -n "$api_base" ]; then
        ok "auth.json 中 apiBasePath 指向官方地址 ✓"
      fi
      if [ -n "$pan_domain" ] && [ "$pan_domain" != "$OFFICIAL_PAN_DOMAIN" ]; then
        fail "auth.json 中 panDomain = $pan_domain (非官方地址！)"
        echo "    应为 $OFFICIAL_PAN_DOMAIN。请在 mcp.json 中配置 env.TCED_PAN_DOMAIN 后重启 MCP 进程。"
      elif [ -n "$pan_domain" ]; then
        ok "auth.json 中 panDomain 指向官方地址 ✓"
      fi
    fi
  else
    warn "凭据文件不存在: $auth_file（首次 login 后自动创建）"
  fi
  return 0
}

# ========== 检查模式 ==========

do_check() {
  echo "=== 腾讯云企业网盘 TCED Skill 环境检查 ==="
  echo ""
  echo "--- 基础环境 ---"
  check_gui_environment || true
  check_node || true
  check_npm || true
  check_npx || true
  echo ""
  echo "--- tced-mcp ---"
  check_tced_mcp_package || true
  check_tced_mcp_global || true
  echo ""
  echo "--- 环境变量 ---"
  check_env_vars || true
  echo ""
  echo "--- 凭据与配置 ---"
  check_auth_file || true
  echo ""
  echo "--- MCP 客户端配置 ---"
  echo ""
  echo "将以下配置添加到你的 MCP 客户端配置文件（mcp.json）中："
  echo ""
  echo '{'
  echo '  "mcpServers": {'
  echo '    "tced-mcp": {'
  echo "      \"command\": \"npx\","
  echo "      \"args\": [\"-y\", \"tced-mcp@${RECOMMENDED_VERSION}\"],"
  echo '      "env": {'
  echo "        \"TCED_PAN_DOMAIN\": \"${OFFICIAL_PAN_DOMAIN}\","
  echo "        \"TCED_BASE_PATH\": \"${OFFICIAL_API_BASE_PATH}\""
  echo '      }'
  echo '    }'
  echo '  }'
  echo '}'
  echo ""
  echo "⚠️  建议锁定具体版本号（当前推荐 ${RECOMMENDED_VERSION}），不要使用 @latest。"
  echo "⚠️  必须配置 env 字段，确保 API 请求指向官方可信端点。"
  echo ""
  echo "然后使用 MCP 工具调用 login 进行 OAuth2 授权即可开始使用。"
}

# ========== 主入口 ==========

case "$1" in
  --check|--check-only)
    do_check
    ;;
  *)
    echo "腾讯云企业网盘 TCED Skill 环境检查工具"
    echo ""
    echo "用法:"
    echo "  $0 --check"
    echo "    检查环境状态和 tced-mcp 可用性"
    echo ""
    echo "安装方式:"
    echo "  tced-mcp 已发布到 npm，无需手动安装。"
    echo "  在 MCP 客户端配置文件中添加以下配置即可："
    echo ""
    echo "  {\"mcpServers\":{\"tced-mcp\":{\"command\":\"npx\",\"args\":[\"-y\",\"tced-mcp@${RECOMMENDED_VERSION}\"],\"env\":{\"TCED_PAN_DOMAIN\":\"${OFFICIAL_PAN_DOMAIN}\",\"TCED_BASE_PATH\":\"${OFFICIAL_API_BASE_PATH}\"}}}}"
    echo ""
    ;;
esac
