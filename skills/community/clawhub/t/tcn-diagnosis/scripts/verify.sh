#!/bin/bash
# TCM Diagnosis 验证脚本
# 检查三层架构完整性

echo "==================================="
echo "     中医诊疗助手 系统验证"
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
FILES="operations/AGENTS.md operations/HEARTBEAT.md operations/ROLE-TCM.md"
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
FILES="knowledge/symptoms/four-diagnostics.md knowledge/formulas/classic-formulas.md knowledge/patterns/differentiation-patterns.md knowledge/MEMORY.md"
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

# 知识库统计
echo ""
echo "📚 知识库统计:"
SYMPTOMS=$(grep -c "###" knowledge/symptoms/four-diagnostics.md 2>/dev/null || echo "0")
FORMULAS=$(grep -c "###" knowledge/formulas/classic-formulas.md 2>/dev/null || echo "0")
PATTERNS=$(grep -c "###" knowledge/patterns/differentiation-patterns.md 2>/dev/null || echo "0")
echo "   • 四诊症状: $SYMPTOMS+ 条目"
echo "   • 经典方剂: $FORMULAS+ 首"
echo "   • 辨证模式: $PATTERNS+ 证型"

# 安全声明检查
echo ""
echo "🔒 安全声明检查:"
if grep -q "安全" identity/SOUL.md && grep -q "仅供参考" identity/SOUL.md; then
    echo "   ✅ 身份层安全声明已配置"
else
    echo "   ❌ 安全声明缺失"
    ((ERRORS++))
fi

# 结果
echo ""
echo "==================================="
if [ $ERRORS -eq 0 ]; then
    echo "     ✅ 验证通过"
    echo "     系统完整性: 100%"
    echo ""
    echo "⚠️  安全提示："
    echo "   本系统所有建议仅供参考学习"
    echo "   不能替代专业医疗诊断和治疗"
else
    echo "     ❌ 发现 $ERRORS 个问题"
    echo "     请检查缺失的文件"
fi
echo "==================================="
echo ""

exit $ERRORS
