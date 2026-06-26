#!/bin/bash
# 完整性校验脚本
# 验证所有技能条目在 SKILL.md 中注册且对应文件夹存在

echo "================================================"
echo "  外科学 Surgery-PMPH-10edition 完整性校验"
echo "================================================"
echo ""

# 检查 SKILL.md 是否存在
if [ ! -f "SKILL.md" ]; then
    echo "❌ SKILL.md 不存在!"
    exit 1
fi
echo "✅ SKILL.md 存在"

# 检查 README.md
if [ ! -f "README.md" ]; then
    echo "⚠️  README.md 不存在"
else
    echo "✅ README.md 存在"
fi

# 检查目录结构
for dir in scripts config tests; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/ 目录存在"
    else
        echo "⚠️  $dir/ 目录不存在"
    fi
done

echo ""
echo "--- 技能条目验证 ---"

# 从 SKILL.md 提取所有 name 字段和 ref 路径
MISSING=0
TOTAL=0

echo "正在逐项验证 240 项技能..."
echo ""

while IFS= read -r ref; do
    TOTAL=$((TOTAL + 1))
    if [ ! -f "$ref" ]; then
        echo "❌ 缺失文件: $ref"
        MISSING=$((MISSING + 1))
    fi
done < <(grep "^  ref:" SKILL.md | sed 's/^  ref: //')

echo ""
echo "--- 结果 ---"
echo "✅ 总计: $TOTAL 项技能"
if [ "$MISSING" -eq 0 ]; then
    echo "✅ 全部验证通过，无缺失文件"
else
    echo "❌ 缺失: $MISSING 个文件"
fi

echo ""
echo "================================================"
echo "校验完成"
echo "================================================"
