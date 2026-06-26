#!/bin/bash
# 小红书内容助手 - 跨平台依赖安装脚本
# 支持: macOS / Linux

set -e

echo "========================================"
echo "  小红书内容助手 - 依赖安装"
echo "========================================"
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "[ERROR] 未找到 Node.js，请先安装 https://nodejs.org/"
    exit 1
fi
echo "[OK] Node.js: $(node --version)"

# 检查 playwright-core（OpenClaw 自带或全局 npm）
check_playwright() {
    # OpenClaw 全局安装路径
    local candidates=(
        "$HOME/.openclaw-global/node_modules/openclaw/node_modules/playwright-core"
        "$HOME/.openclaw/node_modules/playwright-core"
        "$(npm root -g)/playwright-core"
    )

    for p in "${candidates[@]}"; do
        if [ -d "$p" ]; then
            echo "[OK] Playwright-core: $p"
            return 0
        fi
    done
    return 1
}

if check_playwright; then
    : # already found
elif npm list -g playwright-core &> /dev/null; then
    echo "[OK] Playwright-core: 全局 npm"
else
    echo "[WARN] Playwright-core 未找到"
    echo "       OpenClaw 自带 playwright-core，通常无需额外安装"
fi

echo ""
echo "[INFO] 无需安装任何额外依赖！"
echo "       - Playwright: OpenClaw 自带（已兼容 macOS/Linux）"
echo "       - MiniMax 生图: 纯 Node.js，无需 Python"
echo ""
echo "========================================"
echo "  安装完成！"
echo "========================================"
echo ""
echo "下一步："
echo "  1. cp scripts/config.json.example scripts/config.json"
echo "  2. 编辑 config.json，填入 MiniMax API Key（如有）"
echo "  3. node scripts/generate_image_smart.js -p '描述' -n 3"
echo ""
