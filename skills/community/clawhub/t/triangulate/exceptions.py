"""
统一异常定义 — Triangulate 所有模块的唯一异常来源。

异常类型速查：
  WorkflowFailedError       — 工作流执行失败，携带检查点支持恢复
  PipelineConsistencyError  — 管线上下文 sessions 一致性校验失败
  PipelineContractError     — 阶段间输出契约违反（由 PipelineGuard 触发）
  InputValidationError      — 输入适配层校验失败
  DAGValidationError        — TaskDAG 校验失败（循环依赖/依赖缺失）
  SagaConfigurationError    — Saga 配置缺失（如 session_manager 未注入）
"""
from __future__ import annotations

from typing import Optional

from schemas import WorkflowCheckpoint


class WorkflowFailedError(Exception):
    """工作流失败异常 — 携带检查点，支持恢复。

    使用场景：orchestrator.run() / _run_workflow() 中任何不可恢复的错误。
    调用方可通过 e.checkpoint 获取失败时的状态快照。
    """

    def __init__(self, message: str, checkpoint: Optional[WorkflowCheckpoint] = None):
        super().__init__(message)
        self.checkpoint = checkpoint


class PipelineConsistencyError(Exception):
    """管线上下文一致性异常。

    使用场景：PipelineContext.assert_consistency() 检测到
    strategy_sessions + execution_sessions != created_sessions 时抛出。
    """
    pass


class PipelineContractError(Exception):
    """管线契约违反异常。

    使用场景：PipelineGuard 检测到阶段输出不满足下一阶段的输入契约时抛出。
    携带 stage（违反契约的阶段名）和 reason（具体原因）。
    """

    def __init__(self, stage: str, reason: str, ctx_info: Optional[str] = None):
        msg = f"阶段 '{stage}' 输出契约违反: {reason}"
        if ctx_info:
            msg += f" (上下文: {ctx_info})"
        super().__init__(msg)
        self.stage = stage
        self.reason = reason


class InputValidationError(Exception):
    """输入校验失败。

    使用场景：InputAdapter.validate() 检测到不合法输入时抛出。
    携带 raw_input 以便调试。
    """

    def __init__(self, message: str, raw_input=None):
        super().__init__(message)
        self.raw_input = raw_input


class DAGValidationError(Exception):
    """DAG 校验失败。

    使用场景：TaskDecomposer._validate_dag() 检测到循环依赖、
    依赖缺失、或并行约束违反时抛出。携带 dag 以便调试。
    """

    def __init__(self, message: str, dag=None):
        super().__init__(message)
        self.dag = dag


class SagaConfigurationError(Exception):
    """Saga 配置错误。

    使用场景：WorkflowSaga 在回滚时发现 session_manager 未注入，
    无法终止 sessions 时抛出。
    """
    pass
