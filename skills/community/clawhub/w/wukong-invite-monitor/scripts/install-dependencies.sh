#!/bin/bash
# 悟空邀请码监控 - 依赖安装脚本

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║        悟空邀请码监控 - 依赖安装                          ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# 检测系统
if [ -f /etc/os-release ]; then
    . /etc/os-release
    case "$ID" in
        alinux|centos|rhel) OS="rhel" ;;
        ubuntu|debian) OS="debian" ;;
        *) OS="unknown" ;;
    esac
else
    OS="unknown"
fi

echo "检测到系统：$OS"
echo ""

# 检查 Python
echo "=== 检查依赖 ==="
if command -v python3 &> /dev/null; then
    echo "✓ Python3: $(python3 --version)"
else
    echo "✗ Python3: 未安装"
    exit 1
fi

# 检查 Tesseract
TESS_INSTALLED=false
if command -v tesseract &> /dev/null; then
    echo "✓ Tesseract: $(tesseract --version 2>&1 | head -1)"
    if tesseract --list-langs 2>&1 | grep -q "chi_sim\|chs"; then
        echo "  ✓ 中文语言包：已安装"
        TESS_INSTALLED=true
    else
        echo "  ⚠ 中文语言包：未安装"
    fi
else
    echo "✗ Tesseract: 未安装"
fi

# 询问是否安装
if [ "$TESS_INSTALLED" = false ]; then
    echo ""
    echo "需要安装 Tesseract OCR"
    
    case "$OS" in
        rhel)
            CMD="sudo yum install -y tesseract tesseract-langpack-chi_sim"
            ;;
        debian)
            CMD="sudo apt install -y tesseract-ocr tesseract-ocr-chi-sim"
            ;;
        *)
            echo "⚠ 未知系统，请手动安装 Tesseract"
            CMD=""
            ;;
    esac
    
    if [ -n "$CMD" ]; then
        echo "推荐命令：$CMD"
        echo ""
        read -p "是否现在安装？(Y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            eval $CMD || {
                echo "⚠ 安装失败，但可继续使用（无 OCR 功能）"
            }
        fi
    fi
else
    echo ""
    echo "=== 所有依赖已就绪 ==="
fi

echo ""
echo "下一步："
echo "  1. python3 monitor_lite.py init"
echo "  2. python3 monitor_lite.py check"
echo "  3. ./setup-cron.sh 5"
echo ""
