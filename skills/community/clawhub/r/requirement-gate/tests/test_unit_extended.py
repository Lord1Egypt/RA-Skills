"""test_unit_extended.py — 单元扩展测试（30 个）：边界场景、异常处理、并发安全。"""

from __future__ import annotations

import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import AcceptanceCriteria, Priority, Requirement, RequirementGate, Scope


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


# ===================== 边界场景 =====================

def test_completeness_exact_min_description_length():
    """描述正好等于最小长度应通过。"""
    gate = RequirementGate()
    req = _full_requirement()
    req.description = "1234567890"  # 长度 10
    result = gate.check_completeness(req)
    assert "description" not in result.details["failed"]


def test_completeness_below_min_description_length():
    """描述小于最小长度应失败。"""
    gate = RequirementGate()
    req = _full_requirement()
    req.description = "123456789"  # 长度 9
    result = gate.check_completeness(req)
    assert "description" in result.details["failed"]


def test_completeness_whitespace_only_title():
    gate = RequirementGate()
    req = _full_requirement()
    req.title = "   "
    result = gate.check_completeness(req)
    assert "title" in result.details["failed"]


def test_completeness_whitespace_only_description():
    gate = RequirementGate()
    req = _full_requirement()
    req.description = "          "  # 10 个空格，strip 后为 0
    result = gate.check_completeness(req)
    assert "description" in result.details["failed"]


def test_criteria_exact_min_criterion_length():
    """验收标准文本正好等于最小长度应通过。"""
    gate = RequirementGate()
    criteria = [AcceptanceCriteria("12345", measurable=True, testable=True)]
    result = gate.check_acceptance_criteria(criteria)
    assert result.details["issues"] == []
    assert result.passed is True


def test_criteria_below_min_criterion_length():
    gate = RequirementGate()
    criteria = [AcceptanceCriteria("1234", measurable=True, testable=True)]
    result = gate.check_acceptance_criteria(criteria)
    assert result.passed is False
    assert result.details["issues"][0]["issues"] == ["criterion too short or empty"]


def test_scope_exact_min_item_length():
    """范围项正好等于最小长度应通过描述性检查。"""
    gate = RequirementGate()
    scope = Scope(in_scope=["abc"], out_of_scope=["def"])  # 长度 3
    result = gate.check_scope_boundary(scope)
    assert "in_scope_descriptive" not in result.details["failed"]
    assert "out_of_scope_descriptive" not in result.details["failed"]


def test_scope_below_min_item_length():
    gate = RequirementGate()
    scope = Scope(in_scope=["ab"], out_of_scope=["cd"])
    result = gate.check_scope_boundary(scope)
    assert "in_scope_descriptive" in result.details["failed"]
    assert "out_of_scope_descriptive" in result.details["failed"]


def test_scope_whitespace_items_ignored_for_overlap():
    """纯空白项不应被计入重叠。"""
    gate = RequirementGate()
    scope = Scope(in_scope=["   ", "登录"], out_of_scope=["   ", "退出"])
    result = gate.check_scope_boundary(scope)
    assert "no_overlap" not in result.details["failed"]


def test_scope_overlap_case_insensitive():
    gate = RequirementGate()
    scope = Scope(in_scope=["LOGIN"], out_of_scope=["login"])
    result = gate.check_scope_boundary(scope)
    assert "no_overlap" in result.details["failed"]
    assert "login" in result.details["overlap"]


def test_scope_overlap_with_surrounding_whitespace():
    gate = RequirementGate()
    scope = Scope(in_scope=[" 登录 "], out_of_scope=["登录"])
    result = gate.check_scope_boundary(scope)
    assert "no_overlap" in result.details["failed"]


def test_completeness_score_zero_when_all_missing():
    gate = RequirementGate()
    result = gate.check_completeness(Requirement())
    assert result.score == 0.0
    assert result.passed is False


def test_completeness_score_full_when_all_present():
    gate = RequirementGate()
    result = gate.check_completeness(_full_requirement())
    assert result.score == 1.0


def test_scope_score_when_both_empty():
    """空 Scope：in/out 非空检查失败，但无重叠与描述性检查空真通过 → 3/5。"""
    gate = RequirementGate()
    result = gate.check_scope_boundary(Scope())
    assert result.details["passed"] == 3
    assert result.score == 0.6
    assert result.passed is False


def test_scope_score_partial_with_overlap_only():
    """仅重叠失败、其余通过（项足够描述）：4/5。"""
    gate = RequirementGate()
    scope = Scope(in_scope=["登录功能"], out_of_scope=["登录功能"])
    result = gate.check_scope_boundary(scope)
    assert result.details["passed"] == 4
    assert result.score == 0.8
    assert "登录功能" in result.details["overlap"]


# ===================== 异常处理 / 配置 =====================

def test_check_completeness_handles_none_priority():
    gate = RequirementGate()
    req = _full_requirement()
    req.priority = None
    result = gate.check_completeness(req)
    assert "priority" in result.details["failed"]
    assert result.passed is False


def test_check_acceptance_criteria_empty_string_criterion():
    gate = RequirementGate()
    criteria = [AcceptanceCriteria("", measurable=True, testable=True)]
    result = gate.check_acceptance_criteria(criteria)
    assert result.passed is False
    assert "criterion too short or empty" in result.details["issues"][0]["issues"]


def test_run_all_checks_on_empty_requirement():
    gate = RequirementGate()
    results = gate.run_all_checks(Requirement())
    assert len(results) == 3
    assert all(r.passed is False for r in results)


def test_custom_threshold_changes_pass():
    """缺失 3/6 时，默认阈值失败，0.5 阈值通过。"""
    req = _full_requirement()
    req.acceptance_criteria = []
    req.scope.in_scope = []
    req.constraints = []
    # 通过项：title, description, priority → 3/6 = 0.5
    strict = RequirementGate()
    loose = RequirementGate(pass_threshold=0.5)
    assert strict.check_completeness(req).passed is False
    assert loose.check_completeness(req).passed is True


def test_custom_min_description_length():
    gate = RequirementGate(min_description_length=5)
    req = _full_requirement()
    req.description = "12345"  # 5 < 默认 10，但 >= 自定义 5
    result = gate.check_completeness(req)
    assert "description" not in result.details["failed"]


def test_custom_min_criterion_length():
    gate = RequirementGate(min_criterion_length=2)
    criteria = [AcceptanceCriteria("ok", measurable=True, testable=True)]
    result = gate.check_acceptance_criteria(criteria)
    assert result.passed is True


def test_custom_min_scope_item_length():
    gate = RequirementGate(min_scope_item_length=2)
    scope = Scope(in_scope=["ab"], out_of_scope=["cd"])
    result = gate.check_scope_boundary(scope)
    assert "in_scope_descriptive" not in result.details["failed"]


def test_threshold_zero_makes_zero_score_pass():
    """阈值为 0 时，0 分的完整性检查应通过。"""
    gate = RequirementGate(pass_threshold=0.0)
    result = gate.check_completeness(Requirement())
    assert result.score == 0.0
    assert result.passed is True


def test_threshold_above_one_never_passes():
    """阈值大于 1 时，满分也不通过。"""
    gate = RequirementGate(pass_threshold=1.5)
    result = gate.check_completeness(_full_requirement())
    assert result.score == 1.0
    assert result.passed is False


def test_acceptance_criteria_records_correct_indices():
    gate = RequirementGate()
    criteria = [
        AcceptanceCriteria("好的标准一", measurable=True, testable=True),
        AcceptanceCriteria("坏", measurable=False, testable=False),
        AcceptanceCriteria("好的标准二", measurable=True, testable=True),
    ]
    result = gate.check_acceptance_criteria(criteria)
    issue_indices = [i["index"] for i in result.details["issues"]]
    assert issue_indices == [1]
    assert result.details["passed"] == 2


# ===================== 并发安全 =====================

def _run_concurrent(fn, iterations=40, workers=4):
    """在多线程下并发执行 fn，返回所有结果。"""
    results = []
    lock = threading.Lock()

    def runner():
        local = [fn() for _ in range(iterations // workers)]
        with lock:
            results.extend(local)

    threads = [threading.Thread(target=runner) for _ in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return results


def test_concurrent_run_all_checks_thread_safety():
    gate = RequirementGate()
    req = _full_requirement()

    results = _run_concurrent(lambda: gate.run_all_checks(req))
    assert len(results) == 40
    for res in results:
        assert len(res) == 3
        assert all(r.passed for r in res)


def test_concurrent_check_completeness():
    gate = RequirementGate()

    results = _run_concurrent(lambda: gate.check_completeness(_full_requirement()))
    assert len(results) == 40
    assert all(r.score == 1.0 and r.passed for r in results)


def test_concurrent_check_acceptance_criteria():
    gate = RequirementGate()
    criteria = [
        AcceptanceCriteria("响应时间 < 200ms", measurable=True, testable=True),
        AcceptanceCriteria("坏", measurable=False, testable=False),
    ]

    results = _run_concurrent(lambda: gate.check_acceptance_criteria(criteria))
    assert len(results) == 40
    assert all(r.score == 0.5 and not r.passed for r in results)


def test_concurrent_check_scope_boundary():
    gate = RequirementGate()
    scope = Scope(in_scope=["登录"], out_of_scope=["登录"])

    results = _run_concurrent(lambda: gate.check_scope_boundary(scope))
    assert len(results) == 40
    assert all(not r.passed for r in results)
    assert all("登录" in r.details["overlap"] for r in results)


def test_gate_instance_reusable_across_calls():
    """同一个 gate 实例多次调用应保持结果一致。"""
    gate = RequirementGate()
    req = _full_requirement()
    first = gate.run_all_checks(req)
    for _ in range(5):
        again = gate.run_all_checks(req)
        assert [r.to_dict() for r in first] == [r.to_dict() for r in again]
