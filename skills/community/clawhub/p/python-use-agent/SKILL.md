---
name: python-use-agent
description: [已整合] Python 智能执行已整合到 code 统一入口技能
argument-hint: "[任务描述]"
---

# ⚠️ 已整合 - 请使用 code 统一入口

> **本技能保留用于向后兼容，功能已整合到 `code` 统一入口技能**
>
> **推荐使用：** `code python [任务]` 或直接使用本技能（自动转发）

---

# Python-Use Agent（兼容层）

Python 驱动的智能执行技能 - 任务驱动、结果导向。

## 迁移指南

**新用法：**
```
code python 数据分析
code python 调用 API
code python 自动化处理
```

**旧用法（仍然可用）：**
```
python 数据分析
```

## 核心理念
`No Agents, Code is Agent`

## 执行流程
```
用户描述任务 
  ↓
AI 理解并规划 
  ↓
自动生成 Python 代码 
  ↓
执行代码并获取结果 
  ↓
反馈结果/自动修复
```

## 与传统 Agent 的区别
| 传统 Agent 1.0 | Python-Use Agent 2.0 |
|--------------|---------------------|
| Function Calling | 直接编写 Python 代码 |
| 工具注册/配置 | 无需配置，直接用 |
| Workflow 预设 | 动态规划执行 |
