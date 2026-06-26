# Specialist Consultation Schema

专科专家咨询的完整数据结构定义。

## Schema 文件

完整的 JSON Schema 定义：[schema.json](schema.json)

## 字段速查

### 必填字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `consultation_id` | string | 咨询唯一标识符 (spec_YYYYMMDDHHmmssSSS) |
| `consultation_date` | string | 咨询时间 (ISO 8601) |
| `specialty.code` | enum | 专科代码 |
| `specialty.name` | string | 专科名称 |

### 专科代码映射

| 代码 | 专科名称 | 擅长领域 |
|-----|---------|---------|
| `cardio` | 心内科 | 心脏病、高血压、血脂异常 |
| `endo` | 内分泌科 | 糖尿病、甲状腺疾病 |
| `gastro` | 消化科 | 肝病、胃肠疾病 |
| `nephro` | 肾内科 | 肾脏病、电解质紊乱 |
| `heme` | 血液科 | 贫血、凝血异常 |
| `resp` | 呼吸科 | 肺部感染、肺结节 |
| `neuro` | 神经内科 | 脑血管病、头痛头晕 |
| `onco` | 肿瘤科 | 肿瘤标志物、肿瘤筛查 |
| `ortho` | 骨科 | 骨折、关节炎、骨质疏松 |
| `derma` | 皮肤科 | 湿疹、痤疮、皮肤肿瘤 |
| `pedia` | 儿科 | 儿童发育、新生儿疾病 |
| `gyne` | 妇科 | 月经疾病、妇科肿瘤 |
| `general` | 全科 | 综合评估、慢病管理 |
| `psych` | 精神科 | 情绪障碍、心理健康 |

### 数据范围类型 (data_range.type)

`all` (所有数据) | `recent` (最近N条) | `date` (指定日期) | `date_range` (日期范围) | `default` (默认最近3条)

### 慢性病数据读取规则

| 专科代码 | 读取数据文件 |
|---------|-------------|
| `cardio` | data/hypertension-tracker.json |
| `endo` | data/diabetes-tracker.json |
| `resp` | data/copd-tracker.json |
| `nephro` | data/hypertension-tracker.json + data/diabetes-tracker.json |

### 风险等级 (risk_assessment)

`low` (低危) | `medium` (中危) | `high` (高危) | `very_high` (很高危)

### 建议优先级 (priority)

`urgent` (紧急) | `high` (高) | `medium` (中) | `low` (低)

## 数据存储

- 位置: `data/specialist-consultations.json`
- 格式: JSON 数组
- 模式: 追加
