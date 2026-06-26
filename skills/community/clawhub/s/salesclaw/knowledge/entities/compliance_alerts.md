---
title: compliance_alerts - 合规告警表
type: entity
tags: [table, compliance, field]
sources: [salesclaw.db schema + 2条示例数据]
related: [[salesclaw/knowledge/entities/sales_reps]], [[salesclaw/knowledge/entities/doctors]]
---

# compliance_alerts - 合规告警表

## 字段说明

| 字段 | 类型 | 示例 |
|------|------|------|
| `id` | VARCHAR PK | `c1` |
| `severity` | VARCHAR | `high`（还有 critical/medium/low）|
| `risk_type` | VARCHAR | `expense_exceed_limit`、`prescription_decline` |
| `alert_description` | TEXT | `王代表本月招待费已达上限的95%` |
| `alert_status` | VARCHAR | `pending`（还有 active/dismissed）|

## 示例数据

```
c1       | high | expense_exceed_limit | 王代表本月招待费已达上限的95%... | pending
alert_xxx | high | prescription_decline | 通过感知引擎检测到处方量持续下降  | pending
```

## 核心规则

1. **severity = `high`/`critical` 需立即处理**
2. **alert_status = `pending`**：待处理告警
3. **risk_type = `prescription_decline`**：处方量下降告警，来自感知引擎

## 正确查询

```sql
-- 活跃告警（按严重性排序）
SELECT * FROM compliance_alerts
WHERE alert_status = 'active' OR alert_status = 'pending'
ORDER BY
  CASE severity WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 ELSE 4 END;

-- 高风险告警
SELECT * FROM compliance_alerts
WHERE severity IN ('critical', 'high')
  AND alert_status = 'pending';
```

## 错误写法

```sql
-- ❌ compliance_alerts 没有 created_at 列
SELECT * FROM compliance_alerts ORDER BY created_at DESC
```

---

*关联：[[salesclaw/knowledge/entities/sales_reps]]*
