---
name: growth
description: Track child growth measurements (height, weight, BMI, head circumference) with WHO growth standards percentile analysis and velocity tracking. Use when user mentions child height, weight, growth, or physical development.
argument-hint: <操作类型: record/status/percentile/velocity/check/history, 如: record 112.5cm 20.5kg, status, percentile, velocity, check>
allowed-tools: Read, Write
schema: growth/schema.json
---

# Child Growth Curve Tracking Skill

Child growth monitoring and assessment, based on WHO child growth standards, providing percentile analysis and growth abnormality alerts.

## 核心流程

```
用户输入 → 解析测量信息 → 读取儿童信息 → 计算月龄 → 计算百分位/Z-score → 评估生长状态 → 保存数据
```

## 步骤 1: 解析用户输入

### Operation Type Mapping

| Input | action | Description |
|------|--------|-------------|
| record | record | Record growth data |
| status | status | View growth assessment |
| percentile | percentile | Percentile analysis |
| velocity | velocity | Growth velocity |
| check | check | Abnormality check |
| history | history | History records |

### 测量参数识别

| 输入模式 | 参数 | 值示例 |
|----------|------|--------|
| height[:\s]+(\d+\.?\d*) | height | 112.5 |
| (\d+\.?\d*)\s*cm | height | 112.5 |
| weight[:\s]+(\d+\.?\d*) | weight | 20.5 |
| (\d+\.?\d*)\s*kg | weight | 20.5 |
| head[:\s]+(\d+\.?\d*) | head_circumference | 48 |
| date[:\s]+(\d{4}-\d{2}-\d{2}) | date | 2025-06-15 |

## 步骤 2: 检查信息完整性

### record Operation Required:
- At least one measurement value (height/weight/head)

### Must Have (read from profile):
- Child's name
- Birth date
- Gender

## 步骤 3: 计算年龄和月龄

```javascript
birthDate = profile.child_birth_date
measurementDate = date || today

ageMonths = (measurementDate - birthDate) / 30.44
ageYears = ageMonths / 12

// 早产儿矫正（如需要）
if gestational_age < 37 weeks and age < 2 years:
  correctedAge = chronologicalAge - (40 - gestational_age)
```

## 步骤 4: 计算BMI

```javascript
if height && weight:
  bmi = weight / (height / 100)²
```

## 步骤 5: 计算百分位和Z-score

```javascript
// 从WHO标准查找
percentile = calculatePercentile(value, whoData)
zScore = (value - median) / standardDeviation
```

### Z-score分级

| Z-score | Assessment |
|---------|------------|
| < -3 | Severely low |
| -3 to -2 | Significantly low |
| -2 to -1 | Mildly low |
| -1 to +1 | Normal |
| +1 to +2 | Mildly high |
| +2 to +3 | Significantly high |
| > +3 | Severely high |

## 步骤 6: 评估生长状态

### Height Assessment (HAZ)

| HAZ | Assessment |
|-----|------------|
| < -2 | Stunting |
| -2 to -1 | Mild stunting |
| -1 to +1 | Normal |
| > +1 | Tall stature |

### Weight Assessment (WAZ)

| WAZ | Assessment |
|-----|------------------|
| < -3 | Severe underweight |
| -3 to -2 | Moderate underweight |
| -2 to -1 | Mild underweight |
| -1 to +2 | Normal |
| > +2 | Overweight |

### BMI Assessment (BAZ)

| BAZ | Assessment |
|-----|---------------|
| < -2 | Wasting |
| -2 to +1 | Normal |
| > +1 | Overweight risk |
| > +2 | Obese |

## 步骤 7: 生成评估报告

### 正常生长示例:
```
生长数据已记录

测量信息：
  日期：2025年6月20日
  年龄：5岁5个月（65月龄）

  身高：112.5 cm
    百分位：第50百分位 (P50)
    Z-score：0.0
    生长速度：6.5 cm/年（第50百分位）

  体重：20.5 kg
    百分位：第55百分位 (P55)
    Z-score：+0.13
    生长速度：2.8 kg/年（第60百分位）

  BMI：16.2
    百分位：第60百分位 (P60)
    Z-score：+0.25

生长评估：
  身高：正常（第50百分位）
  体重：正常（第55百分位）
  BMI：正常（第60百分位）
  生长速度：正常（第50百分位）
  比例：匀称

综合评估：
  生长正常
  儿童身高、体重、BMI均在正常范围内，
  生长速度正常，身体比例匀称。

建议：
  继续保持健康生活方式
  均衡营养
  适量运动
  充足睡眠
  定期体检

数据已保存
```

### 生长异常警示:
```
生长异常提示

测量信息：
  日期：2025年6月20日
  年龄：5岁5个月（65月龄）

  身高：105.0 cm
    百分位：第3百分位 (P3)
    Z-score：-1.9
    生长速度：4.5 cm/年（第3百分位）

  体重：16.5 kg
    百分位：第5百分位 (P5)
    Z-score：-1.6

  BMI：15.0
    百分位：第15百分位 (P15)

生长评估：
  身高：生长迟缓（第3百分位）
  体重：体重不足（第5百分位）
  生长速度：生长速度缓慢

可能原因：
  遗传因素
  营养不良
  慢性疾病
  内分泌异常
  吸收障碍

建议就医：
  建议尽快咨询：
  - 儿科
  - 儿童保健科
  - 内分泌科（如需要）

  进一步检查：
  - 骨龄评估
  - 营养评估
  - 甲状腺功能
  - 生长激素水平

数据已保存
```

## 步骤 8: 保存数据

保存到 `data/growth-tracker.json`，包含:
- child_profile: 儿童基础信息
- growth_tracking.measurements: 测量记录
- growth_tracking.growth_assessment: 生长评估
- growth_tracking.alerts: 预警信息
- statistics: 统计信息

## 生长速度参考

| 年龄 | 身高速度（男） |
|------|---------------|
| 0-1岁 | 20-30 cm/年 |
| 1-2岁 | 10-14 cm/年 |
| 2-3岁 | 8-11 cm/年 |
| 3-4岁 | 7-9 cm/年 |
| 4-5岁 | 6-8 cm/年 |
| 5-6岁 | 6-7 cm/年 |

## 生长异常预警条件

- 身高 < -2SD（生长迟缓）
- 体重 < -2SD（体重不足）
- BMI > +2SD（肥胖）
- 生长速度 < 第5百分位

## 执行指令

1. 读取 data/profile.json 获取儿童信息
2. 解析测量值
3. 计算月龄、BMI、百分位、Z-score
4. 评估生长状态
5. 保存到 data/growth-tracker.json

## 医学安全原则

### 安全红线
- 不做生长障碍诊断
- 不预测成年身高
- 不推荐生长激素治疗

### 系统能做到的
- 生长数据记录与追踪
- 百分位/Z-score分析
- 生长速度评估
- 生长异常预警

## 重要提示

本系统基于WHO儿童生长标准，**仅供参考，不能替代专业医疗诊断**。

- 早产儿（<37周）需矫正月龄至2岁
- 生长速度比单次测量更重要
- 定期监测，建议每3-6个月一次
- 异常情况请及时就医

如对生长发育有疑问，**建议咨询儿科或儿童保健科医生**。
