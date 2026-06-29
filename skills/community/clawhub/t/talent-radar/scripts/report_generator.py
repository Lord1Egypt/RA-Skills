#!/usr/bin/env python3
"""
报告生成模块
根据匹配结果生成格式化的分析报告
"""

from typing import Dict, List
from datetime import datetime


def generate_hr_report(match_result: Dict, resume: Dict, jd: Dict) -> str:
    """
    生成HR报告
    
    Args:
        match_result: 匹配结果
        resume: 简历数据
        jd: 岗位数据
        
    Returns:
        格式化的HR报告（Markdown格式）
    """
    report = []
    
    # 标题
    report.append("# 人才匹配分析报告")
    report.append("")
    
    # 候选人信息
    report.append("## 候选人信息")
    report.append(f"- **姓名**：{resume.get('name', '未知')}")
    report.append(f"- **应聘岗位**：{jd.get('title', '未知')}")
    report.append(f"- **分析日期**：{datetime.now().strftime('%Y-%m-%d')}")
    if resume.get('years_of_experience'):
        report.append(f"- **工作年限**：{resume['years_of_experience']}年")
    if resume.get('current_position'):
        report.append(f"- **当前职位**：{resume['current_position']}")
    report.append("")
    
    # 匹配度总览
    report.append("## 匹配度总览")
    total_score = match_result.get('total_score', 0)
    level = match_result.get('level', '未知')
    
    # 分数显示（带颜色标记）
    if total_score >= 80:
        score_emoji = "🟢"
    elif total_score >= 60:
        score_emoji = "🟡"
    else:
        score_emoji = "🔴"
    
    report.append(f"- **总匹配度**：{score_emoji} {total_score}分（{level}）")
    
    # 核心优势
    strengths = match_result.get('overall_strengths', [])
    if strengths:
        report.append(f"- **核心优势**：{'、'.join(strengths[:5])}")
    
    # 主要短板
    weaknesses = match_result.get('overall_weaknesses', [])
    if weaknesses:
        report.append(f"- **主要短板**：{'、'.join(weaknesses[:3])}")
    report.append("")
    
    # 分项分析
    report.append("## 分项分析")
    report.append("")
    
    dimensions = match_result.get('dimensions', [])
    for dim in dimensions:
        dim_name = dim.get('name', '')
        dim_score = dim.get('score', 0)
        
        # 分数标记
        if dim_score >= 80:
            dim_emoji = "✅"
        elif dim_score >= 60:
            dim_emoji = "⚠️"
        else:
            dim_emoji = "❌"
        
        report.append(f"### {dim_emoji} {dim_name}（{dim_score}分）")
        
        # 详细信息
        details = dim.get('details', [])
        for detail in details:
            report.append(f"- {detail}")
        
        # 优势
        dim_strengths = dim.get('strengths', [])
        if dim_strengths:
            report.append("- **优势**：" + "、".join(dim_strengths))
        
        # 劣势
        dim_weaknesses = dim.get('weaknesses', [])
        if dim_weaknesses:
            report.append("- **不足**：" + "、".join(dim_weaknesses))
        
        report.append("")
    
    # 推荐意见
    report.append("## 推荐意见")
    recommendation = match_result.get('recommendation', '')
    report.append(recommendation)
    report.append("")
    
    # 风险提示
    report.append("## 风险提示")
    if total_score < 70:
        report.append("- ⚠️ 候选人与岗位匹配度一般，建议重点关注短板领域")
    if weaknesses:
        report.append(f"- ⚠️ 需要关注：{'、'.join(weaknesses[:2])}")
    if not strengths:
        report.append("- ⚠️ 候选人优势不明显，建议深入评估")
    report.append("")
    
    # 下一步行动
    report.append("## 下一步行动建议")
    if total_score >= 80:
        report.append("1. ✅ 建议安排技术面试")
        report.append("2. ✅ 重点考察候选人的实际项目经验")
        report.append("3. ✅ 了解候选人的薪资期望和到岗时间")
    elif total_score >= 60:
        report.append("1. 🔄 建议先进行电话初筛")
        report.append("2. 🔄 重点关注候选人的短板领域")
        report.append("3. 🔄 评估候选人是否愿意接受培训")
    else:
        report.append("1. ❌ 暂不建议安排面试")
        report.append("2. 📝 可将候选人加入人才库，后续有合适岗位再联系")
    
    report.append("")
    report.append("---")
    report.append("*本报告由人才雷达智能匹配系统生成，仅供参考*")
    
    return "\n".join(report)


def generate_jobseeker_report(match_result: Dict, resume: Dict, jd: Dict) -> str:
    """
    生成求职者报告
    
    Args:
        match_result: 匹配结果
        resume: 简历数据
        jd: 岗位数据
        
    Returns:
        格式化的求职者报告（Markdown格式）
    """
    report = []
    
    # 标题
    report.append("# 求职诊断报告")
    report.append("")
    
    # 目标岗位分析
    report.append("## 目标岗位分析")
    report.append(f"- **岗位名称**：{jd.get('title', '未知')}")
    if jd.get('company_name'):
        report.append(f"- **目标公司**：{jd['company_name']}")
    if jd.get('salary_range'):
        report.append(f"- **薪资范围**：{jd['salary_range']}")
    
    # 核心要求
    required_skills = jd.get('required_skills', [])
    if required_skills:
        skill_names = [s.get('name', '') if isinstance(s, dict) else str(s) 
                      for s in required_skills]
        report.append(f"- **核心要求**：{'、'.join(skill_names[:5])}")
    
    report.append("")
    
    # 你的竞争力评估
    report.append("## 你的竞争力评估")
    total_score = match_result.get('total_score', 0)
    level = match_result.get('level', '未知')
    
    # 分数显示
    if total_score >= 80:
        score_emoji = "🟢"
        score_desc = "竞争力强"
    elif total_score >= 60:
        score_emoji = "🟡"
        score_desc = "有竞争力"
    else:
        score_emoji = "🔴"
        score_desc = "需要提升"
    
    report.append(f"- **总匹配度**：{score_emoji} {total_score}分（{level}）")
    report.append(f"- **竞争力评估**：{score_desc}")
    
    # 核心优势
    strengths = match_result.get('overall_strengths', [])
    if strengths:
        report.append(f"- **你的优势**：{'、'.join(strengths[:5])}")
    
    # 待提升领域
    weaknesses = match_result.get('overall_weaknesses', [])
    if weaknesses:
        report.append(f"- **待提升领域**：{'、'.join(weaknesses[:3])}")
    report.append("")
    
    # 差距诊断
    report.append("## 差距诊断")
    report.append("")
    
    dimensions = match_result.get('dimensions', [])
    for dim in dimensions:
        dim_name = dim.get('name', '')
        dim_score = dim.get('score', 0)
        dim_weaknesses = dim.get('weaknesses', [])
        
        if dim_score < 80:
            report.append(f"### {dim_name}（{dim_score}分）")
            if dim_weaknesses:
                for weakness in dim_weaknesses:
                    report.append(f"- ❌ {weakness}")
            
            # 给出具体建议
            if dim_name == "技能匹配":
                report.append("- 💡 **建议**：")
                report.append("  - 学习缺失的核心技能")
                report.append("  - 通过实际项目巩固技能")
                report.append("  - 考取相关技能认证")
            elif dim_name == "经验匹配":
                report.append("- 💡 **建议**：")
                report.append("  - 积累相关行业经验")
                report.append("  - 争取更多项目主导机会")
                report.append("  - 参与开源项目积累经验")
            elif dim_name == "教育匹配":
                report.append("- 💡 **建议**：")
                report.append("  - 考虑在职提升学历")
                report.append("  - 参加专业培训课程")
                report.append("  - 考取行业认可的证书")
            
            report.append("")
    
    # 简历优化建议
    report.append("## 简历优化建议")
    report.append("")
    
    # 根据匹配结果给出具体建议
    if total_score < 70:
        report.append("### 内容优化")
        report.append("1. 突出与岗位相关的核心技能")
        report.append("2. 增加量化的成果描述（如：提升效率30%）")
        report.append("3. 补充与目标岗位相关的项目经验")
        report.append("")
        report.append("### 结构优化")
        report.append("1. 将最相关的内容放在前面")
        report.append("2. 使用STAR法则描述工作经历")
        report.append("3. 技能部分按熟练程度排序")
        report.append("")
        report.append("### 表达优化")
        report.append("1. 使用岗位JD中的关键词")
        report.append("2. 避免过于笼统的描述")
        report.append("3. 突出个人贡献和价值")
    else:
        report.append("1. ✅ 简历与岗位匹配度较高")
        report.append("2. 💡 可以进一步优化成果描述的量化指标")
        report.append("3. 💡 建议突出最亮眼的2-3个项目经验")
    
    report.append("")
    
    # 学习路径推荐
    report.append("## 学习路径推荐")
    report.append("")
    
    # 根据差距推荐学习内容
    skill_gaps = []
    for dim in dimensions:
        if dim.get('name') == '技能匹配':
            skill_gaps = dim.get('weaknesses', [])
            break
    
    if skill_gaps:
        report.append("### 短期（1-3个月）")
        for gap in skill_gaps[:3]:
            skill_name = gap.replace('缺少', '').replace('技能', '')
            report.append(f"- 学习{skill_name}基础知识")
            report.append(f"- 完成{skill_name}相关的小项目")
        report.append("")
        
        report.append("### 中期（3-6个月）")
        report.append("- 深入学习核心技能")
        report.append("- 参与实际项目积累经验")
        report.append("- 考取相关技能认证")
        report.append("")
        
        report.append("### 长期（6-12个月）")
        report.append("- 成为领域专家")
        report.append("- 建立个人技术品牌")
        report.append("- 积累管理经验")
    else:
        report.append("### 短期（1-3个月）")
        report.append("- 巩固现有技能")
        report.append("- 优化简历和面试准备")
        report.append("")
        report.append("### 中期（3-6个月）")
        report.append("- 深入学习目标岗位的核心技术")
        report.append("- 积累更多项目经验")
        report.append("")
        report.append("### 长期（6-12个月）")
        report.append("- 向高级职位发展")
        report.append("- 建立行业人脉")
    
    report.append("")
    
    # 面试准备建议
    report.append("## 面试准备建议")
    report.append("")
    
    if total_score >= 70:
        report.append("### 技术面试准备")
        report.append("1. 复习核心技能的原理和实践")
        report.append("2. 准备2-3个有深度的项目案例")
        report.append("3. 练习手写代码和系统设计")
        report.append("")
        report.append("### HR面试准备")
        report.append("1. 准备自我介绍（1-2分钟）")
        report.append("2. 思考职业规划和发展方向")
        report.append("3. 了解公司文化和价值观")
    else:
        report.append("### 当前阶段重点")
        report.append("1. 先提升技能匹配度")
        report.append("2. 积累相关项目经验")
        report.append("3. 优化简历后再投递")
    
    report.append("")
    report.append("---")
    report.append("*本报告由人才雷达智能匹配系统生成，祝你求职顺利！*")
    
    return "\n".join(report)


def generate_gap_analysis_report(match_result: Dict, resume: Dict, jd: Dict) -> str:
    """
    生成差距分析报告
    
    Args:
        match_result: 匹配结果
        resume: 简历数据
        jd: 岗位数据
        
    Returns:
        格式化的差距分析报告
    """
    report = []
    
    report.append("# 差距分析报告")
    report.append("")
    
    # 总体差距
    total_score = match_result.get('total_score', 0)
    gap = 100 - total_score
    
    report.append("## 总体差距")
    report.append(f"- **当前匹配度**：{total_score}分")
    report.append(f"- **与完美匹配的差距**：{gap}分")
    report.append("")
    
    # 各维度差距
    report.append("## 各维度差距分析")
    report.append("")
    
    report.append("| 维度 | 当前分数 | 目标分数 | 差距 | 优先级 |")
    report.append("|------|---------|---------|------|--------|")
    
    dimensions = match_result.get('dimensions', [])
    for dim in dimensions:
        dim_name = dim.get('name', '')
        dim_score = dim.get('score', 0)
        dim_gap = 100 - dim_score
        
        # 根据权重确定优先级
        weight = dim.get('weight', 0)
        if weight >= 0.3:
            priority = "🔴 高"
        elif weight >= 0.2:
            priority = "🟡 中"
        else:
            priority = "🟢 低"
        
        report.append(f"| {dim_name} | {dim_score} | 100 | {dim_gap} | {priority} |")
    
    report.append("")
    
    # 具体差距清单
    report.append("## 具体差距清单")
    report.append("")
    
    for dim in dimensions:
        dim_name = dim.get('name', '')
        dim_weaknesses = dim.get('weaknesses', [])
        
        if dim_weaknesses:
            report.append(f"### {dim_name}")
            for i, weakness in enumerate(dim_weaknesses, 1):
                report.append(f"{i}. {weakness}")
            report.append("")
    
    # 提升路径
    report.append("## 提升路径")
    report.append("")
    
    # 按优先级排序
    sorted_dims = sorted(dimensions, key=lambda d: d.get('weight', 0), reverse=True)
    
    for i, dim in enumerate(sorted_dims, 1):
        dim_name = dim.get('name', '')
        dim_score = dim.get('score', 0)
        
        if dim_score < 80:
            report.append(f"### 阶段{i}：提升{dim_name}")
            report.append(f"- **当前分数**：{dim_score}分")
            report.append(f"- **目标分数**：80分以上")
            report.append(f"- **预计时间**：{_estimate_time(dim_score)}")
            report.append(f"- **具体行动**：")
            
            if dim_name == "技能匹配":
                report.append("  1. 识别缺失的核心技能")
                report.append("  2. 制定学习计划（每天2-3小时）")
                report.append("  3. 通过在线课程学习理论")
                report.append("  4. 通过实际项目巩固技能")
            elif dim_name == "经验匹配":
                report.append("  1. 争取更多相关项目机会")
                report.append("  2. 参与开源项目积累经验")
                report.append("  3. 做个人项目展示能力")
            elif dim_name == "教育匹配":
                report.append("  1. 考虑在职提升学历")
                report.append("  2. 参加专业培训")
                report.append("  3. 考取行业认证")
            
            report.append("")
    
    report.append("---")
    report.append("*本报告由人才雷达智能匹配系统生成*")
    
    return "\n".join(report)


def _estimate_time(current_score: int) -> str:
    """估算提升时间"""
    gap = 100 - current_score
    if gap <= 10:
        return "1-2周"
    elif gap <= 20:
        return "1-2个月"
    elif gap <= 30:
        return "3-6个月"
    else:
        return "6-12个月"


# 测试代码
if __name__ == "__main__":
    # 模拟数据
    match_result = {
        'total_score': 75.5,
        'level': '良好匹配',
        'dimensions': [
            {
                'name': '技能匹配',
                'score': 80,
                'weight': 0.35,
                'weighted_score': 28,
                'details': ['必须技能匹配率：3/4'],
                'strengths': ['掌握Java', '掌握Spring'],
                'weaknesses': ['缺少微服务经验']
            },
            {
                'name': '经验匹配',
                'score': 70,
                'weight': 0.25,
                'weighted_score': 17.5,
                'details': ['年限匹配：5年/5年'],
                'strengths': ['工作年限达标'],
                'weaknesses': ['行业经验不完全匹配']
            }
        ],
        'overall_strengths': ['掌握Java', '掌握Spring', '工作年限达标'],
        'overall_weaknesses': ['缺少微服务经验', '行业经验不完全匹配'],
        'recommendation': '可以考虑。候选人整体匹配度良好。'
    }
    
    resume = {
        'name': '张三',
        'years_of_experience': 5,
        'current_position': 'Java开发工程师'
    }
    
    jd = {
        'title': '高级Java开发工程师',
        'company_name': '某科技公司',
        'salary_range': '20-30K'
    }
    
    # 生成报告
    hr_report = generate_hr_report(match_result, resume, jd)
    print(hr_report)
    
    print("\n" + "="*50 + "\n")
    
    jobseeker_report = generate_jobseeker_report(match_result, resume, jd)
    print(jobseeker_report)
