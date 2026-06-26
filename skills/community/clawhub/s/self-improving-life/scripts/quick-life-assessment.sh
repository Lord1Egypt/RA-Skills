#!/bin/bash
# 快速生活评估脚本
# 帮助用户快速评估生活满意度

echo "🎯 生活轮快速评估"
echo "================="
echo ""

# 健康领域
echo "1. 健康与 wellness (1-10分)"
read -p "  整体满意度: " health_score
read -p "  睡眠质量 (1-10): " sleep_score
read -p "  运动频率 (次/周): " exercise_freq

# 关系领域
echo ""
echo "2. 关系与社交 (1-10分)"
read -p "  亲密关系质量: " relationship_score
read -p "  朋友社交频率: " social_freq
read -p "  家庭联系质量: " family_score

# 工作领域
echo ""
echo "3. 工作与职业 (1-10分)"
read -p "  工作投入度: " work_engagement
read -p "  职业成长感: " career_growth
read -p "  工作生活平衡: " work_balance

# 生成评估报告
echo ""
echo "📊 生活评估结果"
echo "=============="

# 计算各领域平均分
health_avg=$(echo "scale=1; ($health_score + $sleep_score) / 2" | bc)
relationship_avg=$(echo "scale=1; ($relationship_score + $social_freq + $family_score) / 3" | bc)
work_avg=$(echo "scale=1; ($work_engagement + $career_growth + $work_balance) / 3" | bc)

echo ""
echo "🏥 健康: $health_avg/10"
echo "  • 整体: $health_score/10"
echo "  • 睡眠: $sleep_score/10"
echo "  • 运动: $exercise_freq 次/周"

echo ""
echo "🤝 关系: $relationship_avg/10"
echo "  • 亲密关系: $relationship_score/10"
echo "  • 社交频率: $social_freq/10"
echo "  • 家庭联系: $family_score/10"

echo ""
echo "💼 工作: $work_avg/10"
echo "  • 投入度: $work_engagement/10"
echo "  • 成长感: $career_growth/10"
echo "  • 平衡度: $work_balance/10"

# 识别最低分领域
lowest_domain=""
lowest_score=10

if (( $(echo "$health_avg < $lowest_score" | bc -l) )); then
    lowest_score=$health_avg
    lowest_domain="健康"
fi

if (( $(echo "$relationship_avg < $lowest_score" | bc -l) )); then
    lowest_score=$relationship_avg
    lowest_domain="关系"
fi

if (( $(echo "$work_avg < $lowest_score" | bc -l) )); then
    lowest_score=$work_avg
    lowest_domain="工作"
fi

echo ""
echo "🎯 改进建议"
echo "-----------"
echo "最需要关注的领域: $lowest_domain ($lowest_score/10)"

case $lowest_domain in
    "健康")
        echo "建议行动:"
        echo "1. 确保7-8小时睡眠"
        echo "2. 每周运动3-5次"
        echo "3. 均衡饮食，充足饮水"
        ;;
    "关系")
        echo "建议行动:"
        echo "1. 安排定期社交活动"
        echo "2. 主动联系朋友家人"
        echo "3. 参加兴趣小组或社区"
        ;;
    "工作")
        echo "建议行动:"
        echo "1. 设定明确工作边界"
        echo "2. 规划职业发展路径"
        echo "3. 平衡工作与个人时间"
        ;;
esac

# 保存评估结果
timestamp=$(date +%Y%m%d_%H%M%S)
cat > "life-assessment-$timestamp.md" << EOF
# 生活评估报告
**评估时间**: $(date)

## 领域评分
- 健康: $health_avg/10
  - 整体满意度: $health_score/10
  - 睡眠质量: $sleep_score/10
  - 运动频率: $exercise_freq 次/周
- 关系: $relationship_avg/10
  - 亲密关系: $relationship_score/10
  - 社交频率: $social_freq/10
  - 家庭联系: $family_score/10
- 工作: $work_avg/10
  - 投入度: $work_engagement/10
  - 成长感: $career_growth/10
  - 平衡度: $work_balance/10

## 改进重点
最需要关注的领域: $lowest_domain ($lowest_score/10)

## 建议行动
$(case $lowest_domain in
    "健康") echo "1. 确保7-8小时睡眠\n2. 每周运动3-5次\n3. 均衡饮食，充足饮水" ;;
    "关系") echo "1. 安排定期社交活动\n2. 主动联系朋友家人\n3. 参加兴趣小组或社区" ;;
    "工作") echo "1. 设定明确工作边界\n2. 规划职业发展路径\n3. 平衡工作与个人时间" ;;
esac)

## 后续步骤
1. 使用完整的生活轮模板进行详细评估
2. 设定具体改进目标
3. 每月重新评估进展
4. 调整策略以获得更好平衡
EOF

echo ""
echo "✅ 评估报告已保存到: life-assessment-$timestamp.md"
echo "📚 使用 self-improving-life skill 获取更全面的生活优化指导。"