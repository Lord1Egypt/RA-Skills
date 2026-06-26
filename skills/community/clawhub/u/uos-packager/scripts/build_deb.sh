#!/bin/bash
#
# UOS 应用打包脚本
# 用法: ./build_deb.sh <appid> <version> [arch1,arch2]
# 示例: ./build_deb.sh org.example.myapp 1.0.0 amd64
#

set -e

APPID="${1:-}"
VERSION="${2:-}"
ARCHS="${3:-amd64}"

if [[ -z "$APPID" || -z "$VERSION" ]]; then
    echo "用法: $0 <appid> <version> [arch1,arch2...]"
    echo "示例: $0 org.example.myapp 1.0.0 amd64,arm64"
    exit 1
fi

BUILD_DIR="/tmp/uos_build_$$"
mkdir -p "$BUILD_DIR"

echo "=== UOS 应用打包工具 ==="
echo "  appid:   $APPID"
echo "  version: $VERSION"
echo "  archs:   $ARCHS"
echo "  输出:    $BUILD_DIR"
echo ""

# 解析多架构
IFS=',' read -ra ARCH_ARRAY <<< "$ARCHS"

for ARCH in "${ARCH_ARRAY[@]}"; do
    ARCH=$(echo "$ARCH" | tr -d ' ')
    PKG_DIR="$BUILD_DIR/${APPID}_${VERSION}_${ARCH}"
    
    echo "--- 打包 $ARCH ---"
    
    # 创建目录结构
    mkdir -p "$PKG_DIR/DEBIAN"
    mkdir -p "$PKG_DIR/opt/apps/${APPID}/entries/applications"
    mkdir -p "$PKG_DIR/opt/apps/${APPID}/entries/icons/hicolor/scalable/apps"
    mkdir -p "$PKG_DIR/opt/apps/${APPID}/files/bin"
    
    # 检查 info 文件
    if [[ ! -f "opt/apps/${APPID}/info" ]]; then
        echo "⚠ 警告: ${APPID}/opt/apps/${APPID}/info 不存在，跳过此架构"
        continue
    fi
    
    # 复制应用目录
    if [[ -d "$APPID/entries" ]]; then
        cp -r "$APPID/entries" "$PKG_DIR/opt/apps/${APPID}/"
    fi
    if [[ -d "$APPID/files" ]]; then
        cp -r "$APPID/files" "$PKG_DIR/opt/apps/${APPID}/"
    fi
    if [[ -f "$APPID/info" ]]; then
        cp "$APPID/info" "$PKG_DIR/opt/apps/${APPID}/"
    fi
    
    # 生成 debian/control
    cat > "$PKG_DIR/DEBIAN/control" << EOF
Package: ${APPID}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Maintainer: $(whoami) <$(whoami)@localhost>
Description: UOS Application
EOF

    # 复制 desktop 文件（从 entries 或创建空的）
    if [[ -f "$APPID/entries/applications/${APPID}.desktop" ]]; then
        cp "$APPID/entries/applications/${APPID}.desktop" \
           "$PKG_DIR/DEBIAN/${APPID}.desktop"
    fi
    
    # 检查钩子脚本
    for hook in postinst postrm preinst prerm; do
        if [[ -f "$APPID/DEBIAN/$hook" ]]; then
            cp "$APPID/DEBIAN/$hook" "$PKG_DIR/DEBIAN/$hook"
            echo "⚠ 检测到 $hook，已复制（请确保符合规范）"
            # 检查 rm -rf 用法
            if grep -q 'rm -rf.*\$[A-Z_]' "$PKG_DIR/DEBIAN/$hook"; then
                echo "⚠ 警告: $hook 中 rm -rf 使用了变量，请确保加双引号"
            fi
        fi
    done
    
    # 打包
    DEB_FILE="${APPID}_${VERSION}_${ARCH}.deb"
    dpkg-deb --build "$PKG_DIR" "$DEB_FILE" 2>/dev/null || \
        fakeroot dpkg-deb --build "$PKG_DIR" "$DEB_FILE"
    
    echo "✅ 生成: $DEB_FILE"
    echo ""
done

echo "=== 打包完成 ==="
ls -lh "${APPID}"_*.deb 2>/dev/null || true
echo "输出目录: $BUILD_DIR"
echo ""
echo "提示: 安装测试"
echo "  sudo dpkg -i ${APPID}_${VERSION}_${ARCH_ARRAY[0]}.deb"
echo "  # 或在 UOS 桌面上双击 deb 文件安装"
