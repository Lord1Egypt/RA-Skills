# 前列腺健康 Schema 说明

## 记录类型 (record_type)

| 值 | 说明 |
|----|------|
| psa_test | PSA检测 |
| ipss_score | IPSS症状评分 |
| dre_exam | 直肠指检 |
| ultrasound_exam | 前列腺超声 |
| status | 状态查看 |
| screening_plan | 筛查计划 |
| risk_assessment | 风险评估 |

## PSA检测结果 (psa_result)

- `total_psa`: 总PSA值 (ng/mL)
- `free_psa`: 游离PSA值 (ng/mL)
- `ratio`: 游离/总PSA比值
- `unit`: 单位 - "ng/mL"
- `reference`: 参考值 - "<4.0"
- `trend`: 趋势 - "stable"(稳定) / "increasing"(升高) / "decreasing"(下降)
- `risk_level`: 风险等级
  - "low": 低风险
  - "low-moderate": 低中风险
  - "moderate": 中风险
  - "high": 高风险
- `interpretation`: 结果解释

## IPSS评分 (ipss_score)

### 评分项 (每项0-5分)
- `incomplete_emptying`: 不完全排空感
- `frequency`: 排尿频度
- `intermittency`: 排尿间断
- `urgency`: 排尿犹豫
- `weak_stream`: 尿流弱
- `straining`: 用力排尿
- `nocturia`: 夜尿次数

### 评分结果
- `total_score`: 总分 (0-35)
- `severity`: 严重程度
  - "mild": 轻度 (0-7分)
  - "moderate": 中度 (8-19分)
  - "severe": 重度 (20-35分)
- `quality_of_life_score`: 生活质量评分 (0-6分)

## 直肠指检 (dre)

- `last_exam`: 检查日期
- `findings`: 检查发现
- `size`: 前列腺大小 - "normal"(正常) / "enlarged"(增大) / "atrophied"(缩小)
- `texture`: 质地 - "soft"(软) / "firm"(硬) / "nodular"(结节状) / "hard"(硬)
- `nodule`: 是否有结节
- `tenderness`: 是否有触痛
- `mobility`: 活动度 - "normal"(正常) / "reduced"(降低) / "fixed"(固定)
- `notes`: 备注

## 前列腺体积 (prostate_volume)

- `volume_ml`: 体积 (mL)
- `weight_g`: 估算重量 (g) = 体积 × 1.05
- `inner_gland_cm`: 内腺大小 (cm)
- `residual_urine_ml`: 残余尿量 (mL)
- `nodule`: 是否有结节
- `calcification`: 是否有钙化
- `interpretation`: 结果解释
  - "normal": 正常 (20-30 mL)
  - "mild_enlargement": 轻度增大 (30-50 mL)
  - "moderate_enlargement": 中度增大 (50-80 mL)
  - "severe_enlargement": 重度增大 (>80 mL)
  - "atrophied": 缩小 (<20 mL)

## 筛查计划 (screening_plan)

- `psa_frequency`: PSA检测频率 - "每年1次" / "每年2次"
- `dre_frequency`: DRE检查频率
- `next_psa`: 下次PSA检测日期
- `next_dre`: 下次DRE检查日期
- `risk_category`: 风险类别 - "average"(一般风险) / "high"(高风险)
