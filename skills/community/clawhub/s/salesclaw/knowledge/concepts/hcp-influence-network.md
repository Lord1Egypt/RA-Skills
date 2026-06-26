---
title: HCP影响力网络推理
type: concept
tags: [analysis, network, doctor]
sources: [analyze.py::analyze_hcp_influence_network]
related: [[salesclaw/entities/object_links]], [[salesclaw/entities/doctors]], [[salesclaw/concepts/kol-strategy]]
---

# HCP影响力网络推理（HCP Influence Network）

## 分析目标

基于医生间的关系链接（`object_links`），构建影响力传递网络，识别：
- **网络枢纽**：连接多位医生的关键节点
- **KOL**：高影响力 + 高连接强度 的医生
- **游离医生**：网络中处于孤立位置，流失风险高

## 关系类型

| link_type | 说明 | 影响力传递方向 |
|-----------|------|--------------|
| `INFLUENCES` | 直接处方影响 | 单向传递 |
| `DOCTOR_COLLEAGUE` | 同事关系 | 相互影响 |
| `DOCTOR_REPORT_TO` | 上下级 | 上级影响下级 |
| `DOCTOR_MENTOR` | 师徒关系 | 师父影响徒弟 |

## 度中心性计算

每个医生的网络中心性：

```
中心性 = Σ(link_strength × confidence) ，对该医生的所有关系求和
```

| 节点类型 | 连接数 | link_strength 合计 | 业务含义 |
|---------|--------|-------------------|---------|
| **Hub（枢纽）** | > 5 | 高 | 学术带头人，重点维护 |
| **Connected（连接型）** | 2-5 | 中 | 正常学术圈成员 |
| **Isolated（游离型）** | ≤ 1 | 低 | 需关注，可能流失 |

## KOL 识别标准

```
KOL = influence_score ≥ 7 且 connection_count ≥ 2 且 link_strength > 0.7
```

## 应用场景

1. **学术推广优先覆盖 KOL**：通过 KOL 的影响力间接影响更多医生
2. **识别游离医生**：长期孤立可能导致处方习惯固化或被竞品渗透
3. **预测处方变化传导**：A 医生被竞品影响 → A 的 INFLUENCES 关系 → B 医生也可能变化

## 注意事项

⚠️ 网络分析需要足够多的关系数据才能得出有意义的结论（一般需要 > 10 条关系）
⚠️ `link_strength` 由系统计算或代表录入，需注意数据质量

---

*关联：[[salesclaw/concepts/kol-strategy]] / [[salesclaw/entities/object_links]]*
