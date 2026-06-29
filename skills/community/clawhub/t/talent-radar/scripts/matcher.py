#!/usr/bin/env python3
"""
匹配算法模块
实现简历与岗位的多维度智能匹配
"""

import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class MatchLevel(Enum):
    """匹配等级"""
    PERFECT = "完美匹配"      # 90-100
    HIGH = "高度匹配"        # 80-89
    GOOD = "良好匹配"        # 70-79
    BASIC = "基本匹配"       # 60-69
    INSUFFICIENT = "匹配不足"  # <60


@dataclass
class DimensionScore:
    """维度得分"""
    name: str
    score: float
    weight: float
    weighted_score: float
    details: List[str]
    strengths: List[str]
    weaknesses: List[str]


@dataclass
class MatchResult:
    """匹配结果"""
    total_score: float
    level: MatchLevel
    dimensions: List[DimensionScore]          # 计入总分的维度
    culture_reference: DimensionScore         # 文化匹配（参考，不计入总分）
    overall_strengths: List[str]
    overall_weaknesses: List[str]
    recommendation: str
    match_summary: str


class TalentMatcher:
    """人才匹配器"""
    
    def __init__(self, weights: Dict[str, float] = None):
        """
        初始化匹配器

        Args:
            weights: 各维度权重，如果不提供则使用默认权重。
                     文化匹配不在权重表内，始终作为参考维度单独输出。
        """
        self.default_weights = {
            'skill': 0.40,       # 技能匹配
            'experience': 0.30,  # 经验匹配
            'education': 0.18,   # 教育匹配（仅学历层次+专业方向，不含院校名称）
            'potential': 0.12    # 发展潜力
        }
        self.weights = weights or self.default_weights
    
    def match(self, resume: Dict, jd: Dict) -> MatchResult:
        """
        执行匹配分析
        
        Args:
            resume: 简历数据（字典格式）
            jd: 岗位描述数据（字典格式）
            
        Returns:
            MatchResult对象，包含匹配结果
        """
        # 计算各计分维度（不含文化匹配）
        dimensions = []

        skill_score = self._calculate_skill_match(resume, jd)
        dimensions.append(skill_score)

        experience_score = self._calculate_experience_match(resume, jd)
        dimensions.append(experience_score)

        education_score = self._calculate_education_match(resume, jd)
        dimensions.append(education_score)

        potential_score = self._calculate_potential_match(resume, jd)
        dimensions.append(potential_score)

        # 文化匹配：单独计算，不计入总分
        culture_reference = self._calculate_culture_match(resume, jd)

        # 总分仅由四个客观维度构成
        total_score = sum(d.weighted_score for d in dimensions)

        level = self._get_match_level(total_score)

        overall_strengths = []
        overall_weaknesses = []
        for dim in dimensions:
            overall_strengths.extend(dim.strengths)
            overall_weaknesses.extend(dim.weaknesses)

        recommendation = self._generate_recommendation(
            total_score, level, dimensions
        )
        match_summary = self._generate_match_summary(
            total_score, level, dimensions
        )

        return MatchResult(
            total_score=round(total_score, 1),
            level=level,
            dimensions=dimensions,
            culture_reference=culture_reference,
            overall_strengths=overall_strengths,
            overall_weaknesses=overall_weaknesses,
            recommendation=recommendation,
            match_summary=match_summary
        )
    
    def _calculate_skill_match(self, resume: Dict, jd: Dict) -> DimensionScore:
        """计算技能匹配度"""
        score = 0
        details = []
        strengths = []
        weaknesses = []
        
        # 获取简历中的技能
        resume_skills = set()
        if 'skills' in resume:
            for skill in resume['skills']:
                if isinstance(skill, dict):
                    resume_skills.add(skill.get('name', '').lower())
                else:
                    resume_skills.add(str(skill).lower())
        
        # 获取岗位要求的必须技能
        required_skills = []
        if 'required_skills' in jd:
            for skill in jd['required_skills']:
                if isinstance(skill, dict):
                    required_skills.append({
                        'name': skill.get('name', '').lower(),
                        'level': skill.get('level', '必须')
                    })
                else:
                    required_skills.append({
                        'name': str(skill).lower(),
                        'level': '必须'
                    })
        
        # 计算必须技能匹配
        if required_skills:
            matched_required = 0
            for req_skill in required_skills:
                skill_name = req_skill['name']
                if skill_name in resume_skills:
                    matched_required += 1
                    strengths.append(f"掌握{skill_name}")
                else:
                    if req_skill['level'] == '必须':
                        weaknesses.append(f"缺少{skill_name}技能")
            
            required_ratio = matched_required / len(required_skills)
            score += required_ratio * 70  # 必须技能占70分
            details.append(f"必须技能匹配率：{matched_required}/{len(required_skills)}")
        
        # 获取岗位要求的优先技能
        preferred_skills = []
        if 'preferred_skills' in jd:
            for skill in jd['preferred_skills']:
                if isinstance(skill, dict):
                    preferred_skills.append(skill.get('name', '').lower())
                else:
                    preferred_skills.append(str(skill).lower())
        
        # 计算优先技能匹配
        if preferred_skills:
            matched_preferred = sum(1 for s in preferred_skills if s in resume_skills)
            preferred_ratio = matched_preferred / len(preferred_skills)
            score += preferred_ratio * 30  # 优先技能占30分
            details.append(f"优先技能匹配率：{matched_preferred}/{len(preferred_skills)}")
        else:
            score += 30  # 如果没有优先技能要求，给满分
        
        return DimensionScore(
            name="技能匹配",
            score=min(100, score),
            weight=self.weights['skill'],
            weighted_score=round(min(100, score) * self.weights['skill'], 1),
            details=details,
            strengths=strengths,
            weaknesses=weaknesses
        )
    
    def _calculate_experience_match(self, resume: Dict, jd: Dict) -> DimensionScore:
        """计算经验匹配度"""
        score = 0
        details = []
        strengths = []
        weaknesses = []
        
        # 获取简历中的工作年限
        resume_years = resume.get('years_of_experience', 0)
        
        # 获取岗位要求的工作年限
        jd_years = 0
        if 'experience_requirement' in jd and jd['experience_requirement']:
            exp_str = jd['experience_requirement']
            import re
            year_match = re.search(r'(\d+)', exp_str)
            if year_match:
                jd_years = int(year_match.group(1))
        
        # 计算年限匹配
        if jd_years > 0:
            if resume_years >= jd_years:
                years_score = 100
                strengths.append(f"工作年限{resume_years}年，超过要求的{jd_years}年")
            elif resume_years >= jd_years * 0.8:
                years_score = 80
                details.append(f"工作年限{resume_years}年，接近要求的{jd_years}年")
            else:
                years_score = max(0, 100 - (jd_years - resume_years) * 20)
                weaknesses.append(f"工作年限{resume_years}年，不足要求的{jd_years}年")
            
            score += years_score * 0.4  # 年限占40%
            details.append(f"年限匹配：{resume_years}年/{jd_years}年")
        
        # 计算行业经验匹配
        resume_industries = set()
        if 'work_experience' in resume:
            for exp in resume['work_experience']:
                if isinstance(exp, dict):
                    company = exp.get('company', '')
                    # 简单的行业判断
                    if any(kw in company for kw in ['科技', '技术', '互联网', 'IT']):
                        resume_industries.add('互联网')
                    elif any(kw in company for kw in ['金融', '银行', '证券']):
                        resume_industries.add('金融')
                    elif any(kw in company for kw in ['医疗', '健康']):
                        resume_industries.add('医疗')
        
        jd_industry = jd.get('company_type', '')
        if jd_industry:
            if jd_industry in resume_industries:
                score += 30  # 行业匹配占30%
                strengths.append(f"有{jd_industry}行业经验")
                details.append(f"行业匹配：{jd_industry}")
            else:
                score += 15  # 行业不匹配给一半分
                details.append(f"行业不完全匹配：简历行业{resume_industries}，岗位行业{jd_industry}")
        else:
            score += 30  # 如果没有行业要求，给满分
        
        # 计算岗位级别匹配
        resume_positions = []
        if 'work_experience' in resume:
            for exp in resume['work_experience']:
                if isinstance(exp, dict):
                    position = exp.get('position', '')
                    resume_positions.append(position)
        
        jd_title = jd.get('title', '')
        if jd_title and resume_positions:
            # 简单的级别判断
            senior_keywords = ['高级', '资深', '专家', '总监', '经理']
            is_senior_jd = any(kw in jd_title for kw in senior_keywords)
            is_senior_resume = any(any(kw in pos for kw in senior_keywords) for pos in resume_positions)
            
            if is_senior_jd == is_senior_resume:
                score += 30  # 级别匹配占30%
                strengths.append("岗位级别匹配")
                details.append("级别匹配：匹配")
            else:
                score += 15
                details.append("级别匹配：不完全匹配")
        else:
            score += 30
        
        return DimensionScore(
            name="经验匹配",
            score=min(100, score),
            weight=self.weights['experience'],
            weighted_score=round(min(100, score) * self.weights['experience'], 1),
            details=details,
            strengths=strengths,
            weaknesses=weaknesses
        )
    
    def _calculate_education_match(self, resume: Dict, jd: Dict) -> DimensionScore:
        """计算教育匹配度"""
        score = 0
        details = []
        strengths = []
        weaknesses = []
        
        # 学历等级映射
        degree_levels = {
            '大专': 1,
            '专科': 1,
            '本科': 2,
            '学士': 2,
            '硕士': 3,
            '研究生': 3,
            '博士': 4,
            'MBA': 3,
            'EMBA': 3
        }
        
        # 获取简历中的最高学历
        resume_degree = 0
        resume_major = ""
        if 'education' in resume:
            for edu in resume['education']:
                if isinstance(edu, dict):
                    degree = edu.get('degree', '')
                    for key, level in degree_levels.items():
                        if key in degree:
                            resume_degree = max(resume_degree, level)
                    if edu.get('major'):
                        resume_major = edu['major']
        
        # 获取岗位要求的学历
        jd_degree = 0
        jd_major = ""
        if 'education_requirement' in jd and jd['education_requirement']:
            edu_req = jd['education_requirement']
            for key, level in degree_levels.items():
                if key in edu_req:
                    jd_degree = max(jd_degree, level)
        
        # 计算学历匹配
        if jd_degree > 0:
            if resume_degree >= jd_degree:
                score += 60
                strengths.append(f"学历达标")
                details.append(f"学历匹配：达标")
            elif resume_degree >= jd_degree - 1:
                score += 40
                details.append(f"学历接近要求")
            else:
                score += 20
                weaknesses.append(f"学历不足")
                details.append(f"学历不匹配")
        else:
            score += 60
        
        # 计算专业匹配
        if resume_major:
            # 简单的专业匹配判断
            cs_keywords = ['计算机', '软件', '信息', '电子', '通信', '自动化']
            is_cs_major = any(kw in resume_major for kw in cs_keywords)
            
            if is_cs_major:
                score += 40
                strengths.append(f"专业对口：{resume_major}")
                details.append(f"专业匹配：{resume_major}")
            else:
                score += 20
                details.append(f"专业不完全对口：{resume_major}")
        else:
            score += 20
        
        return DimensionScore(
            name="教育匹配",
            score=min(100, score),
            weight=self.weights['education'],
            weighted_score=round(min(100, score) * self.weights['education'], 1),
            details=details,
            strengths=strengths,
            weaknesses=weaknesses
        )
    
    def _calculate_culture_match(self, resume: Dict, jd: Dict) -> DimensionScore:
        """
        计算文化匹配参考指标。

        此维度**不计入总分**，仅作为面试环节的补充参考。
        评估仅基于简历中有明确文字证据的软性技能描述，
        不使用工作稳定性、跳槽频率等主观推断性因素。
        最终判断须通过面试等人工方式确认。
        """
        score = 60  # 中性基础分，不做倾向性假设
        details = ["⚠️ 此维度不计入总分，仅供面试参考，需人工进一步验证"]
        strengths = []
        weaknesses = []

        soft_skills = []
        if 'soft_skills' in jd:
            for skill in jd['soft_skills']:
                if isinstance(skill, dict):
                    soft_skills.append(skill.get('name', ''))
                else:
                    soft_skills.append(str(skill))

        if soft_skills:
            details.append(f"岗位要求软性技能：{', '.join(soft_skills)}")
            resume_text = str(resume)

            # 仅对有明确文字证据的软技能给分，无法确认则不扣分
            for skill in soft_skills:
                if skill == '沟通能力':
                    if '沟通' in resume_text and (
                        '客户' in resume_text or '协调' in resume_text or '汇报' in resume_text
                    ):
                        score += 5
                        strengths.append("简历中有沟通协调相关经验描述")
                elif skill == '团队协作':
                    if '团队' in resume_text and (
                        '合作' in resume_text or '跨部门' in resume_text
                    ):
                        score += 5
                        strengths.append("简历中有团队合作经验描述")
                elif skill == '学习能力':
                    if '自学' in resume_text or '新技术' in resume_text or '培训' in resume_text:
                        score += 5
                        strengths.append("简历中有主动学习经验描述")

        details.append("文化匹配参考评估：仅基于简历中可验证的软性技能描述")

        return DimensionScore(
            name="文化匹配（参考）",
            score=min(100, score),
            weight=0.0,           # 权重为0，不参与总分计算
            weighted_score=0.0,   # 加权分始终为0
            details=details,
            strengths=strengths,
            weaknesses=weaknesses
        )
    
    def _calculate_potential_match(self, resume: Dict, jd: Dict) -> DimensionScore:
        """计算发展潜力匹配度"""
        score = 70  # 基础分
        details = []
        strengths = []
        weaknesses = []
        
        # 学习能力判断
        if 'certifications' in resume and resume['certifications']:
            score += 15
            strengths.append("有持续学习和考证的习惯")
            details.append(f"证书：{', '.join(resume['certifications'][:3])}")
        
        # 技能广度判断
        if 'skills' in resume:
            skill_count = len(resume['skills'])
            if skill_count >= 5:
                score += 10
                strengths.append("技能栈较广")
                details.append(f"掌握技能数量：{skill_count}")
            elif skill_count >= 3:
                score += 5
                details.append(f"掌握技能数量：{skill_count}")
        
        # 项目经验判断
        if 'projects' in resume and resume['projects']:
            project_count = len(resume['projects'])
            if project_count >= 3:
                score += 10
                strengths.append("有丰富的项目经验")
                details.append(f"项目经验数量：{project_count}")
            elif project_count >= 1:
                score += 5
                details.append(f"项目经验数量：{project_count}")
        
        # 教育背景判断 - 仅评估是否完成学业，不基于学校名称进行歧视性评分
        if 'education' in resume and resume['education']:
            edu_count = len(resume['education'])
            if edu_count > 0:
                score += 10
                strengths.append("有完整的教育背景")
                details.append(f"教育经历数量：{edu_count}")
        
        details.append("发展潜力评估：基于学习能力、技能广度、项目经验")
        
        return DimensionScore(
            name="发展潜力",
            score=min(100, score),
            weight=self.weights['potential'],
            weighted_score=round(min(100, score) * self.weights['potential'], 1),
            details=details,
            strengths=strengths,
            weaknesses=weaknesses
        )
    
    def _get_match_level(self, score: float) -> MatchLevel:
        """获取匹配等级"""
        if score >= 90:
            return MatchLevel.PERFECT
        elif score >= 80:
            return MatchLevel.HIGH
        elif score >= 70:
            return MatchLevel.GOOD
        elif score >= 60:
            return MatchLevel.BASIC
        else:
            return MatchLevel.INSUFFICIENT
    
    def _generate_recommendation(self, total_score: float, level: MatchLevel, 
                                dimensions: List[DimensionScore]) -> str:
        """生成推荐意见"""
        # 找出最强和最弱的维度
        sorted_dims = sorted(dimensions, key=lambda d: d.score, reverse=True)
        strongest = sorted_dims[0]
        weakest = sorted_dims[-1]
        
        if level == MatchLevel.PERFECT:
            return f"强烈推荐。候选人整体匹配度极高（{total_score}分），{strongest.name}表现突出（{strongest.score}分）。建议优先安排面试。"
        elif level == MatchLevel.HIGH:
            return f"推荐。候选人整体匹配度较高（{total_score}分），{strongest.name}是主要优势。建议安排面试，重点关注{weakest.name}方面。"
        elif level == MatchLevel.GOOD:
            return f"可以考虑。候选人整体匹配度良好（{total_score}分），但{weakest.name}存在不足（{weakest.score}分）。建议综合评估后决定是否面试。"
        elif level == MatchLevel.BASIC:
            return f"谨慎考虑。候选人整体匹配度一般（{total_score}分），{weakest.name}是主要短板。建议作为备选或需要培训后上岗。"
        else:
            return f"不推荐。候选人整体匹配度较低（{total_score}分），与岗位要求存在较大差距。建议寻找更合适的候选人。"
    
    def _generate_match_summary(self, total_score: float, level: MatchLevel,
                               dimensions: List[DimensionScore]) -> str:
        """生成匹配摘要"""
        dim_summary = []
        for dim in dimensions:
            if dim.score >= 80:
                dim_summary.append(f"{dim.name}优秀")
            elif dim.score >= 60:
                dim_summary.append(f"{dim.name}达标")
            else:
                dim_summary.append(f"{dim.name}不足")
        
        return f"总分{total_score}分（{level.value}），{', '.join(dim_summary)}。"


def match_to_dict(result: MatchResult) -> Dict:
    """将MatchResult转换为字典"""
    from dataclasses import asdict
    result_dict = asdict(result)
    result_dict['level'] = result.level.value
    result_dict['_note'] = "total_score仅含技能/经验/教育/潜力四个维度；culture_reference为参考项，不计入总分"
    return result_dict


def match_to_json(result: MatchResult) -> str:
    """将MatchResult转换为JSON字符串"""
    return json.dumps(match_to_dict(result), ensure_ascii=False, indent=2)


# 测试代码
if __name__ == "__main__":
    # 模拟简历数据
    resume = {
        'name': '张三',
        'years_of_experience': 5,
        'education': [
            {'degree': '本科', 'school': '北京大学', 'major': '计算机科学'}
        ],
        'work_experience': [
            {'company': '某科技公司', 'position': '高级开发工程师'}
        ],
        'skills': [
            {'name': 'java', 'level': '精通'},
            {'name': 'spring', 'level': '熟练'},
            {'name': 'mysql', 'level': '熟练'},
            {'name': 'redis', 'level': '熟悉'},
            {'name': 'docker', 'level': '熟悉'}
        ],
        'certifications': ['PMP'],
        'projects': [
            {'name': '电商系统'},
            {'name': '支付系统'}
        ]
    }
    
    # 模拟岗位数据
    jd = {
        'title': '高级Java开发工程师',
        'experience_requirement': '5年',
        'education_requirement': '本科',
        'company_type': '互联网',
        'required_skills': [
            {'name': 'java', 'level': '必须'},
            {'name': 'spring', 'level': '必须'},
            {'name': 'mysql', 'level': '必须'}
        ],
        'preferred_skills': [
            {'name': 'redis', 'level': '优先'},
            {'name': 'docker', 'level': '优先'}
        ],
        'soft_skills': [
            {'name': '沟通能力'},
            {'name': '团队协作'}
        ]
    }
    
    # 执行匹配
    matcher = TalentMatcher()
    result = matcher.match(resume, jd)
    
    print(match_to_json(result))
