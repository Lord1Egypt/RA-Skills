---
title: 区域覆盖分析
type: concept
tags: [analysis, coverage, hospital, sales-rep]
sources: [analyze.py::analyze_territory_coverage]
related: [[salesclaw/entities/hospitals]], [[salesclaw/entities/object_links]], [[salesclaw/entities/object_events]]
---

# 区域覆盖分析（Territory Coverage Analysis）

## 分析目标

评估销售代表对所负责区域医院的覆盖质量，识别覆盖缺口。

## 覆盖分类

| 类型 | 定义 | 行动 |
|------|------|------|
| **活跃覆盖** | `access_status = 'active'` 且最近 60 天内有拜访事件 | 正常维护 |
| **待激活** | `access_status = 'active'` 但 60+ 天无拜访 | **重新激活**：尽快安排拜访 |
| **未准入** | `access_status != 'active'` | **推进准入**：市场拓展重点 |
| **高价值未覆盖** | 年营收 > 1000万 且未准入 | **最高优先级** |

## 覆盖率计算

```
覆盖率 = 活跃覆盖医院数 / 总医院数 × 100%
```

| 覆盖率 | 等级 |
|--------|------|
| > 80% | ✅ 良好 |
| 50% - 80% | ⚠️ 一般 |
| < 50% | 🚨 严重不足 |

## 拜访时效判断

通过 `object_events` 的 `Visit` / `VisitCompleted` 事件判断：

```sql
-- 查找某医院最近拜访
SELECT MAX(e.timestamp) as last_visit
FROM object_events e
JOIN object_links ol ON ol.source_id = e.object_id
WHERE ol.target_id = 'h1'
  AND e.event_type LIKE 'Visit%'
```

## 数据来源

| 覆盖维度 | 数据来源 |
|---------|---------|
| 准入状态 | `hospitals.access_status` |
| 医院规模 | `hospitals.annual_revenue` / `beds` |
| 拜访记录 | `object_events.event_type = 'Visit*'` |
| 代表-医院关系 | `object_links.link_type = 'MANAGES'` |

## 注意事项

⚠️ 查询代表负责医院必须用 `object_links` 的 `MANAGES` 关系，不能直接查外键
⚠️ 拜访时效判断依赖 `object_events` 数据，数据录入不及时会导致误判

---

*关联：[[salesclaw/entities/hospitals]] / [[salesclaw/entities/object_events]]*
