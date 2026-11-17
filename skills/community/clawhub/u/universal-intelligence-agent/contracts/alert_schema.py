"""
预警监控契约 — Pydantic v2
───────────────────────────
定义预警和 Cron 监控的严格类型。
"""
from __future__ import annotations

from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime, timezone


class AlertLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertRule(BaseModel):
    """预警规则"""
    rule_id: str = Field(..., description="规则ID")
    query: str = Field(..., min_length=1, description="监控查询")
    check_interval_hours: int = Field(default=24, ge=1, le=168, description="检查间隔(小时)")
    alert_on_change: bool = Field(default=True, description="变化时预警")
    alert_on_new_results: bool = Field(default=True, description="新结果时预警")
    min_credibility: int = Field(default=3, ge=1, le=5, description="最低可信度阈值")
    enabled: bool = Field(default=True, description="是否启用")


class AlertEvent(BaseModel):
    """预警事件"""
    event_id: str = Field(..., description="事件ID")
    rule_id: str = Field(..., description="触发规则ID")
    level: AlertLevel = Field(default=AlertLevel.INFO, description="预警级别")
    title: str = Field(..., description="事件标题")
    description: str = Field(default="", description="事件描述")
    new_results_count: int = Field(default=0, ge=0, description="新结果数")
    changed_results_count: int = Field(default=0, ge=0, description="变化结果数")
    triggered_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="触发时间",
    )
    acknowledged: bool = Field(default=False, description="是否已确认")


class CronConfig(BaseModel):
    """Cron 监控配置"""
    config_id: str = Field(..., description="配置ID")
    query: str = Field(..., min_length=1, description="监控查询")
    schedule: str = Field(default="0 */6 * * *", description="Cron表达式")
    rules: list[AlertRule] = Field(default_factory=list, description="预警规则")
    last_run: Optional[datetime] = Field(default=None, description="上次运行时间")
    next_run: Optional[datetime] = Field(default=None, description="下次运行时间")
    enabled: bool = Field(default=True, description="是否启用")
