#!/bin/bash
# Skill Combo Recommender 安装脚本

set -e

echo "🚀 开始安装 Skill Combo Recommender..."

# 检查 Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    echo "请先安装 Python 3: brew install python3"
    exit 1
fi

# 检查 OpenClaw 技能目录
OPENCLAW_SKILLS_DIR="${OPENCLAW_SKILLS_DIR:-$HOME/.openclaw/skills}"
echo "📁 技能将安装到: $OPENCLAW_SKILLS_DIR"

# 创建目录（如果不存在）
mkdir -p "$OPENCLAW_SKILLS_DIR"

# 复制技能文件
echo "📦 复制技能文件..."
SKILL_NAME="skill-combo-recommender"
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -d "$OPENCLAW_SKILLS_DIR/$SKILL_NAME" ]; then
    echo "⚠️  技能已存在，将覆盖..."
    rm -rf "$OPENCLAW_SKILLS_DIR/$SKILL_NAME"
fi

cp -r "$SKILL_DIR" "$OPENCLAW_SKILLS_DIR/$SKILL_NAME"
echo "✅ 技能文件已复制"

# 设置执行权限
chmod +x "$OPENCLAW_SKILLS_DIR/$SKILL_NAME/source/skill_combo_recommender.py"

# 创建符号链接（可选）
if [ -d "$HOME/.local/bin" ] && [ -w "$HOME/.local/bin" ]; then
    ln -sf "$OPENCLAW_SKILLS_DIR/$SKILL_NAME/source/skill_combo_recommender.py" "$HOME/.local/bin/skill-combo-recommender"
    echo "✅ 已创建符号链接: $HOME/.local/bin/skill-combo-recommender"
fi

# 完成
echo ""
echo "✅ 安装完成！"
echo ""
echo "📖 使用方法:"
echo "  skill-combo-recommender --task \"任务描述\""
echo "  skill-combo-recommender --list-skills"
echo "  skill-combo-recommender --list-workflows"
echo ""
echo "📚 查看完整文档: $OPENCLAW_SKILLS_DIR/$SKILL_NAME/README.md"
