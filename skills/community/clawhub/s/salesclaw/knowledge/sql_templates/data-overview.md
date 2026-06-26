---
title: 数据概览（Data Overview）
type: sql_template
tags: [sql, overview, summary, quick-look]
---

# SQL 模板：数据概览

## 用途

快速查看 salesclaw 数据库各表的记录数和最新更新时间，用于数据质量初检。

```sql
-- 核心表记录数
SELECT 'dim_doctors' as tbl, COUNT(*) as cnt FROM dim_doctors
UNION ALL SELECT 'dim_hospitals', COUNT(*) FROM dim_hospitals
UNION ALL SELECT 'dim_products', COUNT(*) FROM dim_products
UNION ALL SELECT 'dim_reps', COUNT(*) FROM dim_reps
UNION ALL SELECT 'dim_territories', COUNT(*) FROM dim_territories
UNION ALL SELECT 'fct_prescription_flow', COUNT(*) FROM fct_prescription_flow
UNION ALL SELECT 'fct_expense_c2', COUNT(*) FROM fct_expense_c2
UNION ALL SELECT 'fct_visit_detail', COUNT(*) FROM fct_visit_detail
UNION ALL SELECT 'compliance_alerts', COUNT(*) FROM compliance_alerts
UNION ALL SELECT 'fct_diagnosis_session', COUNT(*) FROM fct_diagnosis_session
ORDER BY tbl;
```