"""test_e2e.py — 端到端测试（10 个）：完整流程。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import AcceptanceCriteria, Priority, Requirement, RequirementGate, Scope


def _valid_requirement() -> Requirement:
    return Requirement(
        title="用户登录",
        description="支持账号密码登录并返回 JWT token。",
        priority=Priority.HIGH,
        acceptance_criteria=[
            AcceptanceCriteria("登录成功返回 200 和 token", measurable=True, testable=True),
            AcceptanceCriteria("错误密码返回 401", measurable=True, testable=True),
        ],
        scope=Scope(in_scope=["账号密码登录", "记住我"], out_of_scope=["OAuth 登录", "短信登录"]),
        constraints=["响应时间 < 500ms", "兼容移动端"],
    )


# ===================== 端到端完整流程 =====================

def test_full_valid_requirement_all_pass():
    gate = RequirementGate()
    results = gate.run_all_checks(_valid_requirement())
    assert len(results) == 3
    assert all(r.passed for r in results)
    assert all(r.score == 1.0 for r in results)


def test_full_invalid_requirement_all_fail():
    gate = RequirementGate()
    req = Requirement(title="x", description="short")  # 缺字段、无标准、无范围、无约束
    results = gate.run_all_checks(req)
    assert all(not r.passed for r in results)


def test_e2e_run_all_checks_aggregates_scores():
    gate = RequirementGate()
    req = _valid_requirement()
    results = gate.run_all_checks(req)
    scores = {r.check_name: r.score for r in results}
    assert scores == {"completeness": 1.0, "acceptance_criteria": 1.0, "scope_boundary": 1.0}


def test_e2e_real_world_requirement():
    """模拟真实需求：电商订单系统。"""
    gate = RequirementGate()
    req = Requirement(
        title="订单管理系统",
        description="实现订单的创建、查询、修改和取消功能，包含库存校验。",
        priority=Priority.CRITICAL,
        acceptance_criteria=[
            AcceptanceCriteria("创建订单成功返回 201 和订单号", measurable=True, testable=True),
            AcceptanceCriteria("库存不足返回 409 错误码", measurable=True, testable=True),
            AcceptanceCriteria("取消订单在 5 秒内生效", measurable=True, testable=True),
        ],
        scope=Scope(
            in_scope=["订单 CRUD", "库存校验", "订单状态机"],
            out_of_scope=["支付网关", "物流跟踪", "会员体系"],
        ),
        constraints=["峰值 QPS >= 2000", "可用性 99.9%", "响应 < 300ms"],
    )
    results = gate.run_all_checks(req)
    assert all(r.passed for r in results)
    assert results[1].details["passed"] == 3  # 3 条标准全通过


def test_e2e_check_results_are_serializable_after_run():
    """运行检查后，所有结果可完整序列化往返。"""
    gate = RequirementGate()
    results = gate.run_all_checks(_valid_requirement())
    serialized = [r.to_dict() for r in results]
    text = json.dumps(serialized, ensure_ascii=False)
    restored = json.loads(text)
    assert len(restored) == 3
    assert restored[0]["check_name"] == "completeness"
    assert restored[0]["passed"] is True


def test_e2e_persist_and_reload_then_check(tmp_path):
    """持久化需求 → 重新加载 → 运行门禁，结果应与原始一致。"""
    gate = RequirementGate()
    req = _valid_requirement()
    path = tmp_path / "req.json"
    path.write_text(json.dumps(req.to_dict(), ensure_ascii=False), encoding="utf-8")

    loaded = Requirement.from_dict(json.loads(path.read_text(encoding="utf-8")))
    original_results = gate.run_all_checks(req)
    loaded_results = gate.run_all_checks(loaded)

    for o, l in zip(original_results, loaded_results):
        assert o.to_dict() == l.to_dict()


def test_e2e_threshold_tuning_affects_outcome():
    """缺 1/6 完整性：默认阈值失败，宽松阈值 (0.8) 通过。"""
    req = _valid_requirement()
    req.constraints = []  # 缺约束 → 完整性 5/6 ≈ 0.833
    strict = RequirementGate()  # 默认 1.0
    loose = RequirementGate(pass_threshold=0.8)

    strict_result = strict.check_completeness(req)
    loose_result = loose.check_completeness(req)
    assert strict_result.passed is False
    assert loose_result.passed is True
    assert abs(strict_result.score - 5 / 6) < 1e-9


def test_e2e_empty_requirement_full_flow():
    """空需求跑完整流程：3 项检查全部失败且分数为 0 或合理值。"""
    gate = RequirementGate()
    results = gate.run_all_checks(Requirement())
    assert results[0].passed is False and results[0].score == 0.0  # completeness
    assert results[1].passed is False and results[1].score == 0.0  # acceptance empty
    assert results[2].passed is False  # scope empty


def test_e2e_mixed_requirement_partial_pass():
    """完整性失败，但验收标准与范围通过。"""
    gate = RequirementGate()
    req = _valid_requirement()
    req.constraints = []  # 完整性失败
    results = gate.run_all_checks(req)
    assert results[0].passed is False            # completeness
    assert results[1].passed is True             # acceptance_criteria
    assert results[2].passed is True             # scope_boundary


def test_e2e_multiple_requirements_sequential():
    """顺序处理多个需求，互不影响。"""
    gate = RequirementGate()
    reqs = [
        _valid_requirement(),
        Requirement(title="bad", description="x"),
        Requirement(
            title="OK feature",
            description="一个通过的需求描述。",
            priority=Priority.MEDIUM,
            acceptance_criteria=[
                AcceptanceCriteria("可测试的标准一", measurable=True, testable=True)
            ],
            scope=Scope(in_scope=["范围内功能"], out_of_scope=["范围外功能"]),
            constraints=["约束一"],
        ),
    ]
    outcomes = []
    for r in reqs:
        results = gate.run_all_checks(r)
        outcomes.append(all(res.passed for res in results))
    assert outcomes == [True, False, True]
