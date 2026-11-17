#!/usr/bin/env bash
# setup.sh - text-to-elegant-image 依赖检测
# 容器环境（Node.js / Chrome 已内置），仅检测 puppeteer-core 并按需安装

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

ok()   { echo -e "${GREEN}  ✔ $*${NC}"; }
warn() { echo -e "${YELLOW}  ⚠ $*${NC}"; }
info() { echo -e "${CYAN}  → $*${NC}"; }
fail() { echo -e "${RED}  ✘ $*${NC}"; }
hr()   { echo -e "${BOLD}──────────────────────────────────────────${NC}"; }

hr
echo -e "${BOLD}  text-to-elegant-image — 依赖检测${NC}"
hr

# ── 1. Node.js ──────────────────────────────────────────────
echo ""
echo -e "${BOLD}[1/3] Node.js${NC}"
if command -v node &>/dev/null; then
    NODE_VER=$(node --version)
    NODE_MAJOR=$(echo "$NODE_VER" | sed 's/v\([0-9]*\).*/\1/')
    if [[ "$NODE_MAJOR" -ge 18 ]]; then
        ok "Node.js $NODE_VER（满足要求 >= v18）"
    else
        fail "Node.js $NODE_VER 版本过低，需要 >= v18，请升级到 Node.js >= v18（https://nodejs.org）"
        exit 1
    fi
else
    fail "未检测到 Node.js，请先安装 Node.js >= v18（https://nodejs.org）"
    exit 1
fi

# ── 2. Chrome / Chromium ────────────────────────────────────
echo ""
echo -e "${BOLD}[2/3] Chrome / Chromium${NC}"

CHROME_PATH=""
CHROME_CANDIDATES=(
    "/usr/bin/google-chrome"
    "/usr/bin/google-chrome-stable"
    "/usr/bin/chromium"
    "/usr/bin/chromium-browser"
    "/snap/bin/chromium"
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    "/Applications/Chromium.app/Contents/MacOS/Chromium"
)
for p in "${CHROME_CANDIDATES[@]}"; do
    if [[ -x "$p" ]]; then
        CHROME_PATH="$p"
        break
    fi
done
if [[ -z "$CHROME_PATH" ]]; then
    CHROME_PATH=$(command -v google-chrome chromium chromium-browser 2>/dev/null | head -1 || true)
fi

if [[ -n "$CHROME_PATH" ]]; then
    CHROME_VER=$("$CHROME_PATH" --version 2>/dev/null || echo "未知版本")
    ok "已找到：$CHROME_PATH（$CHROME_VER）"
else
    fail "未检测到 Chrome / Chromium，请先安装 Google Chrome 或 Chromium"
    exit 1
fi

# ── 3. puppeteer-core (npm) ─────────────────────────────────
echo ""
echo -e "${BOLD}[3/3] puppeteer-core（Node 包）${NC}"

if [[ -d "$SKILL_DIR/node_modules/puppeteer-core" ]]; then
    PKG_VER=$(node -e "console.log(require('$SKILL_DIR/node_modules/puppeteer-core/package.json').version)" 2>/dev/null || echo "?")
    ok "puppeteer-core@$PKG_VER 已安装"
else
    warn "puppeteer-core 未安装，正在安装..."
    info "运行：npm install --omit=dev --omit=optional（在 $SKILL_DIR，安装过程输出可见）"
    cd "$SKILL_DIR" && npm install --omit=dev --omit=optional
    PKG_VER=$(node -e "console.log(require('$SKILL_DIR/node_modules/puppeteer-core/package.json').version)" 2>/dev/null || echo "?")
    ok "puppeteer-core@$PKG_VER 安装完成"
fi

# ── 最终验证 ────────────────────────────────────────────────
echo ""
hr
echo -e "${GREEN}${BOLD}  ✔ 所有依赖已就绪，技能可以直接使用！${NC}"
hr
