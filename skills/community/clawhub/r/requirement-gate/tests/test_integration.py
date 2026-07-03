"""test_integration.py — 集成测试（15 个）：序列化与持久化。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import AcceptanceCriteria, GateResult, Priority, Requirement, RequirementGate, Scope


def _sample_requirement() -> Requirement:
    return Requirement(
        title="订单服务",
        description="实现订单创建、查询、取消接口。",
        priority=Priority.HIGH,
        acceptance_criteria=[
            AcceptanceCriteria("创建订单返回 201", measurable=True, testable=True),
            AcceptanceCriteria("取消订单返回 200", measurable=True, testable=True),
        ],
        scope=Scope(in_scope=["订单 CRUD"], out_of_scope=["支付对接"]),
        constraints=["QPS >= 1000", "响应 < 200ms"],
    )


# ===================== 序列化 =====================

def test_requirement_to_dict_roundtrip():
    req = _sample_requirement()
    restored = Requirement.from_dict(req.to_dict())
    assert restored.title == req.title
    assert restored.description == req.description
    assert restored.priority == req.priority
    assert restored.constraints == req.constraints
    assert len(restored.acceptance_criteria) == 2


def test_requirement_from_dict_full():
    data = {
        "title": "T",
        "description": "D",
        "priority": "medium",
        "acceptance_criteria": [
            {"criterion": "c1", "measurable": True, "testable": False}
        ],
        "scope": {"in_scope": ["a"], "out_of_scope": ["b"]},
        "constraints": ["x"],
    }
    req = Requirement.from_dict(data)
    assert req.priority == Priority.MEDIUM
    assert req.acceptance_criteria[0].testable is False


def test_acceptance_criteria_to_dict_roundtrip():
    ac = AcceptanceCriteria("标准", measurable=True, testable=True)
    restored = AcceptanceCriteria.from_dict(ac.to_dict())
    assert restored.criterion == ac.criterion
    assert restored.measurable is True
    assert restored.testable is True


def test_scope_to_dict_roundtrip():
    sc = Scope(in_scope=["a", "b"], out_of_scope=["c"])
    restored = Scope.from_dict(sc.to_dict())
    assert restored.in_scope == ["a", "b"]
    assert restored.out_of_scope == ["c"]


def test_gate_result_to_dict_roundtrip():
    gate = RequirementGate()
    result = gate.check_completeness(_sample_requirement())
    restored = GateResult.from_dict(result.to_dict())
    assert restored.check_name == result.check_name
    assert restored.passed == result.passed
    assert restored.score == result.score
    assert restored.message == result.message
    assert restored.details == result.details


def test_requirement_to_dict_contains_all_fields():
    data = _sample_requirement().to_dict()
    assert set(data.keys()) == {
        "title",
        "description",
        "priority",
        "acceptance_criteria",
        "scope",
        "constraints",
    }


def test_requirement_from_dict_missing_optional_fields():
    """缺失字段应使用默认值，不报错。"""
    req = Requirement.from_dict({"title": "Only title"})
    assert req.title == "Only title"
    assert req.description == ""
    assert req.priority is None
    assert req.acceptance_criteria == []
    assert req.scope.in_scope == []
    assert req.constraints == []


def test_requirement_to_dict_priority_serialization():
    req = Requirement(title="t", priority=Priority.CRITICAL)
    assert req.to_dict()["priority"] == "critical"


def test_requirement_from_dict_priority_deserialization():
    req = Requirement.from_dict({"title": "t", "priority": "low"})
    assert req.priority == Priority.LOW


def test_json_serialization_roundtrip():
    """完整需求经 JSON 序列化/反序列化后应等价。"""
    req = _sample_requirement()
    text = json.dumps(req.to_dict(), ensure_ascii=False)
    restored = Requirement.from_dict(json.loads(text))
    assert restored.to_dict() == req.to_dict()


# ===================== 持久化 =====================

def test_persist_requirement_to_file_and_load(tmp_path):
    req = _sample_requirement()
    path = tmp_path / "req.json"
    path.write_text(json.dumps(req.to_dict(), ensure_ascii=False), encoding="utf-8")

    loaded = Requirement.from_dict(
        json.loads(path.read_text(encoding="utf-8"))
    )
    assert loaded.title == req.title
    assert loaded.priority == req.priority
    assert len(loaded.acceptance_criteria) == 2
    assert loaded.constraints == req.constraints


def test_persist_gate_result_to_file_and_load(tmp_path):
    gate = RequirementGate()
    result = gate.check_completeness(_sample_requirement())
    path = tmp_path / "result.json"
    path.write_text(json.dumps(result.to_dict(), ensure_ascii=False), encoding="utf-8")

    loaded = GateResult.from_dict(
        json.loads(path.read_text(encoding="utf-8"))
    )
    assert loaded.check_name == "completeness"
    assert loaded.passed is True
    assert loaded.score == 1.0


def test_to_dict_does_not_mutate_original():
    req = _sample_requirement()
    original = req.to_dict()
    original["title"] = "CHANGED"
    original["constraints"].append("NEW")
    # 原对象不受影响
    assert req.title == "订单服务"
    assert req.constraints == ["QPS >= 1000", "响应 < 200ms"]


def test_from_dict_does_not_mutate_input():
    data = {"in_scope": ["a"], "out_of_scope": ["b"]}
    scope = Scope.from_dict(data)
    data["in_scope"].append("c")
    assert scope.in_scope == ["a"]  # from_dict 做了拷贝


def test_nested_serialization_integrity():
    """嵌套的验收标准与范围经往返后结构保持完整。"""
    req = _sample_requirement()
    restored = Requirement.from_dict(req.to_dict())
    for orig, new in zip(req.acceptance_criteria, restored.acceptance_criteria):
        assert orig.to_dict() == new.to_dict()
    assert restored.scope.to_dict() == req.scope.to_dict()
