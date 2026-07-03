#!/bin/bash
# todos/scripts/build_release.sh
# 自动构建 release ZIP（用于上传到 QwenPaw Skills Hub）
# 用法：./scripts/build_release.sh [version]
# 版本：v1.0 | 日期：2026-06-11

set -e

VERSION=${1:-"v1.5.0"}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TMP_DIR="/tmp/todo-list-skill-${VERSION}"
ZIP_FILE="/tmp/todo-list-skill-${VERSION}.zip"

echo "🚀 构建 release ZIP..."
echo "   版本: $VERSION"
echo "   项目目录: $PROJECT_DIR"
echo "   输出: $ZIP_FILE"
echo ""

# 1. 清理旧的临时目录
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

# 2. 复制必需文件
echo "📦 复制文件..."
cp "$PROJECT_DIR/SKILL.md" "$PROJECT_DIR/README.md" \
   "$PROJECT_DIR/CHANGELOG.md" "$PROJECT_DIR/CONTRIBUTING.md" \
   "$PROJECT_DIR/DESIGN.md" "$PROJECT_DIR/EXAMPLES.md" \
   "$PROJECT_DIR/INSTALL.md" "$PROJECT_DIR/ROADMAP.md" \
   "$PROJECT_DIR/SECURITY.md" "$PROJECT_DIR/PUBLISH.md" \
   "$PROJECT_DIR/manifest.yaml" "$PROJECT_DIR/pyproject.toml" \
   "$PROJECT_DIR/requirements.txt" "$PROJECT_DIR/cliff.toml" \
   "$PROJECT_DIR/LICENSE" "$TMP_DIR/"

# 3. 复制目录
for dir in src tests references data scripts schema; do
    if [ -d "$PROJECT_DIR/$dir" ]; then
        cp -r "$PROJECT_DIR/$dir" "$TMP_DIR/"
        echo "   ✓ $dir/"
    fi
done

# 4. 创建 ZIP
echo ""
echo "📦 打包 ZIP..."
cd /tmp
rm -f "$ZIP_FILE"
zip -r "$ZIP_FILE" "$(basename "$TMP_DIR")" \
    -x "*/__pycache__/*" "*/.pytest_cache/*" "*.db" "*.egg-info/*" "*.pyc"

# 5. 清理临时目录
rm -rf "$TMP_DIR"

# 6. 输出结果
echo ""
echo "✅ 构建完成！"
echo "   ZIP: $ZIP_FILE"
ls -lh "$ZIP_FILE"
echo ""
echo "📋 下一步："
echo "   1. 上传 ZIP 到 ClawHub: https://clawhub.ai/skills/publish"
echo "   2. 上传 ZIP 到 ModelScope: https://modelscope.cn/skills"
echo "   3. 提交 PR 到 skills.sh: https://github.com/anthropics/skills"
echo ""
echo "或 URL 导入（需要 GitHub mirror）："
echo "   qwenpaw skills install https://github.com/<user>/todo-list-skill"
