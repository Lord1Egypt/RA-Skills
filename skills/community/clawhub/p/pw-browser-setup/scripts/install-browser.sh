#!/usr/bin/env bash
# browser-setup: 安装 Playwright + Chrome (非头模式) + 虚拟显示器
# 模拟真实用户浏览器环境（非 headless）
set -e

OS="$(uname -s)"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="${1:-.}"

echo "=== 浏览器环境安装 ==="
echo ""

# 1. 安装 Xvfb（Linux 虚拟显示器）
if [[ "$OS" == "Linux" ]]; then
  echo "--- 安装 Xvfb 虚拟显示器 ---"
  if ! command -v Xvfb &>/dev/null; then
    echo "正在安装 xvfb..."
    SUDO_OK=true
    if command -v apt-get &>/dev/null; then
      sudo -n apt-get update -qq 2>/dev/null && sudo -n apt-get install -y -qq xvfb 2>/dev/null || SUDO_OK=false
    elif command -v yum &>/dev/null; then
      sudo -n yum install -y xorg-x11-server-Xvfb 2>/dev/null || SUDO_OK=false
    elif command -v dnf &>/dev/null; then
      sudo -n dnf install -y xorg-x11-server-Xvfb 2>/dev/null || SUDO_OK=false
    elif command -v pacman &>/dev/null; then
      sudo -n pacman -S --noconfirm xorg-server-xvfb 2>/dev/null || SUDO_OK=false
    else
      echo "❌ 无法自动安装 Xvfb，请手动安装: apt-get install xvfb / yum install xorg-x11-server-Xvfb"
      exit 1
    fi
    if $SUDO_OK && command -v Xvfb &>/dev/null; then
      echo "✅ Xvfb 安装完成"
    else
      echo "⚠️  Xvfb 安装需要 sudo 权限，请手动执行: sudo apt-get install xvfb"
    fi
  else
    echo "✅ Xvfb 已安装"
  fi

  # 安装 Chrome 所需的系统依赖
  echo ""
  echo "--- 安装 Chrome 系统依赖 ---"
  if command -v apt-get &>/dev/null; then
    echo "正在安装依赖库..."
    if sudo -n apt-get install -y -qq \
      libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
      libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
      libpango-1.0-0 libcairo2 libasound2 libxshmfence1 \
      fonts-noto-cjk fonts-noto-color-emoji 2>/dev/null; then
      echo "✅ 系统依赖安装完成"
    else
      echo "⚠️  系统依赖安装需要 sudo 权限，请手动执行安装命令"
    fi
  elif command -v yum &>/dev/null; then
    echo "提示: yum 系统请确保已安装 nss atk cups libXcomposite 等库"
  fi
fi

# 2. 安装 Playwright npm 包
echo ""
echo "--- 安装 Playwright ---"
if ! command -v npx &>/dev/null; then
  echo "❌ 需要先安装 Node.js 和 npm"
  exit 1
fi

cd "$WORKSPACE"
if [[ ! -d "node_modules/playwright" ]]; then
  npm install playwright 2>&1 | tail -3
else
  echo "✅ Playwright 已安装 (node_modules)"
fi

# 全局 CLI（用于下载浏览器）
if ! command -v playwright &>/dev/null; then
  npm install -g playwright 2>&1 | tail -3
fi
echo "✅ Playwright $(playwright --version 2>/dev/null || echo '已安装')"

# 3. 下载 Chromium 浏览器
echo ""
echo "--- 下载 Chromium 浏览器 ---"
CACHE_DIR="$HOME/.cache/ms-playwright"
if [[ -d "$CACHE_DIR/chromium-"* ]] 2>/dev/null; then
  echo "✅ Chromium 已下载"
else
  echo "正在下载 Chromium（约 300MB，可能需要几分钟）..."
  npx playwright install chromium 2>&1 | tail -5
  echo "✅ Chromium 下载完成"
fi

# 4. 安装 Chrome Headless Shell（备用）
echo ""
echo "--- 下载 Chrome Headless Shell（备用）---"
if [[ -d "$CACHE_DIR/chromium_headless_shell-"* ]] 2>/dev/null; then
  echo "✅ Chrome Headless Shell 已下载"
else
  echo "正在下载 Chrome Headless Shell..."
  npx playwright install chromium-headless-shell 2>&1 | tail -5
  echo "✅ Chrome Headless Shell 下载完成"
fi

# 5. 创建启动脚本
echo ""
echo "--- 创建辅助脚本 ---"

# start-xvfb.sh：启动虚拟显示器
mkdir -p "$SCRIPT_DIR" 2>/dev/null || true
cat > "$SCRIPT_DIR/start-xvfb.sh" << 'XEOF'
#!/usr/bin/env bash
# 启动 Xvfb 虚拟显示器（DISPLAY=:99）
if pgrep -x Xvfb > /dev/null; then
  echo "Xvfb 已在运行 (DISPLAY=:99)"
  exit 0
fi
Xvfb :99 -screen 0 1280x900x24 -ac &
sleep 1
if pgrep -x Xvfb > /dev/null; then
  echo "✅ Xvfb 启动成功 (DISPLAY=:99)"
  export DISPLAY=:99
else
  echo "❌ Xvfb 启动失败"
  exit 1
fi
XEOF
chmod +x "$SCRIPT_DIR/start-xvfb.sh"
echo "✅ start-xvfb.sh 已创建"

echo ""
echo "=== 安装完成 ==="
echo ""
echo "使用方法（非头模式）："
echo "  1. 启动虚拟显示器: export DISPLAY=:99 && Xvfb :99 -screen 0 1280x900x24 -ac &"
echo "  2. Playwright 代码中设置 headless: false（配合 DISPLAY）"
echo ""
echo "验证运行: bash $SCRIPT_DIR/verify-browser.sh"
