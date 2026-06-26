#!/bin/bash
# 发布技能到 ClawHub

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

echo "🚀 发布技能到 ClawHub"
echo "===================="
echo ""

# 检查必要文件
echo "📋 检查必要文件..."
required_files=("SKILL.md" "README.md" "_meta.json" ".clawhub/config.json")
for file in "${required_files[@]}"; do
    if [ ! -f "$BASE_DIR/$file" ]; then
        echo "❌ 缺少必要文件：$file"
        exit 1
    fi
done
echo "✅ 必要文件检查通过"
echo ""

# 运行环境检查
echo "🔍 运行环境检查..."
bash "$BASE_DIR/scripts/setup_runtime.sh" || {
    echo "⚠️  环境检查有警告，但继续发布..."
}
echo ""

# 显示版本信息
version=$(grep -o '"version": "[^"]*"' "$BASE_DIR/_meta.json" | cut -d'"' -f4)
echo "📦 技能信息:"
echo "   名称：typecho-blog-publish"
echo "   版本：$version"
echo ""

# 发布
echo "📤 准备发布..."
echo ""
echo "请选择发布方式:"
echo "1. 发布到 ClawHub (需要 API Key)"
echo "2. 本地打包"
echo "3. 取消"
echo ""
read -p "选择 (1-3): " choice

case $choice in
    1)
        echo "🔗 发布到 ClawHub..."
        if command -v clawhub &> /dev/null; then
            clawhub publish "$BASE_DIR"
        else
            echo "❌ 未找到 clawhub 命令"
            exit 1
        fi
        ;;
    2)
        echo "📦 本地打包..."
        cd "$BASE_DIR"
        tar -czf "typecho-blog-publish-$version.tar.gz" \
            --exclude='.clawhub' \
            --exclude='*.tar.gz' \
            .
        echo "✅ 打包完成：typecho-blog-publish-$version.tar.gz"
        ;;
    3)
        echo "❌ 取消发布"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "✅ 发布完成！"
