---
title: 合规模式挖掘
type: concept
tags: [analysis, compliance, visit, doctor]
sources: [analyze.py::analyze_compliance_pattern]
related: [[salesclaw/entities/object_events]], [[salesclaw/entities/doctors]], [[salesclaw/concepts/visit-effectiveness]]
---

# 合规模式挖掘（Compliance Pattern Mining）

## 分析目标

通过 `object_events` 事件时序分析，检测：
- 拜访频率异常（过高/过低）
- 处方量突变（PrescriptionDrop）
- 医生态度变化（SentimentChange）

识别合规风险模式和需要重点关注的医生。

## 事件类型分析

| 事件类型 | 业务含义 | 预警级别 |
|---------|---------|---------|
| `PrescriptionDrop` | 处方量下降 | 🚨 最高 - 立即关注 |
| `SentimentChange`（负向） | 态度转为负面 | 🚨 高 |
| 拜访频率异常低 | 代表覆盖不足 | ⚠️ 中 |
| 拜访频率异常高 | 资源浪费/虚假拜访 | ⚠️ 中 |

## 异常检测算法

### 拜访频率异常：IQR + Z-score 双重检测

```
Q1 = 25%分位数，Q3 = 75%分位数
IQR = Q3 - Q1
异常区间：< Q1 - 1.5×IQR 或 > Q3 + 1.5×IQR
```

同时用 Z-score 验证：
```
Z = (值 - 均值) / 标准差
|Z| > 2 → 异常
```

**双重检测都触发** = 高风险异常

### 处方量突变

直接检测 `event_type = 'PrescriptionDrop'` 的事件数量和频率。

## 数据来源

| 数据 | 表 | 字段 |
|------|-----|------|
| 拜访事件 | `object_events` | `event_type LIKE 'Visit%'` |
| 处方量下降 | `object_events` | `event_type = 'PrescriptionDrop'` |
| 态度变化 | `object_events` | `event_type = 'SentimentChange'` |
| 代表-医生关系 | `object_links` | `MANAGED_BY` |

## 注意事项

⚠️ 依赖 `object_events` 数据录入及时性
⚠️ 拜访频率分析需要至少 3 个月的数据
⚠️ 异常检测结果是提示，需要人工确认是否是真问题

---

*关联：[[salesclaw/entities/object_events]] / [[salesclaw/concepts/visit-effectiveness]]*
