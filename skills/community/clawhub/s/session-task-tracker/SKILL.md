---
name: task-tracker
description: "Task-based cross-session context management for OpenClaw agents. Maintains persistent task files so context survives session resets, compaction, and channel switches. Use when: (1) A new task or project is discussed, (2) Progress or decisions are made on an existing task, (3) User says 'continue task', 'what is the status', 'where did we leave off', (4) A new session starts and user references prior work, (5) User mentions switching channels or losing context, (6) User asks about task status, progress, or next steps."
---

# Task Tracker

Persist task context across sessions and channels by maintaining per-task files.

## Core Concept

Each task gets a single markdown file in `tasks/`. The file IS the memory —
independent of session history, compaction, or channel.

## When This Skill Fires

| Situation | Action |
|-----------|--------|
| New task/project mentioned | Create task file + update index |
| Progress/decision on existing task | Update that task file |
| Session start (bootstrap) | Read `_INDEX.md` |
| User references a task | Read that task file, respond with context |
| User signals leaving ("先这样", "回家再说") | Ensure all discussed tasks are updated |

## Task Directory

Location: `{workspace}/tasks/`

```
tasks/
├── _INDEX.md          # Task index (auto-maintained)
├── project-alpha.md    # One file per task
└── weekly-report.md
```

## Task File Format

```markdown
# [Task Name]

- **状态：** 进行中 | 暂停 | 待启动 | 已完成 | 已搁置
- **优先级：** 高 | 中 | 低
- **创建时间：** YYYY-MM-DD
- **最后更新：** YYYY-MM-DD
- **标签：** #tag1 #tag2

## 目标
[One sentence: what this task achieves]

## 背景
[Why this task exists, origin context]

## 进展记录
### YYYY-MM-DD
- What was done
- Key decisions made

## 待办
- [ ] TODO item
- [x] Completed item

## 关键信息
[Core facts that must persist: configs, links, accounts, constraints]

## 相关文件
- File description: path/to/file
```

**Rules:**
- 进展记录: newest date on top
- 待办: mark done with `[x]` when complete
- 关键信息: only facts that another session needs to function
- 相关文件: absolute paths, brief description

## Index File (`_INDEX.md`)

```markdown
# 任务索引

## 🟢 进行中
| 任务 | 状态 | 最后更新 | 优先级 |
|------|------|---------|--------|

## 🟡 暂停
| 任务 | 状态 | 最后更新 | 优先级 |
|------|------|---------|--------|

## ⚪ 已完成
| 任务 | 完成时间 |
|------|---------|
```

Maintain this file whenever a task's status changes.

## Workflow

### Creating a New Task

1. Create `tasks/{task-name}.md` using the template above
2. Add entry to `_INDEX.md` under 进行中
3. Confirm creation with user

### Updating a Task

1. Update 进展记录 (prepend new date entry if new day)
2. Update 待办 (check off completed items)
3. Update 状态 if changed
4. Update 最后更新 timestamp
5. Sync 状态 change to `_INDEX.md`

### Session Bootstrap

1. Read `_INDEX.md`
2. No user action needed — just be ready
3. When user mentions a task, read that file and respond with current context

### Task Completion / Archive

- Move file to `tasks/archive/`
- Remove from `_INDEX.md`
- Do this for tasks completed or stalled more than 30 days

## File Naming

- Chinese or English, short and clear
- No special characters, use `-` for spaces
- Max 64 characters
