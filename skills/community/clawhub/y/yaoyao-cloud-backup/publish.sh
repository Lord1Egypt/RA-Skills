#!/bin/bash
# =============================================================================
# 发布脚本 - 从开发版同步到发布版，然后发布
# =============================================================================
# 版本结构：
# - yaoyao-cloud-backup-v2   = 开发版
# - yaoyao-cloud-backup-homo = 使用版（发布专用）
# =============================================================================

set -e

WORKSPACE="$HOME/.openclaw/workspace/skills"
DEV_DIR="$WORKSPACE/yaoyao-cloud-backup-v2"
PUBLISH_DIR="$WORKSPACE/yaoyao-cloud-backup-homo"

if [ -z "$1" ]; then
    echo "用法: ./publish.sh <版本号>"
    echo "例如: ./publish.sh 1.0.0"
    exit 1
fi
VERSION="$1"

echo "=========================================="
echo "🚀 yaoyao-cloud-backup 发布流程"
echo "=========================================="
echo "开发版: $DEV_DIR"
echo "发布版: $PUBLISH_DIR"
echo "版本: $VERSION"

# 步骤1: 从开发版同步到发布版
echo ""
echo "📂 步骤1: 同步开发版 → 发布版..."
rsync -av --exclude='publish.sh' \
    --exclude='__pycache__' --exclude='*.pyc' \
    --exclude='.git' \
    "$DEV_DIR/" "$PUBLISH_DIR/"
echo "✅ 同步完成"

# 步骤2: 更新版本号
echo ""
echo "📝 步骤2: 更新版本号..."
sed -i "s/^version:.*/version: $VERSION/" "$PUBLISH_DIR/SKILL.md"
echo "✅ 版本号更新为 $VERSION"

# 步骤3: 发布到 ClaWHub
echo ""
echo "📤 步骤3: 发布到 ClaWHub..."
clawhub publish . --slug yaoyao-cloud-backup --version "$VERSION"

# 步骤4: 隐藏
echo ""
echo "🙈 步骤4: 隐藏旧版本..."
clawhub hide --yes yaoyao-cloud-backup

echo ""
echo "=========================================="
echo "✅ 发布完成! 版本 $VERSION"
echo "=========================================="
