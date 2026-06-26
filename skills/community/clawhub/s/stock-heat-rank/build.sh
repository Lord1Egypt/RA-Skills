#!/bin/bash

# 跨平台构建脚本
# 为不同操作系统和架构生成可执行文件

set -e

VERSION=${VERSION:-"1.0.0"}
BINARY_NAME="stock-heat-rank"
BUILD_DIR="dist"

# 清理构建目录
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR

# 颜色输出
GREEN='\033[0;32m'
NC='\033[0m'

echo "=== 构建股票热度排名工具 v${VERSION} ==="
echo ""

# 平台列表
PLATFORMS=(
    "darwin/amd64:macos-x64"
    "darwin/arm64:macos-arm64"
    "linux/amd64:linux-x64"
    "linux/arm64:linux-arm64"
    "windows/amd64:windows-x64.exe"
)

# 构建函数
build() {
    local os_arch=$1
    local output_name=$2
    
    IFS='/' read -r GOOS GOARCH <<< "$os_arch"
    
    output_path="${BUILD_DIR}/${output_name}"
    
    echo -e "${GREEN}构建 ${output_name}${NC} (GOOS=$GOOS, GOARCH=$GOARCH)"
    
    CGO_ENABLED=0 GOOS=$GOOS GOARCH=$GOARCH go build \
        -ldflags="-s -w -X main.Version=${VERSION}" \
        -o "$output_path" \
        .
    
    # 添加执行权限
    chmod +x "$output_path" 2>/dev/null || true
}

# 执行构建
for platform in "${PLATFORMS[@]}"; do
    IFS=':' read -r os_arch output_name <<< "$platform"
    build "$os_arch" "$output_name"
done

echo ""
echo "=== 构建完成 ==="
ls -lh $BUILD_DIR/