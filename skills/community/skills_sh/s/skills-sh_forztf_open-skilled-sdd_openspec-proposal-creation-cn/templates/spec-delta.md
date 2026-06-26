# 规范差异：{能力名称}

本文件包含对 `spec/specs/{capability}/spec.md` 的规范变更。

## ADDED 需求

### Requirement: {需求名称}
{WHEN/IF 子句描述触发条件}
系统 SHALL {动作与结果}。

#### Scenario: {正向场景名称}
GIVEN {前置条件}
WHEN {动作}
THEN {期望结果}
AND {附加结果}

#### Scenario: {错误场景名称}
GIVEN {错误前置条件}
WHEN {动作}
THEN {期望的错误处理}

---

## MODIFIED 需求

### Requirement: {现有需求名称}
**Previous**：{旧行为的简要说明}

{采用 EARS 格式的完整更新需求文本}
WHEN {触发条件},
系统 SHALL {新的动作与结果}。

#### Scenario: {更新后的场景名称}
GIVEN {新的前置条件}
WHEN {动作}
THEN {新的期望结果}

---

## REMOVED 需求

### Requirement: {弃用的需求名称}
**移除原因**：{弃用原因}

**迁移路径**：{用户应如何适配}

---

## 备注

- 对全新能力使用 ADDED
- 修改既有行为时使用 MODIFIED（包含完整更新文本）
- 对弃用功能使用 REMOVED
- 每条需求都应包含场景
- 同时考虑正向与错误场景