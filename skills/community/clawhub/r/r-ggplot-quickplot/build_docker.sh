#!/bin/bash
# build_docker.sh - 构建并推送 Docker 镜像
# 用于发布到 Docker Hub 或私有仓库

set -e

IMAGE_NAME="${DOCKER_IMAGE_NAME:-r-ggplot-quickplot}"
DOCKER_USERNAME="${DOCKER_USERNAME:-}"
TAG="${1:-latest}"

echo "========================================"
echo "  构建 r-ggplot-quickplot Docker 镜像"
echo "========================================"
echo ""
echo "镜像名称: $IMAGE_NAME:$TAG"
echo ""

# 构建镜像
echo "正在构建镜像..."
docker build -t $IMAGE_NAME:$TAG .

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ 镜像构建成功"
else
    echo ""
    echo "✗ 镜像构建失败"
    exit 1
fi

# 如果指定了用户名，则推送到仓库
if [ -n "$DOCKER_USERNAME" ]; then
    FULL_IMAGE_NAME="${DOCKER_USERNAME}/${IMAGE_NAME}"

    echo ""
    echo "正在标记镜像..."
    docker tag $IMAGE_NAME:$TAG $FULL_IMAGE_NAME:$TAG

    echo ""
    echo "正在推送镜像到 Docker Hub..."
    echo "提示: 可能需要先登录: docker login"

    docker push $FULL_IMAGE_NAME:$TAG

    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ 推送成功!"
        echo ""
        echo "用户可以通过以下命令使用:"
        echo "  docker pull $FULL_IMAGE_NAME:$TAG"
    fi
else
    echo ""
    echo "镜像已构建完成"
    echo ""
    echo "本地测试运行:"
    echo "  docker run --rm -v \$(pwd)/output:/app/output $IMAGE_NAME:$TAG"
fi

echo ""
echo "========================================"
