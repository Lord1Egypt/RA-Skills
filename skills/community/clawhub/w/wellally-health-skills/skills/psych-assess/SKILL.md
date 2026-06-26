---
name: psych-assess
description: Comprehensive mental health assessment system with standardized scales, crisis detection, and AI-powered psychological support.
argument-hint: <action> [parameter]
allowed-tools: Read, Write, Glob, Grep
schema: psych-assess/schema.json
---

# Mental Health Comprehensive Assessment System

Comprehensive mental health assessment system, combining international standardized psychological scales, multi-dimensional assessment, crisis detection, and AI-powered psychological support.

## Operation Types

### 1. Start Assessment - `start`

Begin a new mental health assessment. AI will guide you to select the appropriate assessment type.

```
/psych-assess start
```

AI guidance includes:
- Select assessment type (quick screening/comprehensive)
- Understand what mental health assessment is
- Get recommendations

### 2. Quick Screening - `quick`

Quick emotional health check, takes about 2 minutes.

**Includes:**
- PHQ-2 (depression quick screening): 2 questions
- GAD-2 (anxiety quick screening): 2 questions
- Crisis indicator detection

```
/psych-assess quick
```

### 3. Full Assessment - `full`

Comprehensive multi-dimensional mental health assessment, takes about 10-15 minutes.

**Includes:**
- Informed consent and baseline assessment
- PHQ-9 (depression symptom assessment): 9 questions
- GAD-7 (anxiety symptom assessment): 7 questions
- PSS-4 (stress level assessment): 4 questions
- WHO-5 (well-being index): 5 questions
- Sleep quality assessment: 4 questions
- Enhanced crisis assessment (if triggered)
- Detailed assessment report and recommendations

```
/psych-assess full
```

### 4. Assessment Report - `report`

Generate detailed mental health assessment report with trend analysis.

```
/psych-assess report              # Latest assessment report
/psych-assess report 2025-12-15   # Report for specific date
/psych-assess report trends       # Trend analysis report
```

### 5. Assessment History - `history`

View mental health assessment history.

```
/psych-assess history             # All assessment history
/psych-assess history recent 5    # Recent 5 assessments
/psych-assess history 2025-12     # Assessments for specific month
```

### 6. Dialogue Support - `dialogue`

Start or continue post-assessment psychological support dialogue.

```
/psych-assess dialogue
```

### 7. Crisis Resources - `crisis`

Get 24-hour crisis intervention resources (no data required).

```
/psych-assess crisis
```

## 执行流程

## Step 1: Informed Consent (Required for Full Assessment)

Display informed consent form, ensure user understands:
- This assessment uses internationally standardized psychometric scales
- Assessment results are for reference only, **not medical diagnosis**
- Results **cannot replace professional psychological counseling or psychiatric evaluation**
- Data is stored locally on device
- Regular assessments are recommended to track changes in trends

**Important Notice:** If any of the following occur, **stop immediately** and seek medical help:
- Suicidal or self-harm thoughts or plans
- Hallucinations or delusions
- Complete inability to perform daily activities
- Recent suicide attempts

## Step 2: Baseline Information Collection (Full Assessment)

Collect the following information to help interpret assessment results:
1. What specific event today prompted you to take this assessment
2. Any life changes in recent weeks
3. Social support situation
4. What you hope to gain from this assessment

## Step 3: Scale Administration

Based on assessment type (quick/full), administer corresponding scales:
- **Quick screening**: PHQ-2 + GAD-2
- **Full assessment**: PHQ-9 + GAD-7 + PSS-4 + WHO-5 + Sleep quality

## Step 4: Crisis Assessment (Triggered when PHQ-9 Question 9 > 0)

Enhanced crisis assessment includes 7 questions:
1. Frequency of thoughts
2. Intensity of thoughts
3. Specificity of plan
4. Availability of means
5. Intent to act
6. Past attempts
7. Protective factors

### 步骤5：数据保存

**File Path Format:**
```
data/psych-assessments/YYYY-MM/YYYY-MM-DD_HHMM_type.json
```

**type:**
- `initial`: Initial assessment
- `followup`: Follow-up assessment
- `quick`: Quick screening

## Step 6: Update Global Index

Add assessment record and update statistics in `data/index.json`.

## Step 7: Output Report

Generate detailed assessment report including:
- Executive summary
- Scale score results
- Risk assessment and crisis detection
- Comprehensive recommendations
- Referral recommendations
- Crisis resources
- Follow-up plan

## 标准化心理量表库

### PHQ-9 抑郁症状量表

| 题号 | 问题内容 | 0分 | 1分 | 2分 | 3分 |
|------|---------|-----|-----|-----|-----|
| 1 | 做事时提不起劲或没有兴趣 | 完全不会 | 几天 | 一半以上天数 | 几乎每天 |
| 2 | 感到心情低落、沮丧或绝望 | 完全不会 | 几天 | 一半以上天数 | 几乎每天 |
| 3 | 入睡困难、睡不安稳或睡眠过多 | 完全不会 | 几天 | 一半以上天数 | 几乎每天 |
| 4 | 感到疲倦或没有活力 | 完全不会 | 几天 | 一半以上天数 | 几乎每天 |
| 5 | 食欲不振或吃得太多 | 完全不会 | 几天 | 一半以上天数 | 几乎每天 |
| 6 | 觉得自己很糟，或觉得自己很失败 | 完全不会 | 几天 | 一半以上天数 | 几乎每天 |
| 7 | 对事物专注有困难 | 完全不会 | 几天 | 一半以上天数 | 几乎每天 |
| 8 | 动作或说话速度变化 | 完全不会 | 几天 | 一半以上天数 | 几乎每天 |
| 9 | 自伤念头 | 完全不会 | 几天 | 一半以上天数 | 几乎每天 |

**评分标准**：
- 0-4分: 无抑郁
- 5-9分: 轻度抑郁
- 10-14分: 中度抑郁
- 15-19分: 中重度抑郁
- 20-27分: 重度抑郁

### GAD-7 焦虑症状量表

| 题号 | 问题内容 | 0分 | 1分 | 2分 | 3分 |
|------|---------|-----|-----|-----|-----|
| 1 | 感到紧张、焦虑或急切 | 完全不会 | 几天 | 一半以上天数 | 几乎每天 |
| 2 | 不能停止或控制担忧 | 完全不会 | 几天 | 一半以上天数 | 几乎每天 |
| 3 | 对各种各样的事情担忧过多 | 完全不会 | 几天 | 一半以上天数 | 几乎每天 |
| 4 | 很难放松下来 | 完全不会 | 几天 | 一半以上天数 | 几乎每天 |
| 5 | 由于不安而无法静坐 | 完全不会 | 几天 | 一半以上天数 | 几乎每天 |
| 6 | 变得容易烦恼或急躁 | 完全不会 | 几天 | 一半以上天数 | 几乎每天 |
| 7 | 感到好像有什么可怕的事发生 | 完全不会 | 几天 | 一半以上天数 | 几乎每天 |

**评分标准**：
- 0-4分: 轻微焦虑
- 5-9分: 轻度焦虑
- 10-14分: 中度焦虑
- 15-21分: 重度焦虑

### PSS-4 知觉压力量表

| 题号 | 问题内容 | 0分 | 1分 | 2分 | 3分 | 4分 |
|------|---------|-----|-----|-----|-----|-----|
| 1 | 感到无法控制生活中的事情 | 从不 | 几乎从不 | 有时 | 经常 | 很经常 |
| 2 | 感到自信心不足 | 从不 | 几乎从不 | 有时 | 经常 | 很经常 |
| 3 | 感到事情顺心如意（反向计分） | 从不 | 几乎从不 | 有时 | 经常 | 很经常 |
| 4 | 感到所有事情都得心应手（反向计分） | 从不 | 几乎从不 | 有时 | 经常 | 很经常 |

**反向计分**：Q3和Q4需要反向计分（0→4, 1→3, 2→2, 3→1, 4→0）

**评分标准**：
- 0-6分: 低压力
- 7-10分: 中等压力
- 11-16分: 高压力

### WHO-5 幸福感指数

| 题号 | 问题内容 | 0分 | 1分 | 2分 | 3分 | 4分 |
|------|---------|-----|-----|-----|-----|-----|
| 1 | 感到心情愉快和精力充沛 | 任何时候都没有 | 有时 | 超过一半时间 | 大部分时间 | 所有时间 |
| 2 | 感到平静和放松 | 任何时候都没有 | 有时 | 超过一半时间 | 大部分时间 | 所有时间 |
| 3 | 感到积极活跃 | 任何时候都没有 | 有时 | 超过一半时间 | 大部分时间 | 所有时间 |
| 4 | 在醒来时感到清新和休息好了 | 任何时候都没有 | 有时 | 超过一半时间 | 大部分时间 | 所有时间 |
| 5 | 日常生活充满兴趣和充实 | 任何时候都没有 | 有时 | 超过一半时间 | 大部分时间 | 所有时间 |

**评分标准**：
- 0-12分: 幸福感低
- 13-18分: 幸福感中等
- 19-25分: 幸福感良好

## 增强危机评估协议

### 五级风险分层系统

| 风险等级 | 触发条件 | 响应行动 |
|---------|---------|---------|
| CRITICAL (危急) | PHQ-9第9题=3、打算近期行动、近期自杀尝试、精神病性症状 | 立即拨打危机热线、前往急诊、不要独处 |
| HIGH (高危) | 明确计划+有手段+实施意图、多次既往尝试、高绝望感 | 立即寻求专业帮助、联系医生、制定安全计划 |
| MODERATE (中危) | 无明确计划但有意向、PHQ-9第9题=1、中度症状 | 48小时内预约心理医生、联系信任的人 |
| LOW (低危) | 轻度自杀念头、偶发绝望感 | 心理咨询、自助资源、2周后复查 |
| MINIMAL (无风险) | 无危机指标、轻度或无症状 | 定期监测、健康生活方式 |

## 危机资源库

**24小时心理危机干预热线**：
- 全国心理援助热线：400-161-9995
- 北京心理危机研究与干预中心：010-82951332
- 上海市心理热线：021-12320-5
- 广州市心理热线：020-81899120
- 深圳市心理热线：0755-25629459
- 报警：110
- 急救：120

## 安全协议与边界

### 安全红线（严格禁止）

1. **不给出具体用药剂量**
2. **不直接开具处方药名**
3. **不判断预后**
4. **不替代医生诊断**
5. **必须识别危机风险并及时预警**

### 免责声明

每次报告必须包含：
- 本评估仅供参考，**不是医疗诊断**
- 结果**不能替代专业心理咨询或精神科评估**
- 所有建议**请咨询医生后执行**
- **不提供药物剂量或具体治疗方案**
- 如有紧急情况，请**立即就医或拨打急救电话**

## 与现有系统集成

- **与 /mood 命令**：同一天记录自动关联，评估报告中可引用情绪趋势
- **与 /symptom 命令**：检测躯体化症状与压力/焦虑的关联
- **与 /consult 命令**：高风险时自动建议精神科专家会诊

## 错误处理

- **未完成评估**：检测到未完成的评估，提示继续
- **无评估记录**：提示开始新评估
- **文件读取错误**：检查文件完整性
- **日期格式错误**：使用 YYYY-MM-DD 格式

## 注意事项

- 本系统使用国际标准化心理测量量表，结果具有参考价值
- 本系统**不能替代专业医疗诊断**
- 如有持续情绪问题，应寻求专业心理咨询师或精神科医生的帮助
- 危机情况下，应立即拨打危机热线或前往医院急诊
- 所有数据仅保存在本地，注意保护个人隐私
- 建议定期评估（每2-4周）以追踪变化趋势

**记住，寻求帮助是勇敢的表现，不是软弱。**
