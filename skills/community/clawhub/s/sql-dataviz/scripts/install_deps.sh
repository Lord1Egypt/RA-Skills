#!/bin/bash
# sql-dataviz 依赖安装脚本
# 支持 Windows (PowerShell) 和 Linux/macOS (Bash)

set -e

echo "=========================================="
echo "sql-dataviz 依赖安装脚本"
echo "=========================================="

# 检测操作系统
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    OS="windows"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    OS="unknown"
fi

echo "检测到操作系统: $OS"

# 检查 Python
echo ""
echo "检查 Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION"

# 检查 pip
echo ""
echo "检查 pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 未安装"
    exit 1
fi

PIP_VERSION=$(pip3 --version 2>&1 | awk '{print $2}')
echo "✓ pip $PIP_VERSION"

# 升级 pip
echo ""
echo "升级 pip..."
pip3 install --upgrade pip

# 安装核心依赖
echo ""
echo "安装核心依赖..."
pip3 install \
    matplotlib \
    seaborn \
    pandas \
    numpy \
    pillow

echo "✓ 核心依赖安装完成"

# 安装可选依赖
echo ""
echo "安装可选依赖..."

# 树状图
echo "  - 安装 squarify (树状图)..."
pip3 install squarify || echo "  ⚠ squarify 安装失败（可选）"

# 地理数据
echo "  - 安装 geopandas (地理数据)..."
pip3 install geopandas shapely || echo "  ⚠ geopandas 安装失败（可选）"

# 交互式图表
echo "  - 安装 plotly (交互式图表)..."
pip3 install plotly || echo "  ⚠ plotly 安装失败（可选）"

echo "✓ 可选依赖安装完成"

# 验证安装
echo ""
echo "验证安装..."
python3 << 'EOF'
try:
    import matplotlib
    import seaborn
    import pandas
    import numpy
    from PIL import Image
    print("✓ 所有核心依赖验证成功")
except ImportError as e:
    print(f"❌ 依赖验证失败: {e}")
    exit(1)
EOF

echo ""
echo "=========================================="
echo "✓ 安装完成！"
echo "=========================================="
echo ""
echo "快速开始:"
echo "  python3 demo.py"
echo ""
