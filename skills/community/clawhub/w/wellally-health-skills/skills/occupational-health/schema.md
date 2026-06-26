# 职业健康数据结构说明

## 字段说明

### timestamp (必填)
- **类型**: `string` (ISO 8601 格式)
- **说明**: 记录的时间戳
- **示例**: `"2026-02-03T10:30:00Z"`

### workType (必填)
- **类型**: `string` (枚举)
- **说明**: 工作类型分类
- **可选值**:
  - `office_work` - 办公室工作
  - `manual_labor` - 体力劳动
  - `shift_work` - 倒班工作
  - `noisy_environment` - 噪音环境工作
  - `dust_chemical_environment` - 粉尘/化学环境工作
  - `other` - 其他

### hoursPerDay
- **类型**: `number`
- **范围**: 0-24
- **说明**: 每天工作小时数

### daysPerWeek
- **类型**: `integer`
- **范围**: 1-7
- **说明**: 每周工作天数

### healthIssues (数组)
健康问题列表，每个问题包含：

#### type
- **类型**: `string` (枚举)
- **说明**: 健康问题类型
- **可选值**:
  - `neck_pain` - 颈痛
  - `shoulder_pain` - 肩痛
  - `back_pain` - 背痛
  - `wrist_pain` - 腕痛
  - `carpal_tunnel` - 腕管综合征
  - `eye_strain` - 眼疲劳
  - `headache` - 头痛
  - `fatigue` - 疲劳
  - `stress` - 工作压力
  - `sleep_disturbance` - 睡眠障碍
  - `other` - 其他

#### severity
- **类型**: `string` (枚举)
- **说明**: 严重程度
- **可选值**: `mild`(轻度) | `moderate`(中度) | `severe`(重度)

#### frequency
- **类型**: `string` (枚举)
- **说明**: 发生频率
- **可选值**:
  - `rare` - 罕见（每月<1次）
  - `occasional` - 偶尔（每月1-4次）
  - `often` - 经常（每周1-3次）
  - `daily` - 每天
  - `constant` - 持续

### riskAssessment (对象)
风险评估结果

#### sedentaryRisk
- **类型**: `string` (枚举)
- **说明**: 久坐风险
- **可选值**: `low` | `medium` | `high`

#### screenRisk
- **类型**: `string` (枚举)
- **说明**: 视屏终端风险
- **可选值**: `low` | `medium` | `high`

#### overallRisk
- **类型**: `string` (枚举)
- **说明**: 综合风险等级
- **可选值**: `low` | `medium` | `high`

### ergonomicScore
- **类型**: `integer`
- **范围**: 0-100
- **说明**: 人机工程评分（越低越好）

### notes
- **类型**: `string`
- **说明**: 额外备注信息

## 数据示例

```json
{
  "timestamp": "2026-02-03T10:30:00Z",
  "workType": "office_work",
  "hoursPerDay": 8,
  "daysPerWeek": 5,
  "healthIssues": [
    {
      "type": "neck_pain",
      "severity": "moderate",
      "frequency": "often",
      "onsetTime": "3个月前"
    },
    {
      "type": "eye_strain",
      "severity": "mild",
      "frequency": "daily"
    }
  ],
  "riskAssessment": {
    "sedentaryRisk": "high",
    "screenRisk": "high",
    "overallRisk": "high"
  },
  "ergonomicScore": 65,
  "notes": "需要改善人机工程设置"
}
```
