#!/bin/bash
# 健康检查：验证文件结构完整性

TEMPLATE_DIR="$(dirname "$0")/.."
ERRORS=0

echo "🔍 开始健康检查..."
echo ""

# 检查必需文件
required_files=(
    "IDENTITY.md"
    "AGENTS.md"
    "README.md"
    "memory/hot.md"
    "logs/index.md"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$TEMPLATE_DIR/$file" ]; then
        echo "❌ 缺少文件: $file"
        ERRORS=$((ERRORS + 1))
    else
        echo "✅ $file"
    fi
done

echo ""

# 检查 hot.md 行数
hot_lines=$(wc -l < "$TEMPLATE_DIR/memory/hot.md" | tr -d ' ')
if [ "$hot_lines" -gt 100 ]; then
    echo "⚠️  memory/hot.md 超过 100 行 (当前 $hot_lines 行)"
    echo "   建议运行: ./scripts/compress_hot.sh"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ memory/hot.md 行数正常 ($hot_lines/100)"
fi

echo ""

# 检查目录结构
required_dirs=(
    "memory/projects"
    "memory/domains"
    "memory/archive"
    "logs"
    "tasks/active"
    "tasks/archive"
    "scripts"
)

for dir in "${required_dirs[@]}"; do
    if [ ! -d "$TEMPLATE_DIR/$dir" ]; then
        echo "❌ 缺少目录: $dir"
        ERRORS=$((ERRORS + 1))
    else
        echo "✅ $dir"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $ERRORS -eq 0 ]; then
    echo "✅ 健康检查通过"
    exit 0
else
    echo "❌ 发现 $ERRORS 个问题"
    exit 1
fi
