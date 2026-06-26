# MenopauseTracker Schema

更年期管理的完整数据结构定义。

## Schema 文件

完整的JSON Schema定义：[schema.json](schema.json)

## 字段速查

### 根级别字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `created_at` | string | ISO 8601 创建时间 |
| `last_updated` | string | ISO 8601 最后更新时间 |
| `menopause_tracking` | object | 更年期追踪数据 |
| `statistics` | object | 统计数据 |
| `settings` | object | 设置 |

### menopause_tracking 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `menopause_id` | string | 记录ID |
| `stage` | enum | 阶段：perimenopausal/menopausal/postmenopausal |
| `age` | int | 年龄（40-65） |
| `last_menstrual_period` | string | 末次月经日期 |
| `months_since_lmp` | int | 距末次月经月数 |
| `symptoms` | object | 症状数据 |
| `symptom_history` | array | 症状历史 |
| `hrt` | object | HRT治疗数据 |
| `bone_density` | object | 骨密度数据 |
| `cardiovascular_risk` | object | 心血管风险 |
| `lifestyle` | object | 生活方式 |

### symptoms 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `hot_flashes` | object | 潮热 |
| `night_sweats` | object | 盗汗 |
| `sleep_issues` | object | 睡眠问题 |
| `mood_changes` | object | 情绪变化 |
| `vaginal_dryness` | object | 阴道干涩 |
| `joint_pain` | object | 关节痛 |

### hot_flashes 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `present` | bool | 是否存在 |
| `frequency` | string | 频率描述 |
| `frequency_count` | int | 频率次数 |
| `severity` | string | 严重程度 |
| `severity_level` | int | 严重级别（1-3） |
| `impact_on_life` | string | 对生活影响 |
| `triggers` | string[] | 触发因素 |
| `relief_methods` | string[] | 缓解方法 |
| `score` | int | 评分 |

### hrt 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `on_treatment` | bool | 是否在治疗 |
| `considering` | bool | 是否考虑 |
| `medication` | string/null | 药物名称 |
| `type` | enum | 治疗类型 |
| `dose` | string/null | 剂量 |
| `route` | enum | 用药方式 |
| `start_date` | string/null | 开始日期 |
| `duration_months` | int/null | 治疗时长 |
| `effectiveness` | string/null | 效果 |
| `effectiveness_rating` | int/null | 效果评分 |
| `side_effects` | string[] | 副作用 |

### bone_density 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `last_check` | string/null | 最后检查日期 |
| `t_score` | number/null | T值 |
| `z_score` | number/null | Z值 |
| `diagnosis` | enum | 诊断结果 |
| `fracture_risk` | enum | 骨折风险 |
| `next_check_due` | string/null | 下次检查日期 |

## 枚举值

### stage
`perimenopausal` (围绝经期) | `menopausal` (绝经) | `postmenopausal` (绝经后)

### diagnosis
`normal` (正常) | `osteopenia` (骨量减少) | `osteoporosis` (骨质疏松)

### fracture_risk
`low` (低) | `moderate` (中) | `high` (高)

### hrt.type
`estrogen_only` (仅雌激素) | `estrogen_plus_progesterone` (雌孕激素联合) | `vaginal_estrogen` (局部雌激素)

### hrt.route
`oral` (口服) | `patch` (贴片) | `gel` (凝胶) | `vaginal` (阴道)

## 数据存储

- 主文件: `data/menopause-tracker.json`
- 详细记录: `data/更年期记录/YYYY-MM/YYYY-MM-DD_症状记录.json`
- 模式: 更新
