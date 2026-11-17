#!/usr/bin/env bash
# smart-web-search setup (Linux/macOS)
# v1.0.4
#
# 功能：
#   - 校验 Node.js >= 18
#   - 自动检测国内/海外，国内自动用 npmmirror 镜像
#   - npm install（仅安装 package.json 声明的依赖）
#   - 检测系统 Chrome/Chromium，存在则跳过 150MB 下载
#   - 否则下载 Playwright Chromium（带镜像）
#
# 此脚本不会执行任何运行时自动 npm install / pip install。

set -e
SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo ""
echo "=== smart-web-search Setup ==="
echo ""
echo "Dependencies:"
echo "  - Node.js >= 18"
echo "  - npm packages: cheerio, commander, iconv-lite, playwright"
echo "  - Chromium ~150MB（若已有系统 Chrome，会跳过下载）"
echo ""

# ------------------------------ Node.js ------------------------------
if ! command -v node >/dev/null 2>&1; then
    echo "[X] Node.js not found"
    echo "   -> https://nodejs.org"
    exit 1
fi
NODE_VERSION="$(node --version)"
MAJOR="$(echo "$NODE_VERSION" | sed 's/^v//' | cut -d. -f1)"
if [ "$MAJOR" -lt 18 ]; then
    echo "[X] Node.js >= 18 required (current: $NODE_VERSION)"
    exit 1
fi
echo "[OK] Node.js $NODE_VERSION"

# ------------------------------ 网络区域 ------------------------------
IN_CHINA=false
echo ""
echo "Detecting network region..."
for url in "https://myip.ipip.net" "https://cip.cc"; do
    if resp="$(curl -sS --max-time 3 "$url" 2>/dev/null)"; then
        if echo "$resp" | grep -qi "中国\|CN"; then
            IN_CHINA=true
            break
        fi
    fi
done

NPM_REGISTRY_ARG=""
if [ "$IN_CHINA" = true ]; then
    echo "[OK] 国内网络，使用 npmmirror 镜像"
    export PLAYWRIGHT_DOWNLOAD_HOST="https://npmmirror.com/mirrors/playwright"
    NPM_REGISTRY_ARG="--registry=https://registry.npmmirror.com"
else
    echo "[OK] 海外网络，使用官方源"
fi

# ------------------------------ npm install ------------------------------
echo ""
echo "Installing npm packages..."
cd "$SKILL_ROOT"
if [ -n "$NPM_REGISTRY_ARG" ]; then
    npm install $NPM_REGISTRY_ARG
else
    npm install
fi
echo "[OK] npm packages installed"

# ------------------------------ Chromium ------------------------------
# 优先：用户自己设的 CHROMIUM_EXECUTABLE_PATH
if [ -n "${CHROMIUM_EXECUTABLE_PATH:-}" ] && [ -x "$CHROMIUM_EXECUTABLE_PATH" ]; then
    echo ""
    echo "[OK] 用户已设置 CHROMIUM_EXECUTABLE_PATH=$CHROMIUM_EXECUTABLE_PATH，跳过下载"
else
    # 次优：系统 Chrome / Chromium（macOS/Linux 常见路径）
    SYSTEM_CHROME=""
    for p in \
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
        "/Applications/Chromium.app/Contents/MacOS/Chromium" \
        "/usr/bin/google-chrome" \
        "/usr/bin/google-chrome-stable" \
        "/usr/bin/chromium" \
        "/usr/bin/chromium-browser" \
        "/snap/bin/chromium"; do
        if [ -x "$p" ]; then
            SYSTEM_CHROME="$p"
            break
        fi
    done

    if [ -n "$SYSTEM_CHROME" ]; then
        echo ""
        echo "[OK] 检测到系统 Chrome: $SYSTEM_CHROME"
        echo "     如要使用系统 Chrome 跳过 150MB 下载："
        echo "       export CHROMIUM_EXECUTABLE_PATH=\"$SYSTEM_CHROME\""
        echo ""
        echo "     仍将下载 Playwright Chromium 作为默认（更稳定，首次较慢）。"
        echo "     如需跳过下载，按 Ctrl+C 中止，设置上面的环境变量后再运行 check-env.js。"
        sleep 2
    fi

    echo ""
    echo "Installing Playwright Chromium (~150MB)..."
    if ! npx --yes playwright install chromium; then
        echo ""
        echo "[!] chromium 主包安装失败，尝试 chromium-headless-shell..."
        if ! npx --yes playwright install chromium-headless-shell; then
            echo ""
            echo "[X] Playwright Chromium 安装失败"
            echo "   重试方法："
            echo "     PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright \\"
            echo "       npx playwright install chromium"
            echo "   或使用系统 Chrome:"
            echo "     export CHROMIUM_EXECUTABLE_PATH=/path/to/chrome"
            exit 1
        fi
    fi
    echo "[OK] Playwright Chromium installed"
fi

# ------------------------------ 验证 ------------------------------
echo ""
echo "Verifying environment..."
if node "$SKILL_ROOT/scripts/check-env.js"; then
    echo ""
    echo "[OK] Setup complete!"
else
    echo ""
    echo "[X] check-env.js 报告问题，请按提示修复"
    exit 1
fi
