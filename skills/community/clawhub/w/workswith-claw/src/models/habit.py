"""
习惯模型
"""
from typing import Optional
from pydantic import BaseModel
from datetime import time


class HabitReport(BaseModel):
    """习惯报告"""
    entity_id: str
    typical_on_time: Optional[str] = None
    typical_off_time: Optional[str] = None
    weekday_pattern: str = "daily"  # daily, weekday, weekend
    confidence: float = 0.0
    sample_count: int = 0
    updated_at: str = ""


class HabitQuery(BaseModel):
    """习惯查询"""
    entity_id: str
    days: int = 30  # 分析最近N天
