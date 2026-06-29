#!/usr/bin/env python3
"""
简历解析模块
从文本或文件中提取结构化的候选人信息
"""

import json
import re
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class Education:
    """教育经历"""
    school: str
    degree: str  # 本科、硕士、博士等
    major: str
    start_date: str
    end_date: str
    gpa: Optional[str] = None


@dataclass
class WorkExperience:
    """工作经历"""
    company: str
    position: str
    start_date: str
    end_date: str
    responsibilities: List[str]
    achievements: List[str]


@dataclass
class Project:
    """项目经验"""
    name: str
    role: str
    description: str
    technologies: List[str]
    achievements: List[str]


@dataclass
class Skill:
    """技能"""
    name: str
    level: str  # 熟练、精通、了解
    years: Optional[int] = None


@dataclass
class Resume:
    """简历结构"""
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None
    years_of_experience: Optional[int] = None
    current_position: Optional[str] = None
    current_company: Optional[str] = None
    education: List[Education] = None
    work_experience: List[WorkExperience] = None
    projects: List[Project] = None
    skills: List[Skill] = None
    certifications: List[str] = None
    languages: List[str] = None
    summary: Optional[str] = None
    
    def __post_init__(self):
        self.education = self.education or []
        self.work_experience = self.work_experience or []
        self.projects = self.projects or []
        self.skills = self.skills or []
        self.certifications = self.certifications or []
        self.languages = self.languages or []


def parse_resume_text(text: str) -> Resume:
    """
    从文本中解析简历信息
    
    Args:
        text: 简历文本内容
        
    Returns:
        Resume对象，包含解析后的结构化信息
    """
    # 初始化简历对象
    resume = Resume(name="")
    
    # 提取姓名（通常在最开始）
    name_match = re.search(r'^([^\n]{2,4})', text.strip())
    if name_match:
        resume.name = name_match.group(1).strip()
    
    # 提取联系方式
    phone_match = re.search(r'1[3-9]\d{9}', text)
    if phone_match:
        resume.phone = phone_match.group()
    
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    if email_match:
        resume.email = email_match.group()
    
    # 提取工作年限
    exp_match = re.search(r'(\d+)\s*[年]', text)
    if exp_match:
        resume.years_of_experience = int(exp_match.group(1))
    
    # 提取教育经历
    resume.education = extract_education(text)
    
    # 提取工作经历
    resume.work_experience = extract_work_experience(text)
    
    # 提取技能
    resume.skills = extract_skills(text)
    
    # 提取项目经验
    resume.projects = extract_projects(text)
    
    # 提取证书
    resume.certifications = extract_certifications(text)
    
    return resume


def extract_education(text: str) -> List[Education]:
    """提取教育经历"""
    education_list = []
    
    # 常见学历关键词
    degree_patterns = [
        r'本科', r'学士', r'硕士', r'博士', r'研究生',
        r'大专', r'专科', r'MBA', r'EMBA'
    ]
    
    # 常见学校关键词
    school_pattern = r'([\u4e00-\u9fa5]{2,}(?:大学|学院|学校))'
    
    # 查找教育经历部分
    edu_section = re.search(r'教育[经历背景]*[：:]*\s*(.*?)(?=(?:工作|项目|技能|证书|$))', 
                           text, re.DOTALL | re.IGNORECASE)
    
    if edu_section:
        edu_text = edu_section.group(1)
        
        # 提取每一项教育经历
        edu_items = re.split(r'\n(?=\d{4})', edu_text)
        
        for item in edu_items:
            if not item.strip():
                continue
            
            edu = Education(school="", degree="", major="", 
                          start_date="", end_date="")
            
            # 提取学校
            school_match = re.search(school_pattern, item)
            if school_match:
                edu.school = school_match.group(1)
            
            # 提取学历
            for degree in degree_patterns:
                if degree in item:
                    edu.degree = degree
                    break
            
            # 提取专业
            major_match = re.search(r'专业[：:]*\s*([^\n]+)', item)
            if major_match:
                edu.major = major_match.group(1).strip()
            
            # 提取时间
            time_match = re.search(r'(\d{4})\s*[-至到]\s*(\d{4}|至今)', item)
            if time_match:
                edu.start_date = time_match.group(1)
                edu.end_date = time_match.group(2)
            
            if edu.school or edu.degree:
                education_list.append(edu)
    
    return education_list


def extract_work_experience(text: str) -> List[WorkExperience]:
    """提取工作经历"""
    work_list = []
    
    # 查找工作经历部分
    work_section = re.search(r'工作[经历经验]*[：:]*\s*(.*?)(?=(?:教育|项目|技能|证书|$))', 
                            text, re.DOTALL | re.IGNORECASE)
    
    if work_section:
        work_text = work_section.group(1)
        
        # 按公司分段
        company_blocks = re.split(r'\n(?=\d{4}|\d{4}\.\d{2})', work_text)
        
        for block in company_blocks:
            if not block.strip():
                continue
            
            work = WorkExperience(
                company="", position="", 
                start_date="", end_date="",
                responsibilities=[], achievements=[]
            )
            
            # 提取公司名称
            company_match = re.search(r'([\u4e00-\u9fa5]{2,}(?:公司|集团|企业|科技|技术))', block)
            if company_match:
                work.company = company_match.group(1)
            
            # 提取职位
            position_match = re.search(r'职位[：:]*\s*([^\n]+)', block)
            if position_match:
                work.position = position_match.group(1).strip()
            
            # 提取时间
            time_match = re.search(r'(\d{4})\s*[-至到]\s*(\d{4}|至今)', block)
            if time_match:
                work.start_date = time_match.group(1)
                work.end_date = time_match.group(2)
            
            # 提取职责描述
            desc_lines = block.split('\n')
            for line in desc_lines:
                line = line.strip()
                if line.startswith('•') or line.startswith('-') or line.startswith('·'):
                    work.responsibilities.append(line.lstrip('•-· '))
                elif '负责' in line or '参与' in line or '主导' in line:
                    work.responsibilities.append(line)
            
            if work.company or work.position:
                work_list.append(work)
    
    return work_list


def extract_skills(text: str) -> List[Skill]:
    """提取技能"""
    skills_list = []
    
    # 常见技能关键词
    tech_skills = [
        'Java', 'Python', 'C++', 'JavaScript', 'TypeScript', 'Go', 'Rust',
        'Spring', 'SpringBoot', 'Django', 'Flask', 'React', 'Vue', 'Angular',
        'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch',
        'Docker', 'Kubernetes', 'K8s', 'Jenkins', 'Git', 'Linux',
        'AWS', 'Azure', '阿里云', '腾讯云',
        '微服务', '分布式', '高并发', '大数据', '机器学习', '深度学习',
        'HTML', 'CSS', 'Node.js', 'Webpack', 'Vite'
    ]
    
    # 查找技能部分
    skill_section = re.search(r'技能[：:]*\s*(.*?)(?=(?:教育|工作|项目|证书|$))', 
                             text, re.DOTALL | re.IGNORECASE)
    
    skill_text = skill_section.group(1) if skill_section else text
    
    # 提取技能
    for skill_name in tech_skills:
        if skill_name.lower() in skill_text.lower():
            # 判断熟练程度
            level = "熟悉"
            if '精通' in skill_text and skill_name in skill_text:
                level = "精通"
            elif '熟练' in skill_text and skill_name in skill_text:
                level = "熟练"
            elif '了解' in skill_text and skill_name in skill_text:
                level = "了解"
            
            skills_list.append(Skill(name=skill_name, level=level))
    
    return skills_list


def extract_projects(text: str) -> List[Project]:
    """提取项目经验"""
    projects_list = []
    
    # 查找项目经验部分
    project_section = re.search(r'项目[经验经历]*[：:]*\s*(.*?)(?=(?:教育|工作|技能|证书|$))', 
                               text, re.DOTALL | re.IGNORECASE)
    
    if project_section:
        project_text = project_section.group(1)
        
        # 按项目分段
        project_blocks = re.split(r'\n(?=项目|[\d{4}])', project_text)
        
        for block in project_blocks:
            if not block.strip():
                continue
            
            project = Project(
                name="", role="", description="",
                technologies=[], achievements=[]
            )
            
            # 提取项目名称
            name_match = re.search(r'项目[名称]*[：:]*\s*([^\n]+)', block)
            if name_match:
                project.name = name_match.group(1).strip()
            
            # 提取角色
            role_match = re.search(r'角色[：:]*\s*([^\n]+)', block)
            if role_match:
                project.role = role_match.group(1).strip()
            
            # 提取技术栈
            tech_match = re.search(r'技术[栈]*[：:]*\s*([^\n]+)', block)
            if tech_match:
                project.technologies = [t.strip() for t in tech_match.group(1).split(',')]
            
            if project.name:
                projects_list.append(project)
    
    return projects_list


def extract_certifications(text: str) -> List[str]:
    """提取证书"""
    certifications = []
    
    # 常见证书
    cert_patterns = [
        r'PMP', r'ACP', r'AWS\s*认证', r'Oracle\s*认证',
        r'软考', r'计算机等级', r'英语[四六]级',
        r'雅思', r'托福', r'GRE'
    ]
    
    for pattern in cert_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        certifications.extend(matches)
    
    return list(set(certifications))


def resume_to_dict(resume: Resume) -> Dict:
    """将Resume对象转换为字典"""
    return asdict(resume)


def resume_to_json(resume: Resume) -> str:
    """将Resume对象转换为JSON字符串"""
    return json.dumps(asdict(resume), ensure_ascii=False, indent=2)


# 测试代码
if __name__ == "__main__":
    sample_resume = """
张三
电话：13800138000
邮箱：zhangsan@example.com
地址：北京市朝阳区

教育经历：
2015-2019 北京大学 本科 计算机科学与技术
2019-2022 清华大学 硕士 软件工程

工作经历：
2022-至今 某科技公司 高级Java开发工程师
• 负责核心业务系统的架构设计和开发
• 主导微服务架构改造，提升系统性能30%
• 带领5人团队完成3个重要项目

技能：
精通Java、Spring Boot、MySQL
熟悉Redis、Kafka、Docker
了解Kubernetes、云原生

证书：
PMP认证
AWS解决方案架构师认证
    """
    
    resume = parse_resume_text(sample_resume)
    print(resume_to_json(resume))
