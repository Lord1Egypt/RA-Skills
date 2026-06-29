#!/bin/bash
# 部署脚本 - Linux/macOS
# 检测并安装Tesseract OCR引擎

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== 财税合规Skill安装脚本 ==="
echo ""

# 检查Python版本
check_python() {
    if command -v python3 &>/dev/null; then
        PYTHON=python3
    elif command -v python &>/dev/null; then
        PYTHON=python
    else
        echo "错误: 未找到Python，请先安装Python 3.8+"
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON -c "import sys; print(sys.version_info[:2])")
    echo "✓ Python版本: $PYTHON_VERSION"
}

# 检查Tesseract
check_tesseract() {
    if command -v tesseract &>/dev/null; then
        TESSERACT_VERSION=$(tesseract --version 2>&1 | head -1)
        echo "✓ Tesseract已安装: $TESSERACT_VERSION"
        return 0
    else
        echo "✗ Tesseract未安装"
        return 1
    fi
}

# 安装Tesseract
install_tesseract() {
    echo ""
    echo "正在尝试安装Tesseract..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &>/dev/null; then
           brew install tesseract tesseract-lang
        else
            echo "请先安装Homebrew: https://brew.sh"
            echo "然后运行: brew install tesseract tesseract-lang"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &>/dev/null; then
            # Debian/Ubuntu
            sudo apt-get update
            sudo apt-get install -y tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-eng
        elif command -v yum &>/dev/null; then
            # CentOS/RHEL
            sudo yum install -y tesseract tesseract-langpack-chi_sim
        elif command -v dnf &>/dev/null; then
            # Fedora
            sudo dnf install -y tesseract tesseract-langpack-chi_sim
        else
            echo "无法检测包管理器，请手动安装Tesseract"
            echo "参考: https://github.com/UB-Mannheim/tesseract/wiki"
        fi
    else
        echo "不支持的操作系统: $OSTYPE"
        echo "请手动安装Tesseract: https://github.com/UB-Mannheim/tesseract/wiki"
    fi
}

# 安装Python依赖
install_python_deps() {
    echo ""
    echo "安装Python依赖..."
    
    $PYTHON -m pip install --upgrade pip
    $PYTHON -m pip install Pillow pytesseract openpyxl pyyaml
    
    # PDF支持（可选）
    if command -v pdftoppm &>/dev/null; then
        $PYTHON -m pip install pdf2image
        echo "✓ PDF支持已启用"
    else
        echo "⚠ poppler未安装，PDF支持不可用"
        echo "  安装poppler: apt-get install poppler-utils (Linux) 或 brew install poppler (macOS)"
    fi
}

# 验证安装
verify_installation() {
    echo ""
    echo "=== 验证安装 ==="
    
    #验证Tesseract
    if command -v tesseract &>/dev/null; then
        echo "✓ Tesseract: $(tesseract --version 2>&1 | head -1)"
    else
        echo "✗ Tesseract: 未安装"
    fi
    
    # 验证Python模块
    $PYTHON -c "
import sys
modules = ['PIL', 'pytesseract', 'openpyxl']
missing = []
for mod in modules:
    try:
        __import__(mod)
        print(f'✓ {mod}')
    except ImportError:
        missing.append(mod)
        print(f'✗ {mod}')
if missing:
    print(f'请运行: pip install {\" \".join(missing)}')
"
}

# 主流程
check_python

if ! check_tesseract; then
    install_tesseract
fi

install_python_deps
verify_installation

echo ""
echo "=== 安装完成 ==="
echo ""
echo "使用方法："
echo "1. 首次使用请编辑 config.yaml 配置企业信息"
echo "2. 识别发票: python scripts/ocr_engine.py --input 发票.png --output receipt.json"
echo "3. 查验真伪: python scripts/verify_abstract.py --config config.yaml --receipt receipt.json"
echo "4. 生成报销单: python scripts/template_matcher.py fill --config config.yaml --receipt receipt.json --template templates/expense_basic.xlsx"