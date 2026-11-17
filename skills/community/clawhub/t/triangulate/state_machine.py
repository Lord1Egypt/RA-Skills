"""
显式状态机 — Triangulate 工作流的 10 状态定义。

每个状态转换都有 Guard 条件，杜绝非法状态跳转。
支持检查点保存和中断恢复。
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Tuple

from schemas import (
    DecisionResult,
    ExecutionReport,
    StrategyRound,
    TaskDAG,
    Tier,
    UserInput,
    WorkflowCheckpoint,
    WorkflowPhase,
)


# ============================================================================
# 状态转换表
# ============================================================================

# (当前状态, 下一状态): [Guard 条件列表]
# Guard 函数签名: (WorkflowCheckpoint) -> Tuple[bool, str]
#   返回 (通过, 失败原因)

STATE_TRANSITIONS: Dict[Tuple[WorkflowPhase, WorkflowPhase], List[Callable]] = {}

# IDLE → INPUT_VALIDATION: 无条件
STATE_TRANSITIONS[(WorkflowPhase.IDLE, WorkflowPhase.INPUT_VALIDATION)] = []

# INPUT_VALIDATION → STRATEGY: input_data 必须存在且有效
STATE_TRANSITIONS[(WorkflowPhase.INPUT_VALIDATION, WorkflowPhase.STRATEGY)] = [
    lambda cp: (cp.input_data is not None, "input_data 不能为空"),
    lambda cp: (
        cp.input_data is not None and len(cp.input_data.task_description) > 0,
        "task_description 不能为空",
    ),
]

# STRATEGY → DISPATCH: 至少一轮共识结果（兜底决策也算）
STATE_TRANSITIONS[(WorkflowPhase.STRATEGY, WorkflowPhase.DISPATCH)] = [
    lambda cp: (len(cp.strategy_rounds) > 0, "没有策略轮次记录"),
    lambda cp: (
        cp.strategy_rounds is not None
        and len(cp.strategy_rounds) > 0
        and len(cp.strategy_rounds[-1].decisions) >= 1,
        f"最后一轮只有 {len(cp.strategy_rounds[-1].decisions) if cp.strategy_rounds and cp.strategy_rounds[-1].decisions else 0} 个决策，至少需要 1 个",
    ),
]

# STRATEGY → FAILED: 分歧轮次 >= 2 时触发
# 对齐共识引擎: max_divergence_rounds=2, 第1轮分歧重试, 第2轮分歧重试, 第3轮分歧转交用户
# 因此 divergence_rounds >= 2 意味着已经过了至少 2 轮分歧 → 进入 FAILED
STATE_TRANSITIONS[(WorkflowPhase.STRATEGY, WorkflowPhase.FAILED)] = [
    lambda cp: (cp.divergence_rounds >= 2, "分歧轮次未达到 2 轮"),
]

# DISPATCH → EXECUTE: TaskDAG 必须存在且有效
STATE_TRANSITIONS[(WorkflowPhase.DISPATCH, WorkflowPhase.EXECUTE)] = [
    lambda cp: (cp.task_dag is not None, "task_dag 不能为空"),
    lambda cp: (
        cp.task_dag is not None and len(cp.task_dag.subtasks) > 0,
        "task_dag.subtasks 不能为空",
    ),
]

# EXECUTE → REVIEW: execution_report 必须存在
STATE_TRANSITIONS[(WorkflowPhase.EXECUTE, WorkflowPhase.REVIEW)] = [
    lambda cp: (cp.execution_report is not None, "execution_report 不能为空"),
]

# REVIEW → RENDER: review_results 必须存在
STATE_TRANSITIONS[(WorkflowPhase.REVIEW, WorkflowPhase.RENDER)] = [
    lambda cp: (len(cp.review_results) > 0, "review_results 不能为空"),
]

# RENDER → DONE: final_report 必须存在
STATE_TRANSITIONS[(WorkflowPhase.RENDER, WorkflowPhase.DONE)] = [
    lambda cp: (cp.final_report is not None, "final_report 不能为空"),
]

# 任何状态 → CANCELLED: 无条件（用户打断）
for phase in WorkflowPhase:
    if phase != WorkflowPhase.CANCELLED:
        STATE_TRANSITIONS[(phase, WorkflowPhase.CANCELLED)] = []

# 任何状态 → FAILED: 无条件（系统异常）
for phase in WorkflowPhase:
    if phase != WorkflowPhase.FAILED:
        STATE_TRANSITIONS[(phase, WorkflowPhase.FAILED)] = []


# ============================================================================
# 状态机引擎
# ============================================================================

@dataclass
class TransitionResult:
    """状态转换结果"""
    success: bool
    from_phase: WorkflowPhase
    to_phase: WorkflowPhase
    reason: str = ""
    checkpoint: Optional[WorkflowCheckpoint] = None


class WorkflowStateMachine:
    """Triangulate 工作流状态机 — 10 状态 + Guard 条件 + 检查点持久化。"""

    CHECKPOINT_DIR = Path(".triangulate_checkpoints")
    MAX_CHECKPOINTS = 10  # 最多保留 10 个检查点文件，防止磁盘泄漏

    def __init__(self):
        self.current_phase: WorkflowPhase = WorkflowPhase.IDLE
        self._checkpoint: WorkflowCheckpoint = WorkflowCheckpoint(
            phase=WorkflowPhase.IDLE,
            tier=Tier.BALANCED,
        )
        self._pipeline_ctx: Any = None  # PipelineContext 引用，由 orchestrator 注入
        self._frozen_checkpoint: Optional[WorkflowCheckpoint] = None  # 恢复时冻结的快照
        self.transition_history: List[TransitionResult] = []
        self._transition_handlers: Dict[WorkflowPhase, Callable] = {}

    @property
    def checkpoint(self) -> WorkflowCheckpoint:
        """获取检查点。

        优先级：
        1. 如果有冻结快照（load_checkpoint 恢复后），返回冻结快照
        2. 如果有 PipelineContext 引用，实时投影
        3. 返回底层 _checkpoint
        """
        if self._frozen_checkpoint is not None:
            return self._frozen_checkpoint
        if self._pipeline_ctx is not None:
            return self._pipeline_ctx.to_checkpoint(
                current_phase=self.current_phase,
                tier=self._pipeline_ctx._infer_tier(),
            )
        return self._checkpoint

    @checkpoint.setter
    def checkpoint(self, value: WorkflowCheckpoint) -> None:
        """设置底层 checkpoint（用于 load_checkpoint 从磁盘恢复）。

        设置后自动冻结检查点，防止实时投影覆盖恢复后的数据。
        调用 set_pipeline_context() 会解冻并恢复实时投影模式。
        """
        self._checkpoint = value
        self._frozen_checkpoint = value  # 冻结：恢复后的检查点不会被实时投影覆盖
        self._pipeline_ctx = None
        self.current_phase = value.phase

    def set_pipeline_context(self, ctx: Any) -> None:
        """注入 PipelineContext 引用，解冻检查点，恢复实时投影模式。

        在 orchestrator.resume_from_checkpoint() 后必须调用此方法，
        将恢复后的状态与新的 PipelineContext 绑定。
        """
        self._pipeline_ctx = ctx
        self._frozen_checkpoint = None  # 解冻：恢复实时投影模式

    # ------------------------------------------------------------------
    # 状态转换
    # ------------------------------------------------------------------

    def can_transition(self, to_phase: WorkflowPhase) -> Tuple[bool, str]:
        """检查能否从当前状态转换到目标状态"""
        key = (self.current_phase, to_phase)

        # 1. 检查是否有合法转换路径
        if key not in STATE_TRANSITIONS:
            return False, (
                f"非法状态转换: {self.current_phase.value} → {to_phase.value}。"
                f"允许的转换: {self._allowed_transitions()}"
            )

        # 2. 执行所有 Guard 条件
        guards = STATE_TRANSITIONS[key]
        for guard in guards:
            passed, reason = guard(self.checkpoint)
            if not passed:
                return False, f"Guard 条件未满足: {reason}"

        return True, ""

    def transition(self, to_phase: WorkflowPhase) -> TransitionResult:
        """执行状态转换"""
        can, reason = self.can_transition(to_phase)
        if not can:
            result = TransitionResult(
                success=False,
                from_phase=self.current_phase,
                to_phase=to_phase,
                reason=reason,
            )
            self.transition_history.append(result)
            return result

        old_phase = self.current_phase
        self.current_phase = to_phase
        self._checkpoint.phase = to_phase
        self._checkpoint.updated_at = time.strftime("%Y-%m-%dT%H:%M:%S")

        # 触发状态进入回调
        if to_phase in self._transition_handlers:
            self._transition_handlers[to_phase](self.checkpoint)

        result = TransitionResult(
            success=True,
            from_phase=old_phase,
            to_phase=to_phase,
            checkpoint=self.checkpoint,
        )
        self.transition_history.append(result)
        return result

    def force_transition(self, to_phase: WorkflowPhase) -> TransitionResult:
        """强制转换（仅用于 CANCELLED / FAILED）"""
        old_phase = self.current_phase
        self.current_phase = to_phase
        self._checkpoint.phase = to_phase
        self._checkpoint.updated_at = time.strftime("%Y-%m-%dT%H:%M:%S")

        result = TransitionResult(
            success=True,
            from_phase=old_phase,
            to_phase=to_phase,
            reason="强制转换",
            checkpoint=self.checkpoint,
        )
        self.transition_history.append(result)
        return result

    # ------------------------------------------------------------------
    # 检查点持久化
    # ------------------------------------------------------------------

    def save_checkpoint(self, name: Optional[str] = None) -> str:
        """保存当前检查点到磁盘（自动清理旧文件，最多保留 MAX_CHECKPOINTS 个）。"""
        self.CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
        filename = name or f"checkpoint_{int(time.time())}.json"
        filepath = self.CHECKPOINT_DIR / filename

        checkpoint_data = self.checkpoint.model_dump(mode="json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(checkpoint_data, f, ensure_ascii=False, indent=2, default=str)

        # 清理旧检查点文件，保留最近 MAX_CHECKPOINTS 个
        all_checkpoints = sorted(
            self.CHECKPOINT_DIR.glob("checkpoint_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        for old_file in all_checkpoints[self.MAX_CHECKPOINTS:]:
            old_file.unlink()

        return str(filepath)

    def load_checkpoint(self, name: str) -> bool:
        """从磁盘恢复检查点"""
        filepath = self.CHECKPOINT_DIR / name
        if not filepath.exists():
            return False

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.checkpoint = WorkflowCheckpoint(**data)
        self.current_phase = self.checkpoint.phase
        return True

    def list_checkpoints(self) -> List[str]:
        """列出所有保存的检查点"""
        if not self.CHECKPOINT_DIR.exists():
            return []
        return sorted(
            [f.name for f in self.CHECKPOINT_DIR.glob("checkpoint_*.json")]
        )

    # ------------------------------------------------------------------
    # 辅助方法
    # ------------------------------------------------------------------

    def _allowed_transitions(self) -> str:
        """获取当前状态允许的转换目标"""
        allowed = [
            to.value
            for (fr, to) in STATE_TRANSITIONS
            if fr == self.current_phase
        ]
        return ", ".join(allowed) if allowed else "无"

    def on_enter(self, phase: WorkflowPhase):
        """注册状态进入回调（装饰器）"""
        def decorator(func: Callable):
            self._transition_handlers[phase] = func
            return func
        return decorator

    def is_terminal(self) -> bool:
        """是否处于终态"""
        return self.current_phase in (
            WorkflowPhase.DONE,
            WorkflowPhase.CANCELLED,
            WorkflowPhase.FAILED,
        )

    def get_state_summary(self) -> Dict:
        """获取当前状态摘要"""
        return {
            "phase": self.current_phase.value,
            "is_terminal": self.is_terminal(),
            "divergence_rounds": self.checkpoint.divergence_rounds,
            "strategy_rounds": len(self.checkpoint.strategy_rounds),
            "has_task_dag": self.checkpoint.task_dag is not None,
            "execution_tasks": (
                len(self.checkpoint.execution_report.results)
                if self.checkpoint.execution_report
                else 0
            ),
            "review_count": len(self.checkpoint.review_results),
            "transitions": len(self.transition_history),
        }
