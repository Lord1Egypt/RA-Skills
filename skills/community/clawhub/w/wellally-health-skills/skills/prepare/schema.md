# Hospital Visit Preparation Schema

医院就诊准备和健康摘要的完整数据结构定义。

## Schema 文件

完整的 JSON Schema 定义：[schema.json](schema.json)

## 字段速查

### 必填字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `preparation_id` | string | 准备记录唯一标识符 (prep_YYYYMMDDHHmmssSSS) |
| `preparation_date` | string | 准备生成时间 (ISO 8601) |
| `health_summary` | object | 健康数据摘要 |

### 就诊目标类型 (visit_target.type)

`symptom` (症状) | `department` (科室) | `exam` (检查) | `general` (通用)

### 紧急程度 (urgency)

`emergency` (紧急) | `urgent` (急) | `routine` (常规)

### 过敏严重程度 (severity)

`mild` (轻度) | `moderate` (中度) | `severe` (重度) | `anaphylaxis` (过敏性休克)

### 症状到科室映射

| 症状关键词 | 推荐科室 |
|----------|---------|
| 头疼、头晕、眩晕 | 神经内科 |
| 胸痛、胸闷、心慌 | 心内科 |
| 咳嗽、咳痰、呼吸困难 | 呼吸内科 |
| 胃疼、肚子疼、腹泻 | 消化内科 |
| 发烧、发热 | 发热门诊或内科 |
| 皮疹、瘙痒 | 皮肤科 |
| 关节痛、腰痛 | 骨科或风湿免疫科 |
| 尿频、尿急、尿痛 | 泌尿外科 |
| 眼疼、视力模糊 | 眼科 |
| 耳朵疼、听力下降 | 耳鼻喉科 |
| 咽喉疼、声音嘶哑 | 耳鼻喉科 |
| 乳房肿块 | 乳腺外科 |
| 甲状腺结节 | 甲状腺外科或内分泌科 |
| 糖尿病、血糖高 | 内分泌科 |
| 高血压 | 心内科 |
| 儿童疾病 | 儿科 |
| 女性妇科问题 | 妇科 |
| 产科检查 | 产科 |
| 精神、情绪、睡眠 | 精神科或心理科 |
| 身体不适检查不明 | 全科/普通内科 |

## 必备证件清单

- 身份证/医保卡/社保卡 (必带)
- 医保卡/就诊卡 (必带)
- 银行卡或手机支付
- 既往病历资料 (如有)
- 过敏史清单 (必带) ⭐
- 过敏急救药物 (如严重过敏) ⭐

## 数据存储

- 位置: `data/hospital-visit-preparations.json`
- 格式: JSON 数组
- 模式: 追加
