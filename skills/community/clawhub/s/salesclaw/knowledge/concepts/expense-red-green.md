---
title: 费用红黄绿灯标准
type: concept
tags: [expense, alert, deltaweight, red-yellow-green, rule]
sources: [SKILL.md - DeltaWeight 计算规范]
related: [[salesclaw/knowledge/entities/fct_expense_c2]], [[salesclaw/knowledge/entities/dim_territories]]
---

# 费用红黄绿灯标准（DeltaWeight 算法）

## 告警级别定义

| 告警级别 | 触发条件 | 响应时间 | 行动 |
|---------|---------|---------|------|
| 🔴 **红灯** | DeltaWeight ≥ 30ppt 或 单笔金额 > 2×全国P90 | 24h 内 | 立即核查+合规审查 |
| 🟡 **黄灯** | DeltaWeight ≥ 15ppt 或 单笔金额 > 1.5×全国P90 | 1周内 | 关注趋势+准备说明 |
| 🟢 **绿灯** | 无显著偏离 | 季度复盘 | 常规监控 |

## DeltaWeight 计算公式

```
DeltaWeight = 某省区某费用类型占比 - 全国该费用类型占比

省区费用占比 = 该省该费用类型金额 / 该省费用总额
全国费用占比 = 该费用类型金额 / 全国费用总额
```

## SQL 实现

```sql
WITH national_ratio AS (
    SELECT
        expense_type,
        SUM(amount) / SUM(SUM(amount)) OVER () AS national_ratio
    FROM fct_expense_c2
    WHERE expense_date BETWEEN '{start_date}' AND '{end_date}'
      AND approval_status = 'approved'
      AND expense_type IS NOT NULL
    GROUP BY expense_type
),
province_ratio AS (
    SELECT
        province,
        expense_type,
        SUM(amount) / SUM(SUM(amount)) OVER (PARTITION BY province) AS province_ratio
    FROM fct_expense_c2
    WHERE expense_date BETWEEN '{start_date}' AND '{end_date}'
      AND approval_status = 'approved'
      AND province IS NOT NULL
      AND expense_type IS NOT NULL
    GROUP BY province, expense_type
)
SELECT
    p.province,
    p.expense_type,
    ROUND(p.province_ratio * 100, 2) as province_pct,
    ROUND(n.national_ratio * 100, 2) as national_pct,
    ROUND((p.province_ratio - n.national_ratio) * 100, 2) AS delta_weight_ppt,
    CASE
        WHEN ABS(p.province_ratio - n.national_ratio) >= 0.30 THEN '🔴 红灯'
        WHEN ABS(p.province_ratio - n.national_ratio) >= 0.15 THEN '🟡 黄灯'
        ELSE '🟢 绿灯'
    END AS alert_level
FROM province_ratio p
JOIN national_ratio n ON p.expense_type = n.expense_type
WHERE ABS(p.province_ratio - n.national_ratio) >= 0.15
ORDER BY ABS(p.province_ratio - n.national_ratio) DESC;
```

## 分析维度

费用异常分析支持以下维度的下探：

| 维度 | 说明 |
|------|------|
| **省区** | 哪个省区超支 |
| **费用类型** | 哪类费用超支（会议费/交通费/拜访费） |
| **代表** | 哪个代表的费用异常 |
| **时间段** | 哪个月份异常突出 |

## 告警触发后的归因流程

1. **结构归因**：哪个省区/费用类型贡献了主要偏离？
2. **行为归因**：超支是因为什么行为？（会议数量增加？单笔金额增大？）
3. **决策归因**：谁应该对这笔费用负责？（代表？地区经理？）

## 合规核查要点

- 会议费：核查会议真实性（参会人数、地点、时间）
- 交通费：核查行程合理性（起点终点、票据完整性）
- 拜访费：核查拜访对象和频率是否合理

## 注意事项

- 仅统计 `approval_status = 'approved'` 的费用，pending 状态不计入
- 需先探查 `expense_type` 的实际枚举值
- 省区字段可能叫 `province` 或 `province_name`，需确认