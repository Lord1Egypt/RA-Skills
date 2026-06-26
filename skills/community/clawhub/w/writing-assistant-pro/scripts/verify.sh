#!/bin/bash
# Writing Assistant 验证脚本
# 检查三层架构完整性

echo "==================================="
echo "     Writing Assistant 系统验证"
echo "==================================="
echo ""

WORK_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORK_DIR"

ERRORS=0

# 第一层检查
echo "🔍 第一层：身份层"
FILES="identity/SOUL.md identity/IDENTITY.md identity/USER.md"
for FILE in $FILES; do
    if [ -f "$FILE" ]; then
        echo "   ✅ $FILE"
    else
        echo "   ❌ $FILE 缺失"
        ((ERRORS++))
    fi
done

# 第二层检查
echo ""
echo "🔍 第二层：操作层"
FILES="operations/AGENTS.md operations/HEARTBEAT.md operations/ROLE-CHIEF-WRITER.md"
for FILE in $FILES; do
    if [ -f "$FILE" ]; then
        echo "   ✅ $FILE"
    else
        echo "   ❌ $FILE 缺失"
        ((ERRORS++))
    fi
done

# 第三层检查
echo ""
echo "🔍 第三层：知识层"
FILES="knowledge/MEMORY.md knowledge/shared-context/state.md"
for FILE in $FILES; do
    if [ -f "$FILE" ]; then
        echo "   ✅ $FILE"
    else
        echo "   ❌ $FILE 缺失"
        ((ERRORS++))
    fi
done

# 其他文件检查
echo ""
echo "🔍 其他文件"
FILES="README.md scripts/startup.sh"
for FILE in $FILES; do
    if [ -f "$FILE" ]; then
        echo "   ✅ $FILE"
    else
        echo "   ❌ $FILE 缺失"
        ((ERRORS++))
    fi
done

# 目录检查
echo ""
echo "🔍 目录结构"
DIRS="logs"
for DIR in $DIRS; do
    if [ -d "$DIR" ]; then
        echo "   ✅ $DIR/"
    else
        echo "   ❌ $DIR/ 缺失"
        ((ERRORS++))
    fi
done

# 结果
echo ""
echo "==================================="
if [ $ERRORS -eq 0 ]; then
    echo "     ✅ 验证通过"
    echo "     系统完整性: 100%"
else
    echo "     ❌ 发现 $ERRORS 个问题"
    echo "     请检查缺失的文件"
fi
echo "==================================="
echo ""

exit $ERRORS
