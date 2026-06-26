# PolypharmacyManagement Schema

多重用药管理的完整数据结构定义。

## Schema 文件

完整的 JSON Schema 定义：[schema.json](schema.json)

## 字段速查

### 用药清单

| 字段 | 类型 | 说明 |
|-----|------|-----|
| name | string | 药物名称 |
| dosage | string | 剂量 |
| frequency | enum | qd/bid/tid/qid/qn/prn |
| indication | string | 适应症 |
| anticholinergic_score | int | 抗胆碱能评分 (0-3) |

### Beers 标准违规

| 字段 | 类型 | 说明 |
|-----|------|-----|
| violation_type | enum | potential_inappropriate/use_with_caution |
| severity | enum | high/moderate/low |
| recommendation | string | 建议 |
| alternative | string | 替代药物 |

### 药物相互作用

| 字段 | 类型 | 说明 |
|-----|------|-----|
| drug_1/drug_2 | string | 相互作用药物 |
| severity | enum | major/moderate/minor |
| interaction_type | enum | drug_drug/drug_disease |
| clinical_significance | enum | 临床意义 |

### 精简计划

| 字段 | 类型 | 说明 |
|-----|------|-----|
| medication_name | string | 药物名称 |
| action | enum | taper/switch/discontinue |
| timeline | string | 时间线 |
| schedule | array | 减药计划表 |

## 枚举值

### 用药频次
`qd` | `bid` | `tid` | `qid` | `qn` | `prn`

### 相互作用严重程度
`major` | `moderate` | `minor`

### 临床意义
`contraindicated` | `significant` | `monitor` | `minor`

### 风险等级
`high` | `moderate` | `low`

### 精简行动
`taper` | `switch` | `discontinue`

## 数据存储

- 位置: `data/polypharmacy-management.json`
- 格式: JSON 对象
