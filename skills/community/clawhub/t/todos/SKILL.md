---
name: todos
displayName: 待办事项管理
description: 简洁高效的待办事项管理技能，支持添加、完成、查看、删除待办，数据存储在本地 JSON 文件
tags:
  - productivity
  - task-management
  - todo
  - 待办
  - 记事本
version: 1.0.0
author: Becker
---

# todos - 待办事项技能

## 功能

待办事项管理技能，支持：
- ✅ 添加待办事项
- ✅ 标记事项为已完成
- ✅ 查看今日待完成/已完成
- ✅ 查询历史已完成事项
- ✅ 查询未来待完成事项
- ✅ 删除事项

## 触发词

- 记事本
- 待办
- todo
- 待办事项
- 任务管理

## 数据文件

待办事项存储在 `~/.openclaw/workspace/memory/todos.json`

## 命令格式

### 添加待办
```
添加待办：明天下午 3 点开会
待办：本周内完成报告
```

### 标记完成
```
完成：[事项 ID 或关键词]
```

### 查看
```
今日待办
今日已完成
本周待办
本周已完成
未来待办
历史完成（过去 7 天）
```

### 删除
```
删除：[事项 ID]
```

## 脚本

Python 脚本位于 `scripts/todos.py`

## 示例

```bash
# 添加待办
python3 scripts/todos.py add "明天下午 3 点开会" --due 2026-03-26T15:00:00

# 查看今日待办
python3 scripts/todos.py list --today --pending

# 标记完成
python3 scripts/todos.py complete 1

# 查询历史
python3 scripts/todos.py list --completed --since 2026-03-18
```
