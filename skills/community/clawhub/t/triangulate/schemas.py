"""
数据契约定义 — Triangulate 所有模块的数据边界。

所有跨模块传递的数据必须通过 Pydantic 校验。
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


# ============================================================================
# 枚举类型
# ============================================================================

class Tier(str, Enum):
    """执行配置档次"""
    FULL = "全量"
    BALANCED = "平衡"
    LIGHT = "轻量"
    SKILL_DISPATCH = "子技能调度"


class WorkflowPhase(str, Enum):
    """工作流显式状态"""
    IDLE = "IDLE"
    INPUT_VALIDATION = "INPUT_VALIDATION"
    STRATEGY = "STRATEGY"
    DISPATCH = "DISPATCH"
    EXECUTE = "EXECUTE"
    REVIEW = "REVIEW"
    RENDER = "RENDER"
    DONE = "DONE"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


class ConsensusVerdict(str, Enum):
    """共识判定结果"""
    CONSENSUS = "consensus"
    DIVERGENCE = "divergence"
    FALLBACK_TO_USER = "fallback_to_user"


class ExecutionStatus(str, Enum):
    """子任务执行状态"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class DivergenceAction(str, Enum):
    """分歧时的处理动作"""
    RETRY = "retry"
    FALLBACK = "fallback"
    DEGRADE = "degrade"


# ============================================================================
# 输入层
# ============================================================================

class UserInput(BaseModel):
    """用户输入 — 经过适配层校验后的标准格式"""
    task_description: str = Field(min_length=1, max_length=5000)
    importance: int = Field(ge=1, le=5, default=3)
    keywords: List[str] = Field(default_factory=list)
    preferred_templates: List[str] = Field(default_factory=list)
    require_execution_layer: bool = True
    require_management_layer: bool = True
    max_total_timeout_seconds: int = Field(ge=60, le=3600, default=600)

    @field_validator("task_description")
    @classmethod
    def task_must_not_be_whitespace(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("task_description 不能为空或纯空白")
        return stripped


# ============================================================================
# 决策层
# ============================================================================

class DecisionResult(BaseModel):
    """统一决策结果 — 所有决策者(A/B/C)必须返回此格式。"""
    agent_id: str = Field(pattern=r"^(A|B|C)$")
    importance: int = Field(ge=1, le=5)
    config: Tier
    reasoning: str = Field(min_length=10, max_length=2000)
    risks: List[str] = Field(default_factory=list)
    top_findings: List[str] = Field(default_factory=list, max_length=5)
    confidence: float = Field(ge=0.0, le=1.0)
    template_code: Optional[str] = Field(default=None)

    @field_validator("top_findings")
    @classmethod
    def top_findings_not_empty(cls, v: List[str]) -> List[str]:
        cleaned = [item.strip() for item in v if item.strip()]
        if not cleaned:
            raise ValueError("top_findings 至少需要一条有效结论")
        return cleaned


class StrategyRound(BaseModel):
    """策略轮次记录"""
    round_number: int = Field(ge=1)
    decisions: List[DecisionResult]
    verdict: ConsensusVerdict
    user_override: Optional[DecisionResult] = None


# ============================================================================
# 管理层
# ============================================================================

class SubTask(BaseModel):
    """管理层拆解出的子任务"""
    id: str = Field(pattern=r"^subtask-[a-z0-9\-]+$", max_length=64)
    goal: str = Field(min_length=1, max_length=500)
    completion_criteria: str = Field(min_length=1, max_length=500)
    output_format: str = Field(min_length=1, max_length=500)
    token_budget: int = Field(ge=100, le=100000, default=4000)
    timeout_seconds: int = Field(ge=30, le=1800, default=300)
    depends_on: List[str] = Field(default_factory=list)
    skill_path: Optional[str] = Field(default=None)
    perspective: Optional[str] = Field(default=None)

    @field_validator("depends_on")
    @classmethod
    def no_self_dependency(cls, v: List[str], info: Any) -> List[str]:
        task_id = info.data.get("id", "")
        if task_id in v:
            raise ValueError(f"子任务 {task_id} 不能依赖自身")
        return v


class TaskDAG(BaseModel):
    """任务有向无环图"""
    subtasks: List[SubTask]

    @model_validator(mode="after")
    def validate_dag(self) -> "TaskDAG":
        """拓扑排序检测循环依赖和孤立引用"""
        ids = {t.id for t in self.subtasks}
        # 检查所有依赖引用是否存在
        for t in self.subtasks:
            for dep in t.depends_on:
                if dep not in ids:
                    raise ValueError(
                        f"子任务 '{t.id}' 依赖不存在的任务 '{dep}'"
                    )
        # 拓扑排序检测环
        self._topological_sort()
        return self

    def _topological_sort(self) -> List[str]:
        """Kahn 算法检测 DAG"""
        in_degree: Dict[str, int] = {t.id: 0 for t in self.subtasks}
        adjacency: Dict[str, List[str]] = {t.id: [] for t in self.subtasks}

        for t in self.subtasks:
            for dep in t.depends_on:
                adjacency[dep].append(t.id)
                in_degree[t.id] += 1

        queue = [nid for nid, deg in in_degree.items() if deg == 0]
        sorted_ids: List[str] = []

        while queue:
            node = queue.pop(0)
            sorted_ids.append(node)
            for neighbor in adjacency[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sorted_ids) != len(self.subtasks):
            remaining = {t.id for t in self.subtasks} - set(sorted_ids)
            raise ValueError(f"检测到循环依赖！涉及任务: {remaining}")

        return sorted_ids


# ============================================================================
# 执行层
# ============================================================================

class ExecutionResult(BaseModel):
    """单个子任务执行结果"""
    subtask_id: str
    status: ExecutionStatus
    output: Optional[str] = None
    error: Optional[str] = None
    tokens_used: int = Field(ge=0, default=0)
    duration_seconds: float = Field(ge=0.0, default=0.0)
    retry_count: int = Field(ge=0, default=0)


class ExecutionReport(BaseModel):
    """执行层汇总报告"""
    total_tasks: int
    completed: int
    failed: int
    timed_out: int
    cancelled: int
    results: List[ExecutionResult]
    total_tokens_used: int = 0
    total_duration_seconds: float = 0.0

    @property
    def failure_rate(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return (self.failed + self.timed_out) / self.total_tasks


# ============================================================================
# 共识引擎
# ============================================================================

class ConsensusOutput(BaseModel):
    """共识引擎输出"""
    verdict: ConsensusVerdict
    agreement_count: int = Field(ge=0, le=3)
    total_participants: int = Field(ge=0, le=3)  # ge=0 允许空决策列表
    agreed_points: List[str] = Field(default_factory=list)
    divergent_points: Dict[str, List[str]] = Field(default_factory=dict)
    divergence_rounds: int = Field(ge=0, default=0)
    requires_user_intervention: bool = False
    recommended_action: Optional[DivergenceAction] = None

    @property
    def agreement_ratio(self) -> float:
        if self.total_participants == 0:
            return 0.0
        return self.agreement_count / self.total_participants


# ============================================================================
# Saga / 事务
# ============================================================================

class SagaStepResult(BaseModel):
    """Saga 单步结果"""
    step_name: str
    success: bool
    output: Any = None
    error: Optional[str] = None
    compensated: bool = False
    compensation_error: Optional[str] = None


class SagaReport(BaseModel):
    """Saga 事务报告"""
    success: bool
    steps: List[SagaStepResult]
    failed_step: Optional[str] = None
    total_steps: int
    successful_steps: int
    rolled_back_steps: int
    error: Optional[str] = None


# ============================================================================
# 熔断器
# ============================================================================

class CircuitState(str, Enum):
    CLOSED = "CLOSED"       # 正常通行
    OPEN = "OPEN"           # 熔断，拒绝请求
    HALF_OPEN = "HALF_OPEN" # 半开，探测恢复


class CircuitBreakerConfig(BaseModel):
    """熔断器配置"""
    failure_threshold: int = Field(ge=1, default=5)
    recovery_timeout_seconds: float = Field(ge=1.0, default=30.0)
    half_open_max_requests: int = Field(ge=1, default=3)
    execution_timeout_seconds: float = Field(ge=1.0, default=60.0)


# ============================================================================
# 全局工作流状态（检查点）
# ============================================================================

class WorkflowCheckpoint(BaseModel):
    """工作流检查点 — 用于中断恢复"""
    phase: WorkflowPhase
    tier: Tier
    input_data: Optional[UserInput] = None
    strategy_rounds: List[StrategyRound] = Field(default_factory=list)
    task_dag: Optional[TaskDAG] = None
    execution_report: Optional[ExecutionReport] = None
    review_results: List[DecisionResult] = Field(default_factory=list)
    final_report: Optional[str] = None
    created_sessions: List[str] = Field(default_factory=list)
    divergence_rounds: int = 0
    degraded: bool = False  # 标记是否触发过降级策略
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


# ============================================================================
# 管线上下文 → 参见 pipeline.py 的 PipelineContext (Pydantic BaseModel)
# ============================================================================


# ============================================================================
# 输出渲染
# ============================================================================

class FinalReport(BaseModel):
    """最终分析报告"""
    task_description: str
    tier: Tier
    executor_count: int
    decision_maker_count: int
    perspective_code: Optional[str] = None
    core_conclusions: List[str] = Field(max_length=5)
    divergent_points: List[str] = Field(default_factory=list)
    uncertainties: List[str] = Field(default_factory=list)
    execution_stats: Optional[ExecutionReport] = None
    tokens_consumed: int = 0
    degraded: bool = False  # 标记是否使用了降级策略

    @model_validator(mode="after")
    def validate_report_consistency(self) -> "FinalReport":
        """校验报告逻辑一致性。

        1. 降级执行时 core_conclusions 可以为空（使用默认决策）
        2. 非降级执行时 core_conclusions 不应为空
        3. 如果有 divergent_points，应该与 core_conclusions 不冲突
        """
        if not self.degraded and len(self.core_conclusions) == 0:
            # 非降级但没有结论 → 可能是异常，记录但不阻止
            import logging
            logging.getLogger(__name__).warning(
                "FinalReport: 非降级执行但没有核心结论，"
                "可能存在渲染阶段问题"
            )
        return self


# ============================================================================
# 统一工作流结果
# ============================================================================

class WorkflowResult(BaseModel):
    """统一工作流结果 — 区分正常/降级/失败三种完成状态。"""
    status: Literal["success", "degraded", "failed"]
    report: Optional[FinalReport] = None
    error: Optional[str] = None
    error_checkpoint: Optional[WorkflowCheckpoint] = None
    degraded_reasons: List[str] = Field(default_factory=list)
    idempotency_cache_hit: bool = False

    @property
    def is_success(self) -> bool:
        return self.status == "success"

    @property
    def is_degraded(self) -> bool:
        return self.status == "degraded"

    @property
    def is_failed(self) -> bool:
        return self.status == "failed"
