"""
契约测试 — 验证所有 Schema 的边界值行为。

确保 Pydantic Schema 在合法输入时正常工作，在非法输入时正确拒绝。
这是"契约锁死"的关键：任何破坏契约的修改都会导致测试失败。
"""
import pytest
from pydantic import ValidationError

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
    ConsensusOutput,
    ConsensusVerdict,
    WorkflowPhase,
)


# ============================================================================
# UserInput 契约测试
# ============================================================================

class TestUserInput:
    """用户输入契约"""

    def test_valid_minimal_input(self):
        """最小有效输入"""
        ui = UserInput(task_description="分析数据库选型")
        assert ui.task_description == "分析数据库选型"
        assert ui.importance == 3
        assert ui.keywords == []

    def test_valid_full_input(self):
        """完整有效输入"""
        ui = UserInput(
            task_description="评估 MongoDB vs PostgreSQL 的技术选型",
            importance=4,
            keywords=["选型", "数据库"],
            preferred_templates=["T-05"],
            require_execution_layer=True,
            require_management_layer=True,
            max_total_timeout_seconds=300,
        )
        assert ui.importance == 4
        assert ui.max_total_timeout_seconds == 300

    def test_empty_task_description_rejected(self):
        """空任务描述应被拒绝"""
        with pytest.raises(ValidationError):
            UserInput(task_description="")

    def test_whitespace_task_description_rejected(self):
        """纯空白任务描述应被拒绝"""
        with pytest.raises(ValidationError):
            UserInput(task_description="   ")

    def test_importance_out_of_range_rejected(self):
        """重要性超出 1-5 应被拒绝"""
        with pytest.raises(ValidationError):
            UserInput(task_description="test", importance=0)

        with pytest.raises(ValidationError):
            UserInput(task_description="test", importance=6)

    def test_timeout_out_of_range_rejected(self):
        """超时超出范围应被拒绝"""
        with pytest.raises(ValidationError):
            UserInput(task_description="test", max_total_timeout_seconds=30)

        with pytest.raises(ValidationError):
            UserInput(task_description="test", max_total_timeout_seconds=7200)


# ============================================================================
# DecisionResult 契约测试
# ============================================================================

class TestDecisionResult:
    """决策结果契约"""

    def test_valid_decision(self):
        """有效决策"""
        dr = DecisionResult(
            agent_id="A",
            importance=4,
            config=Tier.FULL,
            reasoning="需要进行全面评估以确保架构决策的正确性",
            risks=["可能过度工程化"],
            top_findings=["PostgreSQL 更适合事务场景", "MongoDB 更适合文档存储"],
            confidence=0.85,
        )
        assert dr.agent_id == "A"
        assert len(dr.top_findings) == 2

    def test_invalid_agent_id_rejected(self):
        """非法 agent_id 应被拒绝"""
        with pytest.raises(ValidationError):
            DecisionResult(
                agent_id="D",  # 只有 A/B/C
                importance=3,
                config=Tier.BALANCED,
                reasoning="test reasoning with enough length",
                top_findings=["finding 1"],
                confidence=0.5,
            )

    def test_short_reasoning_rejected(self):
        """过短的 reasoning 应被拒绝"""
        with pytest.raises(ValidationError):
            DecisionResult(
                agent_id="A",
                importance=3,
                config=Tier.BALANCED,
                reasoning="短",  # < 10 字符
                top_findings=["finding 1"],
                confidence=0.5,
            )

    def test_empty_top_findings_rejected(self):
        """空 top_findings 应被拒绝"""
        with pytest.raises(ValidationError):
            DecisionResult(
                agent_id="A",
                importance=3,
                config=Tier.BALANCED,
                reasoning="足够长的推理理由说明",
                top_findings=[],
                confidence=0.5,
            )

    def test_whitespace_top_findings_rejected(self):
        """纯空白 top_findings 应被拒绝"""
        with pytest.raises(ValidationError):
            DecisionResult(
                agent_id="A",
                importance=3,
                config=Tier.BALANCED,
                reasoning="足够长的推理理由说明",
                top_findings=["   "],
                confidence=0.5,
            )

    def test_confidence_out_of_range_rejected(self):
        """置信度超出 0-1 应被拒绝"""
        with pytest.raises(ValidationError):
            DecisionResult(
                agent_id="A",
                importance=3,
                config=Tier.BALANCED,
                reasoning="足够长的推理理由说明",
                top_findings=["f1"],
                confidence=1.5,
            )

    def test_too_many_top_findings_rejected(self):
        """超过 5 条 top_findings 应被拒绝"""
        with pytest.raises(ValidationError):
            DecisionResult(
                agent_id="A",
                importance=3,
                config=Tier.BALANCED,
                reasoning="足够长的推理理由说明",
                top_findings=["f1", "f2", "f3", "f4", "f5", "f6"],
                confidence=0.5,
            )


# ============================================================================
# SubTask / TaskDAG 契约测试
# ============================================================================

class TestSubTask:
    """子任务契约"""

    def test_valid_subtask(self):
        """有效子任务"""
        st = SubTask(
            id="subtask-01",
            goal="分析数据库性能",
            completion_criteria="完成性能对比分析",
            output_format="Markdown 表格",
        )
        assert st.token_budget == 4000
        assert st.timeout_seconds == 300

    def test_invalid_id_pattern_rejected(self):
        """非法 ID 格式应被拒绝"""
        with pytest.raises(ValidationError):
            SubTask(
                id="bad id",  # 空格不允许
                goal="test",
                completion_criteria="done",
                output_format="text",
            )

    def test_self_dependency_rejected(self):
        """自依赖应被拒绝"""
        with pytest.raises(ValidationError):
            SubTask(
                id="subtask-01",
                goal="test",
                completion_criteria="done",
                output_format="text",
                depends_on=["subtask-01"],  # 依赖自己
            )

    def test_token_budget_out_of_range_rejected(self):
        """Token 预算超出范围应被拒绝"""
        with pytest.raises(ValidationError):
            SubTask(
                id="subtask-01",
                goal="test",
                completion_criteria="done",
                output_format="text",
                token_budget=50,  # < 100
            )


class TestTaskDAG:
    """TaskDAG 契约"""

    def test_valid_dag(self):
        """有效 DAG"""
        dag = TaskDAG(subtasks=[
            SubTask(
                id="subtask-01",
                goal="分析",
                completion_criteria="done",
                output_format="text",
            ),
            SubTask(
                id="subtask-02",
                goal="对比",
                completion_criteria="done",
                output_format="text",
            ),
        ])
        assert len(dag.subtasks) == 2

    def test_circular_dependency_rejected(self):
        """循环依赖应被拒绝"""
        with pytest.raises(ValidationError):
            TaskDAG(subtasks=[
                SubTask(
                    id="subtask-01",
                    goal="A",
                    completion_criteria="done",
                    output_format="text",
                    depends_on=["subtask-02"],
                ),
                SubTask(
                    id="subtask-02",
                    goal="B",
                    completion_criteria="done",
                    output_format="text",
                    depends_on=["subtask-01"],
                ),
            ])

    def test_missing_dependency_rejected(self):
        """引用不存在的依赖应被拒绝"""
        with pytest.raises(ValidationError):
            TaskDAG(subtasks=[
                SubTask(
                    id="subtask-01",
                    goal="A",
                    completion_criteria="done",
                    output_format="text",
                    depends_on=["subtask-nonexistent"],
                ),
            ])

    def test_topological_sort_valid(self):
        """拓扑排序正确"""
        dag = TaskDAG(subtasks=[
            SubTask(
                id="subtask-01", goal="A",
                completion_criteria="done", output_format="text",
            ),
            SubTask(
                id="subtask-02", goal="B",
                completion_criteria="done", output_format="text",
                depends_on=["subtask-01"],
            ),
            SubTask(
                id="subtask-03", goal="C",
                completion_criteria="done", output_format="text",
                depends_on=["subtask-01"],
            ),
        ])
        sorted_ids = dag._topological_sort()
        assert sorted_ids[0] == "subtask-01"
        assert "subtask-02" in sorted_ids[1:]
        assert "subtask-03" in sorted_ids[1:]


# ============================================================================
# ExecutionResult / ExecutionReport 契约测试
# ============================================================================

class TestExecutionResult:
    """执行结果契约"""

    def test_success_result(self):
        """成功结果"""
        er = ExecutionResult(
            subtask_id="subtask-01",
            status=ExecutionStatus.SUCCESS,
            output="分析完成",
            duration_seconds=2.5,
        )
        assert er.status == ExecutionStatus.SUCCESS
        assert er.retry_count == 0

    def test_failure_result(self):
        """失败结果"""
        er = ExecutionResult(
            subtask_id="subtask-01",
            status=ExecutionStatus.FAILED,
            error="连接超时",
            retry_count=3,
        )
        assert er.status == ExecutionStatus.FAILED
        assert er.retry_count == 3

    def test_negative_tokens_rejected(self):
        """负数 tokens 应被拒绝"""
        with pytest.raises(ValidationError):
            ExecutionResult(
                subtask_id="subtask-01",
                status=ExecutionStatus.SUCCESS,
                tokens_used=-1,
            )


class TestExecutionReport:
    """执行报告契约"""

    def test_failure_rate_calculation(self):
        """失败率计算"""
        report = ExecutionReport(
            total_tasks=10,
            completed=6,
            failed=2,
            timed_out=2,
            cancelled=0,
            results=[],
        )
        assert report.failure_rate == 0.4  # (2+2)/10

    def test_zero_tasks(self):
        """零任务时失败率为 0"""
        report = ExecutionReport(
            total_tasks=0,
            completed=0, failed=0, timed_out=0, cancelled=0,
            results=[],
        )
        assert report.failure_rate == 0.0


# ============================================================================
# FinalReport 契约测试
# ============================================================================

class TestFinalReport:
    """最终报告契约"""

    def test_valid_report(self):
        """有效报告"""
        report = FinalReport(
            task_description="分析数据库选型",
            tier=Tier.FULL,
            executor_count=3,
            decision_maker_count=3,
            core_conclusions=["PostgreSQL 更适合事务场景"],
        )
        assert len(report.core_conclusions) == 1

    def test_max_conclusions_enforced(self):
        """最多 5 条核心结论"""
        with pytest.raises(ValidationError):
            FinalReport(
                task_description="test",
                tier=Tier.BALANCED,
                executor_count=1,
                decision_maker_count=1,
                core_conclusions=["1", "2", "3", "4", "5", "6"],
            )


# ============================================================================
# 边界值测试
# ============================================================================

class TestBoundaryValues:
    """边界值测试 — 确保极端值被正确处理"""

    def test_max_length_task_description(self):
        """最大长度任务描述"""
        desc = "A" * 5000
        ui = UserInput(task_description=desc)
        assert len(ui.task_description) == 5000

    def test_max_length_reasoning(self):
        """最大长度推理"""
        reasoning = "A" * 2000
        dr = DecisionResult(
            agent_id="A", importance=3, config=Tier.BALANCED,
            reasoning=reasoning,
            top_findings=["test"],
            confidence=0.5,
        )
        assert len(dr.reasoning) == 2000

    def test_min_token_budget(self):
        """最小 Token 预算"""
        st = SubTask(
            id="subtask-min",
            goal="test",
            completion_criteria="done",
            output_format="text",
            token_budget=100,
        )
        assert st.token_budget == 100

    def test_min_timeout(self):
        """最小超时"""
        st = SubTask(
            id="subtask-min",
            goal="test",
            completion_criteria="done",
            output_format="text",
            timeout_seconds=30,
        )
        assert st.timeout_seconds == 30

    def test_importance_boundaries(self):
        """重要性边界值"""
        # 1 是有效值
        ui1 = UserInput(task_description="test", importance=1)
        assert ui1.importance == 1

        # 5 是有效值
        ui5 = UserInput(task_description="test", importance=5)
        assert ui5.importance == 5

        # 0 无效
        with pytest.raises(ValidationError):
            UserInput(task_description="test", importance=0)

        # 6 无效
        with pytest.raises(ValidationError):
            UserInput(task_description="test", importance=6)
