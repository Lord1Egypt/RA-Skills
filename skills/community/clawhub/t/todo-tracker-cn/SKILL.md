---
name: todo-tracker
description: 生成、跟踪和验证待办列表的执行状态。提供 generate-todo-list, mark-completed, show-progress, verify-completion 四个核心动作。
metadata:
  openclaw:
    emoji: "✅"
    requires:
      bins: ["python3"]
---

# Todo Tracker Skill

待办事项管理技能，实现任务的生成、跟踪和完成验证。

## 核心功能

1. **generate-todo-list** - 根据任务描述生成结构化待办列表
2. **mark-completed** - 标记某个待办项为已完成
3. **show-progress** - 查看当前待办列表的完成进度
4. **verify-completion** - 验证待办列表是否全部完成

## 使用方式

```bash
# 生成待办列表
python3 ~/.openclaw/workspace/skills/todo-tracker/todo_tracker.py generate-todo-list "分析项目需求"

# 标记完成
python3 ~/.openclaw/workspace/skills/todo-tracker/todo_tracker.py mark-completed "todo_xxx"

# 查看进度
python3 ~/.openclaw/workspace/skills/todo-tracker/todo_tracker.py show-progress

# 验证完成
python3 ~/.openclaw/workspace/skills/todo-tracker/todo_tracker.py verify-completion
```

## 数据存储

待办数据存储在：`~/.openclaw/workspace/todo-current.json`

## 与 Self-Improving 集成

- 任务完成后自动记录到 `~/self-improving/corrections.md`
- 定期清理已完成的待办列表
