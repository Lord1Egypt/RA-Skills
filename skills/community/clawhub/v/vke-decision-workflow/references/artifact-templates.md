# VKE Artifact Templates

Use these templates when creating or rewriting VKE decision artifacts. Adapt headings to the case, but preserve the evidence-led structure.

## 00_request.md

```markdown
---
id: VKE-YYYY-NNN
status: intake
priority:
created:
deadline:
---

# 知识请求: <问题标题>

## 1. 决策背景

## 2. 核心问题

## 3. 子问题

## 4. 已知事实

## 5. 关键不确定性

## 6. 范围

本次包括:

本次不包括:

## 7. 交付要求

## 8. 判断成功标准
```

## 01_problem-brief.md

```markdown
# 问题简报

## 核心问题

## 决策用途

## 暂定假设

## 关键子问题

| 子问题 | 为什么重要 | 需要的证据 | 优先级 |
|---|---|---|---|

## 需要调动的资源

| 资源类型 | 具体对象 | 用途 |
|---|---|---|

## 范围边界

## 截止时间
```

## 02_research-plan.md

```markdown
# 研究计划

## Case 信息

- case_id:
- linked_request:
- owner:
- deadline:

## 研究目标

## 需要验证的假设

## 证据需求

| 证据类型 | 用途 | 优先级 | 目标来源 |
|---|---|---|---|

## 资源调度方案

### 需要哪些领域专家

### 需要哪些机构或卓越中心类型

### 需要哪些数据库和公开来源

### 需要哪些分析工具

### 搜索关键词和检索路径

### 哪些来源应优先验证

### 哪些来源可能存在偏见

## 输出物

- [ ] 证据台账
- [ ] 分析笔记
- [ ] 红队审查
- [ ] 知识产品
- [ ] 监测指标
- [ ] 复盘
```

## 03_evidence-ledger.csv

```csv
evidence_id,case_id,claim_supported,evidence_summary,source_id,source_name,source_date,collection_date,evidence_type,reliability,relevance,confidence_effect,notes
EVD-001,,,,,,,,,,,,
```

## 04_analysis-notes.md

```markdown
# 分析笔记

## 问题

## 工作假设

## 支持证据

## 反向证据

## 替代解释

## 推理链条、关键判断与置信度

### 判断 1：

- 推理链条：
- 证据：
- 替代解释：
- 置信度：
- 还需验证：

## 下一步验证
```

## 05_red-team-review.md

```markdown
# 红队审查

## 被审查的核心判断

## 最强反对意见

## 哪些证据可能被误读?

## 是否存在选择性取证?

## 是否忽略了替代解释?

## 哪个假设一旦错误, 会推翻主要结论?

## 需要降低置信度吗?

## 审查后修改
```

## 06_knowledge-product.md

```markdown
---
product_id:
case_id:
status: draft
confidence:
delivered:
---

# <主题>：商业判断报告

## 1. 核心结论与摘要 (Executive Summary)

### 1.1 一句话结论

### 1.2 核心事实提炼

### 1.3 核心判断与基本假设

| 判断 | 置信度 | 决策含义 |
|---|---|---|

## 2. 证据链条与置信度评估 (Evidence & Confidence)

### 2.1 关键证据台账

| 证据编号 | 证据摘要 | 可靠性 | 相关性 | 对判断的影响 |
|---|---|---|---|---|

### 2.2 整体置信度评估

## 3. 推导逻辑与反向证伪 (Analysis & Counter-Arguments)

### 3.1 正向推导逻辑

### 3.2 替代解释与潜在证伪点

## 4. 商业边界与影响评估 (Impact Assessment)

### 4.1 一阶/二阶/三阶影响

### 4.2 交付风险边界

| 风险边界 | 当前证据 | 商业含义 |
|---|---|---|

## 5. 行动指南与动态触发器 (Action Plan)

### 5.1 行动矩阵

| 类别 | 行动 | 目的 |
|---|---|---|

### 5.2 决策转向触发指标

| 指标 | 触发条件 | 触发后动作 |
|---|---|---|
```

## 07_watchlist.md

```markdown
# 监测指标

## Case 信息

## 当前监测基线

## 指标清单

| indicator_id | 指标 | 为什么重要 | 监测来源 | 频率 | 触发条件 | 触发后动作 | 状态 |
|---|---|---|---|---|---|---|---|

## 优先级

## 判断更新规则

## 下一次复核
```

## 08_retrospective.md

```markdown
# 任务复盘

## 本次任务是否回答了原始问题?

## 哪些来源最有价值?

## 哪些来源噪声大?

## 哪个分析方法可复用?

## 哪些假设需要后续验证?

## 下次如何更快?

## 需要加入资源池的对象

## 需要沉淀为模板的内容
```
