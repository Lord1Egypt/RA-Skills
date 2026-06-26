#!/bin/bash
# 发布脚本 - Agent 自我学习技能

set -e

# 从 SKILL.md 提取版本号
VERSION=$(grep '^version:' SKILL.md | head -1 | sed 's/version: *//' | tr -d '"')
SKILL_NAME="self-learning"
RELEASE_DIR="release"

echo "🚀 开始发布 $SKILL_NAME v$VERSION"

# 检查必要文件
REQUIRED_FILES=(
    "SKILL.md"
    "README.md"
    "config.yaml"
    "requirements.txt"
    "scripts/memory_update.py"
    "scripts/learning_manager.py"
    "scripts/learning_manager_cli.py"
    ".learnings/LEARNINGS.md"
    ".learnings/ERRORS.md"
    ".learnings/FEATURE_REQUESTS.md"
    "hooks/openclaw/handler.js"
    "hooks/openclaw/HOOK.md"
)

echo "📋 检查必要文件..."
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ 缺少文件：$file"
        exit 1
    fi
done
echo "✅ 所有必要文件存在"

# 清理旧发布
rm -rf $RELEASE_DIR
mkdir -p $RELEASE_DIR

# 复制必要文件
echo "📦 打包文件..."
cp -r scripts $RELEASE_DIR/
cp -r .learnings $RELEASE_DIR/
cp -r hooks $RELEASE_DIR/
cp -r examples $RELEASE_DIR/ 2>/dev/null || true
cp -r tests $RELEASE_DIR/
cp SKILL.md $RELEASE_DIR/
cp README.md $RELEASE_DIR/
cp config.yaml $RELEASE_DIR/
cp requirements.txt $RELEASE_DIR/
cp LICENSE $RELEASE_DIR/
cp CHANGELOG.md $RELEASE_DIR/
cp .gitignore $RELEASE_DIR/

# 运行测试 (可选)
echo "🧪 运行测试..."
if [ -d "tests" ] && command -v pytest &> /dev/null; then
    python3 -m pytest tests/ -v || echo "⚠️ 测试失败，继续发布..."
fi

# 创建压缩包
echo "📦 创建压缩包..."
cd $RELEASE_DIR
tar -czf ../${SKILL_NAME}-v${VERSION}.tar.gz *
cd ..

# 清理
rm -rf $RELEASE_DIR

echo ""
echo "✅ 发布完成！"
echo "📦 发布包：${SKILL_NAME}-v${VERSION}.tar.gz"
echo ""
echo "📝 发布到 ClawHub:"
echo "1. 访问 https://clawhub.ai/upload"
echo "2. 上传 ${SKILL_NAME}-v${VERSION}.tar.gz"
echo "3. 填写技能信息"
echo "4. 提交审核"
echo ""
