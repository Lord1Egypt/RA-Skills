#!/bin/bash
# 安装港股分析工具所需的 Python 依赖
# 用法: bash install_deps.sh

echo "正在安装港股分析工具依赖..."

# 检查是否已安装
python3 -c "import numpy; import pandas; print('依赖已安装')" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ 所有依赖已就绪"
    exit 0
fi

# 尝试安装 (兼容 PEP 668 限制)
pip3 install numpy pandas --quiet 2>/dev/null
if [ $? -ne 0 ]; then
    echo "尝试使用 --break-system-packages 安装..."
    pip3 install --break-system-packages numpy pandas --quiet 2>/dev/null
fi

if [ $? -ne 0 ]; then
    echo "尝试使用 --user 安装..."
    pip3 install --user numpy pandas --quiet 2>/dev/null
fi

# 最终验证
python3 -c "import numpy; import pandas" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ 依赖安装成功"
    echo "已安装: numpy, pandas"
else
    echo "❌ 安装失败，请手动运行以下命令之一:"
    echo "   pip3 install numpy pandas"
    echo "   pip3 install --break-system-packages numpy pandas"
    echo "   pip3 install --user numpy pandas"
    exit 1
fi
