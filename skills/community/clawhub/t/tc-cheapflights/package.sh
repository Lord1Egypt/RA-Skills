#!/bin/bash
# 打包技能脚本

set -e

SKILL_NAME="tongcheng-cheap-flights"
VERSION="1.1.0"
PACKAGE_NAME="${SKILL_NAME}-${VERSION}"

echo "📦 打包技能: $SKILL_NAME v$VERSION"

# 检查必要文件
if [ ! -f "SKILL.md" ]; then
    echo "❌ 缺少 SKILL.md 文件"
    exit 1
fi

if [ ! -f ".easyclaw-metadata.json" ]; then
    echo "❌ 缺少 .easyclaw-metadata.json 文件"
    exit 1
fi

# 创建临时目录
TEMP_DIR=$(mktemp -d)
PACKAGE_DIR="$TEMP_DIR/$PACKAGE_NAME"

echo "📁 创建临时目录: $PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR"

# 复制文件
echo "📋 复制文件..."
cp -r ./* "$PACKAGE_DIR/" 2>/dev/null || true

# 删除不需要的文件
echo "🧹 清理文件..."
cd "$PACKAGE_DIR"
rm -rf __pycache__ *.pyc .git .DS_Store logs/*.log data/*.json

# 创建压缩包
cd "$TEMP_DIR"
echo "🗜️  创建压缩包: $PACKAGE_NAME.tar.gz"
tar -czf "$PACKAGE_NAME.tar.gz" "$PACKAGE_NAME"

# 移动到当前目录
cd - > /dev/null
mv "$TEMP_DIR/$PACKAGE_NAME.tar.gz" .

# 清理临时目录
rm -rf "$TEMP_DIR"

echo "✅ 打包完成!"
echo "📦 包文件: $PACKAGE_NAME.tar.gz"
echo ""
echo "安装说明:"
echo "  1. 解压: tar -xzf $PACKAGE_NAME.tar.gz"
echo "  2. 进入目录: cd $PACKAGE_NAME"
echo "  3. 安装: python3 install.py"
echo ""
echo "或直接使用: python3 install.py 进行一键安装"