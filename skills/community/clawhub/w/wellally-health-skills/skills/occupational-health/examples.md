# 职业健康技能示例

## 示例 1: 办公室工作评估

```
用户: 办公室工作，每天8小时，颈痛

解析结果:
{
  "workType": "office_work",
  "hoursPerDay": 8,
  "healthIssues": [
    {"type": "neck_pain", "severity": "moderate"}
  ],
  "riskAssessment": {
    "sedentaryRisk": "high",
    "screenRisk": "high",
    "overallRisk": "high"
  }
}

输出建议:
• 每小时起身活动5-10分钟
• 遵循20-20-20法则保护眼睛
• 调整显示器高度与眼水平
• 检查椅子是否提供足够腰部支撑
```

## 示例 2: 体力劳动

```
用户: 在仓库工作，需要搬运重物，腰痛

解析结果:
{
  "workType": "manual_labor",
  "hoursPerDay": 8,
  "healthIssues": [
    {"type": "back_pain", "severity": "severe", "frequency": "often"}
  ],
  "riskAssessment": {
    "overallRisk": "high"
  }
}

输出建议:
• 学习正确的搬运姿势（弯膝不弯腰）
• 使用辅助设备搬运重物
• 加强核心肌群锻炼
• 如疼痛持续，请就医检查
```

## 示例 3: 倒班工作

```
用户: 夜班护士，每周3次夜班，睡眠不好

解析结果:
{
  "workType": "shift_work",
  "healthIssues": [
    {"type": "sleep_disturbance", "severity": "moderate"}
  ],
  "riskAssessment": {
    "shiftWorkRisk": "high",
    "overallRisk": "medium"
  }
}

输出建议:
• 建立规律的睡眠时间表
• 创造黑暗、安静的睡眠环境
• 使用睡眠面具和耳塞
• 与家人沟通睡眠时间的重要性
• 考虑使用遮光窗帘
```

## 示例 4: 完整评估

```
用户: 程序员，每天对着电脑10小时，眼睛干、手腕疼

解析结果:
{
  "workType": "office_work",
  "hoursPerDay": 10,
  "healthIssues": [
    {"type": "eye_strain", "severity": "moderate", "frequency": "daily"},
    {"type": "wrist_pain", "severity": "mild", "frequency": "often"}
  ],
  "riskAssessment": {
    "sedentaryRisk": "high",
    "screenRisk": "high",
    "overallRisk": "high"
  }
}

输出建议:
━━━━━━━━━━━━━━━━━━━━━━━━━━
风险评估：高风险

立即行动建议：
1. 严格遵守20-20-20法则
2. 每小时起身活动
3. 调整显示器距离（50-70cm）
4. 使用手腕支撑
5. 考虑使用可调节升降桌
6. 定期进行眼科检查
7. 如手腕疼痛持续，请就医检查腕管综合征
```
