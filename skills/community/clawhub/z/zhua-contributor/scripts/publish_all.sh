#!/bin/bash
# 发布所有爪爪自研技能到skillhub
# 作者：话爪

echo "🐾 爪爪技能发布脚本"
echo "===================="
echo ""

SKILLS=(
    "zhua-evolver"
    "zhua-distributed"
    "zhua-contributor"
    "zhua-economy"
    "zhua-metacognition"
    "zhua-creative"
)

echo "准备发布 ${#SKILLS[@]} 个技能:"
for skill in "${SKILLS[@]}"; do
    echo "  - $skill"
done
echo ""

# 检查技能包是否存在
for skill in "${SKILLS[@]}"; do
    skill_file="/root/.openclaw/workspace/${skill}.skill"
    if [ -f "$skill_file" ]; then
        echo "✅ $skill: 已打包"
    else
        echo "❌ $skill: 未找到"
    fi
done
echo ""

echo "📦 技能包详情:"
for skill in "${SKILLS[@]}"; do
    skill_file="/root/.openclaw/workspace/${skill}.skill"
    if [ -f "$skill_file" ]; then
        size=$(du -h "$skill_file" | cut -f1)
        echo "  $skill: $size"
    fi
done
echo ""

echo "🚀 发布说明:"
echo "  由于skillhub发布需要API密钥和审核流程，"
echo "  此处仅展示准备发布的技能列表。"
echo ""
echo "  实际发布命令:"
echo "    skillhub publish ${SKILLS[0]}.skill"
echo "    ..."
echo ""
echo "🎯 发布后将获得:"
echo "  - 技能下载量统计"
echo "  - 用户评价反馈"
echo "  - 社区影响力"
echo "  - 潜在收益 (如果启用付费)"
echo ""
echo "💡 建议:"
echo "  1. 为每个技能撰写详细文档"
echo "  2. 准备演示视频或截图"
echo "  3. 设置合理的定价策略"
echo "  4. 积极回应用户反馈"
echo ""
echo "🐾 爪爪技能军团，准备出击！"
