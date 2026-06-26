# RehabilitationTracker Schema

康复训练管理的完整数据结构定义。

## Schema 文件

完整的 JSON Schema 定义：[schema.json](schema.json)

## 字段速查

### 用户档案

| 字段 | 类型 | 说明 |
|-----|------|-----|
| condition | enum | 康复类型 |
| injury_date | string | 受伤日期 |
| surgery_date | string | 手术日期 |
| current_phase | string | 当前阶段 |

### 训练记录

| 字段 | 类型 | 说明 |
|-----|------|-----|
| exercise_name | string | 训练名称 |
| exercise_category | enum | 训练类别 |
| sets/reps | int | 组数/次数 |
| pain_level | int | 疼痛评分 (0-10) |
| rpe | int | 主观体力感知 (6-20) |

### 功能评估

| 字段 | 类型 | 说明 |
|-----|------|-----|
| rom | object | 关节活动度 |
| muscle_strength | object | 肌力等级 (0-5/5) |
| pain_assessment | object | 疼痛评估 |
| balance | object | 平衡评估 |
| gait | object | 步态评估 |

### 康复目标

| 字段 | 类型 | 说明 |
|-----|------|-----|
| category | enum | rom/strength/functional/pain/activity |
| baseline | number | 基线值 |
| current | number | 当前值 |
| target | number | 目标值 |
| status | enum | 目标状态 |

## 枚举值

### 康复类型
`acl_reconstruction` | `meniscus_surgery` | `fracture` | `joint_replacement` | `spine_surgery` | `ankle_sprain` | `knee_injury` | `shoulder_injury` | `tennis_elbow` | `muscle_strain` | `stroke` | `spinal_cord_injury` | `parkinsons` | `multiple_sclerosis` | `cardiac_surgery` | `copd` | `pneumonia` | `covid_rehab`

### 训练类别
`rom_exercises` | `stretching` | `strength` | `balance` | `functional`

### 目标类别
`rom` | `strength` | `functional` | `pain` | `activity`

### 目标状态
`pending` | `in_progress` | `on_track` | `behind` | `achieved` | `cancelled`

### 平衡测试类型
`single_leg_stance` | `berg_balance` | `tug` | `tinetti`

## 数据存储

- 位置: `data/rehabilitation-tracker.json`
- 格式: JSON 对象
