#!/bin/bash
# run_docker.sh - 通过 Docker 运行 r-ggplot-quickplot
# 用法: ./run_docker.sh <input_csv> [output_dir]

set -e

IMAGE_NAME="r-ggplot-quickplot"
CONTAINER_NAME="r-ggplot-quickplot-run"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================"
echo "  r-ggplot-quickplot (Docker Mode)"
echo "========================================"
echo ""

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker 未安装${NC}"
    echo "请先安装 Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# 检查 Docker 是否运行
if ! docker info &> /dev/null; then
    echo -e "${RED}错误: Docker 未运行${NC}"
    echo "请启动 Docker Desktop"
    exit 1
fi

# 检查镜像是否存在
if ! docker image inspect $IMAGE_NAME &> /dev/null; then
    echo -e "${YELLOW}正在构建 Docker 镜像 (首次需要几分钟)...${NC}"
    echo ""

    # 构建镜像
    docker build -t $IMAGE_NAME .

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 镜像构建成功${NC}"
    else
        echo -e "${RED}✗ 镜像构建失败${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Docker 镜像已就绪${NC}"
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

# 复制输入文件到容器
INPUT_FILENAME=$(basename "$INPUT_FILE")
docker cp "$INPUT_PATH" $CONTAINER_NAME:/app/input/data.csv 2>/dev/null || true

# 运行容器
echo -e "${GREEN}运行图表生成...${NC}"
echo ""

docker run --rm \
    --name $CONTAINER_NAME \
    -v "$(pwd)/$OUTPUT_DIR:/app/output" \
    -v "$INPUT_PATH:/app/input/data.csv:ro" \
    $IMAGE_NAME \
    Rscript /app/run_plot.R /app/input/data.csv --output-dir /app/output

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
