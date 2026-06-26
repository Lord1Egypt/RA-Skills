# HealthFeelingLog Schema

健康感觉记录的完整数据结构定义。

## Schema 文件

完整的 JSON Schema 定义：[schema.json](schema.json)

## 字段速查

### 必填字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `timestamp` | string | ISO 8601 时间戳 |
| `symptom` | string | 症状描述 |

### 核心字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `bodyPart` | enum | 身体部位 |
| `painLevel` | enum | "1"-"10" |
| `severity` | int | 1-10 |
| `painType` | enum | 疼痛类型 |

### 扩展字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `duration` | string | 持续时间 |
| `frequency` | string | 发作频率 |
| `triggers` | string[] | 诱因 |
| `reliefFactors` | string[] | 缓解因素 |
| `accompanyingSymptoms` | string[] | 伴随症状 |
| `notes` | string | 备注 |
| `tags` | string[] | 标签 |
| `mood` | enum | 情绪状态 |
| `energyLevel` | int | 1-5 |

## 枚举值

### bodyPart
`头部` | `颈部` | `肩部` | `背部` | `胸部` | `腹部` | `左腹` | `右腹` | `上腹` | `下腹` | `手臂` | `左手` | `右手` | `腿部` | `左腿` | `右腿` | `脚部` | `全身` | `其他`

### painType
`钝痛` | `刺痛` | `胀痛` | `绞痛` | `隐痛` | `灼痛` | `跳痛` | `无`

### mood
`正常` | `焦虑` | `烦躁` | `低落` | `平静`

## 数据存储

- 位置: `data/health-feeling-logs.json`
- 格式: JSON 数组
- 模式: 追加
