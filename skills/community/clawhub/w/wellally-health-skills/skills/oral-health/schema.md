# OralHealthTracker Schema

口腔健康追踪的完整数据结构定义。

## 字段速查

### 核心字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `checkup_records` | array | 口腔检查记录 |
| `treatment_records` | array | 治疗记录 |
| `hygiene_habits` | object | 卫生习惯 |
| `oral_issues` | array | 口腔问题记录 |
| `screening_records` | object | 疾病筛查记录 |
| `checkup_reminders` | object | 检查提醒 |
| `oral_health_score` | number | 口腔健康评分 |

## checkup_records 数组项

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `id` | string | 记录ID |
| `date` | string | 检查日期 |
| `teeth_status` | object | 牙齿状态 |
| `periodontal_status` | object | 牙周状况 |
| `soft_tissue` | string | 软组织状态 |
| `occlusion` | string | 咬合状态 |
| `tmj` | string | 颞下颌关节状态 |

### teeth_status 对象
- 键：牙位编号（FDI系统）
- 值：{condition: 状态, note: 备注}

### condition 枚举值
- normal（正常）
- caries（龋齿）
- missing（缺失）
- filling（充填）
- crown（牙冠）
- bridge（桥体）
- implant（种植）

## treatment_records 数组项

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `id` | string | 记录ID |
| `date` | string | 治疗日期 |
| `tooth_number` | string | 牙位编号 |
| `treatment_type` | enum | 治疗类型 |
| `material` | string | 治疗材料 |
| `cost` | number | 费用 |
| `anesthesia` | string | 麻醉方式 |
| `description` | string | 治疗描述 |

### treatment_type 枚举值
- filling（补牙）
- root_canal（根管治疗）
- extraction（拔牙）
- implant（种植牙）
- crown（牙冠）
- bridge（桥体）
- denture（假牙）
- orthodontic（正畸）
- scaling（洁牙）
- periodontal（牙周治疗）

## hygiene_habits 对象

### brushing（刷牙）
- frequency: once_daily/twice_daily/more_than_twice/irregular
- method: 刷牙方法
- duration_minutes: 刷牙时长
- toothbrush_type: 牙刷类型

### flossing（使用牙线）
- frequency: rarely/weekly/few_times_week/daily
- time: morning/evening/both

### mouthwash（漱口水）
- frequency: rarely/weekly/few_times_week/daily
- type: 漱口水类型

## oral_issues 数组项

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `id` | string | 记录ID |
| `date` | string | 记录日期 |
| `issue_type` | enum | 问题类型 |
| `tooth_number` | string | 涉及牙位 |
| `severity` | enum | 严重程度 |
| `duration` | string | 持续时间 |
| `description` | string | 描述 |
| `resolved` | boolean | 是否已解决 |

### issue_type 枚举值
- toothache（牙痛）
- bleeding（出血）
- ulcer（溃疡）
- sensitivity（敏感）
- swelling（肿胀）
- bad_breath（口臭）
- dry_mouth（口干）
- clicking（关节弹响）

## screening_records 对象

| 字段 | 说明 |
|-----|------|
| caries_risk | 龋齿风险评估 |
| periodontal_risk | 牙周风险评估 |
| oral_cancer | 口腔癌筛查 |

## 数据存储

- 位置: `data/oral-health-tracker.json`
