# 男性更年期 Schema 说明

## 记录类型 (record_type)

| 值 | 说明 |
|----|------|
| symptom | 症状记录 |
| testosterone_test | 睾酮检测 |
| adam_questionnaire | ADAM问卷 |
| trt_treatment | TRT治疗 |
| monitoring | 监测指标 |
| status | 状态查看 |
| diagnosis | 诊断 |

## 症状记录 (symptoms)

### 性症状 (sexual)
- `libido.present`: 是否存在性欲减退
- `libido.severity`: 严重程度 - "mild"(轻度) / "moderate"(中度) / "severe"(重度)
- `libido.impact`: 影响描述
- `erectile_function.present`: 是否存在勃起功能障碍
- `erectile_function.morning_erection`: 晨勃情况 - "reduced"(减少) / "absent"(消失)

### 躯体症状 (physical)
- `fatigue.present`: 是否容易疲劳
- `fatigue.severity`: 严重程度
- `fatigue.impact_on_activities`: 对活动的影响
- `muscle_mass.present`: 肌肉量变化
- `muscle_mass.changes`: 变化描述 - "slight_decrease"(轻度减少) / "moderate_decrease"(中度减少)
- `body_fat.present`: 体脂变化
- `body_fat.distribution`: 脂肪分布 - "abdominal"(腹部)
- `hot_flashes.present`: 是否有潮热

### 心理症状 (psychological)
- `mood.present`: 情绪变化
- `mood.symptoms`: 症状列表 - "depressed"(抑郁) / "irritability"(易怒) / "anxiety"(焦虑)
- `memory.present`: 记忆力变化
- `memory.complaints`: 主诉描述
- `concentration.present`: 注意力变化
- `concentration.impact`: 影响描述

## 睾酮检测 (testosterone_levels)

### 总睾酮 (total_testosterone)
- `value`: 数值 (nmol/L)
- `reference`: 参考值 "10-35"
- `result`: 结果 - "normal" / "low" / "high"
- `confirmed`: 是否已确认 (需重复测定)
- `repeat_count`: 重复测定次数

### 游离睾酮 (free_testosterone)
- `value`: 数值 (nmol/L)
- `reference`: 参考值 "0.22-0.65"
- `result`: 结果

### SHBG
- `value`: 数值 (nmol/L)
- `reference`: 参考值 "20-50"
- `result`: 结果

## ADAM问卷 (questionnaire_scores.adam)

### 问题列表
每个问题包含:
- `q`: 问题内容
- `answer`: 回答 (true=是, false=否)
- `score`: 得分 (1或0)

### 评估结果
- `total_score`: 总分 (0-10)
- `positive`: 是否阳性 (>=3分为阳性)
- `interpretation`: 结果解释

## TRT治疗 (trt)

- `on_treatment`: 是否正在治疗
- `medication`: 药物名称
- `type`: 剂型 - "gel"(凝胶) / "injection"(注射) / "oral"(口服) / "patch"(贴片)
- `dose`: 剂量
- `frequency`: 使用频次
- `route`: 给药途径
- `start_date`: 开始日期
- `duration_months`: 治疗月数
- `effectiveness`: 疗效评估
- `effectiveness_rating`: 疗效评分 (1-10)
- `side_effects`: 副作用列表
- `side_effects_severity`: 副作用严重程度
- `quality_of_life_improvement`: 生活质量改善
- `notes`: 备注

## 监测指标 (monitoring)

### PSA监测
- `baseline`: 基线值
- `current`: 当前值
- `change`: 变化量
- `date`: 检测日期
- `interpretation`: 结果解释 - "stable"(稳定) / "increased"(升高)

### 红细胞压积 (hematocrit)
- `baseline`: 基线值
- `current`: 当前值
- `threshold`: 警戒值 (54%)
- `status`: 状态 - "normal" / "elevated"(升高)

### 前列腺体积 (prostate_volume)
- `baseline`: 基线值 (mL)
- `current`: 当前值 (mL)
- `date`: 检测日期
- `change`: 变化描述
