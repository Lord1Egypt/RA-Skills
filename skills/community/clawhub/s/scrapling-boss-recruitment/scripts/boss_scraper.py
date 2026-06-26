"""
Boss直聘 招聘爬虫
基于 Scrapling 框架
"""

import time
import random
import logging
from typing import Optional
from dataclasses import dataclass
from scrapling.fetchers import DynamicSession, DynamicFetcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Candidate:
    """候选人数据结构"""
    id: str
    name: str
    position: str
    company: str
    city: str
    experience: str
    degree: str
    salary: str
    skills: list
    update_time: str
    avatar: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Resume:
    """简历数据结构"""
    candidate_id: str
    name: str
    gender: Optional[str] = None
    age: Optional[str] = None
    position: Optional[str] = None
    company: Optional[str] = None
    city: Optional[str] = None
    experience_years: Optional[str] = None
    degree: Optional[str] = None
    salary_expectation: Optional[str] = None
    skills: Optional[list] = None
    work_history: Optional[list] = None
    education: Optional[list] = None
    self_description: Optional[str] = None


class BossRecruiter:
    """Boss直聘招聘助手"""
    
    BASE_URL = "https://www.zhipin.com"
    SEARCH_URL = "/web/candidate/search"
    RESUME_URL = "/web/resume/detail"
    GREET_URL = "/web/chat/add"
    
    # 请求限制配置
    DAILY_SEARCH_LIMIT = 200
    DAILY_GREET_LIMIT = 500
    MIN_DELAY = 3  # 秒
    MAX_DELAY = 10  # 秒
    
    def __init__(self, cookies: dict):
        self.cookies = cookies
        self.search_count = 0
        self.greet_count = 0
        
    def _random_delay(self):
        """随机延迟，模拟真人操作"""
        delay = random.uniform(self.MIN_DELAY, self.MAX_DELAY)
        logger.info(f"延迟 {delay:.1f} 秒")
        time.sleep(delay)
    
    def _check_limits(self, action: str = 'search'):
        """检查操作限制"""
        if action == 'search' and self.search_count >= self.DAILY_SEARCH_LIMIT:
            raise Exception(f"今日搜索次数已达上限 ({self.DAILY_SEARCH_LIMIT}次)")
        if action == 'greet' and self.greet_count >= self.DAILY_GREET_LIMIT:
            raise Exception(f"今日打招呼次数已达上限 ({self.DAILY_GREET_LIMIT}次)")
    
    def search_candidates(
        self,
        keyword: str,
        city: str = None,
        experience: str = None,
        degree: str = None,
        salary: str = None,
        page: int = 1,
        page_size: int = 30
    ) -> list[Candidate]:
        """
        搜索候选人
        
        Args:
            keyword: 搜索关键词（如：Python后端）
            city: 城市（如：北京）
            experience: 经验要求（如：3-5年）
            degree: 学历要求（如：本科）
            salary: 薪资范围
            page: 页码
            page_size: 每页数量
        
        Returns:
            候选人列表
        """
        self._check_limits('search')
        
        # 构建搜索URL
        params = f"?query={keyword}&page={page}&pageSize={page_size}"
        if city:
            params += f"&city={city}"
        if experience:
            params += f"&experience={experience}"
        if degree:
            params += f"&degree={degree}"
        if salary:
            params += f"&salary={salary}"
        
        url = f"{self.BASE_URL}{self.SEARCH_URL}{params}"
        
        logger.info(f"搜索候选人: {url}")
        
        with DynamicSession(headless=True, network_idle=True) as session:
            page = session.fetch(url, cookies=self.cookies)
            
            # 解析候选人列表
            candidates = []
            items = page.css('.job-card-box')
            
            for item in items:
                try:
                    candidate = Candidate(
                        id=item.css('@data-lid').get() or item.css('@data-jobid').get() or '',
                        name=item.css('.name::text').get() or '未知',
                        position=item.css('.job-title::text').get() or '',
                        company=item.css('.company-name::text').get() or '',
                        city=item.css('.city::text').get() or '',
                        experience=item.css('.experience::text').get() or '',
                        degree=item.css('.degree::text').get() or '',
                        salary=item.css('.salary::text').get() or '',
                        skills=item.css('.skill-tag::text').getall() or [],
                        update_time=item.css('.update-time::text').get() or '',
                        avatar=item.css('img.avatar@src').get()
                    )
                    candidates.append(candidate)
                except Exception as e:
                    logger.warning(f"解析候选人失败: {e}")
                    continue
            
            self.search_count += 1
            self._random_delay()
            
            return candidates
    
    def get_resume(self, candidate_id: str) -> Resume:
        """
        获取候选人简历详情
        
        Args:
            candidate_id: 候选人ID
        
        Returns:
            简历对象
        """
        url = f"{self.BASE_URL}{self.RESUME_URL}?lid={candidate_id}"
        
        logger.info(f"获取简历: {candidate_id}")
        
        with DynamicSession(headless=True, network_idle=True) as session:
            page = session.fetch(url, cookies=self.cookies)
            
            # 解析简历详情
            resume = Resume(
                candidate_id=candidate_id,
                name=page.css('.name::text').get() or '未知',
                position=page.css('.job-title::text').get() or '',
                company=page.css('.current-company::text').get() or '',
                city=page.css('.city::text').get() or '',
                experience_years=page.css('.experience::text').get() or '',
                degree=page.css('.degree::text').get() or '',
                salary_expectation=page.css('.salary-expectation::text').get() or '',
                skills=page.css('.skill-tag::text').getall(),
                work_history=self._parse_work_history(page),
                education=self._parse_education(page),
                self_description=page.css('.self-description::text').get()
            )
            
            self._random_delay()
            return resume
    
    def _parse_work_history(self, page) -> list:
        """解析工作经历"""
        history = []
        items = page.css('.work-history-item')
        for item in items:
            history.append({
                'company': item.css('.company::text').get() or '',
                'position': item.css('.position::text').get() or '',
                'duration': item.css('.duration::text').get() or '',
                'description': item.css('.description::text').get() or ''
            })
        return history
    
    def _parse_education(self, page) -> list:
        """解析教育经历"""
        education = []
        items = page.css('.education-item')
        for item in items:
            education.append({
                'school': item.css('.school::text').get() or '',
                'major': item.css('.major::text').get() or '',
                'degree': item.css('.degree::text').get() or '',
                'duration': item.css('.duration::text').get() or ''
            })
        return education
    
    def batch_greet(
        self,
        candidate_ids: list[str],
        greeting_template: str = "您好，{name}，看到您对{position}岗位很感兴趣，我们团队正在招聘，您有兴趣聊聊吗？"
    ) -> dict:
        """
        批量发送招呼
        
        Args:
            candidate_ids: 候选人ID列表
            greeting_template: 招呼语模板
        
        Returns:
            发送结果统计
        """
        self._check_limits('greet')
        
        results = {'success': 0, 'failed': 0, 'failed_ids': []}
        
        logger.info(f"开始批量打招呼，共 {len(candidate_ids)} 人")
        
        for candidate_id in candidate_ids:
            try:
                # 先获取候选人信息用于个性化
                candidate = self.search_candidates(keyword='', page=1)
                # 这里应该根据candidate_id获取详情，简化处理
                
                # 发送招呼
                greeting = greeting_template.format(
                    name='候选人',  # 实际应从候选人详情获取
                    position='相关岗位'
                )
                
                # 实际发送逻辑（需要对接Boss直聘API）
                # with DynamicSession(...) as session:
                #     session.post(self.GREET_URL, data={'lid': candidate_id, 'msg': greeting})
                
                results['success'] += 1
                self.greet_count += 1
                
            except Exception as e:
                logger.warning(f"打招呼失败 {candidate_id}: {e}")
                results['failed'] += 1
                results['failed_ids'].append(candidate_id)
            
            self._random_delay()
        
        return results
    
    def get_candidate_detail(self, candidate_id: str) -> dict:
        """
        获取候选人简要信息（用于打招呼前的详情确认）
        """
        # 简化实现，实际应调用详情API
        return {
            'id': candidate_id,
            'name': '待获取',
            'position': '待获取',
            'company': '待获取'
        }
