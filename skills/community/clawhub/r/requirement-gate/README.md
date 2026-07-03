# Requirement Gate

> 通用需求门禁检查器 — 验证需求完整性、验收标准可量化性、范围边界清晰度。

[![Tests](https://img.shields.io/badge/tests-80-brightgreen)](#测试)

## 概述

Requirement Gate 是一个 OpenClaw Skill，用于在需求评审或进入设计/开发阶段前，自动检查需求的质量：

- **完整性检查**：标题、描述、优先级、验收标准、范围、约束是否齐备
- **验收标准检查**：每条标准是否可量化（measurable）、可测试（testable）
- **范围边界检查**：in_scope / out_of_scope 是否清晰、是否重叠、描述是否充分

## 安装

通过 ClawHub 安装：

```bash
clawhub install requirement-gate
```

## 快速开始

```python
from src import RequirementGate, Requirement, AcceptanceCriteria, Scope, Priority

gate = RequirementGate()
req = Requirement(
    title="登录功能",
    description="实现用户名密码登录并返回 token。",
    priority=Priority.HIGH,
    acceptance_criteria=[
        AcceptanceCriteria("登录成功返回 200 和 token", measurable=True, testable=True),
    ],
    scope=Scope(in_scope=["账号密码登录"], out_of_scope=["第三方登录"]),
    constraints=["必须兼容移动端"],
)
results = gate.run_all_checks(req)
for r in results:
    print(r.check_name, r.passed, r.score, r.message)
```

## API

### `RequirementGate`

| 方法 | 说明 |
|------|------|
| `check_completeness(requirement)` | 检查需求完整性 |
| `check_acceptance_criteria(criteria)` | 检查验收标准可量化/可测试 |
| `check_scope_boundary(scope)` | 检查范围边界清晰度 |
| `run_all_checks(requirement)` | 顺序运行上述三类检查 |

构造参数：`min_description_length=10`、`min_criterion_length=5`、`min_scope_item_length=3`、`pass_threshold=1.0`。

### 数据模型

- `Requirement(title, description, priority, acceptance_criteria, scope, constraints)`
- `AcceptanceCriteria(criterion, measurable, testable)`
- `Scope(in_scope, out_of_scope)`
- `GateResult(check_name, passed, score, message, details)`
- `Priority`: LOW / MEDIUM / HIGH / CRITICAL

所有模型支持 `to_dict()` / `from_dict()` 序列化。

## 测试

```bash
python -m pytest tests/ -v --tb=short
```

共 80 个测试：

| 文件 | 数量 | 覆盖 |
|------|------|------|
| `tests/test_core.py` | 25 | 基础功能 |
| `tests/test_unit_extended.py` | 30 | 边界、异常、并发安全 |
| `tests/test_integration.py` | 15 | 序列化、持久化 |
| `tests/test_e2e.py` | 10 | 端到端完整流程 |

## 依赖

- Python ≥ 3.10
- 无第三方运行时依赖（仅测试需要 `pytest`）

## License

MIT © Terr123123
