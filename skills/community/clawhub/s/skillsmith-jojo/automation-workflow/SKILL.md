---
name: automation-workflow
description: |
  自动化工作流技能模板，用于构建多步骤自动化流程。
  使用场景：
  - 用户说"帮我自动化这个流程"
  - 用户说"定时执行某个任务"
  - 用户说"监控某个服务状态"
  - 用户说"生成每日报告"
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      bins:
        - python3
---

# 自动化工作流技能模板

## 核心脚本

### scheduler.py
定时执行任务，支持 cron 表达式和周期性触发

### monitor.py
监控任务状态，检测异常和失败

### workflow.py
工作流引擎，支持多步骤流程和条件分支

## 工作流模式

### 模式 1: 线性流程
```python
wf.linear("A", "B", "C")
```

### 模式 2: 条件分支
```python
wf.branch("A", if_true="B", if_false="C")
```

### 模式 3: 并行执行
```python
wf.parallel("任务1", "任务2", "任务3")
```

## 错误处理

| 错误类型 | 处理策略 |
|---------|---------|
| 步骤失败 | 重试最多 3 次 |
| 超时错误 | 跳过并记录 |
| 网络错误 | 等待恢复 |
