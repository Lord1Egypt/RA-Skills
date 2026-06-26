---
title: 三层归因操作手册
type: concept
tags: [attribution, diagnosis, structure, behavior, decision, framework]
sources: [SKILL.md - 归因分析：三层归因模型]
related: [[salesclaw/knowledge/concepts/expense-red-green]], [[salesclaw/knowledge/entities/fct_prescription_flow]]
---

# 三层归因操作手册

## 场景定义

当告警触发时（如品种处方量下降15%、费用超限30ppt），必须启动完整的三层归因诊断，不能停在表面数据。

## 三层归因模型

### 第一层：结构归因（What - 规模维度）

**问题**：失血/异常发生在哪个结构单元？

**分析动作**：
- 品种维度：哪个品种贡献了主要失血？
- 组织维度：大区→省区→地区逐层下探
- 时间维度：定位断崖点（哪个月开始下滑）
- 医院类型维度：一级/二级/三级医院分层

**数据来源**：`fct_prescription_flow`、`fct_expense_c2`、`dim_territories`

**输出**：明确失血的"结构单元"（如"广东省 × 诺欣妥 × 心内科"）

---

### 第二层：行为归因（Why - 驱动维度）

**问题**：结构单元的失血是因为什么行为变化？

**分析动作**：
- 覆盖行为：有流向医院家数是否下降？
- 拜访行为：代表拜访频次是否下降？
- 竞品行为：竞品是否有学术活动/准入变化？
- 通道行为：医院准入/招标是否有变化？

**数据来源**：`fct_visit_detail`、`dim_hospital_access`、`dim_competitive_intelligence`

**输出**：明确失血的"驱动因素"（如"竞品在3月开展了5场科室会"）

---

### 第三层：决策归因（Who - 责任维度）

**问题**：谁（哪个代表/哪条线）应对变化负责？

**分析动作**：
- 个人分层：Top/Bottom 代表分层，对比达成率
- 分管人责任：区域经理的覆盖效率是否达标
- 组织连带：区域负责人是否尽到管理责任

**数据来源**：`dim_reps`、`dim_rep_performance`、`fct_budget_allocation`

**输出**：明确"责任归属"（如"某代表处方量下降20%，区域经理未及时介入"）

---

## 结构化推理引擎表

| 表 | 用途 |
|------|------|
| `fct_diagnosis_session` | 每次告警触发一次诊断会话 |
| `fct_reasoning_step` | 每层归因的每一步记录 |
| `dim_diagnosis_rules` | 诊断规则模板（5条预置） |

## 推理会话创建

```sql
INSERT INTO fct_diagnosis_session (
    session_id, trigger_type, trigger_rule_id,
    entity_type, entity_id, entity_name,
    metric_name, metric_value, baseline_value, deviation_pct,
    alert_level, period_type, period_value, province,
    current_phase, status, priority, created_by
) VALUES (
    'DS-2025Q2-001', 'alert', 'R001',
    'product', 'p1', '诺欣妥',
    'prescription_volume', 8500, 10000, -0.15,
    'yellow', 'quarter', '2025Q2', '广东省',
    'structure', 'active', 5, 'agent'
);
```

## 推理步骤记录

```sql
INSERT INTO fct_reasoning_step (
    step_id, session_id, step_order, phase,
    step_name, step_question, sql_query, finding,
    confidence, data_evidence
) VALUES (
    'RS-001', 'DS-2025Q2-001', 1, 'structure',
    '定位失血省区',
    '失血发生在哪个省区？',
    'SELECT province, SUM(prescription_volume) as vol FROM fct_prescription_flow WHERE product_id = ''p1'' GROUP BY province ORDER BY vol DESC',
    '广东省处方量占全国35%，但较上季度下降18%，是主要失血来源',
    0.85,
    '{"province_volumes": {"广东": 2975, "江苏": 2100, "浙江": 1800}}'
);
```

## 结论输出

归因结论必须包含：
1. **归因维度**（结构/行为/决策）
2. **贡献度**（绝对值+占比）
3. **验证方式**（相关性/反例）
4. **不确定性**（数据局限/假设条件）

## 禁止事项

- ❌ 从相关性直接推断因果
- ❌ 忽略负样本（只引用支持假设的数据）
- ❌ 跨层级归因（个人行为不用组织数据解释）
- ❌ 无数据支撑的结论（写"待查"而非编造）