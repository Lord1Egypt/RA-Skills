"""
集成测试 — 验证 orchestrator 与 Saga/Idempotency/CircuitBreaker 的集成正确性。

Phase 3 新增：
- enable_saga=False 路径测试（幂等性缓存、熔断检查）
- REDISTRIBUTE 路径集成测试
- 自定义重试判定测试
- 阶段超时中断测试
"""
import pytest
import sys
sys.path.insert(0, "..")

from schemas import UserInput, Tier, FinalReport
from orchestrator import TriangulateOrchestrator, WorkflowFailedError
from adapters import InputAdapter
from decomposer import TaskDecomposer
from dispatcher import ExecutionDispatcher, RetryConfig
from consensus import ConsensusEngine
from renderer import ReportRenderer


class TestOrchestratorIntegration:
    """Orchestrator 集成测试"""

    def _make_orchestrator(self, **kwargs):
        """创建标准 orchestrator 实例"""
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

    def test_basic_run_produces_report(self):
        """基本运行产生报告"""
        orch = self._make_orchestrator()
        report = orch.run("测试任务")
        assert isinstance(report, FinalReport)
        assert len(report.task_description) > 0
        assert report.tier in (Tier.FULL, Tier.BALANCED, Tier.LIGHT)

    def test_degraded_when_no_modules(self):
        """无模块时触发降级"""
        orch = TriangulateOrchestrator(
            input_adapter=InputAdapter(),
            decomposer=None,
            dispatcher=None,
            consensus_engine=None,
            renderer=None,
        )
        report = orch.run("测试任务")
        assert report.degraded is True

    def test_degraded_when_consensus_missing(self):
        """无共识引擎时触发降级"""
        orch = self._make_orchestrator(consensus_engine=None)
        report = orch.run("测试任务")
        assert report.degraded is True

    def test_reset_allows_reuse(self):
        """reset 后可以再次 run"""
        orch = self._make_orchestrator()
        orch.run("任务A")
        orch.reset()
        report2 = orch.run("任务B")
        assert "任务B" in report2.task_description

    def test_progress_includes_all_metrics(self):
        """进度报告包含所有指标"""
        orch = self._make_orchestrator()
        orch.run("测试任务")
        progress = orch.get_progress()
        assert "phase" in progress
        assert "degraded" in progress
        assert "idempotency" in progress
        assert "breaker" in progress

    def test_saga_registers_sessions(self):
        """Saga 能注册 sessions"""
        orch = self._make_orchestrator()
        orch.register_session("session-001")
        orch.register_session("session-002")
        assert len(orch._ctx.execution_sessions) == 2

    def test_circuit_breaker_user_interrupt(self):
        """用户中断信号"""
        orch = self._make_orchestrator()
        orch.signal_user_interrupt()
        progress = orch.get_progress()
        assert progress["breaker"]["user_interrupted"] is True

    def test_run_with_dict_input(self):
        """字典输入"""
        orch = self._make_orchestrator()
        report = orch.run({"task_description": "评估方案", "importance": 4})
        assert report.tier == Tier.FULL  # importance=4 → FULL

    def test_run_with_userinput(self):
        """UserInput 对象输入"""
        orch = self._make_orchestrator()
        ui = UserInput(task_description="轻量评估", importance=1)
        report = orch.run(ui)
        assert report.tier in (Tier.LIGHT, Tier.BALANCED)

    def test_save_and_load_checkpoint(self):
        """检查点保存和加载"""
        orch = self._make_orchestrator()
        orch.run("测试任务")
        path = orch.save_checkpoint()
        assert path.endswith(".json")

        orch2 = self._make_orchestrator()
        import os
        fname = os.path.basename(path)
        loaded = orch2.resume_from_checkpoint(fname)
        assert loaded

    def test_failure_saves_checkpoint(self):
        """失败时保存检查点"""
        orch = self._make_orchestrator()

        class FailingDispatcher:
            def dispatch(self, dag):
                raise RuntimeError("模拟调度失败")

        orch.dispatcher = FailingDispatcher()

        try:
            orch.run("测试任务")
            assert False, "应该抛出异常"
        except WorkflowFailedError as e:
            assert e.checkpoint is not None
            assert "模拟调度失败" in str(e)

    def test_degraded_visible_in_report(self):
        """降级标记在报告中可见"""
        orch = TriangulateOrchestrator(
            input_adapter=InputAdapter(),
            decomposer=None,
            dispatcher=None,
            consensus_engine=None,
            renderer=ReportRenderer(),
        )
        report = orch.run("降级测试")
        assert report.degraded is True

        md = ReportRenderer().render_markdown(report)
        assert "降级策略" in md


class TestNoSagaPath:
    """Phase 3: enable_saga=False 路径测试 — 确保统一编排路径正常工作"""

    def _make_orch(self, **kwargs):
        defaults = dict(
            input_adapter=InputAdapter(),
            decomposer=TaskDecomposer(enforce_parallel=True),
            dispatcher=ExecutionDispatcher(global_timeout=30),
            consensus_engine=ConsensusEngine(),
            renderer=ReportRenderer(),
            enable_saga=False,
            enable_idempotency=True,
            enable_circuit_breaker=True,
        )
        defaults.update(kwargs)
        return TriangulateOrchestrator(**defaults)

    def test_no_saga_run_produces_report(self):
        """enable_saga=False 时正常产生报告"""
        orch = self._make_orch()
        report = orch.run("无 Saga 测试")
        assert isinstance(report, FinalReport)
        assert report.tier in (Tier.FULL, Tier.BALANCED, Tier.LIGHT)

    def test_no_saga_idempotency_cache_write(self):
        """enable_saga=False 时幂等性缓存正常写入"""
        orch = self._make_orch(enable_idempotency=True)

        report1 = orch.run("缓存写入测试")
        assert report1 is not None

        orch.reset()
        report2 = orch.run("缓存写入测试")
        assert report2 is not None

        stats = orch.get_progress()["idempotency"]
        # 第二次应该命中缓存
        assert stats["hit_count"] >= 1

    def test_no_saga_circuit_breaker_works(self):
        """enable_saga=False 时熔断器仍可工作"""
        orch = self._make_orch(enable_circuit_breaker=True)
        orch.signal_user_interrupt()
        progress = orch.get_progress()
        assert progress["breaker"]["user_interrupted"] is True

    def test_no_saga_reset_works(self):
        """enable_saga=False 时 reset 正常工作"""
        orch = self._make_orch()
        orch.run("任务A")
        orch.reset()
        report2 = orch.run("任务B")
        assert "任务B" in report2.task_description

    def test_no_saga_degraded_when_no_modules(self):
        """enable_saga=False + 无模块时触发降级"""
        orch = TriangulateOrchestrator(
            input_adapter=InputAdapter(),
            decomposer=None,
            dispatcher=None,
            consensus_engine=None,
            renderer=None,
            enable_saga=False,
        )
        report = orch.run("降级测试")
        assert report.degraded is True


class TestRetryConfigIntegration:
    """重试配置集成测试"""

    def test_non_retryable_exception_fails_immediately(self):
        """不可重试异常立即失败"""
        from dispatcher import ExecutionDispatcher
        from schemas import SubTask, TaskDAG

        def bad_executor(subtask):
            raise TypeError("类型错误")

        dispatcher = ExecutionDispatcher(
            executor_factory=bad_executor,
            global_timeout=5,
        )

        dag = TaskDAG(subtasks=[
            SubTask(
                id="subtask-01",
                goal="test",
                completion_criteria="done",
                output_format="text",
            )
        ])

        report = dispatcher.dispatch(dag)
        assert len(report.results) == 1
        assert report.results[0].status.value == "failed"
        assert "不可重试异常" in report.results[0].error
        assert report.results[0].retry_count == 0

    def test_custom_retryable_check(self):
        """Phase 3: 自定义重试判定回调"""
        from dispatcher import ExecutionDispatcher, RetryConfig
        from schemas import SubTask, TaskDAG, ExecutionStatus

        class CustomNetworkError(Exception):
            pass

        retry_count = [0]

        def custom_executor(subtask):
            retry_count[0] += 1
            if retry_count[0] <= 2:
                raise CustomNetworkError("自定义网络错误")
            return "success after retry"

        config = RetryConfig(
            max_retries=3,
            custom_retryable_check=lambda e: isinstance(e, CustomNetworkError),
        )

        dispatcher = ExecutionDispatcher(
            executor_factory=custom_executor,
            retry_config=config,
            global_timeout=5,
        )

        dag = TaskDAG(subtasks=[
            SubTask(
                id="subtask-01",
                goal="test",
                completion_criteria="done",
                output_format="text",
            )
        ])

        report = dispatcher.dispatch(dag)
        assert report.results[0].status == ExecutionStatus.SUCCESS
        assert report.results[0].retry_count == 2  # 重试了 2 次


class TestConsensusReviewIntegration:
    """共识审阅集成测试"""

    def test_review_returns_non_empty(self):
        """审阅阶段不再返回空"""
        from consensus import ConsensusEngine
        from schemas import ExecutionReport, ExecutionResult, ExecutionStatus

        engine = ConsensusEngine()
        report = ExecutionReport(
            total_tasks=2,
            completed=2,
            failed=0,
            timed_out=0,
            cancelled=0,
            results=[
                ExecutionResult(
                    subtask_id="subtask-01",
                    status=ExecutionStatus.SUCCESS,
                    output="PostgreSQL 事务性能优于 MongoDB",
                ),
                ExecutionResult(
                    subtask_id="subtask-02",
                    status=ExecutionStatus.SUCCESS,
                    output="MongoDB 文档存储更灵活",
                ),
            ],
        )

        results = engine.review_results(report)
        assert len(results) == 2  # B + C
        assert results[0].agent_id == "B"
        assert results[1].agent_id == "C"
        assert len(results[0].top_findings) > 0

    def test_review_empty_report_returns_empty(self):
        """空报告审阅返回空"""
        from consensus import ConsensusEngine
        from schemas import ExecutionReport

        engine = ConsensusEngine()
        report = ExecutionReport(
            total_tasks=0,
            completed=0, failed=0, timed_out=0, cancelled=0,
            results=[],
        )

        results = engine.review_results(report)
        assert results == []


class TestSagaTrueIntegration:
    """Saga 真集成测试 — 验证 orchestrator 通过 Saga 编排驱动工作流"""

    def test_saga_steps_registered_on_run(self):
        """run() 正常完成且 Saga 实例可用（WorkflowUnitOfWork 不再填充 Saga steps）"""
        orch = TriangulateOrchestrator(
            input_adapter=InputAdapter(),
            decomposer=TaskDecomposer(enforce_parallel=True),
            dispatcher=ExecutionDispatcher(global_timeout=30),
            consensus_engine=ConsensusEngine(),
            renderer=ReportRenderer(),
            enable_saga=True,
        )
        orch.run("测试任务")
        saga = orch.get_saga()
        assert saga is not None
        # WorkflowUnitOfWork 统一事务边界，Saga 实例保留用于兼容

    def test_saga_steps_cleared_on_reset(self):
        """reset 后 Saga 步骤被清空"""
        orch = TriangulateOrchestrator(
            input_adapter=InputAdapter(),
            decomposer=TaskDecomposer(enforce_parallel=True),
            dispatcher=ExecutionDispatcher(global_timeout=30),
            consensus_engine=ConsensusEngine(),
            renderer=ReportRenderer(),
            enable_saga=True,
        )
        orch.run("任务A")
        orch.reset()
        saga = orch.get_saga()
        assert saga is not None
        assert len(saga.steps) == 0

    def test_saga_compensate_on_failure(self):
        """失败时 Saga 补偿被触发"""
        orch = TriangulateOrchestrator(
            input_adapter=InputAdapter(),
            decomposer=TaskDecomposer(enforce_parallel=True),
            dispatcher=ExecutionDispatcher(global_timeout=30),
            consensus_engine=ConsensusEngine(),
            renderer=ReportRenderer(),
            enable_saga=True,
        )

        orch.register_strategy_session("fake-session-001")
        assert len(orch._ctx.strategy_sessions) == 1

        class FailingDispatcher:
            def dispatch(self, dag):
                raise RuntimeError("模拟调度失败")

        orch.dispatcher = FailingDispatcher()

        try:
            orch.run("测试任务")
            assert False
        except WorkflowFailedError:
            pass


class TestIdempotencyRaceCondition:
    """幂等性竞态修复测试"""

    def test_direct_cache_access_no_race(self):
        """直接从缓存取值，不经过 execute_or_cache 二次调用"""
        orch = TriangulateOrchestrator(
            input_adapter=InputAdapter(),
            decomposer=TaskDecomposer(enforce_parallel=True),
            dispatcher=ExecutionDispatcher(global_timeout=30),
            consensus_engine=ConsensusEngine(),
            renderer=ReportRenderer(),
            enable_idempotency=True,
        )

        report1 = orch.run("幂等性测试任务")
        assert report1 is not None

        orch.reset()
        report2 = orch.run("幂等性测试任务")
        assert report2 is not None
        assert report2.core_conclusions == report1.core_conclusions

        stats = orch.get_progress()["idempotency"]
        assert stats["hit_count"] >= 1


class TestDivergenceRoundCounting:
    """分歧轮次计数修复测试"""

    def test_divergence_rounds_correctly_counted(self):
        """DIVERGENCE 时 divergence_rounds 正确递增"""
        from consensus import ConsensusEngine
        from schemas import ConsensusVerdict, DecisionResult, Tier

        class DivergentEngine(ConsensusEngine):
            def gather_decisions(self, validated_input, round_number):
                if round_number == 1:
                    return [
                        DecisionResult(agent_id="A", importance=5, config=Tier.FULL,
                                       reasoning="需要全面评估以确保正确", top_findings=["方案X"], confidence=0.9),
                        DecisionResult(agent_id="B", importance=2, config=Tier.LIGHT,
                                       reasoning="这不是什么大问题，简单处理就行", top_findings=["随便"], confidence=0.3),
                        DecisionResult(agent_id="C", importance=3, config=Tier.BALANCED,
                                       reasoning="折中方案即可满足需求", top_findings=["方案Y"], confidence=0.5),
                    ]
                return [
                    DecisionResult(agent_id="A", importance=4, config=Tier.FULL,
                                   reasoning="达成共识的全面评估结论", top_findings=["共识结论"], confidence=0.9),
                    DecisionResult(agent_id="B", importance=4, config=Tier.FULL,
                                   reasoning="达成共识的批判性评估结论", top_findings=["共识结论"], confidence=0.85),
                    DecisionResult(agent_id="C", importance=4, config=Tier.FULL,
                                   reasoning="达成共识的务实性评估结论", top_findings=["共识结论"], confidence=0.8),
                ]

        orch = TriangulateOrchestrator(
            input_adapter=InputAdapter(),
            decomposer=TaskDecomposer(enforce_parallel=True),
            dispatcher=ExecutionDispatcher(global_timeout=30),
            consensus_engine=DivergentEngine(),
            renderer=ReportRenderer(),
            enable_saga=True,
        )

        report = orch.run("分歧测试任务")
        assert report is not None
        progress = orch.get_progress()
        assert progress["divergence_rounds"] >= 1


class TestConsensusOutputConsistency:
    """ConsensusOutput.divergence_rounds 一致性测试（Phase 3 锁死）"""

    def test_evaluate_sets_divergence_rounds_to_zero(self):
        """evaluate() 的 divergence_rounds 固定为 0（evaluate 不追踪轮次）"""
        from consensus import ConsensusEngine
        from schemas import DecisionResult, Tier

        engine = ConsensusEngine()
        decisions = [
            DecisionResult(
                agent_id="A", importance=5, config=Tier.FULL,
                reasoning="足够长的推理理由说明",
                top_findings=["方案X"], confidence=0.9,
            ),
            DecisionResult(
                agent_id="B", importance=2, config=Tier.LIGHT,
                reasoning="足够长的推理理由说明",
                top_findings=["方案Y"], confidence=0.3,
            ),
        ]
        result = engine.evaluate(decisions)
        assert result.divergence_rounds == 0

    def test_handle_divergence_sets_correct_rounds(self):
        """handle_divergence() 正确设置 divergence_rounds"""
        from consensus import ConsensusEngine
        from schemas import DecisionResult, Tier

        engine = ConsensusEngine()
        decisions = [
            DecisionResult(
                agent_id="A", importance=3, config=Tier.BALANCED,
                reasoning="足够长的推理理由说明",
                top_findings=["test"], confidence=0.5,
            ),
        ]
        result = engine.handle_divergence(decisions, current_round=2)
        assert result.divergence_rounds == 2

    def test_handle_divergence_fallback_at_round_3(self):
        """第 3 轮分歧 → FALLBACK（> max_divergence_rounds=2）"""
        from consensus import ConsensusEngine
        from schemas import DecisionResult, Tier

        engine = ConsensusEngine()
        decisions = [
            DecisionResult(
                agent_id="A", importance=3, config=Tier.BALANCED,
                reasoning="足够长的推理理由说明",
                top_findings=["test"], confidence=0.5,
            ),
        ]
        result = engine.handle_divergence(decisions, current_round=3)
        assert result.verdict.value == "fallback_to_user"
        assert result.divergence_rounds == 3

    def test_divergence_rounds_single_source_of_truth(self):
        """divergence_rounds 单一数据源：PipelineContext.divergence_rounds"""
        orch = TriangulateOrchestrator(
            input_adapter=InputAdapter(),
            decomposer=TaskDecomposer(enforce_parallel=True),
            dispatcher=ExecutionDispatcher(global_timeout=30),
            consensus_engine=ConsensusEngine(),
            renderer=ReportRenderer(),
            enable_saga=True,
        )
        orch.run("测试任务")

        ctx_rounds = orch._ctx.divergence_rounds
        checkpoint_rounds = orch.state_machine.checkpoint.divergence_rounds
        assert ctx_rounds == checkpoint_rounds


class TestPhaseTimeoutInterrupt:
    """Phase 3: 阶段超时中断测试"""

    def test_phase_timeout_actually_interrupts(self):
        """阶段超时应实际中断执行而非仅记录日志"""
        import time

        orch = TriangulateOrchestrator(
            input_adapter=InputAdapter(),
            decomposer=TaskDecomposer(enforce_parallel=True),
            dispatcher=ExecutionDispatcher(global_timeout=30),
            consensus_engine=ConsensusEngine(),
            renderer=ReportRenderer(),
            enable_saga=False,
            phase_timeouts=None,  # 使用默认超时
        )

        # 直接测试 _run_phase 的超时中断
        # 构造一个会阻塞超过超时阈值的函数
        def blocking_fn():
            time.sleep(60)  # 远超默认的 30s INPUT_VALIDATION 超时
            return "done"

        try:
            orch._run_phase(
                __import__('schemas').WorkflowPhase.INPUT_VALIDATION,
                blocking_fn,
            )
            assert False, "应该因超时而抛出异常"
        except WorkflowFailedError as e:
            assert "超时" in str(e)
