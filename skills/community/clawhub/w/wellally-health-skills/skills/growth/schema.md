# 儿童生长数据结构说明

## 数据文件
`data/growth-tracker.json`

## 主要结构

### child_profile (儿童基础信息)

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| child_id | string | 是 | 儿童唯一标识 |
| name | string | 是 | 儿童姓名 |
| birth_date | string | 是 | 出生日期 YYYY-MM-DD |
| gender | string | 是 | 性别：male/female |

### measurements (测量记录)

| 字段 | 类型 | 说明 |
|------|------|------|
| date | string | 测量日期 |
| age_months | integer | 月龄 |

### height (身高数据)

| 字段 | 类型 | 说明 |
|------|------|------|
| value | number | 身高值（cm） |
| percentile | number | 百分位（0-100） |
| z_score | number | Z-score标准差分数 |
| velocity | number | 生长速度（cm/年） |
| velocity_period | string | 速度计算周期（如"12_months"） |
| velocity_percentile | number | 速度百分位 |

### weight (体重数据)

| 字段 | 类型 | 说明 |
|------|------|------|
| value | number | 体重值（kg） |
| percentile | number | 百分位 |
| z_score | number | Z-score |
| velocity | number | 生长速度（kg/年） |
| velocity_percentile | number | 速度百分位 |

### bmi (BMI数据)

| 字段 | 类型 | 说明 |
|------|------|------|
| value | number | BMI值 |
| percentile | number | 百分位 |
| z_score | number | Z-score |

### head_circumference (头围数据，0-3岁)

| 字段 | 类型 | 说明 |
|------|------|------|
| value | number | 头围值（cm） |
| percentile | number | 百分位 |
| z_score | number | Z-score |

### growth_assessment (生长评估)

| 字段 | 类型 | 说明 |
|------|------|------|
| overall | string | 整体评估 |
| height_status | string | 身高状态 |
| weight_status | string | 体重状态 |
| bmi_status | string | BMI状态 |

### 评估状态值

| overall | 说明 |
|---------|------|
| normal | 正常 |
| stunting | 生长迟缓 |
| underweight | 体重不足 |
| overweight | 超重 |
| obesity | 肥胖 |

| height_status | 说明 |
|-------------|------|
| normal | 正常 |
| stunted | 生长迟缓（HAZ<-2） |
| tall | 高身材 |

| weight_status | 说明 |
|-------------|------|
| normal | 正常 |
| underweight | 体重不足（WAZ<-2） |
| overweight | 超重（WAZ>+2） |

| bmi_status | 说明 |
|-----------|------|
| normal | 正常 |
| wasting | 消瘦（BAZ<-2） |
| overweight | 超重风险（BAZ>+1） |
| obese | 肥胖（BAZ>+2） |

## Z-score 解释

Z-score 表示测量值偏离同龄同性别儿童平均值的标准差数量：

| Z-score | 解释 |
|---------|------|
| -3 | 严重偏低（0.13%） |
| -2 | 明显偏低（2.3%） |
| -1 | 轻度偏低（15.9%） |
| 0 | 平均值（50%） |
| +1 | 轻度偏高（84.1%） |
| +2 | 明显偏高（97.7%） |
| +3 | 严重偏高（99.87%） |

## WHO 生长标准

本系统使用WHO儿童生长标准：
- 0-5岁：WHO Child Growth Standards
- 5-19岁：WHO Growth Reference 2007

## 生长异常判断标准

| 异常类型 | 判断条件 |
|----------|----------|
| 生长迟缓 | HAZ < -2 |
| 体重不足 | WAZ < -2 |
| 消瘦 | WHZ < -2 |
| 超重 | WAZ > +1 或 BAZ > +1 |
| 肥胖 | BAZ > +2 |
| 速度异常 | 速度 < 第5百分位 |
