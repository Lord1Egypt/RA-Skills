"""
管线上下文 — Triangulate 工作流的不可变数据载体 (Pydantic BaseModel)。

设计原则：
- 不可变：evolve() 返回新实例而非原地修改
- 类型安全：所有字段有显式类型注解
- 单一数据源：divergence_rounds 等关键字段只在这里定义
"""
from __future__ import annotations

import time as _time
from collections import Counter
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator

from schemas import (
    DecisionResult,
    ExecutionReport,
    FinalReport,
    StrategyRound,
    TaskDAG,
    Tier,
    UserInput,
    WorkflowCheckpoint,
    WorkflowPhase,
)
from exceptions import PipelineConsistencyError


class PipelineContext(BaseModel):
    """Triangulate 工作流的不可变管线上下文。

    每个阶段函数接收 PipelineContext，返回新的 PipelineContext。
    禁止在任何阶段函数中原地修改传入的 ctx。
    """

    model_config = {"arbitrary_types_allowed": False}

    # ---- 阶段数据 ----
    validated_input: Optional[UserInput] = None
    strategy_rounds: List[StrategyRound] = Field(default_factory=list)
    task_dag: Optional[TaskDAG] = None
    exec_report: Optional[ExecutionReport] = None
    review_results: List[DecisionResult] = Field(default_factory=list)
    final_report: Optional["FinalReport"] = None

    # ---- 副作用追踪 ----
    strategy_sessions: List[str] = Field(default_factory=list)
    execution_sessions: List[str] = Field(default_factory=list)
    created_sessions: List[str] = Field(default_factory=list)

    # ---- 状态标记 ----
    degraded: bool = False
    divergence_rounds: int = Field(ge=0, default=0)

    # ---- 时间追踪 ----
    workflow_start_time: float = 0.0
    phase_start_times: Dict[str, float] = Field(default_factory=dict)

    # ---- 检查点（exclude=True 避免序列化循环引用） ----
    checkpoint: Optional[object] = Field(default=None, exclude=True)

    @model_validator(mode="after")
    def _validate_consistency(self) -> "PipelineContext":
        """Pydantic validator：构造时自动校验 sessions 一致性。

        跳过空 sessions（初始构造场景），仅在非空时校验。
        """
        # 跳过空状态（初始构造时所有 sessions 列表为空）
        if not self.strategy_sessions and not self.execution_sessions and not self.created_sessions:
            return self

        if not self.check_consistency():
            raise PipelineConsistencyError(
                f"created_sessions 与 strategy+execution sessions 不一致: "
                f"strategy={self.strategy_sessions}, "
                f"execution={self.execution_sessions}, "
                f"created={self.created_sessions}"
            )
        return self

    def check_consistency(self) -> bool:
        """校验上下文一致性：strategy_sessions + execution_sessions 应等于 created_sessions。"""
        expected = set(dict.fromkeys(
            self.strategy_sessions + self.execution_sessions
        ))
        actual = set(self.created_sessions)
        return expected == actual

    def assert_consistency(self) -> None:
        """断言上下文一致性，不一致时抛出 PipelineConsistencyError。"""
        if not self.check_consistency():
            raise PipelineConsistencyError(
                f"created_sessions 与 strategy+execution sessions 不一致: "
                f"strategy={self.strategy_sessions}, "
                f"execution={self.execution_sessions}, "
                f"created={self.created_sessions}"
            )

    @property
    def all_sessions(self) -> List[str]:
        """所有已注册的 session IDs（策略 + 执行）"""
        return self.strategy_sessions + self.execution_sessions

    @property
    def elapsed_seconds(self) -> float:
        """工作流已运行秒数"""
        if self.workflow_start_time == 0.0:
            return 0.0
        return _time.time() - self.workflow_start_time

    def evolve(self, **kwargs: Any) -> "PipelineContext":
        """返回新实例，保留未修改的字段。禁止原地修改。

        使用 copy.deepcopy 确保 list/dict 字段完全隔离，
        杜绝浅拷贝导致的多持有者共享底层引用问题。

        Usage:
            ctx = ctx.evolve(validated_input=ui, divergence_rounds=1)
        """
        import copy
        new_data = {}
        for field_name in PipelineContext.model_fields:
            if field_name in kwargs:
                new_data[field_name] = kwargs[field_name]
            else:
                # deepcopy 确保 list/dict 字段（strategy_rounds,
                # strategy_sessions, execution_sessions, created_sessions 等）
                # 在新旧实例之间完全隔离
                new_data[field_name] = copy.deepcopy(getattr(self, field_name))
        return PipelineContext(**new_data)

    def add_strategy_session(self, session_id: str) -> "PipelineContext":
        """注册策略阶段创建的 session（返回新实例）"""
        return self.evolve(
            strategy_sessions=self.strategy_sessions + [session_id],
            created_sessions=self.created_sessions + [session_id],
        )

    def add_execution_session(self, session_id: str) -> "PipelineContext":
        """注册执行阶段创建的 session（返回新实例）"""
        return self.evolve(
            execution_sessions=self.execution_sessions + [session_id],
            created_sessions=self.created_sessions + [session_id],
        )

    def record_phase_start(self, phase: WorkflowPhase) -> "PipelineContext":
        """记录阶段开始时间"""
        new_times = dict(self.phase_start_times)
        new_times[phase] = _time.time()
        return self.evolve(phase_start_times=new_times)

    def to_checkpoint(self, current_phase: WorkflowPhase, tier: Tier) -> WorkflowCheckpoint:
        """从 PipelineContext 实时投影为 WorkflowCheckpoint。

        这是 checkpoint 的唯一数据源——orchestrator 不再手动同步。
        """
        return WorkflowCheckpoint(
            phase=current_phase,
            tier=tier,
            input_data=self.validated_input,
            strategy_rounds=self.strategy_rounds,
            task_dag=self.task_dag,
            execution_report=self.exec_report,
            review_results=self.review_results,
            final_report=(
                self.final_report.model_dump_json(indent=2)
                if self.final_report and hasattr(self.final_report, "model_dump_json")
                else str(self.final_report) if self.final_report else None
            ),
            created_sessions=self.created_sessions,
            divergence_rounds=self.divergence_rounds,
            degraded=self.degraded,
            created_at=_time.strftime("%Y-%m-%dT%H:%M:%S"),
            updated_at=_time.strftime("%Y-%m-%dT%H:%M:%S"),
        )

    def _infer_tier(self) -> Tier:
        """从当前上下文中推断配置档次"""
        if self.strategy_rounds:
            last_round = self.strategy_rounds[-1]
            if last_round.decisions:
                configs = [d.config for d in last_round.decisions]
                most_common = Counter(configs).most_common(1)
                if most_common:
                    return most_common[0][0]
        if self.validated_input:
            if self.validated_input.importance >= 4:
                return Tier.FULL
            elif self.validated_input.importance >= 2:
                return Tier.BALANCED
        return Tier.BALANCED

    @classmethod
    def create(
        cls,
        checkpoint: Optional[WorkflowCheckpoint] = None,
        workflow_start_time: Optional[float] = None,
    ) -> "PipelineContext":
        """创建初始上下文"""
        return cls(
            checkpoint=checkpoint,
            workflow_start_time=workflow_start_time or _time.time(),
        )



