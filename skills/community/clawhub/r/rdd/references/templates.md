# RDD 文件模板

全链条下使用。Lite 通道可内联 Story 进 FE；Solo-dev 超轻量路径用 commit message 代替文件（不产这些）。

## RR 模板

```markdown
---
id: RR-{id}
type: rr
parent: null
status: draft
owner: human
created: {date}
---

# Raw Requirement: {title}

## 来源
{来源描述}

## 业务目标
{目标描述}

## 需求描述
{原始需求文本}

## 范围
{边界定义}

## 未确定事项
- {待确认项}
```

## Spec 模板

```yaml
spec:
  id: SPEC-{id}
  story: US-{id}
  status: draft

  behaviors:
    - id: B-{n}
      description: ""

  constraints:
    - id: C-{n}
      description: ""

  invariants:
    - id: I-{n}
      description: ""

  acceptance_criteria:
    - id: AC-{n}
      given: ""
      when: ""
      then: ""

  open_questions:
    - id: Q-{n}
      question: ""
      options: []
      status: unresolved

  decisions:
    - id: DEC-{n}
      question: ""
      selected: ""
      decided_by: human
      reason: ""
      status: frozen

  assumptions:
    - id: A-{n}
      description: ""
      status: inferred
```

## Traceability 模板

```yaml
traceability:
  - rr: RR-001
    features: [FE-001]
    stories: [US-001, US-002]
    specs: [SPEC-001]        # AC 即测试契约，不另列 TEST
    code: [src/batch-modify.ts]   # solo-dev 用 commit message 代替此文件
```
