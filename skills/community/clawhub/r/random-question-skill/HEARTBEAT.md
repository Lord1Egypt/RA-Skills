# Heartbeat 配置

## 随机提问任务

每30分钟有30%概率触发随机提问。

### 执行逻辑
1. 生成1-10的随机数
2. 如果随机数 > 7，则调用 random-question 技能
3. 否则回复 HEARTBEAT_OK 并静默

### 调用示例
```bash
!use skill:random-question
```

## 工作时间段配置

```yaml
heartbeat:
  enabled: true
  interval_minutes: 30
  probability: 30
  
  work_hours:
    monday: ["09:00", "18:00"]
    tuesday: ["09:00", "18:00"]
    wednesday: ["09:00", "18:00"]
    thursday: ["09:00", "18:00"]
    friday: ["09:00", "18:00"]
    saturday: []
    sunday: []
```

## 集成方式

### 与日记技能集成
```yaml
workflows:
  morning_checkin:
    - skill: "random-question"
    - skill: "daily-journal"
    params:
      prompt: "回答刚才的随机问题"
```

### 自定义触发条件
```python
import random
from scripts.random_selector import RandomQuestionGenerator

generator = RandomQuestionGenerator()

# 根据时间决定是否触发
hour = datetime.now().hour
if 9 <= hour <= 18:  # 工作时间
    question = generator.get_random_question(force=True)
    if question:
        print(f"!announce {question['question']}")
```

## 配置选项

### 触发概率
- 0: 从不触发
- 30: 30%概率触发（推荐）
- 50: 50%概率触发
- 100: 总是触发

### 活跃时间段
- start: 开始时间（HH:MM格式）
- end: 结束时间（HH:MM格式）

### 最小间隔
- min_interval_minutes: 两次提问之间的最小间隔（分钟）

## 使用建议

### 初期设置
- 触发概率: 30%
- 间隔: 30分钟
- 时间段: 08:00-23:00

### 适应后
- 触发概率: 50%
- 间隔: 60分钟
- 时间段: 自定义

### 深度使用
- 自定义时间表
- 按工作日/周末区分
- 按项目类型区分
