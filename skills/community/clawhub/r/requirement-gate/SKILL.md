---
name: requirement-gate
version: 1.0.0
description: A requirement gate checker for requirement completeness, acceptance criteria, and scope validation.
author: Terr123123
license: MIT
tags: [requirements, gate, validation, acceptance-criteria]
---

# Requirement Gate — 需求门禁检查 Skill

> OpenClaw Skill: 通用需求门禁检查器，验证需求完整性、验收标准可量化性与范围边界清晰度。

## 场景描述 (When to Use)

- 需求评审前，自动检查需求文档是否字段齐备、可量化、可测试
- 进入设计/开发阶段前，作为需求门禁阻塞不完整需求
- 验收标准撰写后，检查每条标准是否 measurable / testable
- 范围定义后，检查 in_scope / out_of_scope 是否清晰、是否重叠

## 检查维度 (Check Categories)

| 检查 | 说明 | 失败示例 |
|------|------|----------|
| completeness / 完整性 | 标题、描述、优先级、验收标准、范围、约束是否齐备 | 标题为空 / 描述过短 |
| acceptance_criteria / 验收标准 | 每条标准是否可量化、可测试 | "系统应该好用" 不可量化 |
| scope_boundary / 范围边界 | 范围内外是否清晰、是否重叠、描述是否充分 | 同一功能同时出现在范围内外 |

## 使用示例 (Usage)

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
print(all(r.passed for r in results))  # True
```

## 数据模型 (Data Models)

- `Requirement`: title, description, priority, acceptance_criteria, scope, constraints
- `AcceptanceCriteria`: criterion, measurable, testable
- `Scope`: in_scope, out_of_scope
- `GateResult`: check_name, passed, score, message, details

所有模型支持 `to_dict()` / `from_dict()` 序列化，便于持久化与传输。

## 门禁结果

每个 `GateResult` 包含：
- `passed`: 是否通过（默认要求所有检查项全部通过，可通过 `pass_threshold` 调整）
- `score`: 通过率 `[0.0, 1.0]`
- `message`: 人类可读说明
- `details`: 详细信息（失败项、计数、重叠项等）

## 配置选项

`RequirementGate` 构造参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `min_description_length` | 10 | 描述最小字符数 |
| `min_criterion_length` | 5 | 验收标准文本最小字符数 |
| `min_scope_item_length` | 3 | 范围项最小字符数 |
| `pass_threshold` | 1.0 | 通过阈值（score >= threshold 即通过） |

## 依赖

- Python ≥ 3.10
- 无第三方依赖

## 测试

```bash
python -m pytest tests/ -v --tb=short
```

包含 80 个测试：基础功能、边界/异常/并发、序列化/持久化、端到端流程。
