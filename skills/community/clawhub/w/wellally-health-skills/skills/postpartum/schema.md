# PostpartumTracker Schema

产后护理管理的完整数据结构定义。

## Schema 文件

完整的JSON Schema定义：[schema.json](schema.json)

## 字段速查

### 根级别字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `created_at` | string | ISO 8601 创建时间 |
| `last_updated` | string | ISO 8601 最后更新时间 |
| `current_postpartum` | object/null | 当前产后记录 |
| `postpartum_history` | array | 产后历史记录 |
| `statistics` | object | 统计数据 |
| `settings` | object | 设置 |

### current_postpartum 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `postpartum_id` | string | 记录ID，格式：postpartum_YYYYMMDD |
| `delivery_date` | string | 分娩日期 |
| `delivery_type` | enum | 分娩方式：vaginal/c-section |
| `baby_count` | int | 宝宝数量（1-4） |
| `tracking_period` | enum | 追踪期：6weeks/6months/1year |
| `tracking_end_date` | string | 追踪结束日期 |

### current_status 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `days_postpartum` | int | 产后天数 |
| `stage` | enum | 阶段：immediate/early/subacute/late |
| `progress_percentage` | int | 进度百分比 |

### recovery_tracking 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `lochia` | object | 恶露记录 |
| `perineal_care` | object | 会阴护理 |
| `breastfeeding` | object | 哺乳记录 |
| `pain` | object | 疼痛记录 |

### lochia 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `stage` | enum | 阶段：rubra/serosa/alba |
| `amount` | enum | 量：light/moderate/heavy |
| `last_updated` | string/null | 最后更新时间 |

### mental_health 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `epds` | object | EPDS筛查数据 |
| `mood_log` | array | 情绪日志 |

### epds 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `last_screened` | string/null | 最后筛查日期 |
| `total_score` | int/null | 总分（0-30） |
| `risk_level` | enum | 风险：low/moderate/high/emergency |
| `q10_positive` | bool | Q10是否阳性 |
| `last_updated` | string/null | 最后更新时间 |

### babies 数组元素

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `baby_id` | string | 宝宝标识（A/B/C/D） |
| `name` | string/null | 姓名 |
| `gender` | string/null | 性别 |
| `birth_weight` | number/null | 出生体重 |
| `current_weight` | object/null | 当前体重 |
| `feeding` | object | 喂养记录 |
| `sleep` | object | 睡眠记录 |
| `diapers` | object | 尿布记录 |

### feeding 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `method` | enum | 方式：exclusive/mixed/formula |
| `pattern` | string | 模式：on_demand/scheduled |
| `last_feed` | object/null | 最后喂养 |
| `feeds_today` | int/null | 今日喂养次数 |

## 枚举值

### delivery_type
`vaginal` (顺产) | `c-section` (剖宫产)

### stage
`immediate` (急性期0-2天) | `early` (早期3-14天) | `subacute` (亚急性期15-42天) | `late` (恢复期43天+)

### lochia.stage
`rubra` (红色) | `serosa` (浆液性) | `alba` (白色)

### lochia.amount
`light` (少) | `moderate` (中) | `heavy` (多)

### feeding.method
`exclusive` (纯母乳) | `mixed` (混合) | `formula` (配方奶)

### epds.risk_level
`low` (低风险) | `moderate` (中度风险) | `high` (高风险) | `emergency` (紧急)

## 数据存储

- 主文件: `data/postpartum-tracker.json`
- 详细记录: `data/产后记录/YYYY-MM/YYYY-MM-DD_产后记录.json`
- 模式: 更新/追加
