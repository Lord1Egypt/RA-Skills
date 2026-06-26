---
name: occupational-health
description: Conduct occupational health assessments, record work-related health issues, evaluate ergonomics, screen for occupational disease risks, and manage work environment factors.
argument-hint: <自然语言描述，如：办公室工作，每天8小时，颈痛>
allowed-tools: Read, Write
schema: occupational-health/schema.json
---

# Occupational Health Skill

Interactive occupational health assessment, recording work-related health issues, and evaluating ergonomics.

## 核心流程

```
用户输入 → 解析工作类型和健康问题 → 评估风险 → 生成报告 → 保存数据
```

## 步骤 1: 解析用户输入

### 工作类型识别

| Input Keywords | Work Type |
|---------------|-----------|
| office, computer, desk sitting | office_work |
| manual labor, lifting, standing | manual_labor |
| shift work, night shift, rotating | shift_work |
| noise, loud | noisy_environment |
| dust, chemical | dust_chemical_environment |

### 健康问题类型

| Input Keywords | Problem Type |
|---------------|-------------|
| neck pain | neck_pain |
| shoulder pain | shoulder_pain |
| back pain, lower back pain | back_pain |
| wrist pain | wrist_pain, carpal_tunnel |
| eye strain, dry eyes | eye_strain |
| headache | headache |
| fatigue | fatigue |
| stress | stress |
| sleep problem | sleep_disturbance |

### 严重程度

| Input | Severity |
|-------|----------|
| mild, slight | mild |
| moderate | moderate |
| severe | severe |

## 步骤 2: 检查信息完整性

### Must Have (ask if missing):
- `workType` - Work type

### Recommended (ask if missing):
- `hoursPerDay` - Working hours per day
- `healthIssues` - List of health issues
- `symptoms` - Symptom description

## 步骤 3: 交互式询问

```
用户: 我工作很累

AI: 请问您是什么类型的工作？
    A. 办公室工作（主要用电脑）
    B. 体力劳动（搬运重物）
    C. 倒班工作（夜班）
    D. 其他

用户: A

AI: 大概每天工作几小时？有没有什么特别的不适？
```

## 步骤 4: 风险评估

### 久坐风险评分

| 条件 | 风险等级 |
|-----|---------|
| 每天久坐<4小时，每小时休息 | 低 |
| 每天久坐4-8小时，每2小时休息 | 中 |
| 每天久坐>8小时，休息间隔>3小时 | 高 |

### 视屏终端风险评分

| 条件 | 风险等级 |
|-----|---------|
| 每天屏幕时间<4小时，遵守20-20-20法则 | 低 |
| 每天屏幕时间4-8小时 | 中 |
| 每天屏幕时间>8小时 | 高 |

### 综合风险等级

- **低风险**: 所有风险因素都在可控范围内
- **中风险**: 存在多个风险因素，需要关注
- **高风险**: 存在严重风险因素，需要立即行动

## 步骤 5: 生成 JSON

```json
{
  "timestamp": "2026-02-03T10:30:00Z",
  "workType": "office_work",
  "hoursPerDay": 8,
  "healthIssues": [
    {
      "type": "neck_pain",
      "severity": "moderate",
      "frequency": "often"
    }
  ],
  "riskAssessment": {
    "sedentaryRisk": "high",
    "screenRisk": "high",
    "overallRisk": "high"
  },
  "notes": "长时间使用电脑，需要改善人机工程设置"
}
```

## 步骤 6: 保存数据

保存到 `data/occupational-health-records.json`

## 执行指令

```
1. 解析用户输入，识别工作类型和健康问题
2. 检查必填字段（workType）
3. 如有缺失，使用 AskUserQuestion 询问用户
4. 进行风险评估（久坐、视屏终端、倒班等）
5. 生成符合 schema.json 的 JSON
6. 保存到 data/occupational-health-records.json
7. 向用户展示风险评估结果和改进建议
```

## 示例交互

```
用户: 办公室工作，每天8小时，颈痛

AI: 我了解了您的职业健康情况。

    工作类型：办公室工作
    每天工作时长：8小时
    健康问题：颈痛

    风险评估结果：
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • 久坐风险：高（每天>8小时）
    • 视屏终端风险：高
    • 综合风险等级：高风险

    改进建议：
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    1. 每小时起身活动5-10分钟
    2. 遵循20-20-20法则保护眼睛
    3. 调整显示器高度与眼水平
    4. 检查椅子是否提供足够腰部支撑
    5. 考虑使用可调节升降桌

    记录已保存。

用户: 谢谢

AI: 不客气！建议您每3个月重新评估一次职业健康状况。
    如有持续或加重的症状，请及时就医。
```

## 20-20-20法则

使用视屏终端时保护眼睛：
- 每**20分钟**
- 看向**20英尺**（约6米）外
- 保持**20秒**

## 紧急情况指南

出现以下情况请立即就医：
- 突发严重呼吸困难
- 胸痛或心悸
- 突然视力丧失或剧烈眼痛
- 严重肌肉骨骼损伤
