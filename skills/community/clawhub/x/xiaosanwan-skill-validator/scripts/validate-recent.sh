#!/bin/bash
# 验证最近安装的 Skill
# 用法: validate-recent.sh

SKILL_DIR="/root/.openclaw/workspace/skills"

# 获取最近修改的 Skill
echo "🔍 查找最近安装的技能..."
echo ""

# 按修改时间排序，取最近 3 个
recent_skills=$(ls -lt "$SKILL_DIR" 2>/dev/null | grep "^d" | head -4 | tail -3 | awk '{print $NF}')

if [ -z "$recent_skills" ]; then
    echo "未找到已安装的技能"
    exit 1
fi

echo "最近安装的技能:"
echo "$recent_skills"
echo ""

# 验证每个技能
for skill in $recent_skills; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    bash ~/.openclaw/workspace/skills/skill-validator/scripts/validate.sh "$skill"
done
