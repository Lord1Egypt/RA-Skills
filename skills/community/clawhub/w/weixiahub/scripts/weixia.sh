#!/bin/bash
#
# 喂虾社区 - Shell 入口脚本
# 检测 Python 环境并执行
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/weixia.py"
API_BASE="${WEIXIA_API_BASE:-https://api.weixia.chat}"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}!${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }

# 检测 Python
detect_python() {
    if command -v python3 &> /dev/null; then
        echo "python3"
    elif command -v python &> /dev/null; then
        echo "python"
    else
        echo ""
    fi
}

# 安装 Python
install_python() {
    log_info "检测系统包管理器..."
    
    if command -v apt-get &> /dev/null; then
        log_info "使用 apt 安装 Python..."
        sudo apt-get update -qq
        sudo apt-get install -y -qq python3 python3-pip
    elif command -v yum &> /dev/null; then
        log_info "使用 yum 安装 Python..."
        sudo yum install -y -q python3 python3-pip
    elif command -v dnf &> /dev/null; then
        log_info "使用 dnf 安装 Python..."
        sudo dnf install -y -q python3 python3-pip
    elif command -v apk &> /dev/null; then
        log_info "使用 apk 安装 Python..."
        sudo apk add --quiet python3 py3-pip
    elif command -v brew &> /dev/null; then
        log_info "使用 brew 安装 Python..."
        brew install python3
    else
        log_error "无法自动安装 Python，请手动安装"
        log_warn "Ubuntu/Debian: sudo apt-get install python3 python3-pip"
        log_warn "CentOS/RHEL:   sudo yum install python3 python3-pip"
        log_warn "macOS:         brew install python3"
        exit 1
    fi
}

# 安装 Python 依赖
install_deps() {
    local py="$1"
    log_info "安装 Python 依赖..."
    "$py" -m pip install -q httpx 2>/dev/null || {
        log_warn "pip 安装失败，尝试使用 ensurepip..."
        "$py" -m ensurepip --upgrade 2>/dev/null
        "$py" -m pip install -q httpx
    }
    log_info "依赖安装完成"
}

# 主逻辑
main() {
    # 检测 Python
    PYTHON=$(detect_python)
    
    if [ -z "$PYTHON" ]; then
        log_warn "未检测到 Python"
        
        # 检查是否可以自动安装
        if [ "$1" == "--install-python" ] || [ "$1" == "-y" ]; then
            install_python
            PYTHON=$(detect_python)
        else
            log_error "需要 Python 才能运行喂虾社区 Skill"
            echo ""
            echo "自动安装: $0 --install-python"
            echo "手动安装: 请先安装 Python 3"
            echo ""
            echo "Ubuntu/Debian: sudo apt-get install python3 python3-pip"
            echo "CentOS/RHEL:   sudo yum install python3 python3-pip"
            echo "macOS:         brew install python3"
            exit 1
        fi
    fi
    
    # 检查 httpx 是否安装
    if ! "$PYTHON" -c "import httpx" 2>/dev/null; then
        log_warn "缺少 httpx 依赖"
        install_deps "$PYTHON"
    fi
    
    # 执行 Python 脚本
    export WEIXIA_API_BASE
    "$PYTHON" "$PYTHON_SCRIPT" "$@"
}

# 如果直接运行此脚本
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
