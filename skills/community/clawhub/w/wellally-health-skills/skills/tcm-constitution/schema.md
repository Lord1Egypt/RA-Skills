# TCMConstitutionTracker Schema

中医体质辨识与养生管理的完整数据结构定义。

## 字段速查

### 核心字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `constitution_tracking` | object | 体质追踪数据 |
| `wellness_plan` | object | 养生计划 |
| `questionnaire_progress` | object | 问卷进度 |

## constitution_tracking 对象

| 字段 | 说明 |
|-----|------|
| `user_profile` | 用户基本信息 |
| `latest_assessment` | 最近评估结果 |
| `assessment_history` | 评估历史 |
| `trend_analysis` | 趋势分析 |

### latest_assessment 对象

| 字段 | 说明 |
|-----|------|
| `primary_type` | 主体质类型 |
| `secondary_types` | 兼夹体质 |
| `scores` | 各体质评分 |

### nine_types（九种体质）

| 体质 | 英文 | 说明 |
|-----|------|------|
| 平和质 | peaceful | 阴阳气血调和 |
| 气虚质 | qi_deficiency | 疲乏、气短、自汗 |
| 阳虚质 | yang_deficiency | 畏寒、怕冷、手脚凉 |
| 阴虚质 | yin_deficiency | 盗汗、咽干、手足心热 |
| 痰湿质 | phlegm_dampness | 肥胖、腹部肥满、面油 |
| 湿热质 | damp_heat | 面垢油光、易生痤疮 |
| 血瘀质 | blood_stasis | 肤色晦暗、易有瘀斑 |
| 气郁质 | qi_stagnation | 精神抑郁、多愁善感 |
| 特禀质 | special_constitution | 易过敏、喷嚏、鼻塞 |

## wellness_plan 对象

### dietary_recommendations（饮食建议）

| 字段 | 说明 |
|-----|------|
| `constitution_type` | 体质类型 |
| `foods_to_eat` | 宜食食物 |
| `foods_to_avoid` | 忌食食物 |
| `recipes` | 推荐食谱 |

### exercise_recommendations（运动建议）

| 字段 | 说明 |
|-----|------|
| `recommended_exercises` | 推荐运动 |
| `frequency` | 频率 |
| `duration_minutes` | 时长 |
| `intensity` | 强度 |
| `precautions` | 注意事项 |

### acupoint_recommendations（穴位保健）

| 字段 | 说明 |
|-----|------|
| `acupoints` | 推荐穴位数组 |
| `name` | 穴位名称 |
| `location` | 位置 |
| `method` | 方法 |
| `duration_minutes` | 时长 |
| `frequency` | 频率 |

### herbal_references（中药参考）

| 字段 | 说明 |
|-----|------|
| `constitution_formulas` | 各体质对应方剂 |
| `formula_name` | 方剂名称 |
| `ingredients` | 组成 |
| `indications` | 适应症 |
| `contra_indications` | 禁忌症 |
| `warnings` | 警告 |

## 问卷进度对象

| 字段 | 说明 |
|-----|------|
| `is_active` | 问卷是否进行中 |
| `current_question` | 当前题目编号 |
| `answers` | 已记录答案 |

## 评分判定标准

| 体质 | 转化分 | 判定结果 |
|-----|-------|---------|
| 平和质 | <30分 且 其他8种<40分 | 是 |
| 偏颇质 | >=40分 | 是 |
| 兼夹质 | 2-3种>=40分 | 是 |

## 数据存储

- 位置: `data/tcm-constitution-tracker.json`
