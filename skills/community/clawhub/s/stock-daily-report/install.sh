#!/bin/bash
# A 股每日报告 Pro - 安装脚本
# 自动安装所需的 Python 依赖和系统字体

set -e

echo "🚀 开始安装 A 股每日报告 Pro 依赖..."

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python3，请先安装 Python3"
    exit 1
fi

echo "✅ Python3 已安装：$(python3 --version)"

# 检查并安装 pip
if ! command -v pip3 &> /dev/null; then
    echo "⚠️ pip3 未安装，尝试安装..."
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y python3-pip
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-pip
    elif command -v brew &> /dev/null; then
        brew install python3
    else
        echo "❌ 无法自动安装 pip，请手动安装"
        exit 1
    fi
fi

echo "✅ pip3 已安装：$(pip3 --version)"

# 安装 Python 依赖
echo "📦 安装 Python 依赖..."
pip3 install matplotlib --user
pip3 install pyppeteer --user

echo "✅ Python 依赖安装完成"

# 检查并安装中文字体
echo "🔤 检查中文字体..."
FONT_INSTALLED=false

# 检查常见字体路径
if [ -f "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc" ] || \
   [ -f "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc" ] || \
   [ -f "/usr/share/fonts/opentype/noto-cjk/NotoSansCJK-Regular.ttc" ]; then
    echo "✅ 中文字体已安装"
    FONT_INSTALLED=true
fi

# 如果未安装，尝试安装
if [ "$FONT_INSTALLED" = false ]; then
    echo "⚠️ 未找到中文字体，尝试安装..."
    
    if command -v apt &> /dev/null; then
        echo "📦 检测到 Debian/Ubuntu 系统，安装 fonts-noto-cjk..."
        sudo apt update
        sudo apt install -y fonts-noto-cjk
        FONT_INSTALLED=true
    elif command -v yum &> /dev/null; then
        echo "📦 检测到 CentOS/RHEL 系统，安装 google-noto-sans-cjk-fonts..."
        sudo yum install -y google-noto-sans-cjk-fonts
        FONT_INSTALLED=true
    elif command -v dnf &> /dev/null; then
        echo "📦 检测到 Fedora 系统，安装 google-noto-sans-cjk-fonts..."
        sudo dnf install -y google-noto-sans-cjk-fonts
        FONT_INSTALLED=true
    elif command -v pacman &> /dev/null; then
        echo "📦 检测到 Arch 系统，安装 noto-fonts-cjk..."
        sudo pacman -S --noconfirm noto-fonts-cjk
        FONT_INSTALLED=true
    elif command -v brew &> /dev/null; then
        echo "📦 检测到 macOS 系统，macOS 自带中文字体"
        FONT_INSTALLED=true
    else
        echo "⚠️ 无法自动安装字体，请手动安装中文字体"
        echo "   Debian/Ubuntu: sudo apt install fonts-noto-cjk"
        echo "   CentOS/RHEL: sudo yum install google-noto-sans-cjk-fonts"
        echo "   Fedora: sudo dnf install google-noto-sans-cjk-fonts"
        echo "   Arch: sudo pacman -S noto-fonts-cjk"
    fi
fi

# 刷新字体缓存
if [ "$FONT_INSTALLED" = true ]; then
    echo "🔄 刷新字体缓存..."
    if command -v fc-cache &> /dev/null; then
        fc-cache -fv 2>/dev/null || true
    fi
fi

# 预下载 pyppeteer 的 Chromium
echo "🌐 预下载 pyppeteer 所需的 Chromium（首次运行可能需要几分钟）..."
python3 -c "import asyncio; from pyppeteer import chromium_downloader; asyncio.get_event_loop().run_until_complete(chromium_downloader.download())" 2>/dev/null || echo "⚠️ Chromium 下载失败，将在首次生成图片时自动下载"

echo ""
echo "✅ 安装完成！"
echo ""
echo "📖 使用方法："
echo "   # 生成 HTML + 长图片报告"
echo "   python3 generate_report.py --format both"
echo ""
echo "   # 指定股票代码"
echo "   python3 generate_report.py --stocks 002973,600095 --format both"
echo ""
echo "   # 编辑配置文件 config.json 设置自选股"
echo ""
echo "⚠️ 注意：如果中文显示异常，请确保系统已安装中文字体"
