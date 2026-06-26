---
name: goal
description: Health goal and habit management with SMART goal setting, progress tracking, and visualization reports
argument-hint: <操作类型，如：set weight-loss 5公斤 2025-06-30/progress 3.5公斤/habit record 早上拉伸/review/report>
allowed-tools: Read, Write
schema: goal/schema.json
---

# Health Goal and Habit Management Skill

Set health goals, track progress, build habits, and generate visualization reports.

## 核心流程

```
用户输入 -> 识别操作类型 -> 解析信息 -> 检查完整性 -> SMART验证 -> 生成JSON -> 保存数据
```

## 步骤 1: 解析用户输入

### 操作类型识别

| Input Keywords | Operation Type |
|---------------|----------------|
| set | Set goal |
| progress | Update progress |
| habit | Record habit |
| review | View goals and progress |
| report | Generate visualization report |
| achieve | View achievement system |
| complete | Complete goal |
| adjust | Adjust goal |

### Goal Type Recognition

| Type | Keywords |
|------|----------|
| weight-loss | Lose weight, weight loss goal |
| weight-gain | Gain weight, muscle gain goal |
| exercise | Exercise, workout, fitness |
| diet | Diet, nutrition, meal |
| sleep | Sleep, rest |
| health-metric | Blood pressure, blood sugar, health metric |

## 步骤 2: 检查信息完整性

### Set Goal (set)
- **Required**: Goal type, goal description
- **Recommended**: Goal value, deadline
- **Optional**: Action plan

### Update Progress (progress)
- **Required**: Progress information
- **Recommended**: Specific value

### Record Habit (habit)
- **Required**: Habit identifier or description
- **Recommended**: Completion status

## 步骤 3: SMART原则验证

### SMART检查清单

- **S**pecific: Clear and specific goal
- **M**easurable: Progress can be quantified
- **A**chievable: Realistic and attainable
- **R**elevant: Health-related
- **T**ime-bound: Has clear deadline |

### 验证提示

```
Goal Validation:
✓ Specific: Clear goal content
✓ Measurable: Has quantifiable metrics
✓ Achievable: Realistic and feasible
✓ Relevant: Health-related
✓ Time-bound: Has deadline

If validation fails, user will be prompted to adjust goal
```

## 步骤 4: 生成 JSON

### 目标数据结构

```json
{
  "goal_id": "goal_20250101_001",
  "type": "weight-loss",
  "title": "减重5公斤",
  "description": "在6个月内减重5公斤",
  "start_date": "2025-01-01",
  "target_date": "2025-06-30",
  "current_value": 0,
  "target_value": 5,
  "unit": "公斤",
  "status": "in_progress",
  "progress_percentage": 0,
  "smart_verified": true,
  "action_plan": [
    "每周运动4次",
    "减少500卡路里摄入",
    "每天吃5份蔬果"
  ],
  "milestones": [
    {
      "target": 2.5,
      "date": "2025-03-31",
      "achieved": false
    }
  ],
  "created_at": "2025-01-01T00:00:00.000Z"
}
```

### 习惯数据结构

```json
{
  "habit_id": "habit_20250101_001",
  "name": "morning-stretch",
  "title": "早上拉伸",
  "description": "每天早上7点拉伸10分钟",
  "frequency": "daily",
  "trigger": "起床后",
  "streak": 7,
  "longest_streak": 21,
  "total_completions": 45,
  "created_at": "2025-01-01T00:00:00.000Z"
}
```

完整 Schema 定义参见 [schema.json](schema.json)。

## 步骤 5: 保存数据

1. 生成唯一ID
2. 保存到 `data/goal-tracker.json`
3. 更新进度统计

## 成就系统

### 基础成就列表

| Achievement | Unlock Condition |
|------------|------------------|
| First Goal | Complete first health goal |
| 7-Day Streak | Complete any habit for 7 consecutive days |
| 21-Day Streak | Complete any habit for 21 consecutive days |
| 30-Day Streak | Complete any habit for 30 consecutive days |
| Halfway | Complete 50% of any goal |
| Goal Complete | Complete a health goal |
| Early Finish | Complete goal ahead of schedule |
| Exceed Goal | Exceed goal target |

## 进度预测算法

```javascript
// Predict completion date based on current progress
function predictCompletion(goal) {
  const daysPassed = getDaysBetween(goal.start_date, new Date());
  const daysRemaining = getDaysBetween(new Date(), goal.target_date);
  const progressPerDay = goal.current_value / daysPassed;

  const predictedDays = (goal.target_value - goal.current_value) / progressPerDay;
  const predictedDate = addDays(new Date(), predictedDays);

  return {
    predicted_date: predictedDate,
    on_track: predictedDate <= goal.target_date,
    days_ahead: getDaysBetween(predictedDate, goal.target_date)
  };
}
```

## 执行指令

```
1. 识别操作类型
2. 解析输入参数，提取所有可用信息
3. 检查必填字段，如有缺失则询问用户
4. 对目标进行SMART原则验证
5. 生成符合 schema.json 的 JSON
6. 保存到数据文件
7. 向用户确认保存成功，并显示摘要和建议
8. 如达成成就，自动解锁并提示
```

## 示例交互

### 示例 1: 设定减重目标
```
用户: 设定目标 减重5公斤 2025年6月30日
AI: ✅ 目标设定成功

    目标信息:
    类型: 减重目标
    目标: 减重5公斤
    开始日期: 2025-01-01
    目标日期: 2025-06-30

    SMART验证: ✅ 通过
    ✓ 具体: 明确减重5公斤
    ✓ 可衡量: 可追踪体重变化
    ✓ 可实现: 现实可行
    ✓ 相关: 与健康相关
    ✓ 有时限: 6个月期限

    行动计划建议:
    • 每周运动4次，每次30分钟
    • 每天减少500卡路里摄入
    • 每天吃5份蔬果
    • 戒烟限酒

    已保存至健康目标
```

### 示例 2: 记录习惯
```
用户: 记录习惯 早上拉伸 完成
AI: ✅ 习惯记录已更新

    习惯: 早上拉伸
    连续天数: 8天
    最长连续: 21天
    总完成次数: 46次

    🎉 新成就解锁: 连续7天！

    继续保持！还有13天解锁"连续21天"成就
```

### 示例 3: 生成进度报告
```
用户: 目标进度报告
AI: 📊 健康目标进度报告

    减重目标:
    进度: 3.5/5公斤 (70%)
    预计完成: 2025年5月20日 (提前41天)
    状态: 进展顺利 ✅

    运动目标:
    进度: 2/4次 (50%)
    本周完成: 2次
    状态: 需要努力 ⚠️

    习惯追踪:
    • 早上拉伸: 7天连续 ✅
    • 餐前喝水: 5天连续

    [生成完整可视化报告...]
```

## 重要提示

- 本系统提供的健康目标设定和追踪仅供参考
- 不构成医疗诊断、治疗或专业建议
- 设定极端或不健康的减重/增重目标会收到警告
- 如有慢性疾病，设定目标前请咨询医生
- 所有数据仅保存在本地
