# ================================ =======================
# tests/test_spin_sales.py - Spin-Sales 技能单元测试
# 使用: pytest tests/
# ================================ =======================

import sys
import os
import pytest

# 将被测模块加入路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))


class TestQuestionGenerator:
    """测试 question_generator.py"""

    def test_generate_spin_questions_returns_dict(self):
        from question_generator import generate_spin_questions
        result = generate_spin_questions("物流", "车队管理系统")
        assert isinstance(result, dict)

    def test_generate_spin_questions_has_four_stages(self):
        from question_generator import generate_spin_questions
        result = generate_spin_questions("医疗", "病历系统")
        stages = result["questions_by_stage"]
        assert "situation" in stages
        assert "problem" in stages
        assert "implication" in stages
        assert "need_payoff" in stages

    def test_each_stage_has_at_least_three_questions(self):
        from question_generator import generate_spin_questions
        result = generate_spin_questions("制造", "MES")
        for stage, qs in result["questions_by_stage"].items():
            assert len(qs) >= 3, f"{stage} 只有 {len(qs)} 个问题"

    def test_industry_and_product_are_stored(self):
        from question_generator import generate_spin_questions
        result = generate_spin_questions("物流", "WMS")
        assert result["industry"] == "物流"
        assert result["product"] == "WMS"


class TestOpening:
    """测试 opening.py"""

    def test_get_industry_context_known_industry(self):
        from opening import get_industry_context
        ctx = get_industry_context("金融科技")
        assert "pain_points" in ctx
        assert len(ctx["pain_points"]) > 0

    def test_get_industry_context_unknown_industry(self):
        from opening import get_industry_context
        ctx = get_industry_context("未知行业")
        assert "pain_points" in ctx  # 应返回默认值

    def test_generate_insightful_opener_returns_string(self):
        from opening import generate_insightful_opener
        opener = generate_insightful_opener("医疗")
        assert isinstance(opener, str)
        assert len(opener) > 20

    def test_generate_insightful_opener_contains_industry(self):
        from opening import generate_insightful_opener
        opener = generate_insightful_opener("物流")
        assert "物流" in opener or "配送" in opener

    def test_execute_opening_ritual_no_error(self):
        from opening import execute_opening_ritual
        # 只要能运行不抛异常就算通过
        try:
            execute_opening_ritual("金融科技")
        except Exception:
            pytest.fail("execute_opening_ritual 抛出了异常")


class TestStateMachine:
    """测试 demo_interview.py"""

    def test_situation_question_returns_list(self):
        from demo_interview import SpinStateMachine
        sm = SpinStateMachine()
        qs = sm.get_situation_question("物流")
        assert isinstance(qs, list)
        assert len(qs) > 0

    def test_problem_question_returns_list(self):
        from demo_interview import SpinStateMachine
        sm = SpinStateMachine()
        qs = sm.get_problem_question("医疗")
        assert isinstance(qs, list)
        assert len(qs) > 0

    def test_implication_question_returns_list(self):
        from demo_interview import SpinStateMachine
        sm = SpinStateMachine()
        qs = sm.get_implication_question("制造")
        assert isinstance(qs, list)
        assert len(qs) > 0

    def test_need_payoff_question_returns_list(self):
        from demo_interview import SpinStateMachine
        sm = SpinStateMachine()
        qs = sm.get_need_payoff_question("物流")
        assert isinstance(qs, list)
        assert len(qs) > 0

    def test_check_and_redirect_good_ratio(self):
        from demo_interview import SpinStateMachine
        sm = SpinStateMachine()
        result = sm.check_and_redirect(75.0)
        assert result is False  # ≥70% 不需调整

    def test_check_and_redirect_bad_ratio(self):
        from demo_interview import SpinStateMachine
        sm = SpinStateMachine()
        result = sm.check_and_redirect(50.0)
        assert result is True  # <70% 需要调整

    def test_generate_action_plan_has_milestones(self):
        from demo_interview import SpinStateMachine
        sm = SpinStateMachine()
        plan = sm.generate_action_plan()
        assert "milestones" in plan
        assert len(plan["milestones"]) > 0

    def test_generate_action_plan_has_success_criteria(self):
        from demo_interview import SpinStateMachine
        sm = SpinStateMachine()
        plan = sm.generate_action_plan()
        assert "success_criteria" in plan


class TestBasicDemo:
    """测试 basic_demo.py（集成测试）"""

    def test_run_spin_demo_no_error(self):
        from basic_demo import run_spin_demo
        try:
            run_spin_demo()
        except Exception as e:
            pytest.fail(f"run_spin_demo 抛出了异常: {e}")
