# -*- coding: utf-8 -*-
"""
SkillPilot - 智能技能路由引擎
数据模型定义
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class SkillCategory(Enum):
    """技能类别"""
    SEARCH = "search"
    FETCH = "fetch"
    SUMMARIZE = "summarize"
    ANALYZE = "analyze"
    OTHER = "other"


class CircuitState(Enum):
    """熔断器状态"""
    CLOSED = "closed"       # 正常状态
    OPEN = "open"           # 熔断状态
    HALF_OPEN = "half-open" # 半开状态 (测试恢复)


@dataclass
class SkillMetadata:
    """技能元数据"""
    name: str
    category: str
    capabilities: List[str] = field(default_factory=list)
    priority: int = 5  # 1-10
    timeout: float = 30.0  # 秒
    cost: int = 0  # 0=免费，1-10=成本递增
    
    # 动态指标
    health_score: float = 100.0  # 0-100
    success_rate: float = 1.0    # 0-1
    avg_response_time: float = 0.0  # ms
    last_used: Optional[datetime] = None
    total_calls: int = 0
    failed_calls: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "category": self.category,
            "capabilities": self.capabilities,
            "priority": self.priority,
            "timeout": self.timeout,
            "cost": self.cost,
            "health_score": self.health_score,
            "success_rate": self.success_rate,
            "avg_response_time": self.avg_response_time,
            "total_calls": self.total_calls,
            "failed_calls": self.failed_calls
        }


@dataclass
class SkillRequest:
    """技能请求"""
    category: str
    query: Optional[str] = None
    url: Optional[str] = None
    content: Optional[str] = None
    preferences: Dict[str, Any] = field(default_factory=dict)
    requirements: List[str] = field(default_factory=list)
    max_retries: int = 3
    timeout: Optional[float] = None
    budget: str = "free"  # free/low/medium/high


@dataclass
class SkillResult:
    """技能调用结果"""
    success: bool
    content: Optional[str] = None
    error: Optional[str] = None
    used_skill: Optional[str] = None
    primary_skill: Optional[str] = None
    tried_skills: List[str] = field(default_factory=list)
    fallback_count: int = 0
    response_time: float = 0.0  # ms
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "content": self.content[:500] if self.content else None,
            "error": self.error,
            "used_skill": self.used_skill,
            "primary_skill": self.primary_skill,
            "tried_skills": self.tried_skills,
            "fallback_count": self.fallback_count,
            "response_time": self.response_time
        }


@dataclass
class Scenario:
    """使用场景"""
    required_caps: List[str] = field(default_factory=list)
    weights: Dict[str, float] = field(default_factory=lambda: {
        "reliability": 0.3,
        "localization": 0.2,
        "cost": 0.2,
        "speed": 0.2,
        "accuracy": 0.1
    })


@dataclass
class CircuitBreaker:
    """熔断器"""
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    last_failure: float = 0.0
    cooldown: float = 60.0  # 秒
    half_open_successes: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "last_failure": self.last_failure,
            "cooldown": self.cooldown,
            "half_open_successes": self.half_open_successes
        }


@dataclass
class SkillMetrics:
    """技能指标"""
    skill_name: str
    period: str  # "1h"/"24h"/"7d"/"30d"
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    avg_response_time: float = 0.0
    min_response_time: float = float('inf')
    max_response_time: float = 0.0
    p95_response_time: float = 0.0
    p99_response_time: float = 0.0
    
    @property
    def success_rate(self) -> float:
        if self.total_calls == 0:
            return 1.0
        return self.successful_calls / self.total_calls
    
    def to_dict(self) -> Dict:
        return {
            "skill_name": self.skill_name,
            "period": self.period,
            "total_calls": self.total_calls,
            "success_rate": self.success_rate,
            "avg_response_time": self.avg_response_time,
            "min_response_time": self.min_response_time,
            "max_response_time": self.max_response_time,
            "p95_response_time": self.p95_response_time,
            "p99_response_time": self.p99_response_time
        }
