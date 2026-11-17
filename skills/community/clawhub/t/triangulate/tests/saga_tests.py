"""
Saga 回滚机制测试 — 验证副作用管理和回滚的正确性。
"""
import pytest
import sys
sys.path.insert(0, "..")

from saga import WorkflowSaga, SagaStep, create_triangulate_saga


class TestSagaStep:
    """Saga 单步测试"""

    def test_successful_step(self):
        """成功步骤"""
        step = SagaStep(
            name="test_step",
            action=lambda: "result",
            compensate=lambda: None,
        )
        result = step.execute()
        assert result.success
        assert result.output == "result"
        assert result.step_name == "test_step"

    def test_failed_step(self):
        """失败步骤"""
        def failing_action():
            raise ValueError("模拟失败")

        step = SagaStep(
            name="failing_step",
            action=failing_action,
            compensate=lambda: None,
        )
        result = step.execute()
        assert not result.success
        assert "模拟失败" in result.error

    def test_rollback_step(self):
        """补偿步骤"""
        rollback_called = []

        step = SagaStep(
            name="rollback_step",
            action=lambda: "ok",
            compensate=lambda: rollback_called.append(True),
        )
        result = step.rollback()
        assert result.compensated
        assert len(rollback_called) == 1


class TestWorkflowSaga:
    """Saga 编排器测试"""

    def test_all_steps_succeed(self):
        """所有步骤成功 — 不回滚"""
        execution_order = []
        rollback_order = []

        saga = WorkflowSaga()
        saga.add_step(
            name="step1",
            action=lambda: execution_order.append(1) or "r1",
            compensate=lambda: rollback_order.append(1),
        )
        saga.add_step(
            name="step2",
            action=lambda: execution_order.append(2) or "r2",
            compensate=lambda: rollback_order.append(2),
        )
        saga.add_step(
            name="step3",
            action=lambda: execution_order.append(3) or "r3",
            compensate=lambda: rollback_order.append(3),
        )

        report = saga.execute()

        assert report.success
        assert report.total_steps == 3
        assert report.successful_steps == 3
        assert report.rolled_back_steps == 0
        assert execution_order == [1, 2, 3]
        assert rollback_order == []  # 没有回滚

    def test_mid_step_failure_triggers_rollback(self):
        """中间步骤失败 — 逆序回滚"""
        execution_order = []
        rollback_order = []

        saga = WorkflowSaga()
        saga.add_step(
            name="step1",
            action=lambda: execution_order.append(1) or "r1",
            compensate=lambda: rollback_order.append(1),
        )
        saga.add_step(
            name="step2",
            action=lambda: (_ for _ in ()).throw(ValueError("step2 失败")),
            compensate=lambda: rollback_order.append(2),
        )
        saga.add_step(
            name="step3",
            action=lambda: execution_order.append(3) or "r3",
            compensate=lambda: rollback_order.append(3),
        )

        report = saga.execute()

        assert not report.success
        assert report.failed_step == "step2"
        assert report.successful_steps == 1  # step1 成功
        assert report.rolled_back_steps == 1  # step1 被回滚
        assert execution_order == [1]
        assert rollback_order == [1]  # 逆序回滚 step1

    def test_first_step_failure_no_rollback(self):
        """第一步失败 — 无需回滚"""
        rollback_order = []

        saga = WorkflowSaga()
        saga.add_step(
            name="step1",
            action=lambda: (_ for _ in ()).throw(ValueError("step1 失败")),
            compensate=lambda: rollback_order.append(1),
        )

        report = saga.execute()

        assert not report.success
        assert report.successful_steps == 0
        assert report.rolled_back_steps == 0  # 没有成功步骤需要回滚
        assert rollback_order == []

    def test_compensation_failure_does_not_block_others(self):
        """补偿失败不阻塞其他补偿"""
        rollback_order = []

        saga = WorkflowSaga()
        saga.add_step(
            name="step1",
            action=lambda: "r1",
            compensate=lambda: rollback_order.append(1),
        )
        saga.add_step(
            name="step2",
            action=lambda: "r2",
            compensate=lambda: (_ for _ in ()).throw(ValueError("补偿失败")),
        )
        saga.add_step(
            name="step3",
            action=lambda: (_ for _ in ()).throw(ValueError("step3 失败")),
            compensate=lambda: None,
        )

        report = saga.execute()

        assert not report.success
        # step1 和 step2 成功，step3 失败
        # 逆序回滚: step2 (补偿失败), step1 (补偿成功)
        assert rollback_order == [1]  # step1 补偿成功

    def test_no_steps(self):
        """空 Saga"""
        saga = WorkflowSaga()
        report = saga.execute()
        assert report.success
        assert report.total_steps == 0



class TestPrebuiltSteps:
    """通用 add_step 测试（预置方法已移除，功能由 orchestrator 内联闭包替代）"""

    def test_custom_step(self):
        """自定义步骤通过 add_step 创建"""
        saga = WorkflowSaga()
        saga.add_step(
            name="custom_validation",
            action=lambda: "validated",
            compensate=lambda: None,
            metadata={"type": "pure_computation"},
        )
        report = saga.execute()
        assert report.success
        assert report.total_steps == 1

    def test_decompose_style_step(self):
        """模拟拆解步骤"""
        saga = WorkflowSaga()
        saga.add_step(
            name="decompose",
            action=lambda: "dag",
            compensate=lambda: None,
            metadata={"type": "pure_computation"},
        )
        report = saga.execute()
        assert report.success


class TestIdempotentRollback:
    """幂等回滚测试 — 验证多次 rollback 只执行一次补偿"""

    def test_double_rollback_only_compensates_once(self):
        """双重回滚只补偿一次（Phase 1 修复）"""
        compensate_count = [0]

        step = SagaStep(
            name="idempotent_step",
            action=lambda: "ok",
            compensate=lambda: compensate_count.__setitem__(0, compensate_count[0] + 1),
        )
        step.execute()

        # 第一次 rollback
        result1 = step.rollback()
        assert result1.compensated
        assert compensate_count[0] == 1

        # 第二次 rollback — 应该跳过
        result2 = step.rollback()
        assert result2.compensated
        assert compensate_count[0] == 1  # 仍然是 1，未重复执行

    def test_rollback_before_execute_is_safe(self):
        """未执行就回滚是安全的"""
        compensate_count = [0]

        step = SagaStep(
            name="not_executed",
            action=lambda: "ok",
            compensate=lambda: compensate_count.__setitem__(0, compensate_count[0] + 1),
        )
        # 未 execute 直接 rollback — 应该执行补偿（因为 _compensated=False）
        result = step.rollback()
        assert result.compensated
        assert compensate_count[0] == 1

    def test_execute_resets_on_new_saga_run(self):
        """每次 saga.execute() 重置补偿标记"""
        compensate_count = [0]

        saga = WorkflowSaga()
        saga.add_step(
            name="step1",
            action=lambda: "r1",
            compensate=lambda: compensate_count.__setitem__(0, compensate_count[0] + 1),
        )
        saga.add_step(
            name="step2",
            action=lambda: (_ for _ in ()).throw(ValueError("失败")),
            compensate=lambda: None,
        )

        # 第一次 execute → 失败 → 回滚 step1
        report1 = saga.execute()
        assert not report1.success
        assert compensate_count[0] == 1

        # 第二次 execute → 重置补偿标记 → 再次失败 → 再次回滚 step1
        report2 = saga.execute()
        assert not report2.success
        assert compensate_count[0] == 2  # 第二次补偿成功执行
