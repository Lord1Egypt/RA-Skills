#!/bin/bash
# r-ggplot-quickplot 快速运行脚本 (Linux/macOS)
# 用法: ./run.sh [input_file]
# 示例: ./run.sh input/sample_data.csv

echo "========================================"
echo "  r-ggplot-quickplot"
echo "========================================"
echo ""

# 检查 Rscript 是否安装
if ! command -v Rscript &> /dev/null; then
    echo "错误: 未找到 Rscript"
    echo "请先安装 R (>= 4.0)"
    echo "下载地址: https://cran.r-project.org/"
    exit 1
fi

# 检查 ggplot2 是否安装
Rscript -e "if(!requireNamespace('ggplot2', quietly=TRUE)) install.packages('ggplot2')" 2>/dev/null

# 获取输入文件路径
if [ -z "$1" ]; then
    INPUT_FILE="input/sample_data.csv"
else
    INPUT_FILE="$1"
fi

echo "输入文件: $INPUT_FILE"
echo "输出目录: output"
echo ""

# 运行绘图脚本
Rscript run_plot.R "$INPUT_FILE"

echo ""
echo "完成!"
