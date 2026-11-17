"""
管道状态契约 — Pydantic v2
───────────────────────────
定义管道状态机和事务的严格类型。
状态转换必须有显式合法性校验。
"""
from __future__ import annotations

from pydantic import BaseModel, Field, model_validator
from enum import Enum
from typing import Optional, Any
from datetime import datetime, timezone


class PipelinePhase(str, Enum):
    IDLE = "idle"
    PENDING = "pending"
    SEARCHING = "searching"
    CRAWLING = "crawling"
    ANALYZING = "analyzing"
    REPORTING = "reporting"
    DELIVERING = "delivering"
    DONE = "done"
    FAILED = "failed"
    RETRYING = "retrying"


# 合法的状态转换
VALID_TRANSITIONS: dict[PipelinePhase, set[PipelinePhase]] = {
    PipelinePhase.IDLE:       {PipelinePhase.PENDING},
    PipelinePhase.PENDING:    {PipelinePhase.SEARCHING, PipelinePhase.FAILED},
    PipelinePhase.SEARCHING:  {PipelinePhase.CRAWLING, PipelinePhase.FAILED, PipelinePhase.RETRYING},
    PipelinePhase.CRAWLING:   {PipelinePhase.ANALYZING, PipelinePhase.FAILED, PipelinePhase.RETRYING},
    PipelinePhase.ANALYZING:  {PipelinePhase.REPORTING, PipelinePhase.FAILED, PipelinePhase.RETRYING},
    PipelinePhase.REPORTING:  {PipelinePhase.DELIVERING, PipelinePhase.FAILED, PipelinePhase.RETRYING},
    PipelinePhase.DELIVERING: {PipelinePhase.DONE, PipelinePhase.FAILED},
    PipelinePhase.DONE:       {PipelinePhase.IDLE},
    PipelinePhase.FAILED:     {PipelinePhase.RETRYING, PipelinePhase.IDLE},
    PipelinePhase.RETRYING:   {PipelinePhase.SEARCHING, PipelinePhase.CRAWLING,
                               PipelinePhase.ANALYZING, PipelinePhase.REPORTING,
                               PipelinePhase.FAILED},
}


class PhaseContext(BaseModel):
    """阶段上下文 — 用于跨会话恢复"""
    phase: PipelinePhase = Field(..., description="阶段")
    started_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="开始时间",
    )
    completed_at: Optional[datetime] = Field(default=None, description="完成时间")
    attempt: int = Field(default=1, ge=1, le=10, description="尝试次数")
    max_attempts: int = Field(default=3, ge=1, le=10, description="最大尝试次数")
    data_snapshot: dict[str, Any] = Field(default_factory=dict, description="阶段产出物快照")
    errors: list[str] = Field(default_factory=list, description="错误列表")


class PipelineState(BaseModel):
    """
    全局管道状态 — 不可变值对象

    状态转换合法性在 transition_to() 方法中强制校验。
    非法转换直接抛异常，不做任何默认处理。
    """
    session_id: str = Field(..., min_length=1, description="会话ID")
    current_phase: PipelinePhase = Field(default=PipelinePhase.IDLE, description="当前阶段")
    phase_history: list[PhaseContext] = Field(default_factory=list, description="阶段历史")
    circuit_breaker_open: bool = Field(default=False, description="熔断器是否打开")
    global_timeout: int = Field(default=600, ge=30, le=3600, description="全局超时(秒)")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="创建时间",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="更新时间",
    )

    def transition_to(self, new_phase: PipelinePhase) -> PipelineState:
        """
        状态转换 — 带合法性校验

        Raises:
            ValueError: 非法状态转换
        """
        valid = VALID_TRANSITIONS.get(self.current_phase, set())
        if new_phase not in valid:
            raise ValueError(
                f"非法状态转换: {self.current_phase.value} → {new_phase.value}. "
                f"合法转换: {[p.value for p in valid]}"
            )

        # 记录阶段历史
        new_history = list(self.phase_history)
        new_history.append(PhaseContext(
            phase=self.current_phase,
            completed_at=datetime.now(timezone.utc),
        ))

        return self.model_copy(update={
            "current_phase": new_phase,
            "phase_history": new_history,
            "updated_at": datetime.now(timezone.utc),
        })

    def can_retry(self, phase: PipelinePhase) -> bool:
        """检查某个阶段是否可以重试"""
        for ctx in self.phase_history:
            if ctx.phase == phase and ctx.attempt >= ctx.max_attempts:
                return False
        return True

    model_config = {"frozen": True}


class WALEntry(BaseModel):
    """WAL 日志条目"""
    session_id: str = Field(..., description="会话ID")
    phase: str = Field(..., description="阶段")
    action: str = Field(..., description="操作")
    status: str = Field(..., description="状态: prepared | committed | rolled_back")
    details: str = Field(default="", description="详情")
    timestamp: float = Field(default_factory=lambda: __import__("time").time(), description="时间戳")
