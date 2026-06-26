# 药物相互作用检查 Schema

药物相互作用检查和管理的完整数据结构定义。

## 严重程度分级

| 级别 | 名称 | 代码 | 风险 |
|-----|------|------|------|
| 安全 | A | 1 | 无显著相互作用 |
| 谨慎使用 | B | 2 | 风险较低 |
| 相对禁忌 | C | 3 | 有临床意义 |
| 禁忌 | D | 4 | 风险大于获益 |
| 绝对禁忌 | X | 5 | 危及生命 |

## 相互作用类型

| 类型 | 代码 | 说明 |
|-----|------|------|
| 药物-药物 | drug_drug | 药物之间的相互作用 |
| 药物-疾病 | drug_disease | 药物与疾病冲突 |
| 药物-剂量 | drug_dosage | 剂量安全问题 |
| 药物-食物 | drug_food | 药物与食物相互作用 |

## 检查记录字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `date` | string | 检查日期 |
| `medications_count` | int | 当前用药数量 |
| `interactions_detected.total` | int | 检测到的相互作用总数 |
| `interactions_detected.by_severity` | object | 按严重程度分类 |
| `interactions[]` | array | 相互作用详情列表 |

## 数据存储

- 检查记录: `data/interactions/interaction-logs/YYYY-MM/YYYY-MM-DD.json`
- 规则库: `data/interactions/interaction-db.json`
- 历史汇总: `data/interactions/interaction-history.json`
