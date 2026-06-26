# MentalHealthTracker Schema

心理健康管理的完整数据结构定义。

## Schema 文件

完整的 JSON Schema 定义：[schema.json](schema.json)

## 字段速查

### 心理评估

| 字段 | 类型 | 说明 |
|-----|------|-----|
| scale | enum | phq9/gad7/psqi/gds/epds |
| total_score | int | 总分 |
| severity | string | 严重程度 |
| items | array | 各项得分 |

### 情绪日记

| 字段 | 类型 | 说明 |
|-----|------|-----|
| mood | enum | 情绪类型 |
| intensity | int | 强度 (1-10) |
| triggers | array | 触发因素 |
| coping_strategies | array | 应对方式 |
| effectiveness | enum | 效果评估 |

### 治疗记录

| 字段 | 类型 | 说明 |
|-----|------|-----|
| session_number | int | 会话编号 |
| therapy_type | enum | 治疗类型 |
| topics_discussed | array | 讨论主题 |
| mood_before/after | enum | 治疗前后情绪 |

### 危机计划

| 字段 | 类型 | 说明 |
|-----|------|-----|
| warning_signs | array | 预警信号 |
| emergency_contacts | array | 紧急联系人 |
| coping_strategies | array | 应对策略 |
| current_risk_level | enum | 风险等级 |

## 枚举值

### 情绪类型
`happy` | `calm` | `anxious` | `sad` | `angry` | `tired` | `frustrated` | `excited` | `depressed` | `irritable` | `nervous`

### 评估量表
`phq9` | `gad7` | `psqi` | `gds` | `epds`

### 治疗类型
`CBT` | `psychodynamic` | `humanistic` | `family` | `group` | `DBT` | `EMDR`

### 风险等级
`low` | `medium` | `high`

### 预警信号
`hopelessness` | `social_withdrawal` | `extreme_mood_swings` | `talk_of_death` | `giving_away_possessions` | `self_harm` | `suicidal_thoughts`

## 数据存储

- 位置: `data/mental-health-tracker.json`
- 格式: JSON 对象
