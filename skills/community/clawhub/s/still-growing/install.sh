#!/bin/bash
# Still Growing / 第二代父母 安装脚本
# 交互式安装：先预览，再确认

set -e

echo "=========================================="
echo "Still Growing / 第二代父母"
echo "困在自己没走完的成长里，把孩子当成答案的一代人"
echo "=========================================="
echo ""

# 检测 skills 目录
if [ -d "$HOME/.hermes/skills" ]; then
    SKILLS_DIR="$HOME/.hermes/skills"
elif [ -d "$HOME/.claude/skills" ]; then
    SKILLS_DIR="$HOME/.claude/skills"
elif [ -d "$HOME/.cache/hermes/skills" ]; then
    SKILLS_DIR="$HOME/.cache/hermes/skills"
else
    echo "❌ 未找到 skills 目录"
    exit 1
fi

TARGET_DIR="$SKILLS_DIR/mark-still-growing"

# 检查是否已安装
if [ -d "$TARGET_DIR" ]; then
    echo "⚠️  已安装现有版本"
    echo "   路径: $TARGET_DIR"
    read -p "是否更新? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "取消安装"
        exit 0
    fi
fi

echo "📦 安装到: $TARGET_DIR"

# 创建目录
mkdir -p "$TARGET_DIR"

# 复制文件（不覆盖现有文件）
for f in SKILL.md README.md LICENSE.md VERSION_RULE.md; do
    if [ -f "$TARGET_DIR/$f" ]; then
        echo "   保留现有: $f"
    else
        cp "$f" "$TARGET_DIR/"
        echo "   安装: $f"
    fi
done

echo ""
echo "✅ 安装完成!"
echo "   路径: $TARGET_DIR"
echo ""
echo "使用方式:"
echo "   当你提到以下话题时，AI 会自动加载此技能："
echo "   - 第二代父母、父母成长、亲子关系"
echo "   - 孩子问题行为、教育焦虑、情绪失控"
echo "   - 父母倦怠、原生家庭、童年创伤"
echo ""
