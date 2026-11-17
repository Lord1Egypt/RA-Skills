"""
并发安全测试 — 验证多次 run() 调用之间没有状态泄漏。

Phase 3 新增：
- reset() 完整性测试：确保所有状态字段被正确清理
- enable_saga=False 路径测试
- 多次 run() 不互相污染
- PipelineContext 不可变性保证
"""
import pytest
import sys
sys.path.insert(0, "..")

from schemas import UserInput, Tier, FinalReport
from orchestrator import TriangulateOrchestrator, WorkflowFailedError
from adapters import InputAdapter
from decomposer import TaskDecomposer
from dispatcher import ExecutionDispatcher
from consensus import ConsensusEngine
from renderer import ReportRenderer


class TestResetCompleteness:
    """reset() 完整性测试 — 确保所有状态被正确清理"""

    def _make_orch(self, **kwargs):
        defaults = dict(
            input_adapter=InputAdapter(),
            decomposer=TaskDecomposer(enforce_parallel=True),
            dispatcher=ExecutionDispatcher(global_timeout=30),
            consensus_engine=ConsensusEngine(),
            renderer=ReportRenderer(),
            enable_saga=True,
            enable_idempotency=True,
            enable_circuit_breaker=True,
        )
        defaults.update(kwargs)
        return TriangulateOrchestrator(**defaults)

    def test_reset_clears_pipeline_context(self):
        """reset 后 PipelineContext 回到初始状态"""
        orch = self._make_orch()
        orch.run("任务A")

        assert orch._ctx.validated_input is not None

        orch.reset()

        assert orch._ctx.validated_input is None
        assert orch._ctx.strategy_rounds == []
        assert orch._ctx.task_dag is None
        assert orch._ctx.exec_report is None
        assert orch._ctx.review_results == []
        assert orch._ctx.final_report is None
        assert orch._ctx.strategy_sessions == []
        assert orch._ctx.execution_sessions == []
        assert orch._ctx.created_sessions == []
        assert orch._ctx.degraded is False
        assert orch._ctx.divergence_rounds == 0

    def test_reset_allows_independent_runs(self):
        """reset 后两次 run 互不影响"""
        orch = self._make_orch()
        report1 = orch.run("任务A")
        orch.reset()
        report2 = orch.run("任务B")

        assert "任务A" in report1.task_description
        assert "任务B" in report2.task_description
        assert report1.task_description != report2.task_description

    def test_reset_clears_circuit_breaker(self):
        """reset 清空熔断器状态"""
        orch = self._make_orch()
        orch.signal_user_interrupt()
        assert orch.get_progress()["breaker"]["user_interrupted"] is True

        orch.reset()
        assert orch.get_progress()["breaker"]["user_interrupted"] is False

    def test_reset_clears_saga_steps(self):
        """reset 后 Saga 实例仍然可用（WorkflowUnitOfWork 不再填充 Saga steps）"""
        orch = self._make_orch(enable_saga=True)
        orch.run("任务A")

        saga = orch.get_saga()
        assert saga is not None
        # WorkflowUnitOfWork 统一事务边界，不再通过 Saga 闭包注册步骤
        # Saga 实例保留用于 orchestrator.reset() 兼容性

        orch.reset()

        saga = orch.get_saga()
        assert saga is not None
        assert len(saga.steps) == 0

    def test_multiple_runs_no_cross_contamination(self):
        """多次 run 不互相污染状态"""
        orch = self._make_orch()

        orch.run("高重要性任务")
        progress1 = orch.get_progress()

        orch.reset()

        orch.run("低重要性任务")
        progress2 = orch.get_progress()

        assert progress2["phase"] == "DONE"

    def test_reset_preserves_module_references(self):
        """reset 后模块引用保持有效"""
        orch = self._make_orch()
        orch.run("任务A")

        adapter_before = orch.input_adapter
        decomposer_before = orch.decomposer
        dispatcher_before = orch.dispatcher

        orch.reset()

        assert orch.input_adapter is adapter_before
        assert orch.decomposer is decomposer_before
        assert orch.dispatcher is dispatcher_before

    def test_no_saga_reset_clears_pipeline_context(self):
        """Phase 3: enable_saga=False 时 reset 正常清理"""
        orch = self._make_orch(enable_saga=False)
        orch.run("任务A")

        assert orch._ctx.validated_input is not None

        orch.reset()

        assert orch._ctx.validated_input is None
        assert orch._ctx.strategy_rounds == []
        assert orch._ctx.final_report is None


class TestContextImmutability:
    """PipelineContext 不可变性在 orchestrator 中的体现"""

    def _make_orch(self, **kwargs):
        defaults = dict(
            input_adapter=InputAdapter(),
            decomposer=TaskDecomposer(enforce_parallel=True),
            dispatcher=ExecutionDispatcher(global_timeout=30),
            consensus_engine=ConsensusEngine(),
            renderer=ReportRenderer(),
        )
        defaults.update(kwargs)
        return TriangulateOrchestrator(**defaults)

    def test_run_creates_new_context(self):
        """每次 run() 创建新的 PipelineContext"""
        orch = self._make_orch()

        orch.run("任务A")
        ctx_after_first = orch._ctx

        orch.reset()
        orch.run("任务B")
        ctx_after_second = orch._ctx

        assert ctx_after_first is not ctx_after_second

    def test_no_saga_run_creates_new_context(self):
        """Phase 3: enable_saga=False 时每次 run() 创建新上下文"""
        orch = self._make_orch(enable_saga=False)

        orch.run("任务A")
        ctx_after_first = orch._ctx

        orch.reset()
        orch.run("任务B")
        ctx_after_second = orch._ctx

        assert ctx_after_first is not ctx_after_second


class TestDegradedFlagConsistency:
    """降级标记一致性测试"""

    def _make_orch(self, **kwargs):
        defaults = dict(
            input_adapter=InputAdapter(),
            decomposer=TaskDecomposer(enforce_parallel=True),
            dispatcher=ExecutionDispatcher(global_timeout=30),
            consensus_engine=ConsensusEngine(),
            renderer=ReportRenderer(),
        )
        defaults.update(kwargs)
        return TriangulateOrchestrator(**defaults)

    def test_degraded_flag_in_report_matches_context(self):
        """报告中的 degraded 标记与 PipelineContext 一致"""
        orch = self._make_orch()
        report = orch.run("测试任务")

        assert report.degraded == orch._ctx.degraded

    def test_no_saga_degraded_flag_consistent(self):
        """Phase 3: enable_saga=False 时 degraded 标记一致"""
        orch = self._make_orch(enable_saga=False)
        report = orch.run("测试任务")

        assert report.degraded == orch._ctx.degraded
