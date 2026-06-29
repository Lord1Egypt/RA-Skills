#!/usr/bin/env python3
"""
岗位分析模块
从岗位描述（JD）中提取结构化的岗位要求
"""

import json
import re
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class Requirement:
    """要求项"""
    name: str
    level: str  # 必须、优先、加分
    description: str


@dataclass
class JobDescription:
    """岗位描述结构"""
    title: str
    department: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    education_requirement: Optional[str] = None
    experience_requirement: Optional[str] = None
    age_requirement: Optional[str] = None
    
    # 硬性要求
    required_skills: List[Requirement] = None
    preferred_skills: List[Requirement] = None
    
    # 软性要求
    soft_skills: List[Requirement] = None
    
    # 岗位职责
    responsibilities: List[str] = None
    
    # 福利待遇
    benefits: List[str] = None
    
    # 公司信息
    company_name: Optional[str] = None
    company_type: Optional[str] = None  # 互联网、金融、医疗等
    company_size: Optional[str] = None
    
    def __post_init__(self):
        self.required_skills = self.required_skills or []
        self.preferred_skills = self.preferred_skills or []
        self.soft_skills = self.soft_skills or []
        self.responsibilities = self.responsibilities or []
        self.benefits = self.benefits or []


def parse_job_description(text: str) -> JobDescription:
    """
    从文本中解析岗位描述
    
    Args:
        text: 岗位描述文本
        
    Returns:
        JobDescription对象，包含解析后的结构化信息
    """
    # 初始化岗位描述对象
    jd = JobDescription(title="")
    
    # 提取岗位名称
    title_match = re.search(r'(?:岗位|职位|招聘)[名称]*[：:]*\s*([^\n]+)', text)
    if title_match:
        jd.title = title_match.group(1).strip()
    else:
        # 尝试从第一行提取
        first_line = text.strip().split('\n')[0]
        if len(first_line) < 20:
            jd.title = first_line
    
    # 提取部门
    dept_match = re.search(r'部门[：:]*\s*([^\n]+)', text)
    if dept_match:
        jd.department = dept_match.group(1).strip()
    
    # 提取工作地点
    location_match = re.search(r'(?:工作地点|地点|城市)[：:]*\s*([^\n]+)', text)
    if location_match:
        jd.location = location_match.group(1).strip()
    
    # 提取薪资范围
    salary_match = re.search(r'(?:薪资|薪酬|工资)[：:]*\s*([^\n]+)', text)
    if salary_match:
        jd.salary_range = salary_match.group(1).strip()
    else:
        # 尝试匹配薪资格式如 15-25K
        salary_pattern = re.search(r'(\d+\s*[-至到]\s*\d+\s*[Kk万])', text)
        if salary_pattern:
            jd.salary_range = salary_pattern.group(1)
    
    # 提取学历要求
    edu_match = re.search(r'学历[要求]*[：:]*\s*([^\n]+)', text)
    if edu_match:
        jd.education_requirement = edu_match.group(1).strip()
    else:
        # 尝试匹配常见学历要求
        if '本科' in text or '学士' in text:
            jd.education_requirement = '本科'
        elif '硕士' in text or '研究生' in text:
            jd.education_requirement = '硕士'
        elif '博士' in text:
            jd.education_requirement = '博士'
        elif '大专' in text or '专科' in text:
            jd.education_requirement = '大专'
    
    # 提取经验要求
    exp_match = re.search(r'(?:经验|工作年限)[要求]*[：:]*\s*(\d+)\s*年', text)
    if exp_match:
        jd.experience_requirement = f"{exp_match.group(1)}年"
    
    # 提取年龄要求
    age_match = re.search(r'年龄[要求]*[：:]*\s*(\d+)\s*[-至到]\s*(\d+)', text)
    if age_match:
        jd.age_requirement = f"{age_match.group(1)}-{age_match.group(2)}岁"
    
    # 提取岗位职责
    jd.responsibilities = extract_responsibilities(text)
    
    # 提取技能要求
    jd.required_skills = extract_required_skills(text)
    jd.preferred_skills = extract_preferred_skills(text)
    
    # 提取软性要求
    jd.soft_skills = extract_soft_skills(text)
    
    # 提取福利待遇
    jd.benefits = extract_benefits(text)
    
    # 提取公司信息
    jd.company_name = extract_company_name(text)
    jd.company_type = extract_company_type(text)
    jd.company_size = extract_company_size(text)
    
    return jd


def extract_responsibilities(text: str) -> List[str]:
    """提取岗位职责"""
    responsibilities = []
    
    # 查找职责部分
    resp_section = re.search(
        r'(?:岗位职责|工作职责|职责描述|工作内容)[：:]*\s*(.*?)(?=(?:任职要求|岗位要求|任职资格|技能要求|福利|$))',
        text, re.DOTALL | re.IGNORECASE
    )
    
    if resp_section:
        resp_text = resp_section.group(1)
        
        # 提取每一项职责
        lines = resp_text.split('\n')
        for line in lines:
            line = line.strip()
            if line and (line.startswith('•') or line.startswith('-') or 
                        line.startswith('·') or line.startswith('1') or
                        line.startswith('2') or line.startswith('3')):
                # 清理前缀
                cleaned = re.sub(r'^[•\-·\d.]+\s*', '', line)
                if cleaned:
                    responsibilities.append(cleaned)
    
    return responsibilities


def extract_required_skills(text: str) -> List[Requirement]:
    """提取必须技能要求"""
    skills = []
    
    # 常见技术技能
    tech_skills = {
        'Java': r'Java',
        'Python': r'Python',
        'C++': r'C\+\+',
        'JavaScript': r'JavaScript|JS',
        'TypeScript': r'TypeScript|TS',
        'Go': r'Go(?:lang)?',
        'Rust': r'Rust',
        'Spring': r'Spring(?:Boot)?',
        'React': r'React',
        'Vue': r'Vue(?:\.js)?',
        'Angular': r'Angular',
        'MySQL': r'MySQL',
        'PostgreSQL': r'PostgreSQL',
        'MongoDB': r'MongoDB',
        'Redis': r'Redis',
        'Kafka': r'Kafka',
        'Docker': r'Docker',
        'Kubernetes': r'Kubernetes|K8s',
        'Linux': r'Linux',
        'Git': r'Git',
        '微服务': r'微服务',
        '分布式': r'分布式',
        '高并发': r'高并发',
        '大数据': r'大数据',
        '机器学习': r'机器学习|ML',
        '深度学习': r'深度学习|DL',
    }
    
    # 查找要求部分
    req_section = re.search(
        r'(?:任职要求|岗位要求|任职资格|技能要求)[：:]*\s*(.*?)(?=(?:福利|待遇|公司|联系|$))',
        text, re.DOTALL | re.IGNORECASE
    )
    
    req_text = req_section.group(1) if req_section else text
    
    # 检查必须技能
    for skill_name, pattern in tech_skills.items():
        if re.search(pattern, req_text, re.IGNORECASE):
            # 判断是必须还是优先
            level = "必须"
            context = get_skill_context(req_text, skill_name)
            if '优先' in context or '加分' in context:
                level = "优先"
            
            skills.append(Requirement(
                name=skill_name,
                level=level,
                description=context
            ))
    
    return skills


def extract_preferred_skills(text: str) -> List[Requirement]:
    """提取优先技能要求"""
    skills = []
    
    # 查找优先技能部分
    pref_section = re.search(
        r'(?:优先考虑|加分项|优先条件)[：:]*\s*(.*?)(?=(?:福利|待遇|公司|联系|$))',
        text, re.DOTALL | re.IGNORECASE
    )
    
    if pref_section:
        pref_text = pref_section.group(1)
        
        # 提取技能
        tech_skills = {
            '开源贡献': r'开源',
            '技术博客': r'博客',
            '架构设计': r'架构',
            '团队管理': r'管理|带队',
            '项目管理': r'项目管理|PMP',
        }
        
        for skill_name, pattern in tech_skills.items():
            if re.search(pattern, pref_text, re.IGNORECASE):
                skills.append(Requirement(
                    name=skill_name,
                    level="优先",
                    description=""
                ))
    
    return skills


def extract_soft_skills(text: str) -> List[Requirement]:
    """提取软性技能要求"""
    skills = []
    
    soft_skill_patterns = {
        '沟通能力': r'沟通',
        '团队协作': r'团队|协作',
        '学习能力': r'学习',
        '抗压能力': r'抗压|压力',
        '责任心': r'责任',
        '自驱力': r'自驱|主动',
        '逻辑思维': r'逻辑',
        '解决问题': r'问题解决|解决问题',
    }
    
    for skill_name, pattern in soft_skill_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            skills.append(Requirement(
                name=skill_name,
                level="软性要求",
                description=""
            ))
    
    return skills


def extract_benefits(text: str) -> List[str]:
    """提取福利待遇"""
    benefits = []
    
    # 查找福利部分
    benefit_section = re.search(
        r'(?:福利|待遇|我们提供)[：:]*\s*(.*?)(?=(?:联系|公司介绍|$))',
        text, re.DOTALL | re.IGNORECASE
    )
    
    if benefit_section:
        benefit_text = benefit_section.group(1)
        
        # 常见福利关键词
        benefit_keywords = [
            '五险一金', '六险一金', '年终奖', '股票', '期权',
            '带薪年假', '弹性工作', '远程办公', '免费三餐',
            '健身房', '团建', '旅游', '培训', '晋升',
            '加班补贴', '交通补贴', '住房补贴', '通讯补贴'
        ]
        
        for keyword in benefit_keywords:
            if keyword in benefit_text:
                benefits.append(keyword)
    
    return benefits


def extract_company_name(text: str) -> Optional[str]:
    """提取公司名称"""
    # 尝试匹配公司名称
    company_match = re.search(
        r'(?:公司名称|关于我们|企业介绍)[：:]*\s*([^\n]+)',
        text, re.IGNORECASE
    )
    if company_match:
        return company_match.group(1).strip()
    
    # 尝试匹配常见公司格式
    company_pattern = re.search(
        r'([\u4e00-\u9fa5]{2,}(?:科技|技术|网络|信息|软件|互联网))',
        text
    )
    if company_pattern:
        return company_pattern.group(1)
    
    return None


def extract_company_type(text: str) -> Optional[str]:
    """提取公司类型"""
    type_keywords = {
        '互联网': r'互联网|IT|科技',
        '金融': r'金融|银行|证券|保险',
        '医疗': r'医疗|健康|生物',
        '教育': r'教育|培训',
        '电商': r'电商|电子商务',
        '游戏': r'游戏',
        '人工智能': r'人工智能|AI',
    }
    
    for company_type, pattern in type_keywords.items():
        if re.search(pattern, text, re.IGNORECASE):
            return company_type
    
    return None


def extract_company_size(text: str) -> Optional[str]:
    """提取公司规模"""
    size_match = re.search(
        r'(?:公司规模|团队规模|人员规模)[：:]*\s*([^\n]+)',
        text, re.IGNORECASE
    )
    if size_match:
        return size_match.group(1).strip()
    
    # 尝试匹配规模描述
    size_patterns = [
        (r'(\d+)\s*人以上', lambda m: f"{m.group(1)}人以上"),
        (r'(\d+)\s*[-至到]\s*(\d+)\s*人', lambda m: f"{m.group(1)}-{m.group(2)}人"),
    ]
    
    for pattern, formatter in size_patterns:
        match = re.search(pattern, text)
        if match:
            return formatter(match)
    
    return None


def get_skill_context(text: str, skill_name: str) -> str:
    """获取技能在文本中的上下文"""
    # 查找技能所在的句子
    sentences = re.split(r'[。；;]', text)
    for sentence in sentences:
        if skill_name in sentence:
            return sentence.strip()
    return ""


def jd_to_dict(jd: JobDescription) -> Dict:
    """将JobDescription对象转换为字典"""
    return asdict(jd)


def jd_to_json(jd: JobDescription) -> str:
    """将JobDescription对象转换为JSON字符串"""
    return json.dumps(asdict(jd), ensure_ascii=False, indent=2)


# 测试代码
if __name__ == "__main__":
    sample_jd = """
高级Java开发工程师

岗位职责：
1. 负责核心业务系统的架构设计和开发
2. 参与系统性能优化和技术难题攻关
3. 指导初中级开发人员，提升团队技术水平
4. 参与技术方案评审和代码审查

任职要求：
1. 本科及以上学历，计算机相关专业
2. 5年以上Java开发经验
3. 精通Java、Spring Boot、MySQL
4. 熟悉Redis、Kafka、Docker等中间件
5. 有微服务架构经验优先
6. 有大型分布式系统经验优先
7. 良好的沟通能力和团队协作精神

福利待遇：
- 五险一金
- 年终奖
- 带薪年假
- 弹性工作
- 免费三餐

公司：某互联网科技公司
规模：500-1000人
    """
    
    jd = parse_job_description(sample_jd)
    print(jd_to_json(jd))
