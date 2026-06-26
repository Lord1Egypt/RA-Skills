# SleepTracker Schema

睡眠追踪的完整数据结构定义。

## 字段速查

### 核心字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `sleep_tracking` | object | 睡眠追踪配置 |
| `sleep_records` | array | 每日睡眠记录 |
| `sleep_assessments` | object | 睡眠评估（PSQI/Epworth/ISI） |
| `sleep_problems` | object | 睡眠问题记录 |
| `sleep_hygiene` | object | 睡眠卫生评估 |

## sleep_records 数组项

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `id` | string | 记录ID |
| `date` | string | 睡眠日期 |
| `sleep_times` | object | 睡眠时间 |
| `sleep_metrics` | object | 睡眠指标 |
| `sleep_stages` | object | 睡眠阶段 |
| `awakenings` | object | 夜间觉醒 |
| `sleep_quality` | object | 主观睡眠质量 |
| `factors` | object | 影响因素 |

### sleep_times 对象

| 字段 | 格式 | 说明 |
|-----|------|-----|
| `bedtime` | HH:mm | 上床时间 |
| `sleep_onset_time` | HH:mm | 入睡时间 |
| `wake_time` | HH:mm | 醒来时间 |
| `out_of_bed_time` | HH:mm | 起床时间 |

### sleep_metrics 对象

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `sleep_duration_hours` | number | 睡眠时长（小时） |
| `time_in_bed_hours` | number | 在床时长（小时） |
| `sleep_latency_minutes` | number | 入睡潜伏期（分钟） |
| `sleep_efficiency` | number | 睡眠效率（%） |
| `sleep_debt` | number | 睡眠债 |

### awakenings 对象

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `count` | integer | 觉醒次数 |
| `total_duration_minutes` | number | 总觉醒时长 |
| `causes` | array | 觉醒原因 |

### sleep_quality 对象

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `subjective_quality` | enum | excellent/very_good/good/fair/poor/very_poor |
| `quality_score` | integer | 1-10评分 |
| `rested_feeling` | enum | not_at_all/slightly/somewhat/quite/very |
| `morning_mood` | enum | very_tired/tired/neutral/energized/very_energized |

## sleep_assessments 对象

### psqi（匹兹堡睡眠质量指数）

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `components` | object | 7个成分评分（各0-3分） |
| `total_score` | integer | 总分（0-21分） |
| `interpretation` | enum | good/fair/poor |

### PSQI成分

| 成分 | 说明 |
|-----|------|
| `subjective_quality` | 主观睡眠质量 |
| `sleep_latency` | 入睡时间 |
| `sleep_duration` | 睡眠时间 |
| `sleep_efficiency` | 睡眠效率 |
| `sleep_disturbances` | 睡眠障碍 |
| `hypnotic_use` | 催眠药物使用 |
| `daytime_dysfunction` | 日间功能障碍 |

### epworth（Epworth嗜睡量表）

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `responses` | array | 8种情况评分（各0-3分） |
| `total_score` | integer | 总分（0-24分） |
| `interpretation` | enum | normal/mild/moderate/severe |

### isi（ISI失眠严重度）

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `total_score` | integer | 总分（0-28分） |
| `interpretation` | enum | no_clinical_insomnia/mild/moderate/severe |

## sleep_problems 对象

| 问题 | 字段 | 说明 |
|-----|------|-----|
| 失眠 | `insomnia` | type/onset/maintenance/mixed/early_awakening |
| 呼吸暂停 | `sleep_apnea` | risk_level/stop_bang_score/snoring |
| 不宁腿 | `rls` | presence/severity |

## sleep_hygiene 对象

### environment（睡眠环境）

| 字段 | 说明 |
|-----|------|
| `temperature` | 温度（理想18-22℃） |
| `lighting` | dark/dim/bright |
| `noise` | quiet/moderate/loud |
| `mattress` | good/fair/poor |
| `pillow` | good/fair/poor |

### habits（睡眠习惯）

| 字段 | 说明 |
|-----|------|
| `screen_time_before_bed` | 睡前屏幕时间（分钟） |
| `caffeine_cutoff` | 咖啡因截止时间 |
| `exercise_time` | 运动时间 |
| `routine_consistency` | routine一致性 |

## 数据存储

- 位置: `data/sleep-tracker.json`
