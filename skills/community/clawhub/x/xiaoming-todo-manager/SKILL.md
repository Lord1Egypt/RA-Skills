---
name: todo-manager
description: 待办事项管理 - 任务列表、提醒、优先级、进度追踪
---

# Todo Manager

待办事项管理工具，帮助高效完成任务。

## 功能

- ✅ 任务列表管理
- ✅ 优先级设置
- ✅ 定时提醒
- ✅ 进度追踪
- ✅ 任务分类

## 使用

```bash
# 添加任务
clawhub todo add --title "完成报告" --priority high --due "2026-04-18"

# 查看任务
clawhub todo list --status pending

# 完成任务
clawhub todo complete --id 1

# 设置提醒
clawhub todo remind --id 1 --time "2026-04-18 09:00"
```

## 定价

| 版本 | 价格 | 功能 |
|------|------|------|
| 免费版 | ¥0 | 20 个任务 |
| Pro 版 | ¥29 | 无限任务 |
| 订阅版 | ¥6/月 | Pro+ 云同步 |
