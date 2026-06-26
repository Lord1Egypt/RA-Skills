#!/usr/bin/env bash
# RPG Travel — 依赖检查与安装脚本
# 用途：检查运行环境是否满足要求，缺失时给出安装指引
# 用法：bash scripts/setup.sh

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS=0
FAIL=0

check() {
    local name="$1"
    local cmd="$2"
    local install_hint="$3"

    if eval "$cmd" >/dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} $name"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}✗${NC} $name — 未安装"
        echo -e "    ${YELLOW}安装指引: $install_hint${NC}"
        FAIL=$((FAIL + 1))
    fi
}

check_version() {
    local name="$1"
    local cmd="$2"
    local min_version="$3"
    local install_hint="$4"

    local version
    version=$(eval "$cmd" 2>/dev/null || echo "0.0.0")
    # Extract major.minor
    local major minor
    major=$(echo "$version" | cut -d. -f1)
    minor=$(echo "$version" | cut -d. -f2)
    local min_major min_minor
    min_major=$(echo "$min_version" | cut -d. -f1)
    min_minor=$(echo "$min_version" | cut -d. -f2)

    if [ "$major" -gt "$min_major" ] || { [ "$major" -eq "$min_major" ] && [ "$minor" -ge "$min_minor" ]; }; then
        echo -e "  ${GREEN}✓${NC} $name (v$version)"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}✗${NC} $name — 版本过低 (v$version, 需要 >= v$min_version)"
        echo -e "    ${YELLOW}安装指引: $install_hint${NC}"
        FAIL=$((FAIL + 1))
    fi
}

echo "============================================"
echo "  RPG Travel — 依赖检查"
echo "============================================"
echo ""

echo "核心依赖:"
check_version "Python 3" "python3 --version | awk '{print \$2}'" "3.9" \
    "macOS: brew install python3 | Ubuntu: sudo apt install python3"
check "FlyAI CLI" "flyai --version" \
    "联系 FlyAI 平台获取安装方式，或访问 flyai 官方文档"

echo ""
echo "可选依赖 (不影响基本功能):"
check "Node.js (FlyAI 运行环境)" "node --version" \
    "macOS: brew install node | Ubuntu: sudo apt install nodejs"

echo ""
echo "============================================"
echo "  检查结果: $PASS 通过, $FAIL 失败"
echo "============================================"

if [ "$FAIL" -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}提示: 安装缺失依赖后重新运行此脚本${NC}"
    echo -e "${YELLOW}      或手动安装后直接运行: python3 scripts/generate_map.py --stdin${NC}"
fi

# Check FlyAI credential configuration
echo ""
echo "FlyAI 凭据配置:"
if command -v flyai >/dev/null 2>&1; then
    if flyai --version >/dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} FlyAI CLI 已安装"
        echo "  提示: 请确保已通过 flyai login 或配置文件设置了认证凭据"
    fi
else
    echo -e "  ${YELLOW}!${NC} FlyAI CLI 未安装，无法检查凭据配置"
fi

echo ""
echo "完成。"
