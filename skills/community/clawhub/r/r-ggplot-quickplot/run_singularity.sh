#!/bin/bash
# run_singularity.sh - 通过 Singularity 运行 r-ggplot-quickplot
# 用于 HPC/共享服务器环境
# 用法: ./run_singularity.sh <input_csv> [output_dir]

set -e

IMAGE_NAME="r-ggplot-quickplot.sif"
CONTAINER_NAME="r-ggplot-quickplot"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================"
echo "  r-ggplot-quickplot (Singularity Mode)"
echo "========================================"
echo ""

# 检查 Singularity 是否安装
if ! command -v singularity &> /dev/null; then
    echo -e "${RED}错误: Singularity 未安装${NC}"
    echo "请联系管理员安装 Singularity"
    echo "或使用 Docker 模式: ./run_docker.sh"
    exit 1
fi

# 检查镜像是否存在
if [ ! -f "$IMAGE_NAME" ]; then
    echo -e "${YELLOW}镜像不存在，正在构建...${NC}"
    echo ""

    # 构建镜像
    singularity build $IMAGE_NAME Singularity.def

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 镜像构建成功${NC}"
    else
        echo -e "${RED}✗ 镜像构建失败${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Singularity 镜像已就绪${NC}"
fi

# 获取输入文件
INPUT_FILE="${1:-input/sample_data.csv}"

if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${RED}错误: 输入文件不存在 - $INPUT_FILE${NC}"
    exit 1
fi

# 获取绝对路径
INPUT_PATH=$(cd "$(dirname "$INPUT_FILE")" && pwd)/$(basename "$INPUT_FILE")

# 获取输出目录
OUTPUT_DIR="${2:-output}"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

echo ""
echo "输入文件: $INPUT_PATH"
echo "输出目录: $OUTPUT_DIR"
echo ""

# 运行 Singularity 容器
echo -e "${GREEN}运行图表生成...${NC}"
echo ""

singularity exec \
    --bind "$INPUT_PATH:/app/input/data.csv:ro" \
    --bind "$(pwd)/$OUTPUT_DIR:/app/output" \
    --bind "$(pwd):/app/workdir" \
    $IMAGE_NAME \
    bash -c "cd /app/workdir && Rscript /app/run_plot.R /app/input/data.csv --output-dir /app/output"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ 执行成功!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "生成的图表:"
    ls -lh "$OUTPUT_DIR"/*.png 2>/dev/null | awk '{print "  - " $NF " (" $5 ")"}'
else
    echo -e "${RED}执行失败${NC}"
    exit 1
fi
