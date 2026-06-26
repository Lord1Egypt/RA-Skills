#!/bin/bash
# build_singularity.sh - 构建 Singularity 镜像
# 用于 HPC/共享服务器环境

set -e

IMAGE_NAME="${1:-r-ggplot-quickplot.sif}"
DEF_FILE="Singularity.def"

echo "========================================"
echo "  构建 r-ggplot-quickplot Singularity 镜像"
echo "========================================"
echo ""
echo "镜像名称: $IMAGE_NAME"
echo ""

# 检查 Singularity
if ! command -v singularity &> /dev/null; then
    echo "错误: Singularity 未安装"
    echo ""
    echo "在本地构建需要 Singularity"
    echo "在 HPC 环境中，通常可以直接构建"
    echo ""
    echo "如果需要在本地构建 (需要 root):"
    echo "  1. 安装 Singularity"
    echo "  2. 使用 Docker Hub 中的预构建镜像"
    exit 1
fi

# 检查定义文件
if [ ! -f "$DEF_FILE" ]; then
    echo "错误: $DEF_FILE 不存在"
    exit 1
fi

echo "正在构建镜像..."
echo "注意: 这可能需要几分钟时间"
echo ""

singularity build $IMAGE_NAME $DEF_FILE

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ 镜像构建成功"
    echo ""
    echo "镜像大小:"
    ls -lh $IMAGE_NAME | awk '{print "  " $NF ": " $5}'
    echo ""
    echo "使用方法:"
    echo "  singularity exec $IMAGE_NAME Rscript /app/run_plot.R input.csv"
    echo ""
    echo "或使用提供的脚本:"
    echo "  ./run_singularity.sh input.csv"
else
    echo ""
    echo "✗ 镜像构建失败"
    exit 1
fi

echo ""
echo "========================================"
