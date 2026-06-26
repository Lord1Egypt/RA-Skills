# 男性生育健康 Schema 说明

## 记录类型 (record_type)

| 值 | 说明 |
|----|------|
| semen_analysis | 精液分析记录 |
| hormone_test | 激素检测记录 |
| varicocele_exam | 精索静脉曲张检查 |
| infection_test | 生殖道感染检查 |
| fertility_status | 生育健康状态 |
| diagnosis | 不育诊断 |

## 精液分析 (semen_analysis)

### 基本信息
- `abstinence_period`: 禁欲时间，格式如 "3_days"

### 精液量 (volume)
- `value`: 精液量数值 (mL)
- `reference`: 参考值 ">=1.5"
- `result`: 结果 "normal" / "abnormal" / "low"

### 精子密度 (concentration)
- `value`: 密度数值 (10^6/mL)
- `reference`: 参考值 ">=15"
- `result`: 结果

### 精子总数 (total_count)
- `value`: 总数值 (10^6)
- `reference`: 参考值 ">=39"
- `result`: 结果

### 精子活力 (motility)
- `pr.value`: 前向运动百分比，参考值 ">=32"
- `np.value`: 非前向运动百分比，参考值 ">=40"
- `im.value`: 不动精子百分比

### 精子形态 (morphology)
- `value`: 正常形态百分比
- `reference`: 参考值 ">=4"
- `result`: 结果

### pH值 (ph)
- `value`: pH数值
- `reference`: 参考值 "7.2-8.0"
- `result`: 结果

### 液化时间 (liquefaction)
- `value`: 液化时间 (分钟)
- `reference`: 参考值 "<=60"
- `result`: 结果

### 诊断 (diagnosis)
| 值 | 说明 |
|----|------|
| normospermia | 正常精液 |
| oligozoospermia | 少精症 |
| azoospermia | 无精症 |
| asthenozoospermia | 弱精症 |
| teratozoospermia | 畸形精子症 |
| hypospermia | 精液减少 |
| mixed_abnormalities | 混合异常 |

## 激素检测 (hormones)

### 睾酮 (testosterone)
- `total`: 总睾酮值 (nmol/L)，参考值 "10-35"
- `free`: 游离睾酮值 (nmol/L)，参考值 "0.22-0.65"
- `result`: "normal" / "low" / "high"

### 促黄体生成素 (lh)
- `value`: 数值 (IU/L)，参考值 "1.7-8.6"
- `result`: 结果

### 促卵泡刺激素 (fsh)
- `value`: 数值 (IU/L)，参考值 "1.5-12.4"
- `result`: 结果

### 泌乳素 (prl)
- `value`: 数值 (ng/mL)，参考值 "<15"
- `result`: 结果

### 雌二醇 (e2)
- `value`: 数值 (pg/mL)，参考值 "<70"
- `result`: 结果

## 精索静脉曲张 (varicocele)

- `present`: 是否存在
- `side`: 部位 - "none"(无) / "left"(左侧) / "right"(右侧) / "bilateral"(双侧)
- `grade`: 分级 - "I" / "II" / "III"
- `confirmed_by`: 确诊方式 - "ultrasound"(超声) / "physical_exam"(体检)
- `surgery`: 是否手术
- `surgery_date`: 手术日期

## 生殖道感染 (infections)

- `chlamydia`: 衣原体 - "positive"(阳性) / "negative"(阴性) / "not_tested"(未检测)
- `gonorrhea`: 淋球菌 - 同上
- `mycoplasma`: 支原体 - 同上
- `ureaplasma`: 解脲支原体 - 同上
- `date`: 检测日期
- `treated`: 是否已治疗
