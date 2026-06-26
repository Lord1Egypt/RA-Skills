# -*- coding: utf-8 -*-
"""
SkillPilot - 智能技能路由引擎
路由决策器
"""

import re
import time
from typing import List, Dict, Optional, Any
from .models import SkillRequest, Scenario, SkillMetadata
from .registry import SkillRegistry


class RouteDecision:
    """路由决策器"""
    
    def __init__(self, registry: SkillRegistry, config: Dict = None):
        self.registry = registry
        self.context: Dict[str, Any] = {}
        self.config = config or {}
        self.silent_mode = self.config.get('silent_mode', 'balanced')  # quiet/balanced/verbose
    
    def decide(self, request: SkillRequest) -> List[str]:
        """
        决策返回有序技能列表
        返回：[首选技能，备选技能 1, 备选技能 2, ...]
        """
        start_time = time.time()
        
        # 1. 场景识别
        scenario = self._identify_scenario(request)
        
        # 2. 获取候选技能
        candidates = self.registry.get_candidates(
            category=request.category,
            required_caps=scenario.required_caps
        )
        
        # 3. 计算动态优先级
        ranked = self._rank_candidates(candidates, request, scenario)
        
        # 4. 记录决策日志
        decision_time = (time.time() - start_time) * 1000
        self._log_decision(request, ranked, scenario, decision_time)
        
        return ranked
    
    def _identify_scenario(self, request: SkillRequest) -> Scenario:
        """识别使用场景"""
        scenario = Scenario()
        
        # 分析查询内容或 URL
        text_to_analyze = request.query or request.url or request.content
        if not text_to_analyze:
            return scenario
        
        # 中文内容检测
        if self._contains_chinese(text_to_analyze):
            scenario.required_caps.append("chinese")
            scenario.weights["localization"] = 0.3
        
        # 反爬检测 (微信/知乎/豆瓣等)
        if self._is_anti_bot_url(request.url):
            scenario.required_caps.append("anti_bot")
            scenario.weights["reliability"] = 0.4
        
        # 技术内容检测
        if self._is_technical_query(text_to_analyze):
            scenario.required_caps.append("technical")
            scenario.weights["accuracy"] = 0.3
        
        # 成本敏感检测
        if request.budget == "free":
            scenario.required_caps.append("free")
            scenario.weights["cost"] = 0.3
        
        # 速度敏感检测
        if request.preferences.get("speed") == "fast":
            scenario.weights["speed"] = 0.3
        
        # 应用用户显式要求
        for req in request.requirements:
            if req not in scenario.required_caps:
                scenario.required_caps.append(req)
        
        return scenario
    
    def _rank_candidates(self, candidates: List[str], request: SkillRequest, scenario: Scenario) -> List[str]:
        """动态排名候选技能"""
        if not candidates:
            return []
        
        scores: Dict[str, float] = {}
        
        for name in candidates:
            meta = self.registry.get_skill(name)
            if not meta:
                continue
            
            # 基础分数 (健康分 + 优先级)
            base_score = meta.health_score * 0.5 + meta.priority * 5
            
            # 加权分数
            weighted_score = 0.0
            
            for factor, weight in scenario.weights.items():
                factor_score = self._calculate_factor_score(meta, factor)
                weighted_score += factor_score * weight
            
            # 用户偏好调整
            preference_bonus = self._calculate_preference_bonus(meta, request.preferences)
            
            # 总分
            scores[name] = base_score + weighted_score + preference_bonus
        
        # 排序 (分数高到低)
        ranked = sorted(scores.keys(), key=lambda n: scores[n], reverse=True)
        return ranked
    
    def _calculate_factor_score(self, meta: SkillMetadata, factor: str) -> float:
        """计算单个因素的分数"""
        if factor == "reliability":
            return meta.success_rate * 100
        elif factor == "localization":
            return 100 if "chinese" in meta.capabilities else 50
        elif factor == "cost":
            return (10 - meta.cost) * 10  # cost 越低分数越高
        elif factor == "speed":
            if meta.avg_response_time == 0:
                return 80  # 无历史数据，给中等分数
            return max(0, 100 - meta.avg_response_time / 100)  # 响应越快分数越高
        elif factor == "accuracy":
            return meta.priority * 10  # 优先级高的通常更准确
        else:
            return 50  # 默认中等分数
    
    def _calculate_preference_bonus(self, meta: SkillMetadata, preferences: Dict) -> float:
        """计算用户偏好加分"""
        bonus = 0.0
        
        # 区域偏好
        if preferences.get("region") == "cn" and "chinese" in meta.capabilities:
            bonus += 20
        
        # 成本偏好
        if preferences.get("budget") == "free" and meta.cost == 0:
            bonus += 15
        
        # 速度偏好
        if preferences.get("speed") == "fast" and meta.avg_response_time < 500:
            bonus += 15
        
        return bonus
    
    def _contains_chinese(self, text: str) -> bool:
        """检测是否包含中文"""
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
        return bool(chinese_pattern.search(text))
    
    def _is_anti_bot_url(self, url: Optional[str]) -> bool:
        """检测是否是反爬网站"""
        if not url:
            return False
        
        anti_bot_domains = [
            'mp.weixin.qq.com',
            'zhihu.com',
            'douban.com',
            'weibo.com',
            'xiaohongshu.com',
            'jianshu.com'
        ]
        
        return any(domain in url for domain in anti_bot_domains)
    
    def _is_technical_query(self, text: str) -> bool:
        """检测是否是技术查询"""
        technical_keywords = [
            'api', 'sdk', 'github', 'code', 'python', 'javascript',
            '开发', '编程', '技术', '框架', '库', '函数', '类',
            'error', 'bug', 'debug', 'install', 'deploy'
        ]
        
        text_lower = text.lower()
        return any(kw in text_lower for kw in technical_keywords)
    
    def _log_decision(self, request: SkillRequest, ranked: List[str], scenario: Scenario, decision_time: float):
        """记录决策日志"""
        # 简化日志，实际可写入文件或数据库
        log_entry = {
            "timestamp": time.time(),
            "category": request.category,
            "ranked_skills": ranked[:3],  # 只记录前 3 个
            "required_caps": scenario.required_caps,
            "decision_time_ms": decision_time
        }
        # 实际使用时可写入日志文件
        # print(f"[RouteDecision] {log_entry}")
