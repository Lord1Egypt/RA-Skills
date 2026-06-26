"""
简历解析器
使用LLM + 正则 提取结构化简历信息
"""

import re
import json
import logging
from typing import Optional
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class ParsedResume:
    """结构化简历数据"""
    raw_text: str
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None
    city: Optional[str] = None
    experience_years: Optional[int] = None
    degree: Optional[str] = None
    current_company: Optional[str] = None
    current_position: Optional[str] = None
    salary_current: Optional[str] = None
    salary_expectation: Optional[str] = None
    skills: list = None
    work_history: list = None
    education: list = None
    
    def __post_init__(self):
        if self.skills is None:
            self.skills = []
        if self.work_history is None:
            self.work_history = []
        if self.education is None:
            self.education = []
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class ResumeParser:
    """简历解析器"""
    
    # 正则模式
    PHONE_PATTERN = re.compile(r'1[3-9]\d{9}')
    EMAIL_PATTERN = re.compile(r'[\w.-]+@[\w.-]+\.\w+')
    AGE_PATTERN = re.compile(r'(\d{2})岁')
    DEGREE_PATTERN = re.compile(r'(博士|硕士|本科|大专|高中|中专|初中)')
    EXPERIENCE_PATTERN = re.compile(r'(\d+)年.*经验')
    SALARY_PATTERN = re.compile(r'(\d+(?:\.\d+)?)[kK]?-(\d+(?:\.\d+)?)[kK]?')
    
    def __init__(self, llm_client=None):
        """
        初始化解析器
        
        Args:
            llm_client: LLM客户端（可选，用于高级解析）
        """
        self.llm_client = llm_client
    
    def parse(self, text: str) -> ParsedResume:
        """
        解析简历文本
        
        Args:
            text: 原始简历文本
        
        Returns:
            结构化简历对象
        """
        resume = ParsedResume(raw_text=text)
        
        # 基础信息提取
        resume.phone = self._extract_phone(text)
        resume.email = self._extract_email(text)
        resume.age = self._extract_age(text)
        resume.degree = self._extract_degree(text)
        resume.experience_years = self._extract_experience(text)
        
        # 薪资提取
        salary_info = self._extract_salary(text)
        resume.salary_current = salary_info.get('current')
        resume.salary_expectation = salary_info.get('expectation')
        
        # 技能提取
        resume.skills = self._extract_skills(text)
        
        # 工作经历解析
        resume.work_history = self._parse_work_history(text)
        
        # 教育经历解析
        resume.education = self._parse_education(text)
        
        return resume
    
    def _extract_phone(self, text: str) -> Optional[str]:
        match = self.PHONE_PATTERN.search(text)
        return match.group(0) if match else None
    
    def _extract_email(self, text: str) -> Optional[str]:
        match = self.EMAIL_PATTERN.search(text)
        return match.group(0) if match else None
    
    def _extract_age(self, text: str) -> Optional[str]:
        match = self.AGE_PATTERN.search(text)
        return match.group(1) if match else None
    
    def _extract_degree(self, text: str) -> Optional[str]:
        match = self.DEGREE_PATTERN.search(text)
        return match.group(1) if match else None
    
    def _extract_experience(self, text: str) -> Optional[int]:
        match = self.EXPERIENCE_PATTERN.search(text)
        return int(match.group(1)) if match else None
    
    def _extract_salary(self, text: str) -> dict:
        """提取薪资信息"""
        result = {'current': None, 'expectation': None}
        
        # 当前薪资
        current_match = re.search(r'目前薪资.*?(\d+(?:\.\d+)?)[kK]?', text)
        if current_match:
            result['current'] = current_match.group(0)
        
        # 期望薪资
        expect_match = re.search(r'期望薪资.*?(\d+(?:\.\d+)?)[kK]?', text)
        if expect_match:
            result['expectation'] = expect_match.group(0)
        
        return result
    
    def _extract_skills(self, text: str) -> list:
        """提取技能标签"""
        # 常见技能关键词
        skill_keywords = [
            'Python', 'Java', 'JavaScript', 'Go', 'Rust', 'C++', 'C#',
            'React', 'Vue', 'Angular', 'Node.js',
            'MySQL', 'PostgreSQL', 'MongoDB', 'Redis',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes',
            'Machine Learning', 'Deep Learning', 'NLP',
            'Git', 'Linux', 'Nginx', 'Kafka'
        ]
        
        found_skills = []
        text_upper = text.upper()
        for skill in skill_keywords:
            if skill.upper() in text_upper:
                found_skills.append(skill)
        
        return found_skills
    
    def _parse_work_history(self, text: str) -> list:
        """解析工作经历"""
        history = []
        
        # 简单实现：按换行分割，查找公司/职位模式
        lines = text.split('\n')
        current_item = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检测公司名模式（如：xx公司、xx科技）
            if re.search(r'(公司|科技|集团|有限|企业)', line) and len(line) < 30:
                if current_item:
                    history.append(current_item)
                current_item = {'company': line}
            
            # 检测职位模式
            elif re.search(r'(工程师|经理|总监|主管|架构师|开发者)', line):
                current_item['position'] = line
            
            # 检测时间范围
            elif re.search(r'\d{4}.\d{2}', line):
                current_item['duration'] = line
            
            # 检测描述
            elif current_item and 'position' in current_item:
                current_item['description'] = current_item.get('description', '') + line
        
        if current_item:
            history.append(current_item)
        
        return history
    
    def _parse_education(self, text: str) -> list:
        """解析教育经历"""
        education = []
        
        # 常见学校/大学关键词
        school_pattern = re.compile(r'(大学|学院|学校|研究院)')
        
        lines = text.split('\n')
        for line in lines:
            if school_pattern.search(line):
                edu_item = {'school': line.strip()}
                
                # 提取学历
                degree_match = self.DEGREE_PATTERN.search(line)
                if degree_match:
                    edu_item['degree'] = degree_match.group(1)
                
                # 提取专业
                major_match = re.search(r'(计算机|软件|电子|机械|化学|物理|数学|经济|管理)', line)
                if major_match:
                    edu_item['major'] = major_match.group(0)
                
                education.append(edu_item)
        
        return education
    
    def parse_with_llm(self, text: str, llm_prompt: str = None) -> ParsedResume:
        """
        使用LLM增强解析
        
        Args:
            text: 简历文本
            llm_prompt: 自定义LLM提示词
        
        Returns:
            结构化简历对象
        """
        if not self.llm_client:
            logger.warning("未提供LLM客户端，使用基础解析")
            return self.parse(text)
        
        default_prompt = """
        请从以下简历文本中提取结构化信息，返回JSON格式：
        {
            "name": "姓名",
            "gender": "性别",
            "age": "年龄",
            "position": "当前职位",
            "city": "所在城市",
            "experience_years": 工作年限（数字）,
            "degree": "最高学历",
            "current_company": "当前公司",
            "skills": ["技能1", "技能2"],
            "work_history": [{"company": "公司", "position": "职位", "duration": "时间"}],
            "education": [{"school": "学校", "major": "专业", "degree": "学历"}]
        }
        
        简历文本：
        {text}
        """
        
        prompt = llm_prompt or default_prompt.format(text=text)
        
        try:
            response = self.llm_client.generate(prompt)
            # 解析LLM返回的JSON
            data = json.loads(response)
            
            # 合并基础解析和LLM解析
            base_resume = self.parse(text)
            for key, value in data.items():
                if value and getattr(base_resume, key) is None:
                    setattr(base_resume, key, value)
            
            return base_resume
            
        except Exception as e:
            logger.error(f"LLM解析失败: {e}")
            return self.parse(text)


# 使用示例
if __name__ == '__main__':
    sample_resume = """
    张三
    男 | 28岁 | 13800138000 | zhangsan@email.com
    
    Python高级工程师
    北京 | 5年经验 | 本科
    
    目前薪资：30K
    期望薪资：40K-50K
    
    技能：Python, Django, FastAPI, MySQL, Redis, Docker, AWS, Git
    
    工作经历：
    2020.03 - 至今    字节跳动    后端工程师
    负责短视频推荐系统后端开发，使用Python/Django构建高性能API服务。
    优化数据库查询性能，QPS提升50%。
    
    2018.07 - 2020.02    阿里巴巴    Java开发
    参与电商平台订单系统开发。
    
    教育经历：
    2014.09 - 2018.06    北京大学    计算机科学与技术    本科
    """
    
    parser = ResumeParser()
    resume = parser.parse(sample_resume)
    print(resume.to_json())
