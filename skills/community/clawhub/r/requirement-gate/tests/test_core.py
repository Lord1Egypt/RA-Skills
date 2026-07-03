"""test_core.py — 基础功能测试（25 个）。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import AcceptanceCriteria, GateResult, Priority, Requirement, RequirementGate, Scope


# --- 模型默认值 / 数据结构 ---

def test_requirement_default_fields():
    """Requirement 默认值应为空字符串/空列表。"""
    req = Requirement()
    assert req.title == ""
    assert req.description == ""
    assert req.priority is None
    assert req.acceptance_criteria == []
    assert req.constraints == []
    assert req.scope.in_scope == []
    assert req.scope.out_of_scope == []


def test_acceptance_criteria_default_flags():
    """AcceptanceCriteria 默认 measurable/testable 为 False。"""
    ac = AcceptanceCriteria("some criterion")
    assert ac.measurable is False
    assert ac.testable is False


def test_scope_default_empty():
    """Scope 默认两个列表都为空。"""
    sc = Scope()
    assert sc.in_scope == []
    assert sc.out_of_scope == []


def test_gate_result_fields():
    """GateResult 字段应正确保存。"""
    r = GateResult("x", True, 1.0, "ok", {"k": 1})
    assert r.check_name == "x"
    assert r.passed is True
    assert r.score == 1.0
    assert r.message == "ok"
    assert r.details == {"k": 1}


def test_priority_enum_values():
    """Priority 枚举应有 4 个值。"""
    assert Priority.LOW.value == "low"
    assert Priority.MEDIUM.value == "medium"
    assert Priority.HIGH.value == "high"
    assert Priority.CRITICAL.value == "critical"


# --- 完整性检查 ---

def _full_requirement() -> Requirement:
    return Requirement(
        title="登录功能",
        description="实现用户名密码登录并返回 token。",
        priority=Priority.HIGH,
        acceptance_criteria=[
            AcceptanceCriteria("登录成功返回 200", measurable=True, testable=True)
        ],
        scope=Scope(in_scope=["账号密码登录"], out_of_scope=["第三方登录"]),
        constraints=["必须兼容移动端"],
    )


def test_check_completeness_passes_with_valid_requirement():
    """完整需求应通过完整性检查。"""
    gate = RequirementGate()
    result = gate.check_completeness(_full_requirement())
    assert result.check_name == "completeness"
    assert result.passed is True
    assert result.score == 1.0


def test_check_completeness_fails_without_title():
    gate = RequirementGate()
    req = _full_requirement()
    req.title = ""
    result = gate.check_completeness(req)
    assert result.passed is False
    assert "title" in result.details["failed"]


def test_check_completeness_fails_without_description():
    gate = RequirementGate()
    req = _full_requirement()
    req.description = ""
    result = gate.check_completeness(req)
    assert result.passed is False
    assert "description" in result.details["failed"]


def test_check_completeness_fails_short_description():
    gate = RequirementGate()
    req = _full_requirement()
    req.description = "short"  # 5 < 10
    result = gate.check_completeness(req)
    assert result.passed is False
    assert "description" in result.details["failed"]


def test_check_completeness_fails_without_priority():
    gate = RequirementGate()
    req = _full_requirement()
    req.priority = None
    result = gate.check_completeness(req)
    assert result.passed is False
    assert "priority" in result.details["failed"]


def test_check_completeness_fails_without_criteria():
    gate = RequirementGate()
    req = _full_requirement()
    req.acceptance_criteria = []
    result = gate.check_completeness(req)
    assert result.passed is False
    assert "acceptance_criteria" in result.details["failed"]


def test_check_completeness_fails_without_scope_in():
    gate = RequirementGate()
    req = _full_requirement()
    req.scope.in_scope = []
    result = gate.check_completeness(req)
    assert result.passed is False
    assert "scope_in_scope" in result.details["failed"]


def test_check_completeness_fails_without_constraints():
    gate = RequirementGate()
    req = _full_requirement()
    req.constraints = []
    result = gate.check_completeness(req)
    assert result.passed is False
    assert "constraints" in result.details["failed"]


# --- 验收标准检查 ---

def test_check_acceptance_criteria_passes():
    gate = RequirementGate()
    criteria = [
        AcceptanceCriteria("响应时间 < 200ms", measurable=True, testable=True),
        AcceptanceCriteria("错误码符合 HTTP 标准", measurable=True, testable=True),
    ]
    result = gate.check_acceptance_criteria(criteria)
    assert result.passed is True
    assert result.score == 1.0
    assert result.details["passed"] == 2


def test_check_acceptance_criteria_empty_list():
    gate = RequirementGate()
    result = gate.check_acceptance_criteria([])
    assert result.passed is False
    assert result.score == 0.0
    assert result.details["total"] == 0


def test_check_acceptance_criteria_not_measurable():
    gate = RequirementGate()
    criteria = [AcceptanceCriteria("系统应该好用", measurable=False, testable=True)]
    result = gate.check_acceptance_criteria(criteria)
    assert result.passed is False
    assert "not measurable" in result.details["issues"][0]["issues"]


def test_check_acceptance_criteria_not_testable():
    gate = RequirementGate()
    criteria = [AcceptanceCriteria("系统应该好用", measurable=True, testable=False)]
    result = gate.check_acceptance_criteria(criteria)
    assert result.passed is False
    assert "not testable" in result.details["issues"][0]["issues"]


def test_check_acceptance_criteria_short_criterion():
    gate = RequirementGate()
    criteria = [AcceptanceCriteria("ok", measurable=True, testable=True)]  # 2 < 5
    result = gate.check_acceptance_criteria(criteria)
    assert result.passed is False
    assert "criterion too short or empty" in result.details["issues"][0]["issues"]


def test_check_acceptance_criteria_partial_score():
    gate = RequirementGate()
    criteria = [
        AcceptanceCriteria("响应时间 < 200ms", measurable=True, testable=True),
        AcceptanceCriteria("系统好用", measurable=False, testable=False),
    ]
    result = gate.check_acceptance_criteria(criteria)
    assert result.passed is False
    assert result.score == 0.5
    assert result.details["passed"] == 1


# --- 范围边界检查 ---

def test_check_scope_boundary_passes():
    gate = RequirementGate()
    scope = Scope(in_scope=["账号密码登录"], out_of_scope=["第三方登录"])
    result = gate.check_scope_boundary(scope)
    assert result.passed is True
    assert result.score == 1.0


def test_check_scope_boundary_empty_in_scope():
    gate = RequirementGate()
    scope = Scope(in_scope=[], out_of_scope=["第三方登录"])
    result = gate.check_scope_boundary(scope)
    assert result.passed is False
    assert "in_scope_not_empty" in result.details["failed"]


def test_check_scope_boundary_empty_out_scope():
    gate = RequirementGate()
    scope = Scope(in_scope=["账号密码登录"], out_of_scope=[])
    result = gate.check_scope_boundary(scope)
    assert result.passed is False
    assert "out_of_scope_not_empty" in result.details["failed"]


def test_check_scope_boundary_overlap():
    gate = RequirementGate()
    scope = Scope(in_scope=["登录"], out_of_scope=["登录"])
    result = gate.check_scope_boundary(scope)
    assert result.passed is False
    assert "no_overlap" in result.details["failed"]
    assert "登录" in result.details["overlap"]


def test_check_scope_boundary_short_items():
    gate = RequirementGate()
    scope = Scope(in_scope=["ab"], out_of_scope=["cd"])  # 2 < 3
    result = gate.check_scope_boundary(scope)
    assert result.passed is False
    assert "in_scope_descriptive" in result.details["failed"]
    assert "out_of_scope_descriptive" in result.details["failed"]


# --- run_all_checks ---

def test_run_all_checks_returns_three_results():
    gate = RequirementGate()
    results = gate.run_all_checks(_full_requirement())
    assert len(results) == 3
    names = [r.check_name for r in results]
    assert names == ["completeness", "acceptance_criteria", "scope_boundary"]
    assert all(r.passed for r in results)
