---
title: 处方渗透率分析
type: concept
tags: [analysis, penetration, doctor, metric]
sources: [analyze.py::analyze_prescription_penetration]
related: [[salesclaw/entities/doctors]], [[salesclaw/entities/customer_compliances]], [[salesclaw/entities/object_links]]
---

# 处方渗透率分析（Prescription Penetration Analysis）

## 分析目标

衡量某产品在某医生（或某医院某科室）的处方渗透程度，是销售团队评估**上量空间**的核心指标。

## 计算逻辑

```
渗透率 = 医生处方量 / (处方能力 × 基准处方量)
```

### 简化计算

在 SalesClaw 中，使用以下近似公式：

```
渗透率 ≈ 医生当前处方量 / (影响力评分 × 100)
```

| 渗透率范围 | 业务含义 | 行动建议 |
|-----------|---------|---------|
| < 30% | 潜力未充分挖掘 | **重点上量**：增加拜访频次，传递学术信息 |
| 30% - 70% | 正常渗透区间 | 维持现状，关注竞品动向 |
| > 70% | 高位渗透 | **维持**：防止竞品替代 |

## 数据来源

| 数据 | 来源表 | 字段 |
|------|--------|------|
| 医生处方量（快照） | `doctors` | `prescription_volume` |
| 处方量趋势 | `customer_compliances` | `series_name='prescriptionVolume'` |
| 处方能力 | `doctors` | `prescription_power` |
| 影响力评分 | `doctors` | `influence_score` |

## 分析维度

1. **单医生维度**：某医生对某产品的渗透率
2. **医院维度**：某医院所有医生的渗透率分布
3. **区域维度**：某代表区域内所有医生的平均渗透率

## 趋势判断

基于 `customer_compliances` 时序数据，用**线性回归斜率**判断趋势：
- slope > 0.08（每期增长 > 8%）→ 📈 上升
- slope < -0.08 → 📉 下降
- 其他 → ➡️ 稳定

## 注意事项

⚠️ 处方量是**产品维度**的，需要先通过 `object_links` 的 `PRESCRIBES` 关系确认医生-产品关联
⚠️ 渗透率只是一个近似值，真实上量空间需要结合科室患者量、竞品使用情况综合判断

---

*关联：[[salesclaw/entities/doctors]] / [[salesclaw/entities/customer_compliances]]*
