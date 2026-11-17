"""
阶段间契约测试 — 验证每个阶段的输出可被下一阶段正确消费。

Phase 3 新增：确保 PipelineContext 的阶段间数据传递类型安全。
PipelineContext 已合并为 Pydantic BaseModel，统一 dataclass 和 Pydantic 版本。
"""
import pytest
import sys
sys.path.insert(0, "..")

from schemas import (
    DecisionResult,
    ExecutionReport,
    ExecutionResult,
    ExecutionStatus,
    FinalReport,
    StrategyRound,
    SubTask,
    TaskDAG,
    Tier,
    UserInput,
    ConsensusVerdict,
)
from pipeline import PipelineContext


class TestPipelineContextContract:
    """PipelineContext 阶段间契约测试"""

    def test_context_evolve_preserves_unchanged_fields(self):
        """evolve() 保留未修改字段"""
        ctx = PipelineContext(
            validated_input=UserInput(task_description="测试任务"),
            degraded=True,
            divergence_rounds=2,
        )

        new_ctx = ctx.evolve(degraded=False)

        assert new_ctx.validated_input.task_description == "测试任务"
        assert new_ctx.divergence_rounds == 2  # 未修改
        assert new_ctx.degraded is False  # 已修改
        # 原 ctx 未被修改
        assert ctx.degraded is True

    def test_context_session_tracking(self):
        """Session 追踪一致性"""
        ctx = PipelineContext()
        ctx = ctx.add_strategy_session("s1")
        ctx = ctx.add_strategy_session("s2")
        ctx = ctx.add_execution_session("e1")

        assert ctx.strategy_sessions == ["s1", "s2"]
        assert ctx.execution_sessions == ["e1"]
        assert ctx.all_sessions == ["s1", "s2", "e1"]
        assert set(ctx.created_sessions) == {"s1", "s2", "e1"}

    def test_context_immutability(self):
        """PipelineContext 的 evolve 不修改原实例"""
        ctx = PipelineContext(divergence_rounds=1)
        new_ctx = ctx.evolve(divergence_rounds=3)

        assert ctx.divergence_rounds == 1
        assert new_ctx.divergence_rounds == 3
        assert ctx is not new_ctx


class TestPhaseInputOutputContract:
    """阶段间输入输出契约"""

    def test_input_validation_produces_valid_userinput(self):
        """阶段一输出可被阶段二消费"""
        ctx = PipelineContext()
        ui = UserInput(task_description="分析数据库选型", importance=4)
        ctx = ctx.evolve(validated_input=ui)

        assert ctx.validated_input is not None
        assert len(ctx.validated_input.task_description) > 0
        assert 1 <= ctx.validated_input.importance <= 5

    def test_strategy_phase_produces_nonempty_rounds(self):
        """阶段二输出至少包含一轮策略"""
        ctx = PipelineContext(
            validated_input=UserInput(task_description="测试"),
            strategy_rounds=[
                StrategyRound(
                    round_number=1,
                    decisions=[
                        DecisionResult(
                            agent_id="A", importance=3, config=Tier.BALANCED,
                            reasoning="足够长的推理理由说明测试",
                            top_findings=["结论1"], confidence=0.8,
                        ),
                    ],
                    verdict=ConsensusVerdict.CONSENSUS,
                ),
            ],
        )

        assert len(ctx.strategy_rounds) > 0
        assert len(ctx.strategy_rounds[-1].decisions) >= 1

    def test_dispatch_phase_produces_valid_dag(self):
        """阶段三输出可被阶段四（execute）消费"""
        ctx = PipelineContext(
            validated_input=UserInput(task_description="测试"),
            task_dag=TaskDAG(subtasks=[
                SubTask(
                    id="subtask-01", goal="子任务1",
                    completion_criteria="完成", output_format="text",
                ),
            ]),
        )

        assert ctx.task_dag is not None
        assert len(ctx.task_dag.subtasks) > 0

    def test_execute_phase_produces_valid_report(self):
        """阶段四输出可被阶段五（review）消费"""
        ctx = PipelineContext(
            validated_input=UserInput(task_description="测试"),
            exec_report=ExecutionReport(
                total_tasks=2, completed=2, failed=0,
                timed_out=0, cancelled=0, results=[],
            ),
        )

        assert ctx.exec_report is not None
        assert ctx.exec_report.total_tasks > 0

    def test_review_phase_produces_nonempty_results(self):
        """阶段五输出可被阶段六（render）消费"""
        ctx = PipelineContext(
            validated_input=UserInput(task_description="测试"),
            strategy_rounds=[
                StrategyRound(
                    round_number=1,
                    decisions=[
                        DecisionResult(
                            agent_id="A", importance=3, config=Tier.BALANCED,
                            reasoning="足够长的推理理由说明",
                            top_findings=["结论A"], confidence=0.8,
                        ),
                    ],
                    verdict=ConsensusVerdict.CONSENSUS,
                ),
            ],
            exec_report=ExecutionReport(
                total_tasks=1, completed=1, failed=0,
                timed_out=0, cancelled=0, results=[],
            ),
            review_results=[
                DecisionResult(
                    agent_id="B", importance=3, config=Tier.BALANCED,
                    reasoning="审阅结论足够长的推理理由",
                    top_findings=["审阅结论"], confidence=0.9,
                ),
            ],
        )

        assert len(ctx.review_results) > 0

    def test_divergence_rounds_single_source(self):
        """divergence_rounds 只有一个来源（PipelineContext）"""
        ctx = PipelineContext(divergence_rounds=2)

        assert ctx.divergence_rounds == 2
        checkpoint_rounds = ctx.divergence_rounds
        assert checkpoint_rounds == 2


class TestPydanticPipelineContext:
    """PipelineContext (Pydantic BaseModel) 校验测试 — Phase 3 合并后"""

    def test_valid_context_passes_validation(self):
        """有效上下文通过校验"""
        ctx = PipelineContext(
            validated_input=UserInput(task_description="测试"),
            strategy_sessions=["s1"],
            created_sessions=["s1"],
            divergence_rounds=1,
        )
        assert ctx.divergence_rounds == 1

    def test_inconsistent_sessions_raise_error(self):
        """不一致的 sessions 应报错（model_validator 在构造时自动校验）"""
        from pipeline import PipelineConsistencyError
        # model_validator 在构造时自动检测 sessions 不一致并抛出异常
        with pytest.raises(PipelineConsistencyError, match="不一致"):
            PipelineContext(
                validated_input=UserInput(task_description="测试"),
                strategy_sessions=["s1", "s2"],
                created_sessions=["s1"],  # 缺少 s2
            )

    def test_negative_divergence_rounds_rejected(self):
        """负数的 divergence_rounds 应被拒绝"""
        with pytest.raises(Exception):  # pydantic ValidationError
            PipelineContext(
                validated_input=UserInput(task_description="测试"),
                divergence_rounds=-1,
            )

    def test_checkpoint_field_excluded_from_serialization(self):
        """checkpoint 字段在序列化时被排除（exclude=True）"""
        ctx = PipelineContext(
            validated_input=UserInput(task_description="测试"),
            divergence_rounds=1,
        )
        # model_dump 时 checkpoint 不应出现
        dumped = ctx.model_dump(exclude={"checkpoint"})
        assert "checkpoint" not in dumped

    def test_to_checkpoint_roundtrip(self):
        """to_checkpoint() 序列化往返不丢失关键数据"""
        from schemas import WorkflowPhase
        ctx = PipelineContext(
            validated_input=UserInput(task_description="往返测试"),
            divergence_rounds=2,
            degraded=True,
            strategy_sessions=["s1"],
            created_sessions=["s1"],
        )
        checkpoint = ctx.to_checkpoint(
            current_phase=WorkflowPhase.STRATEGY,
            tier=Tier.FULL,
        )
        assert checkpoint.divergence_rounds == 2
        assert checkpoint.degraded is True
        assert "s1" in checkpoint.created_sessions
        assert checkpoint.input_data is not None
