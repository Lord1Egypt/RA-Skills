#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"
PYTHON_MIN_VERSION="3.10"

echo "=== Yintai Tasks Runner 安装脚本 ==="
echo ""

check_python() {
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 未安装"
        echo "请先安装 Python 3.10+: https://www.python.org/downloads/"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info[0])')
    PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info[1])')
    
    REQUIRED_MINOR=$(echo $PYTHON_MIN_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt "$REQUIRED_MINOR" ]); then
        echo "❌ Python 版本过低: $PYTHON_VERSION"
        echo "需要 Python $PYTHON_MIN_VERSION 或更高版本"
        exit 1
    fi
    
    echo "✓ Python 版本: $PYTHON_VERSION"
}

check_pip() {
    if ! python3 -m pip --version &> /dev/null; then
        echo "❌ pip 未安装，尝试安装..."
        python3 -m ensurepip --upgrade 2>/dev/null || {
            echo "请手动安装 pip: curl https://bootstrap.pypa.io/get-pip.py | python3"
            exit 1
        }
    fi
    echo "✓ pip 可用"
}

create_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        echo ""
        echo "创建虚拟环境..."
        python3 -m venv "$VENV_DIR"
        echo "✓ 虚拟环境已创建: $VENV_DIR"
    else
        echo "✓ 虚拟环境已存在: $VENV_DIR"
    fi
}

activate_venv() {
    source "${VENV_DIR}/bin/activate"
    echo "✓ 虚拟环境已激活"
}

install_deps() {
    echo ""
    echo "安装依赖..."
    
    pip install --upgrade pip
    
    pip install httpx>=0.25.0
    
    echo "✓ 依赖安装完成"
}

verify_install() {
    echo ""
    echo "验证安装..."
    
    python3 -c "import httpx; print('✓ httpx', httpx.__version__)"
    
    cd "$SCRIPT_DIR"
    python3 -c "from yintai_tasks_runner.config import load_config; print('✓ yintai_tasks_runner 模块可导入')"
    
    echo "✓ 安装验证通过"
}

main() {
    echo ""
    check_python
    check_pip
    create_venv
    activate_venv
    install_deps
    verify_install
    
    echo ""
    echo "=== 安装完成 ==="
    echo ""
    echo "激活虚拟环境并运行:"
    echo "  source ${VENV_DIR}/bin/activate"
    echo "  python -m skills.yintai_tasks_runner --once"
    echo ""
}

main "$@"
