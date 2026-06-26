#!/bin/bash
# =============================================================================
# 发布脚本 - 从开发版同步到发布版，然后发布
# =============================================================================
# 版本结构：
# - yaoyao-memory-v2   = 开发版
# - yaoyao-memory-homo = 使用版（发布专用）
# =============================================================================

set -e

WORKSPACE="$HOME/.openclaw/workspace/skills"
DEV_DIR="$WORKSPACE/yaoyao-memory-v2"
PUBLISH_DIR="$WORKSPACE/yaoyao-memory-homo"

if [ -z "$1" ]; then
    echo "用法: ./publish.sh <版本号>"
    echo "例如: ./publish.sh 3.9.0"
    exit 1
fi
VERSION="$1"

echo "=========================================="
echo "🚀 yaoyao-memory 发布流程"
echo "=========================================="
echo "开发版: $DEV_DIR"
echo "发布版: $PUBLISH_DIR"
echo "版本: $VERSION"

# 步骤1: 从开发版同步到发布版
echo ""
echo "📂 步骤1: 同步开发版 → 发布版..."
rsync -av --exclude='publish.sh' --exclude='publish-clean.sh' \
    --exclude='__pycache__' --exclude='*.pyc' \
    --exclude='.git' --exclude='.core_installed' \
    --exclude='.installed_modules.json' \
    --exclude='.migration_state.json' \
    "$DEV_DIR/" "$PUBLISH_DIR/"
echo "✅ 同步完成"

# 步骤1b: 验证关键文件
echo ""
echo "📋 步骤1b: 验证关键文件..."
for f in MODULES.json install_modules.py migrate.py WELCOME.py BOOTSTRAP.md; do
    if [ ! -f "$PUBLISH_DIR/$f" ]; then
        echo "⚠️  缺少关键文件: $f"
    fi
done
echo "✅ 关键文件验证完成"

# 步骤2: 在发布版执行清理
echo ""
echo "🧹 步骤2: 执行隐私清理..."
cd "$PUBLISH_DIR"
./publish-clean.sh

# 步骤3: 验证敏感文件
echo ""
echo "🔍 步骤3: 验证清理结果..."
for f in embeddings_cache.json persona_update.json user_config.json samba.json llm_config.json; do
    if [ -f "config/$f" ]; then
        echo "❌ 发现敏感文件: config/$f"
        exit 1
    fi
done
echo "✅ 验证通过"

# 步骤3b: VirusTotal 预检
echo ""
echo "🔍 步骤3b: VirusTotal 预检..."
if [ -f "scripts/virustotal_scan.py" ]; then
    result=$(cd "$PUBLISH_DIR" && python3 scripts/virustotal_scan.py 2>&1)
    echo "$result"
    if echo "$result" | grep -q "⚠️  发现问题"; then
        echo ""
        echo "❌ 预检失败，请修复问题后重新发布"
        exit 1
    fi
    echo "✅ 预检通过"
else
    echo "⚠️  预检脚本不存在，跳过"
fi

# 步骤4: 更新版本号
echo ""
echo "📝 步骤4: 更新版本号..."
sed -i "s/^version:.*/version: $VERSION/" "$PUBLISH_DIR/SKILL.md"
sed -i "s/\"version\": \"[^\"]*\"/\"version\": \"$VERSION\"/" "$PUBLISH_DIR/_meta.json"
echo "✅ 版本号更新为 $VERSION"

# 步骤5: 发布到 ClaWHub
echo ""
echo "📤 步骤5: 发布到 ClaWHub..."
clawhub publish . --slug yaoyao-memory-v2 --version "$VERSION"

# 步骤6: 隐藏
echo ""
echo "🙈 步骤6: 隐藏旧版本..."
clawhub hide --yes yaoyao-memory-v2

# 步骤7: 重启 API server
echo ""
echo "🔄 步骤7: 重启 API server..."
pkill -f "api_server.py" 2>/dev/null || true
sleep 2
cd "$PUBLISH_DIR"
nohup python3 scripts/api_server.py > /tmp/yaoyao-api.log 2>&1 &
sleep 2
if pgrep -f "api_server.py" > /dev/null; then
    echo "✅ API server 已切换到发布版"
else
    echo "⚠️  API server 启动可能失败，请检查日志"
fi

echo ""
echo "=========================================="
echo "✅ 发布完成! 版本 $VERSION"
echo "=========================================="
