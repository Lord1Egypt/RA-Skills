#!/bin/bash
# ClawHub 技能发布脚本
# 用法: bash publish.sh <skill-path> [--version <version>] [--changelog <message>] [--skip-validate] [--skip-slug-check]

set -e

SKILL_PATH=""
VERSION=""
CHANGELOG=""
SKIP_VALIDATE=false
SKIP_SLUG_CHECK=false

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --version)
            VERSION="$2"
            shift 2
            ;;
        --changelog)
            CHANGELOG="$2"
            shift 2
            ;;
        --skip-validate)
            SKIP_VALIDATE=true
            shift
            ;;
        --skip-slug-check)
            SKIP_SLUG_CHECK=true
            shift
            ;;
        *)
            if [ -z "$SKILL_PATH" ]; then
                SKILL_PATH="$1"
            fi
            shift
            ;;
    esac
done

if [ -z "$SKILL_PATH" ]; then
    echo "❌ 缺少技能路径"
    echo "用法: bash publish.sh <skill-path> [--version <version>] [--changelog <message>]"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SKILL_PATH" && pwd)"
SKILL_NAME=$(basename "$SKILL_DIR")

echo "🚀 发布技能: $SKILL_NAME"
echo "📁 路径: $SKILL_DIR"
echo ""

# 1. 技能名称占用检测
if [ "$SKIP_SLUG_CHECK" = false ]; then
    echo "🔍 检测技能名称..."
    python3 "$SCRIPT_DIR/check_slug.py" "$SKILL_NAME"
    if [ $? -eq 1 ]; then
        echo ""
        echo "❌ 名称已被占用，请修改技能名称后重试"
        exit 1
    fi
    echo ""
fi

# 2. 元数据验证
if [ "$SKIP_VALIDATE" = false ]; then
    echo "🔍 验证元数据..."
    python3 "$SCRIPT_DIR/validate_meta.py" "$SKILL_DIR"
    echo ""
fi

# 3. 读取当前版本
META_FILE="$SKILL_DIR/_meta.json"
if [ -f "$META_FILE" ]; then
    CURRENT_VERSION=$(python3 -c "import json; print(json.load(open('$META_FILE')).get('version', '1.0.0'))")
else
    CURRENT_VERSION="1.0.0"
    echo "{\"slug\": \"$SKILL_NAME\", \"version\": \"1.0.0\"}" > "$META_FILE"
fi

echo "📌 当前版本: $CURRENT_VERSION"

# 4. 计算新版本（如果未指定）
if [ -z "$VERSION" ]; then
    # 自动递增 patch 版本
    VERSION=$(python3 -c "
parts = '$CURRENT_VERSION'.split('.')
parts[-1] = str(int(parts[-1]) + 1)
print('.'.join(parts))
")
    echo "📌 建议版本: $VERSION (自动递增)"
fi

# 5. 更新 _meta.json
python3 -c "
import json
meta = {'slug': '$SKILL_NAME', 'version': '$VERSION'}
with open('$META_FILE', 'w') as f:
    json.dump(meta, f, indent=2)
"
echo "📝 已更新 _meta.json"

# 6. 发布
echo ""
echo "📤 发布到 ClawHub..."

if [ -z "$CHANGELOG" ]; then
    clawhub publish "$SKILL_DIR" --version "$VERSION"
else
    clawhub publish "$SKILL_DIR" --version "$VERSION" --changelog "$CHANGELOG"
fi

# 7. 记录发布历史
python3 "$SCRIPT_DIR/publish_history.py" record "$SKILL_NAME" "$VERSION" "${CHANGELOG:-发布}" "$SKILL_DIR"

echo ""
echo "✅ 发布完成: $SKILL_NAME@$VERSION"
